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

src/common/tools/service/DeviceCheckers.py
    import grpc
    from common.database.api.Database import Database
    from common.database.api.context.topology.device.Device import Device
    from common.database.api.context.topology.device.Endpoint import Endpoint
    from common.exceptions.ServiceException import ServiceException

    def check_device_exists(database : Database, context_id : str, topology_id : str, device_id : str) -> Device:
        db_context = database.context(context_id).create()
        db_topology = db_context.topology(topology_id).create()
        if db_topology.devices.contains(device_id): return db_topology.device(device_id)
        msg = 'Context({})/Topology({})/Device({}) does not exist in the database.'
        msg = msg.format(context_id, topology_id, device_id)
        raise ServiceException(grpc.StatusCode.NOT_FOUND, msg)


src/common/tools/service/LinkCheckers.py
    import grpc
    from common.database.api.Database import Database
    from common.database.api.context.topology.link.Link import Link
    from common.exceptions.ServiceException import ServiceException

    def check_link_exists(database : Database, context_id : str, topology_id : str, link_id : str) -> Link:
        db_context = database.context(context_id).create()
        db_topology = db_context.topology(topology_id).create()
        if db_topology.links.contains(link_id): return db_topology.link(link_id)
        msg = 'Context({})/Topology({})/Link({}) does not exist in the database.'
        msg = msg.format(context_id, topology_id, link_id)
        raise ServiceException(grpc.StatusCode.NOT_FOUND, msg)


src/common/tools/service/ServiceCheckers.py
    import grpc
    from common.database.api.Database import Database
    from common.exceptions.ServiceException import ServiceException

    def check_service_exists(database : Database, context_id : str, service_id : str):
        if not database.contexts.contains(context_id):
            msg = 'Context({}) does not exist in the database.'
            msg = msg.format(context_id)
            raise ServiceException(grpc.StatusCode.NOT_FOUND, msg)

        db_context = database.context(context_id)
        if db_context.services.contains(service_id):
            return db_context.service(service_id)

        msg = 'Context({})/Service({}) does not exist in the database.'
        msg = msg.format(context_id, service_id)
        raise ServiceException(grpc.StatusCode.NOT_FOUND, msg)


src/device/service/Tools.py
    import grpc, logging
    from typing import Dict, List, Set, Tuple
    from common.Checkers import chk_options, chk_string
    from common.database.api.Database import Database
    from common.database.api.context.Constants import DEFAULT_CONTEXT_ID, DEFAULT_TOPOLOGY_ID
    from common.database.api.context.topology.device.Endpoint import Endpoint
    from common.database.api.context.topology.device.OperationalStatus import OperationalStatus, \
        operationalstatus_enum_values, to_operationalstatus_enum
    from common.exceptions.ServiceException import ServiceException
    from common.tools.service.DeviceCheckers import check_device_endpoint_exists
    from common.tools.service.EndpointIdCheckers import check_endpoint_id
    from common.tools.service.EnumCheckers import check_enum
    from common.tools.service.DeviceCheckers import check_device_exists, check_device_not_exists
    from device.proto.context_pb2 import Device, DeviceId

    # For each method name, define acceptable device operational statuses. Empty set means accept all.
    ACCEPTED_DEVICE_OPERATIONAL_STATUSES : Dict[str, Set[OperationalStatus]] = {
        'AddDevice': set([OperationalStatus.ENABLED, OperationalStatus.DISABLED]),
        'UpdateDevice': set([OperationalStatus.KEEP_STATE, OperationalStatus.ENABLED, OperationalStatus.DISABLED]),
    }

    def _check_device_exists(method_name : str, database : Database, device_id : str):
        if method_name in ['AddDevice']:
            check_device_not_exists(database, DEFAULT_CONTEXT_ID, DEFAULT_TOPOLOGY_ID, device_id)
        elif method_name in ['UpdateDevice', 'DeleteDevice']:
            check_device_exists(database, DEFAULT_CONTEXT_ID, DEFAULT_TOPOLOGY_ID, device_id)
        else:                                       # pragma: no cover (test requires malforming the code)
            msg = 'Unexpected condition: _check_device_exists(method_name={}, device_id={})'
            msg = msg.format(str(method_name), str(device_id))
            raise ServiceException(grpc.StatusCode.UNIMPLEMENTED, msg)

    def _check_device_endpoint_exists_or_get_pointer(
        method_name : str, database : Database, parent_name : str, device_id : str, endpoint_id : str) -> Endpoint:

        if method_name in ['AddDevice']:
            db_context = database.context(DEFAULT_CONTEXT_ID)
            db_topology = db_context.topology(DEFAULT_TOPOLOGY_ID)
            db_device = db_topology.device(device_id)
            return db_device.endpoint(endpoint_id)
        elif method_name in ['UpdateDevice', 'DeleteDevice']:
            return check_device_endpoint_exists(
                database, parent_name, DEFAULT_CONTEXT_ID, DEFAULT_TOPOLOGY_ID, device_id, endpoint_id)
        else:                                       # pragma: no cover (test requires malforming the code)
            msg = 'Unexpected condition: _check_device_endpoint_exists_or_get_pointer(method_name={}, ' \
                'parent_name={}, device_id={}, endpoint_id={})'
            msg = msg.format(str(method_name), str(parent_name), str(device_id), str(endpoint_id))
            raise ServiceException(grpc.StatusCode.UNIMPLEMENTED, msg)

    def check_device_operational_status(method_name : str, value : str) -> OperationalStatus:
        return check_enum(
            'OperationalStatus', method_name, value, to_operationalstatus_enum, ACCEPTED_DEVICE_OPERATIONAL_STATUSES)

    def check_device_request(
        method_name : str, request : Device, database : Database, logger : logging.Logger
        ) -> Tuple[str, str, str, OperationalStatus, List[Tuple[Endpoint, str]]]:

        # ----- Parse attributes -------------------------------------------------------------------------------------------
        try:
            device_id     = chk_string ('device.device_id.device_id.uuid',
                                        request.device_id.device_id.uuid,
                                        allow_empty=False)
            device_type   = chk_string ('device.device_type',
                                        request.device_type,
                                        allow_empty=False)
            device_config = chk_string ('device.device_config.device_config',
                                        request.device_config.device_config,
                                        allow_empty=True)
            device_opstat = chk_options('device.devOperationalStatus',
                                        request.devOperationalStatus,
                                        operationalstatus_enum_values())
        except Exception as e:
            logger.exception('Invalid arguments:')
            raise ServiceException(grpc.StatusCode.INVALID_ARGUMENT, str(e))

        device_opstat = check_device_operational_status(method_name, device_opstat)

        # ----- Check if device exists in database -------------------------------------------------------------------------
        _check_device_exists(method_name, database, device_id)

        # ----- Parse endpoints and check if they exist in the database as device endpoints --------------------------------
        add_topology_devices_endpoints : Dict[str, Dict[str, Set[str]]] = {}
        db_endpoints__port_types : List[Tuple[Endpoint, str]] = []
        for endpoint_number,endpoint in enumerate(request.endpointList):
            parent_name = 'Endpoint(#{}) of Context({})/Topology({})/Device({})'
            parent_name = parent_name.format(endpoint_number, DEFAULT_CONTEXT_ID, DEFAULT_TOPOLOGY_ID, device_id)

            _, ep_device_id, ep_port_id = check_endpoint_id(
                logger, endpoint_number, parent_name, endpoint.port_id, add_topology_devices_endpoints,
                predefined_device_id=device_id, acceptable_device_ids=set([device_id]),
                prevent_same_device_multiple_times=False)

            try:
                ep_port_type = chk_string('endpoint[#{}].port_type'.format(endpoint_number),
                                        endpoint.port_type,
                                        allow_empty=False)
            except Exception as e:
                logger.exception('Invalid arguments:')
                raise ServiceException(grpc.StatusCode.INVALID_ARGUMENT, str(e))

            db_endpoint = _check_device_endpoint_exists_or_get_pointer(
                method_name, database, parent_name, ep_device_id, ep_port_id)
            db_endpoints__port_types.append((db_endpoint, ep_port_type))

        return device_id, device_type, device_config, device_opstat, db_endpoints__port_types

    def check_device_id_request(
        method_name : str, request : DeviceId, database : Database, logger : logging.Logger) -> str:

        # ----- Parse attributes -------------------------------------------------------------------------------------------
        try:
            device_id = chk_string('device_id.device_id.uuid',
                                request.device_id.uuid,
                                allow_empty=False)
        except Exception as e:
            logger.exception('Invalid arguments:')
            raise ServiceException(grpc.StatusCode.INVALID_ARGUMENT, str(e))

        # ----- Check if device exists in database ---------------------------------------------------------------------------
        _check_device_exists(method_name, database, device_id)

        return device_id


src/service/service/Tools.py
