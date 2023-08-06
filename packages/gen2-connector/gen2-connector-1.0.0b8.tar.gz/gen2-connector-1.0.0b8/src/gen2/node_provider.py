#
# (C) Copyright IBM Corp. 2021
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import inspect

import logging
import time
from uuid import uuid4

import re
import threading

from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_platform_services import GlobalSearchV2, GlobalTaggingV1
from ibm_vpc import VpcV1
from ray.autoscaler.node_provider import NodeProvider
from ray.autoscaler.tags import TAG_RAY_CLUSTER_NAME, TAG_RAY_NODE_NAME, TAG_RAY_NODE_KIND, TAG_RAY_LAUNCH_CONFIG
from ray.autoscaler._private.cli_logger import cli_logger


logger = logging.getLogger(__name__)

INSTANCE_NAME_UUID_LEN = 8
INSTANCE_NAME_MAX_LEN = 64

#TODO: move to constants
PROFILE_NAME_DEFAULT = 'cx2-2x4'
VOLUME_TIER_NAME_DEFAULT = 'general-purpose'
RAY_RECYCLABLE = 'ray-recyclable'

def _create_vpc_client(endpoint, authenticator):
    """
    Creates an IBM VPC python-sdk instance
    """
    ibm_vpc_client = VpcV1('2021-01-19', authenticator=authenticator)
    ibm_vpc_client.set_service_url(endpoint + '/v1')

    return ibm_vpc_client


class Gen2NodeProvider(NodeProvider):

    def log_in_out(func):

      def decorated_func(*args, **kwargs):
        name = func.__name__
        logger.info(f"Enter {name} from {inspect.stack()[0][3]} {inspect.stack()[1][3]}  {inspect.stack()[2][3]} ")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Leave {name} from {inspect.stack()[1][3]}")
        except:
            cli_logger.error(f"Error in {name}")
            raise
        return result
      return decorated_func

    @log_in_out
    def _init(self):
        endpoint = self.provider_config["endpoint"]
        iam_api_key = self.provider_config["iam_api_key"]

        self.authenticator = IAMAuthenticator(iam_api_key)

        self.ibm_vpc_client = _create_vpc_client(endpoint, self.authenticator)
        self.global_tagging_service = GlobalTaggingV1(self.authenticator)
        self.global_search_service = GlobalSearchV2(self.authenticator)

    def __init__(self, provider_config, cluster_name):
        NodeProvider.__init__(self, provider_config, cluster_name)

        self._init()

        self.lock = threading.RLock()
        # Cache of node objects from the last nodes() call
        self.cached_nodes = {}
        self.cache_stopped_nodes = provider_config.get("cache_stopped_nodes", True)

    def _get_node_type(self, node):
        for tag in node['tags']:
            kv = tag.split(':')
            if kv[0] == 'ray-node-type':
                return kv[1]

    @log_in_out
    def non_terminated_nodes(self, tag_filters):
        # get all nodes tagged for cluster "query":"tags:\"ray-cluster-name:default\" AND tags:\"ray-node-type:head\""
        query = f"tags:\"{TAG_RAY_CLUSTER_NAME}:{self.cluster_name}\""
        for k, v in tag_filters.items():
            query += f" AND tags:\"{k}:{v}\""

        with self.lock:
          try:
            result = self.global_search_service.search(query=query, fields=['*']).get_result()
          except ApiException as e:
                cli_logger.warning(f"failed to query global search service with message: {e.message}, reiniting now")
                self._init()
                result = self.global_search_service.search(query=query, fields=['*']).get_result()

          items = result['items']
          nodes = []

          # update objects with floating ips. 
          for node in items:

            # TODO: should be special case here in case of cache_stopped_nodes?
            if node['doc']['status'] not in ['pending', 'starting', 'running']:
                continue

            instance_id = node['resource_id']
            try:
                self.ibm_vpc_client.get_instance(instance_id)
            except Exception as e:
                cli_logger.warning(instance_id)
                if e.message == 'Instance not found':
                    continue
                raise e

            node_type = self._get_node_type(node)
            if node_type == 'head':
                nic_id = node['doc']['network_interfaces'][0]['id']
                res = self.ibm_vpc_client.list_instance_network_interface_floating_ips(instance_id, nic_id).get_result()

                floating_ips = res['floating_ips']
                if len(floating_ips) == 0:
                    # not adding a head node that is missing floating ip
                    continue
                else:
                    # currently head node should always have floating ip.
                    # in case floating ip present we want to add it
                    node['floating_ips'] = floating_ips
            nodes.append(node)

          self.cached_nodes = {node["resource_id"]: node for node in nodes}

        return [node["resource_id"] for node in nodes]

    @log_in_out
    def is_running(self, node_id):
        with self.lock:
            node = self._get_cached_node(node_id)
            return node['doc']['status'] == 'running'

    @log_in_out
    def is_terminated(self, node_id):
        with self.lock:
            node = self._get_cached_node(node_id)
            state = node['doc']['status']
            return state not in ["running", "starting"] #todo: add state provisioning/running whatever gen2 has. maybe via ibm_vpc client?

    def _tags_to_dict(self, tags_list):
        tags_dict = {}
        logger.info(f'in _tags_to_dict with {tags_list}')
        for tag in tags_list:
            _tags_split = tag.split(':')
            logger.info(f'in _tags_to_dict - {_tags_split}')
            tags_dict[_tags_split[0]] = _tags_split[1]

        return tags_dict

    @log_in_out
    def node_tags(self, node_id):
        with self.lock:
            node = self._get_cached_node(node_id)
            return self._tags_to_dict(node['tags'])

    def _get_hybrid_ip(self, node_id):
        node = self._get_cached_node(node_id)
        node_type = self._get_node_type(node)
        if node_type == 'head':
            fip = node.get("floating_ips")
            if fip:
                return fip[0]['address']

            node = self._get_node(node_id)
            fip = node.get("floating_ips")
            if fip:
                return fip[0]['address']
        else:
            return self.internal_ip(node_id)

    @log_in_out
    def external_ip(self, node_id):
        with self.lock:
            if self.provider_config.get('use_hybrid_ips'):
                return self._get_hybrid_ip(node_id)

            node = self._get_cached_node(node_id)

            fip = node.get("floating_ips")
            if fip:
                return fip[0]['address']
            
            node = self._get_node(node_id)
            fip = node.get("floating_ips")
            if fip:
                return fip[0]['address']

    def internal_ip(self, node_id):
        node = self._get_cached_node(node_id)

        try:
            primary_ipv4_address = node['doc']['network_interfaces'][0].get('primary_ipv4_address')
            if primary_ipv4_address is None:
                node = self._get_node(node_id)
        except Exception:
            node = self._get_node(node_id)

        return node['doc']['network_interfaces'][0].get('primary_ipv4_address')

    def _attach_tags(self, resource_model, _tags):
        RETRIES = 3
        e = None
        for retry in range(RETRIES):
            try:
                tag_results = self.global_tagging_service.attach_tag(
                    resources=[resource_model],
                    tag_names=_tags,
                    tag_type='user').get_result()

                if not tag_results['results'][0]['is_error']:
                    return True
                else:
                    logger.error(f"failed to attach tags, {tag_results}")
            except Exception as e:
                logger.error(f"failed to attach tags, {e}")

            # try to reinit clients
            self._init()
            time.sleep(10)

        # if exception occured and reinit didn't help, raise exception
        if e:
            raise e
        else:
            return False

    @log_in_out
    def set_node_tags(self, node_id, tags):
        node = self._get_node(node_id)
        with self.lock:
            #import pdb;pdb.set_trace()
            if not isinstance(node['tags'], dict):
                tags_dict = self._tags_to_dict(node['tags'])
            else:
                tags_dict = node['tags']

            resource_crn = node['crn']
            resource_model = {'resource_id': resource_crn}

            # find all tags with same key as new tags but will different value
            for old_tag_key in list(tags_dict.keys()):
                if old_tag_key not in tags or tags.get(old_tag_key) == tags_dict[old_tag_key]:
                    del tags_dict[old_tag_key]

            # first attach new tags
            _tags = [f"{k}:{v}" for k,v in tags.items()]
            if not self._attach_tags(resource_model, _tags):
                cli_logger.error(f"failed to tag node {node_id}, raising error")
                raise

            logger.info("===========================")
            logger.info(f"attached {_tags}")
            logger.info("===========================")

            # convert to gen2 format
            old_tags = [f"{k}:{v}" for k,v in tags_dict.items()]

            # and now detach old tags. yes, it probably may break few things, because set_tags is not atomic
            if old_tags:
                self.global_tagging_service.detach_tag(
                    resources=[resource_model],
                    tag_names=old_tags,
                    tag_type='user').get_result()

                logger.info("===========================")
                logger.info(f"detached {old_tags}")
                logger.info("===========================")

            return {} 

    def _get_instance_data(self, name):
        """
        Returns the instance information
        """
        instances_data = self.ibm_vpc_client.list_instances(name=name).get_result()
        if len(instances_data['instances']) > 0:
            return instances_data['instances'][0]            
        return None

    def _create_instance(self, name, base_config):
        """
        Creates a new VM instance

        TODO: consider to use gen2 template file instead of generating dict
        """
        logger.debug("Creating new VM instance {}".format(name))

        security_group_identity_model = {'id': base_config['security_group_id']}
        subnet_identity_model = {'id': base_config['subnet_id']}
        primary_network_interface = {
            'name': 'eth0',
            'subnet': subnet_identity_model,
            'security_groups': [security_group_identity_model]
        }

        boot_volume_profile = {
            'capacity': 100,
            'name': '{}-boot'.format(name),
            'profile': {'name': base_config.get('volume_tier_name', VOLUME_TIER_NAME_DEFAULT)}}

        boot_volume_attachment = {
            'delete_volume_on_instance_delete': True,
            'volume': boot_volume_profile
        }

        key_identity_model = {'id': base_config['key_id']}
        profile_name = base_config.get('instance_profile_name', PROFILE_NAME_DEFAULT)

        instance_prototype = {}
        instance_prototype['name'] = name
        instance_prototype['keys'] = [key_identity_model]
        instance_prototype['profile'] = {'name': profile_name}
        instance_prototype['resource_group'] = {'id': base_config['resource_group_id']}
        instance_prototype['vpc'] = {'id': base_config['vpc_id']}
        instance_prototype['image'] = {'id': base_config['image_id']}
        instance_prototype['zone'] = {'name': self.provider_config['zone_name']}
        instance_prototype['boot_volume_attachment'] = boot_volume_attachment
        instance_prototype['primary_network_interface'] = primary_network_interface

        try:
            resp = self.ibm_vpc_client.create_instance(instance_prototype)
        except ApiException as e:
            if e.code == 400 and 'already exists' in e.message:
                return self._get_instance_data(name)
            elif e.code == 400 and 'over quota' in e.message:
                cli_logger.error("Create VM instance {} failed due to quota limit"
                             .format(name))
            else:
                cli_logger.error("Create VM instance {} failed with status code {}"
                             .format(name, str(e.code)))
            raise e

        logger.info("VM instance {} created successfully ".format(name))

        return resp.result

    def _create_floating_ip(self, base_config):
        """
        Creates or attaches floating IP address
        """
        if base_config.get('head_ip'):
            for ip in self.ibm_vpc_client.list_floating_ips().get_result()['floating_ips']:
                if ip['address'] == base_config['head_ip']:
                    return ip

        floating_ip_name = '{}-{}'.format(RAY_RECYCLABLE, uuid4().hex[:4]) 
            
        logger.debug('Creating floating IP {}'.format(floating_ip_name))
        floating_ip_prototype = {}
        floating_ip_prototype['name'] = floating_ip_name
        floating_ip_prototype['zone'] = {'name': self.provider_config['zone_name']}
        floating_ip_prototype['resource_group'] = {'id': base_config['resource_group_id']}
        response = self.ibm_vpc_client.create_floating_ip(floating_ip_prototype)
        floating_ip_data = response.result

        return floating_ip_data

    def _attach_floating_ip(self, instance, fip_data):
        fip = fip_data['address']
        fip_id = fip_data['id']

        logger.debug('Attaching floating IP {} to VM instance {}'.format(fip, instance['id']))

        # we need to check if floating ip is not attached already. if not, attach it to instance
        instance_primary_ni = instance['primary_network_interface']

        if instance_primary_ni['primary_ipv4_address'] and instance_primary_ni['id'] == fip_id:
            # floating ip already attached. do nothing
            logger.debug('Floating IP {} already attached to eth0'.format(fip))
        else:
            self.ibm_vpc_client.add_instance_network_interface_floating_ip(
                instance['id'], instance['network_interfaces'][0]['id'], fip_id)        

    def _stopped_nodes(self, tags):
        # get all nodes tagged for cluster "query":"tags:\"ray-cluster-name:default\" AND tags:\"ray-node-type:head\""
        query = f"tags:\"{TAG_RAY_CLUSTER_NAME}:{self.cluster_name}\""
        query += f" AND tags:\"{TAG_RAY_NODE_KIND}:{tags[TAG_RAY_NODE_KIND]}\""
        query += f" AND tags:\"{TAG_RAY_LAUNCH_CONFIG}:{tags[TAG_RAY_LAUNCH_CONFIG]}\""

        with self.lock:
            try:
                result = self.global_search_service.search(query=query, fields=['*']).get_result()
            except ApiException as e:
                cli_logger.warning(f"failed to query global search service with message: {e.message}, reiniting now")
                self._init()
                result = self.global_search_service.search(query=query, fields=['*']).get_result()

            items = result['items']
            nodes = []

            # filter instances by state (stopped,stopping)
            for node in items:
                instance_id = node['resource_id']
                try:
                    instance = self.ibm_vpc_client.get_instance(instance_id)
                    state = node['doc']['status']
                    if state in ["stopped", "stopping"]:
                        nodes.append(node)
                except Exception as e:
                    cli_logger.warning(instance_id)
                    if e.message == 'Instance not found':
                       continue
                    raise e
            return nodes

    def _create_node(self, base_config, tags, count):
        name_tag = tags[TAG_RAY_NODE_NAME]
        assert (len(name_tag) <=
                (INSTANCE_NAME_MAX_LEN - INSTANCE_NAME_UUID_LEN - 1)) and re.match("^[a-z0-9-:-]*$", name_tag), (
                    name_tag, len(name_tag))

        name = "{name_tag}-{uuid}".format(
                                name_tag=name_tag,
                                uuid=uuid4().hex[:INSTANCE_NAME_UUID_LEN])
        logger.info(f"self._create_instance with {name}")
        instance = self._create_instance(name, base_config)

        resource_model = {'resource_id': instance['crn']}
        tags[TAG_RAY_CLUSTER_NAME] = self.cluster_name

        _tags = [f"{k}:{v}" for k,v in tags.items()]
        if not self._attach_tags(resource_model, _tags):
            # terminate the weird node that failed to be tagged
            self._delete_node(instance['resource_id'])
            cli_logger.error(f"failed to tag node {instance}, terminating instance")
            return {}

        # currently always creating public ip for head node
        if tags['ray-node-type'] == 'head':# or not self.provider_config.get("use_internal_ips", False):
            fip_data = self._create_floating_ip(base_config)
            self._attach_floating_ip(instance, fip_data)

        return instance

    @log_in_out
    def create_node(self, base_config, tags, count) -> None:
        with self.lock:

            # here will be implementation of reuse of stopped instances
            stopped_nodes_dict = {}
        
            # Try to reuse previously stopped nodes with compatible configs
            if self.cache_stopped_nodes:
                stopped_nodes = self._stopped_nodes(tags)
                stopped_nodes_ids = [n['resource_id'] for n in stopped_nodes]
                stopped_nodes_dict = {n['resource_id']: n for n in stopped_nodes}

                if stopped_nodes:
                    cli_logger.print(f"Reusing nodes {stopped_nodes_ids}. "
                    "To disable reuse, set `cache_stopped_nodes: False` "
                    "under `provider` in the cluster configuration.")

                for node in stopped_nodes:
                    logger.info(f"Starting instance {node['resource_id']}")
                    self.ibm_vpc_client.create_instance_action(node['resource_id'], 'start')

                time.sleep(1)

                for node_id in stopped_nodes_ids:
                    #import pdb;pdb.set_trace()
                    self.set_node_tags(node_id, tags)

                count -= len(stopped_nodes_ids)

            created_nodes_dict = {}
            if count:
                created_nodes_dict = self._create_node(base_config, tags, count)

            all_created_nodes = stopped_nodes_dict
            all_created_nodes.update(created_nodes_dict)
            return all_created_nodes

    def _delete_node(self, resource_id):
        logger.error(f'in _delete_node with id {resource_id}')
        try:
            node = self._get_node(resource_id)
            self.ibm_vpc_client.delete_instance(resource_id)
            floating_ips = node.get('floating_ips', [])
            for ip in floating_ips:
                if ip['name'].startswith(RAY_RECYCLABLE): # TODO: replace prefix with tags
                    self.ibm_vpc_client.delete_floating_ip(ip['id'])
        except ApiException as e:
            if e.code == 404:
                pass
            else:
                raise e

    @log_in_out
    def terminate_node(self, node_id):  # TODO: implement  terminate_nodes() as well to optimize. use instance group instead of single instance
        """
        Deletes the VM instance and the associated volume
        """
        logger.debug("Deleting VM instance {}".format(node_id))

        with self.lock:
            """
            Deletes the VM instance and the associated volume
            """
            try:
                if self.cache_stopped_nodes:
                    cli_logger.print(f"Stopping instance {node_id}. To terminate instead, set `cache_stopped_nodes: False` "
                                    "under `provider` in the cluster configuration")

                    self.ibm_vpc_client.create_instance_action(node_id, 'stop')
                else:
                    self._delete_node(node_id)
            except ApiException as e:
                if e.code == 404:
                    pass
                else:
                    raise e

    def _get_node(self, node_id):
        """Refresh and get info for this node, updating the cache."""
        self.non_terminated_nodes({})  # Side effect: updates cache

        with self.lock:
            if node_id in self.cached_nodes:
                return self.cached_nodes[node_id]

            try:
                node = self.ibm_vpc_client.get_instance(node_id).get_result()
            except Exception as e:
                logger.error(f'failed to get instance with id {node_id}')
                raise e
            try:
                node_tags = self.global_tagging_service.list_tags(attached_to=node['crn']).get_result()['items']
            except Exception as e:
                print(f'Error listing tags: {e}')
                self._init()
                node_tags = self.global_tagging_service.list_tags(attached_to=node['crn']).get_result()['items']

            node['tags'] = node_tags[0]
            return node


    def _get_cached_node(self, node_id):
        """Return node info from cache if possible, otherwise fetches it."""
        if node_id in self.cached_nodes:
            return self.cached_nodes[node_id]

        return self._get_node(node_id)


    @staticmethod
    def bootstrap_config(cluster_config):
        return cluster_config
