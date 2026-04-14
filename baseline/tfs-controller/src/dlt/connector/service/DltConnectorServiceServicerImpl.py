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

import logging
from grpc.aio import ServicerContext
from typing import Optional
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method_async
from common.proto.context_pb2 import Empty, TopologyId
from common.proto.dlt_connector_pb2 import DltDeviceId, DltLinkId, DltServiceId, DltSliceId
from common.proto.dlt_connector_pb2_grpc import DltConnectorServiceServicer
from common.proto.dlt_gateway_pb2 import DltRecord, DltRecordId, DltRecordOperationEnum, DltRecordTypeEnum
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from dlt.connector.client.DltGatewayClientAsync import DltGatewayClientAsync
from .tools.Checkers import record_exists

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('DltConnector', 'RPC')

class DltConnectorServiceServicerImpl(DltConnectorServiceServicer):
    def __init__(self):
        LOGGER.debug('Creating Servicer...')
        self.dltgateway_client = DltGatewayClientAsync()
        LOGGER.debug('Servicer Created')

    async def initialize(self):
        await self.dltgateway_client.connect()

    @safe_and_metered_rpc_method_async(METRICS_POOL, LOGGER)
    async def RecordAll(self, request : TopologyId, context : ServicerContext) -> Empty:
        return Empty()

    @safe_and_metered_rpc_method_async(METRICS_POOL, LOGGER)
    async def RecordAllDevices(self, request : TopologyId, context : ServicerContext) -> Empty:
        return Empty()

    @safe_and_metered_rpc_method_async(METRICS_POOL, LOGGER)
    async def RecordDevice(self, request : DltDeviceId, context : ServicerContext) -> Empty:
        data_json = None
        LOGGER.debug('RECORD_DEVICE = {:s}'.format(grpc_message_to_json_string(request)))
        if not request.delete:       
            context_client = ContextClient()
            device = context_client.GetDevice(request.device_id)
            data_json = grpc_message_to_json_string(device)

        await self._record_entity(
            request.topology_id.topology_uuid.uuid, DltRecordTypeEnum.DLTRECORDTYPE_DEVICE,
            request.device_id.device_uuid.uuid, request.delete, data_json)
        return Empty()

    @safe_and_metered_rpc_method_async(METRICS_POOL, LOGGER)
    async def RecordAllLinks(self, request : TopologyId, context : ServicerContext) -> Empty:
        return Empty()

    @safe_and_metered_rpc_method_async(METRICS_POOL, LOGGER)
    async def RecordLink(self, request : DltLinkId, context : ServicerContext) -> Empty:
        data_json = None
        LOGGER.debug('RECORD_LINK = {:s}'.format(grpc_message_to_json_string(request)))

        if not request.delete:
            context_client = ContextClient()
            link = context_client.GetLink(request.link_id)
            data_json = grpc_message_to_json_string(link)

        await self._record_entity(
            request.topology_id.topology_uuid.uuid, DltRecordTypeEnum.DLTRECORDTYPE_LINK,
            request.link_id.link_uuid.uuid, request.delete, data_json)
        return Empty()

    @safe_and_metered_rpc_method_async(METRICS_POOL, LOGGER)
    async def RecordAllServices(self, request : TopologyId, context : ServicerContext) -> Empty:
        return Empty()

    @safe_and_metered_rpc_method_async(METRICS_POOL, LOGGER)
    async def RecordService(self, request : DltServiceId, context : ServicerContext) -> Empty:
        data_json = None
        if not request.delete:
            context_client = ContextClient()
            service = context_client.GetService(request.service_id)
            data_json = grpc_message_to_json_string(service)

        await self._record_entity(
            request.topology_id.topology_uuid.uuid, DltRecordTypeEnum.DLTRECORDTYPE_SERVICE,
            request.service_id.service_uuid.uuid, request.delete, data_json)
        return Empty()

    @safe_and_metered_rpc_method_async(METRICS_POOL, LOGGER)
    async def RecordAllSlices(self, request : TopologyId, context : ServicerContext) -> Empty:
        return Empty()

    @safe_and_metered_rpc_method_async(METRICS_POOL, LOGGER)
    async def RecordSlice(self, request : DltSliceId, context : ServicerContext) -> Empty:
        data_json = None
        if not request.delete:
            context_client = ContextClient()
            slice_ = context_client.GetSlice(request.slice_id)
            data_json = grpc_message_to_json_string(slice_)

        await self._record_entity(
            request.topology_id.topology_uuid.uuid, DltRecordTypeEnum.DLTRECORDTYPE_SLICE,
            request.slice_id.slice_uuid.uuid, request.delete, data_json)
        return Empty()

    async def _record_entity(
        self, dlt_domain_uuid : str, dlt_record_type : DltRecordTypeEnum, dlt_record_uuid : str, delete : bool,
        data_json : Optional[str] = None
    ) -> None:
        dlt_record_id = DltRecordId()
        dlt_record_id.domain_uuid.uuid = dlt_domain_uuid    # pylint: disable=no-member
        dlt_record_id.type             = dlt_record_type
        dlt_record_id.record_uuid.uuid = dlt_record_uuid    # pylint: disable=no-member

        str_dlt_record_id = grpc_message_to_json_string(dlt_record_id)
        LOGGER.debug('[_record_entity] sent dlt_record_id = {:s}'.format(str_dlt_record_id))
        dlt_record = await self.dltgateway_client.GetFromDlt(dlt_record_id)
        str_dlt_record = grpc_message_to_json_string(dlt_record)
        LOGGER.debug('[_record_entity] recv dlt_record = {:s}'.format(str_dlt_record))

        exists = record_exists(dlt_record)
        LOGGER.debug('[_record_entity] exists = {:s}'.format(str(exists)))

        dlt_record = DltRecord()
        dlt_record.record_id.CopyFrom(dlt_record_id)    # pylint: disable=no-member
        if delete and exists:
            dlt_record.operation = DltRecordOperationEnum.DLTRECORDOPERATION_DELETE
        elif not delete and exists:
            dlt_record.operation = DltRecordOperationEnum.DLTRECORDOPERATION_UPDATE
            if data_json is None:
                raise Exception('data_json must be provided when updating')
            dlt_record.data_json = data_json
        elif not delete and not exists:
            dlt_record.operation = DltRecordOperationEnum.DLTRECORDOPERATION_ADD
            if data_json is None:
                raise Exception('data_json must be provided when adding')
            dlt_record.data_json = data_json
        else:
            return

        str_dlt_record = grpc_message_to_json_string(dlt_record)
        LOGGER.debug('[_record_entity] sent dlt_record = {:s}'.format(str_dlt_record))
        dlt_record_status = await self.dltgateway_client.RecordToDlt(dlt_record)
        str_dlt_record_status = grpc_message_to_json_string(dlt_record_status)
        LOGGER.debug('[_record_entity] recv dlt_record_status = {:s}'.format(str_dlt_record_status))
