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

import json
import logging
from typing import Dict, List
from flask.json import jsonify
from flask_restful import Resource, request
from werkzeug.exceptions import BadRequest
from common.proto.context_pb2 import Empty, LinkTypeEnum
from common.tools.grpc.Tools import grpc_message_to_json
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from service.client.ServiceClient import ServiceClient
from slice.client.SliceClient import SliceClient
from vnt_manager.client.VNTManagerClient import VNTManagerClient

from .Tools import (
    format_grpc_to_json, grpc_connection_id, grpc_context, grpc_context_id, grpc_device,
    grpc_device_id, grpc_link, grpc_link_id, grpc_policy_rule_id,
    grpc_service_id, grpc_service, grpc_slice, grpc_slice_id, grpc_topology, grpc_topology_id
)

LOGGER = logging.getLogger(__name__)


class _Resource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.context_client = ContextClient()
        self.device_client  = DeviceClient()
        self.service_client = ServiceClient()
        self.vntmanager_client = VNTManagerClient()
        self.slice_client   = SliceClient()

class ContextIds(_Resource):
    def get(self):
        return format_grpc_to_json(self.context_client.ListContextIds(Empty()))

class Contexts(_Resource):
    def get(self):
        return format_grpc_to_json(self.context_client.ListContexts(Empty()))

    def post(self):
        json_requests = request.get_json()
        if 'contexts' in json_requests:
            json_requests = json_requests['contexts']
        return jsonify([
            grpc_message_to_json(self.context_client.SetContext(grpc_context(context)))
            for context in json_requests
        ])

class Context(_Resource):
    def get(self, context_uuid : str):
        return format_grpc_to_json(self.context_client.GetContext(grpc_context_id(context_uuid)))

    def put(self, context_uuid : str):
        context = request.get_json()
        if context_uuid != context['context_id']['context_uuid']['uuid']:
            raise BadRequest('Mismatching context_uuid')
        return format_grpc_to_json(self.context_client.SetContext(grpc_context(context)))

    def delete(self, context_uuid : str):
        return format_grpc_to_json(self.context_client.RemoveContext(grpc_context_id(context_uuid)))

class DummyContexts(_Resource):
    def get(self):
        contexts = grpc_message_to_json(
            self.context_client.ListContexts(Empty()),
            use_integers_for_enums=True
        )['contexts']
        devices = grpc_message_to_json(
            self.context_client.ListDevices(Empty()),
            use_integers_for_enums=True
        )['devices']
        links = grpc_message_to_json(
            self.context_client.ListLinks(Empty()),
            use_integers_for_enums=True
        )['links']

        topologies  = list()
        slices      = list()
        services    = list()
        connections = list()

        for context in contexts:
            context_uuid = context['context_id']['context_uuid']['uuid']
            context_id = grpc_context_id(context_uuid)

            topologies.extend(grpc_message_to_json(
                self.context_client.ListTopologies(context_id),
                use_integers_for_enums=True
            )['topologies'])

            slices.extend(grpc_message_to_json(
                self.context_client.ListSlices(context_id),
                use_integers_for_enums=True
            )['slices'])

            context_services = grpc_message_to_json(
                self.context_client.ListServices(context_id),
                use_integers_for_enums=True
            )['services']
            services.extend(context_services)

            for service in context_services:
                service_uuid = service['service_id']['service_uuid']['uuid']
                service_id = grpc_service_id(context_uuid, service_uuid)
                connections.extend(grpc_message_to_json(
                    self.context_client.ListConnections(service_id),
                    use_integers_for_enums=True
                )['connections'])

        for device in devices:
            for config_rule in device['device_config']['config_rules']:
                if 'custom' not in config_rule: continue
                resource_value = config_rule['custom']['resource_value']
                if not isinstance(resource_value, str): continue
                try:
                    resource_value = json.loads(resource_value)
                except: # pylint: disable=bare-except
                    pass
                config_rule['custom']['resource_value'] = resource_value

        dummy_context = {'dummy_mode': True}
        if len(contexts   ) > 0: dummy_context['contexts'   ] = contexts
        if len(topologies ) > 0: dummy_context['topologies' ] = topologies
        if len(devices    ) > 0: dummy_context['devices'    ] = devices
        if len(links      ) > 0: dummy_context['links'      ] = links
        if len(slices     ) > 0: dummy_context['slices'     ] = slices
        if len(services   ) > 0: dummy_context['services'   ] = services
        if len(connections) > 0: dummy_context['connections'] = connections
        return jsonify(dummy_context)

class TopologyIds(_Resource):
    def get(self, context_uuid : str):
        return format_grpc_to_json(self.context_client.ListTopologyIds(grpc_context_id(context_uuid)))

class Topologies(_Resource):
    def get(self, context_uuid : str):
        return format_grpc_to_json(self.context_client.ListTopologies(grpc_context_id(context_uuid)))

    def post(self, context_uuid : str):
        json_requests = request.get_json()
        if 'topologies' in json_requests:
            json_requests = json_requests['topologies']
        for topology in json_requests:
            if context_uuid != topology['topology_id']['context_id']['context_uuid']['uuid']:
                raise BadRequest('Mismatching context_uuid')
        return jsonify([
            grpc_message_to_json(self.context_client.SetTopology(grpc_topology(topology)))
            for topology in json_requests
        ])

class Topology(_Resource):
    def get(self, context_uuid : str, topology_uuid : str):
        return format_grpc_to_json(self.context_client.GetTopology(grpc_topology_id(context_uuid, topology_uuid)))

    def put(self, context_uuid : str, topology_uuid : str):
        topology = request.get_json()
        if context_uuid != topology['topology_id']['context_id']['context_uuid']['uuid']:
            raise BadRequest('Mismatching context_uuid')
        if topology_uuid != topology['topology_id']['topology_uuid']['uuid']:
            raise BadRequest('Mismatching topology_uuid')
        return format_grpc_to_json(self.context_client.SetTopology(grpc_topology(topology)))

    def delete(self, context_uuid : str, topology_uuid : str):
        return format_grpc_to_json(self.context_client.RemoveTopology(grpc_topology_id(context_uuid, topology_uuid)))

class TopologyDetails(_Resource):
    def get(self, context_uuid : str, topology_uuid : str):
        topology_id = grpc_topology_id(context_uuid, topology_uuid)
        return format_grpc_to_json(self.context_client.GetTopologyDetails(topology_id))

class ServiceIds(_Resource):
    def get(self, context_uuid : str):
        return format_grpc_to_json(self.context_client.ListServiceIds(grpc_context_id(context_uuid)))

class Services(_Resource):
    def get(self, context_uuid : str):
        return format_grpc_to_json(self.context_client.ListServices(grpc_context_id(context_uuid)))

    def post(self, context_uuid : str):
        json_requests = request.get_json()
        if 'services' in json_requests:
            json_requests = json_requests['services']
        if isinstance(json_requests, dict):
            json_requests = [json_requests]
        for service in json_requests:
            if context_uuid != service['service_id']['context_id']['context_uuid']['uuid']:
                raise BadRequest('Mismatching context_uuid')
        return jsonify([
            grpc_message_to_json(self.service_client.CreateService(grpc_service(service)))
            for service in json_requests
        ])

class Service(_Resource):
    def get(self, context_uuid : str, service_uuid : str):
        return format_grpc_to_json(self.context_client.GetService(grpc_service_id(context_uuid, service_uuid)))

    def put(self, context_uuid : str, service_uuid : str):
        service = request.get_json()
        if context_uuid != service['service_id']['context_id']['context_uuid']['uuid']:
            raise BadRequest('Mismatching context_uuid')
        if service_uuid != service['service_id']['service_uuid']['uuid']:
            raise BadRequest('Mismatching service_uuid')
        return format_grpc_to_json(self.service_client.UpdateService(grpc_service(service)))

    def delete(self, context_uuid : str, service_uuid : str):
        return format_grpc_to_json(self.service_client.DeleteService(grpc_service_id(context_uuid, service_uuid)))

class SliceIds(_Resource):
    def get(self, context_uuid : str):
        return format_grpc_to_json(self.context_client.ListSliceIds(grpc_context_id(context_uuid)))

class Slices(_Resource):
    def get(self, context_uuid : str):
        return format_grpc_to_json(self.context_client.ListSlices(grpc_context_id(context_uuid)))

    def post(self, context_uuid : str):
        json_requests = request.get_json()
        if 'slices' in json_requests:
            json_requests = json_requests['slices']
        for slice_ in json_requests:
            if context_uuid != slice_['slice_id']['context_id']['context_uuid']['uuid']:
                raise BadRequest('Mismatching context_uuid')
        return jsonify([
            grpc_message_to_json(self.slice_client.CreateSlice(grpc_slice(slice_)))
            for slice_ in json_requests
        ])

class Slice(_Resource):
    def get(self, context_uuid : str, slice_uuid : str):
        return format_grpc_to_json(self.context_client.GetSlice(grpc_slice_id(context_uuid, slice_uuid)))

    def put(self, context_uuid : str, slice_uuid : str):
        slice_ = request.get_json()
        if context_uuid != slice_['slice_id']['context_id']['context_uuid']['uuid']:
            raise BadRequest('Mismatching context_uuid')
        if slice_uuid != slice_['slice_id']['slice_uuid']['uuid']:
            raise BadRequest('Mismatching slice_uuid')
        return format_grpc_to_json(self.slice_client.UpdateSlice(grpc_slice(slice_)))

    def delete(self, context_uuid : str, slice_uuid : str):
        return format_grpc_to_json(self.slice_client.DeleteSlice(grpc_slice_id(context_uuid, slice_uuid)))

class DeviceIds(_Resource):
    def get(self):
        return format_grpc_to_json(self.context_client.ListDeviceIds(Empty()))

class Devices(_Resource):
    def get(self):
        return format_grpc_to_json(self.context_client.ListDevices(Empty()))

    def post(self):
        json_requests = request.get_json()
        if 'devices' in json_requests:
            json_requests = json_requests['devices']
        return jsonify([
            grpc_message_to_json(self.device_client.AddDevice(grpc_device(device)))
            for device in json_requests
        ])

class Device(_Resource):
    def get(self, device_uuid : str):
        return format_grpc_to_json(self.context_client.GetDevice(grpc_device_id(device_uuid)))

    def put(self, device_uuid : str):
        device = request.get_json()
        if device_uuid != device['device_id']['device_uuid']['uuid']:
            raise BadRequest('Mismatching device_uuid')
        return format_grpc_to_json(self.device_client.ConfigureDevice(grpc_device(device)))

    def delete(self, device_uuid : str):
        return format_grpc_to_json(self.device_client.DeleteDevice(grpc_device_id(device_uuid)))

class LinkIds(_Resource):
    def get(self):
        return format_grpc_to_json(self.context_client.ListLinkIds(Empty()))

class Links(_Resource):
    def get(self):
        return format_grpc_to_json(self.context_client.ListLinks(Empty()))

    def post(self):
        json_requests = request.get_json()
        if 'links' in json_requests:
            json_requests = json_requests['links']
        json_link_ids : List[Dict] = list()
        for link_json in json_requests:
            link = grpc_link(link_json)
            if link.link_type == LinkTypeEnum.LINKTYPE_VIRTUAL:
                link_id = self.vntmanager_client.SetVirtualLink(link)
            else:
                link_id = self.context_client.SetLink(link)
            json_link_ids.append(grpc_message_to_json(link_id))
        return jsonify(json_link_ids)

class Link(_Resource):
    def get(self, link_uuid : str):
        return format_grpc_to_json(self.context_client.GetLink(grpc_link_id(link_uuid)))

    def put(self, link_uuid : str):
        link_json = request.get_json()
        link = grpc_link(link_json)
        if link_uuid != link.link_id.link_uuid.uuid:
            raise BadRequest('Mismatching link_uuid')
        if link.link_type == LinkTypeEnum.LINKTYPE_VIRTUAL:
            return format_grpc_to_json(self.vntmanager_client.SetVirtualLink(link))
        else:
            return format_grpc_to_json(self.context_client.SetLink(link))

    def delete(self, link_uuid : str):
        link_id = grpc_link_id(link_uuid)
        link = self.context_client.GetLink(link_id)
        if link.link_type == LinkTypeEnum.LINKTYPE_VIRTUAL:
            return format_grpc_to_json(self.vntmanager_client.RemoveVirtualLink(link_id))
        else:
            return format_grpc_to_json(self.context_client.RemoveLink(link_id))

class ConnectionIds(_Resource):
    def get(self, context_uuid : str, service_uuid : str):
        return format_grpc_to_json(self.context_client.ListConnectionIds(grpc_service_id(context_uuid, service_uuid)))

class Connections(_Resource):
    def get(self, context_uuid : str, service_uuid : str):
        return format_grpc_to_json(self.context_client.ListConnections(grpc_service_id(context_uuid, service_uuid)))

class Connection(_Resource):
    def get(self, connection_uuid : str):
        return format_grpc_to_json(self.context_client.GetConnection(grpc_connection_id(connection_uuid)))

class PolicyRuleIds(_Resource):
    def get(self):
        return format_grpc_to_json(self.context_client.ListPolicyRuleIds(Empty()))

class PolicyRules(_Resource):
    def get(self):
        return format_grpc_to_json(self.context_client.ListPolicyRules(Empty()))

class PolicyRule(_Resource):
    def get(self, policy_rule_uuid : str):
        return format_grpc_to_json(self.context_client.GetPolicyRule(grpc_policy_rule_id(policy_rule_uuid)))
