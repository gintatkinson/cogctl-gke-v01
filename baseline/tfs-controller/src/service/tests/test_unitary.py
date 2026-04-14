# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy, grpc, logging, pytest
from common.proto.context_pb2 import (
    Context, ContextId, Device, DeviceId, Link, LinkId, Service, ServiceId, Topology, TopologyId)
from common.tests.PytestGenerateTests import pytest_generate_tests # (required) pylint: disable=unused-import
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from service.client.ServiceClient import ServiceClient
from .PrepareTestScenario import ( # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    # mock_service,
    service_service, context_client, device_client, service_client
)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

try:
    from .ServiceHandlersToTest import SERVICE_HANDLERS_TO_TEST
except ImportError:
    LOGGER.exception('Unable to load service handlers, nothing will be tested.')
    SERVICE_HANDLERS_TO_TEST = []

class TestServiceHandlers:
    scenarios = SERVICE_HANDLERS_TO_TEST

    def test_prepare_environment(
        self, contexts, topologies, devices, links, service_id, service_descriptor, service_endpoint_ids,
        service_config_rules, service_constraints, service_constraints_location, service_constraints_location_new,
        context_client : ContextClient,     # pylint: disable=redefined-outer-name
        device_client : DeviceClient,       # pylint: disable=redefined-outer-name
        service_client : ServiceClient):    # pylint: disable=redefined-outer-name

        for context in contexts: context_client.SetContext(Context(**context))
        for topology in topologies: context_client.SetTopology(Topology(**topology))
        for device in devices: device_client.AddDevice(Device(**device))
        for link in links: context_client.SetLink(Link(**link))


    def test_service_create_error_cases(
        self, contexts, topologies, devices, links, service_id, service_descriptor, service_endpoint_ids,
        service_config_rules, service_constraints, service_constraints_location, service_constraints_location_new,
        context_client : ContextClient,     # pylint: disable=redefined-outer-name
        device_client : DeviceClient,       # pylint: disable=redefined-outer-name
        service_client : ServiceClient):    # pylint: disable=redefined-outer-name

        with pytest.raises(grpc.RpcError) as e:
            service_with_endpoints = copy.deepcopy(service_descriptor)
            service_with_endpoints['service_endpoint_ids'].extend(service_endpoint_ids)
            service_client.CreateService(Service(**service_with_endpoints))
        assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        msg_head = 'service.service_endpoint_ids(['
        msg_tail = ']) is invalid; RPC method CreateService does not accept Endpoints. '\
                'Endpoints should be configured after creating the service.'
        except_msg = str(e.value.details())
        assert except_msg.startswith(msg_head) and except_msg.endswith(msg_tail)

        with pytest.raises(grpc.RpcError) as e:
            service_with_config_rules = copy.deepcopy(service_descriptor)
            service_with_config_rules['service_config']['config_rules'].extend(service_config_rules)
            service_client.CreateService(Service(**service_with_config_rules))
        assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        msg_head = 'service.service_config.config_rules(['
        msg_tail = ']) is invalid; RPC method CreateService does not accept Config Rules. '\
                'Config Rules should be configured after creating the service.'
        except_msg = str(e.value.details())
        assert except_msg.startswith(msg_head) and except_msg.endswith(msg_tail)

        with pytest.raises(grpc.RpcError) as e:
            service_with_constraints = copy.deepcopy(service_descriptor)
            service_with_constraints['service_constraints'].extend(service_constraints)
            service_client.CreateService(Service(**service_with_constraints))
        assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT
        msg_head = 'service.service_constraints(['
        msg_tail = ']) is invalid; RPC method CreateService does not accept Constraints. '\
                'Constraints should be configured after creating the service.'
        except_msg = str(e.value.details())
        assert except_msg.startswith(msg_head) and except_msg.endswith(msg_tail)


    def test_service_create_correct(
        self, contexts, topologies, devices, links, service_id, service_descriptor, service_endpoint_ids,
        service_config_rules, service_constraints, service_constraints_location, service_constraints_location_new,
        context_client : ContextClient,     # pylint: disable=redefined-outer-name
        device_client : DeviceClient,       # pylint: disable=redefined-outer-name
        service_client : ServiceClient):    # pylint: disable=redefined-outer-name

        service_client.CreateService(Service(**service_descriptor))


    def test_service_get_created(
        self, contexts, topologies, devices, links, service_id, service_descriptor, service_endpoint_ids,
        service_config_rules, service_constraints, service_constraints_location, service_constraints_location_new,
        context_client : ContextClient,     # pylint: disable=redefined-outer-name
        device_client : DeviceClient,       # pylint: disable=redefined-outer-name
        service_client : ServiceClient):    # pylint: disable=redefined-outer-name

        service_data = context_client.GetService(ServiceId(**service_id))
        LOGGER.info('service_data = {:s}'.format(grpc_message_to_json_string(service_data)))


    def test_service_update_configure(
        self, contexts, topologies, devices, links, service_id, service_descriptor, service_endpoint_ids,
        service_config_rules, service_constraints, service_constraints_location, service_constraints_location_new,
        context_client : ContextClient,     # pylint: disable=redefined-outer-name
        device_client : DeviceClient,       # pylint: disable=redefined-outer-name
        service_client : ServiceClient):    # pylint: disable=redefined-outer-name

        service_with_settings = copy.deepcopy(service_descriptor)
        service_with_settings['service_endpoint_ids'].extend(service_endpoint_ids)
        service_with_settings['service_config']['config_rules'].extend(service_config_rules)
        service_with_settings['service_constraints'].extend(service_constraints)
        service_client.UpdateService(Service(**service_with_settings))
        for endpoint_id in service_endpoint_ids:
            device_id = endpoint_id['device_id']
            device_data = context_client.GetDevice(DeviceId(**device_id))
            for i,config_rule in enumerate(device_data.device_config.config_rules):
                LOGGER.info('device_data[{:s}][#{:d}] => {:s}'.format(
                    str(device_id), i, grpc_message_to_json_string(config_rule)))

    def test_service_update_deconfigure(
        self, contexts, topologies, devices, links, service_id, service_descriptor, service_endpoint_ids,
        service_config_rules, service_constraints, service_constraints_location, service_constraints_location_new,
        context_client : ContextClient,     # pylint: disable=redefined-outer-name
        device_client : DeviceClient,       # pylint: disable=redefined-outer-name
        service_client : ServiceClient):    # pylint: disable=redefined-outer-name

        service_with_settings = copy.deepcopy(service_descriptor)
        service_with_settings['service_endpoint_ids'].extend([]) # remove endpoints
        service_client.UpdateService(Service(**service_with_settings))

        for endpoint_id in service_endpoint_ids:
            device_id = endpoint_id['device_id']
            device_data = context_client.GetDevice(DeviceId(**device_id))
            for i,config_rule in enumerate(device_data.device_config.config_rules):
                LOGGER.info('device_data[{:s}][#{:d}] => {:s}'.format(
                    str(device_id), i, grpc_message_to_json_string(config_rule)))


    def test_service_get_updated(
        self, contexts, topologies, devices, links, service_id, service_descriptor, service_endpoint_ids,
        service_config_rules, service_constraints, service_constraints_location, service_constraints_location_new,
        context_client : ContextClient,     # pylint: disable=redefined-outer-name
        device_client : DeviceClient,       # pylint: disable=redefined-outer-name
        service_client : ServiceClient):    # pylint: disable=redefined-outer-name

        service_data = context_client.GetService(ServiceId(**service_id))
        LOGGER.info('service_data = {:s}'.format(grpc_message_to_json_string(service_data)))


    def test_service_update_configure_loc(
        self, contexts, topologies, devices, links, service_id, service_descriptor, service_endpoint_ids,
        service_config_rules, service_constraints, service_constraints_location, service_constraints_location_new,
        context_client : ContextClient,     # pylint: disable=redefined-outer-name
        device_client : DeviceClient,       # pylint: disable=redefined-outer-name
        service_client : ServiceClient):    # pylint: disable=redefined-outer-name

        service_with_settings = copy.deepcopy(service_descriptor)
        service_with_settings['service_config']['config_rules'].extend(service_config_rules)
        service_with_settings['service_constraints'].extend(service_constraints_location)
        service_client.UpdateService(Service(**service_with_settings))

        for endpoint_id in service_endpoint_ids:
            device_id = endpoint_id['device_id']
            device_data = context_client.GetDevice(DeviceId(**device_id))
            for i,config_rule in enumerate(device_data.device_config.config_rules):
                LOGGER.info('device_data[{:s}][#{:d}] => {:s}'.format(
                    str(device_id), i, grpc_message_to_json_string(config_rule)))


    def test_service_get_updated_1(
        self, contexts, topologies, devices, links, service_id, service_descriptor, service_endpoint_ids,
        service_config_rules, service_constraints, service_constraints_location, service_constraints_location_new,
        context_client : ContextClient,     # pylint: disable=redefined-outer-name
        device_client : DeviceClient,       # pylint: disable=redefined-outer-name
        service_client : ServiceClient):    # pylint: disable=redefined-outer-name

        service_data = context_client.GetService(ServiceId(**service_id))
        LOGGER.info('service_data = {:s}'.format(grpc_message_to_json_string(service_data)))


    def test_service_update_configure_loc_new(
        self, contexts, topologies, devices, links, service_id, service_descriptor, service_endpoint_ids,
        service_config_rules, service_constraints, service_constraints_location, service_constraints_location_new,
        context_client : ContextClient,     # pylint: disable=redefined-outer-name
        device_client : DeviceClient,       # pylint: disable=redefined-outer-name
        service_client : ServiceClient):    # pylint: disable=redefined-outer-name
    
        service_with_settings = copy.deepcopy(service_descriptor)
        service_with_settings['service_config']['config_rules'].extend(service_config_rules)
        service_with_settings['service_constraints'].extend(service_constraints_location_new)
        service_client.UpdateService(Service(**service_with_settings))

        for endpoint_id in service_endpoint_ids:
            device_id = endpoint_id['device_id']
            device_data = context_client.GetDevice(DeviceId(**device_id))
            for i,config_rule in enumerate(device_data.device_config.config_rules):
                LOGGER.info('device_data[{:s}][#{:d}] => {:s}'.format(
                    str(device_id), i, grpc_message_to_json_string(config_rule)))


    def test_service_get_updated_2(
        self, contexts, topologies, devices, links, service_id, service_descriptor, service_endpoint_ids,
        service_config_rules, service_constraints, service_constraints_location, service_constraints_location_new,
        context_client : ContextClient,     # pylint: disable=redefined-outer-name
        device_client : DeviceClient,       # pylint: disable=redefined-outer-name
        service_client : ServiceClient):    # pylint: disable=redefined-outer-name

        service_data = context_client.GetService(ServiceId(**service_id))
        LOGGER.info('service_data = {:s}'.format(grpc_message_to_json_string(service_data)))

    def test_service_delete_loc(
        self, contexts, topologies, devices, links, service_id, service_descriptor, service_endpoint_ids,
        service_config_rules, service_constraints, service_constraints_location, service_constraints_location_new,
        context_client : ContextClient,     # pylint: disable=redefined-outer-name
        device_client : DeviceClient,       # pylint: disable=redefined-outer-name
        service_client : ServiceClient):    # pylint: disable=redefined-outer-name

        service_client.DeleteService(ServiceId(**service_id))

    def test_cleanup_environment(
        self, contexts, topologies, devices, links, service_id, service_descriptor, service_endpoint_ids,
        service_config_rules, service_constraints, service_constraints_location, service_constraints_location_new,
        context_client : ContextClient,     # pylint: disable=redefined-outer-name
        device_client : DeviceClient,       # pylint: disable=redefined-outer-name
        service_client : ServiceClient):    # pylint: disable=redefined-outer-name

        for link in links: context_client.RemoveLink(LinkId(**link['link_id']))
        for device in devices: device_client.DeleteDevice(DeviceId(**device['device_id']))
        for topology in topologies: context_client.RemoveTopology(TopologyId(**topology['topology_id']))
        for context in contexts: context_client.RemoveContext(ContextId(**context['context_id']))
