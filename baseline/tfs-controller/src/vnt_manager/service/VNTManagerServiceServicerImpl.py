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

from typing import Dict, Optional
import grpc, json, logging, uuid
from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import Producer as KafkaProducer
from confluent_kafka import KafkaError
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.proto.context_pb2 import Empty, Link, LinkId, LinkList, LinkTypeEnum
from common.proto.vnt_manager_pb2_grpc import VNTManagerServiceServicer
#from common.tools.context_queries.EndPoint import get_endpoint_names
from common.tools.grpc.Tools import grpc_message_to_json, grpc_message_to_json_string
from common.tools.kafka.Variables import KafkaConfig, KafkaTopic
#from common.tools.object_factory.Device import json_device_id
#from common.tools.object_factory.EndPoint import json_endpoint_id
from common.tools.object_factory.Link import json_link, json_link_id
from context.client.ContextClient import ContextClient
#from .vntm_config_device import configure, deconfigure


LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('VNTManager', 'RPC')


class VNTManagerServiceServicerImpl(VNTManagerServiceServicer):
    def __init__(self):
        LOGGER.debug('Creating Servicer...')
        self.context_client = ContextClient()
        self.links = []
        LOGGER.debug('Servicer Created')

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListVirtualLinks(self, request : Empty, context : grpc.ServicerContext) -> LinkList:
        links = self.context_client.ListLinks(Empty()).links
        return [link for link in links if link.virtual]

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetVirtualLink(self, request : LinkId, context : grpc.ServicerContext) -> Link:
        link = self.context_client.GetLink(request)
        return link if link.virtual else Empty()

    def send_recommendation(self, vntm_request : Dict) -> str:
        request_key = str(uuid.uuid4())
        vntm_request = json.dumps(vntm_request)
        MSG = '[send_recommendation] request_key={:s} vntm_request={:s}'
        LOGGER.info(MSG.format(str(request_key), str(vntm_request)))
        self.kafka_producer = KafkaProducer({
            'bootstrap.servers' : KafkaConfig.get_kafka_address()
        })
        self.kafka_producer.produce(
            KafkaTopic.VNTMANAGER_REQUEST.value,
            key=request_key.encode('utf-8'),
            value=vntm_request.encode('utf-8'),
        )
        self.kafka_producer.flush()
        return request_key

    def send_vlink_create(self, request : Link) -> str:
        return self.send_recommendation({
            'event': 'vlink_create', 'data': grpc_message_to_json_string(request)
        })

    def send_vlink_remove(self, request : LinkId) -> str:
        return self.send_recommendation({
            'event': 'vlink_remove', 'data': grpc_message_to_json_string(request)
        })

    def wait_for_reply(self, request_key : str) -> Optional[Dict]:
        LOGGER.info('[wait_for_reply] request_key={:s}'.format(str(request_key)))

        self.kafka_consumer = KafkaConsumer({
            'bootstrap.servers'   : KafkaConfig.get_kafka_address(),
            'group.id'            : str(uuid.uuid4()),
            'auto.offset.reset'   : 'latest',
            'max.poll.interval.ms': 600000,
            'session.timeout.ms'  : 60000,
        })
        self.kafka_consumer.subscribe([KafkaTopic.VNTMANAGER_RESPONSE.value])

        while True:
            receive_msg = self.kafka_consumer.poll(2.0)
            if receive_msg is None: continue
            LOGGER.info('[wait_for_reply] receive_msg={:s}'.format(str(receive_msg)))
            if receive_msg.error():
                if receive_msg.error().code() == KafkaError._PARTITION_EOF: continue
                LOGGER.error('[wait_for_reply] Consumer error: {:s}'.format(str(receive_msg.error())))
                return None
            
            reply_key = receive_msg.key().decode('utf-8')
            LOGGER.info('[wait_for_reply] reply_key={:s}'.format(str(reply_key)))
            if reply_key == request_key:
                LOGGER.info('[wait_for_reply] match!')
                break
            LOGGER.info('[wait_for_reply] no match... waiting...')

        json_receive_msg = json.loads(receive_msg.value().decode('utf-8'))
        LOGGER.info('[wait_for_reply] json_receive_msg={:s}'.format(str(json_receive_msg)))

        if 'data' not in json_receive_msg:
            MSG = 'Malformed reply: {:s}'
            raise Exception(MSG.format(str(json_receive_msg)))
        data = json_receive_msg['data']

        if 'error' in data:
            MSG = 'Something went wrong: {:s}'
            raise Exception(MSG.format(str(data['error'])))

        if 'result' not in data:
            MSG = 'Malformed reply: {:s}'
            raise Exception(MSG.format(str(data)))
        return data['result']

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SetVirtualLink(self, request : Link, context : grpc.ServicerContext) -> LinkId:
        try:
            LOGGER.info('[SetVirtualLink] request={:s}'.format(grpc_message_to_json_string(request)))
            request_key = self.send_vlink_create(request)
            reply = self.wait_for_reply(request_key)
            LOGGER.info('[SetVirtualLink] reply={:s}'.format(str(reply)))

            # At this point, we know the request is processed and an optical connection was created

            vlink_uuid = reply['vlink_uuid']
            LOGGER.info('[SetVirtualLink] vlink_uuid={:s}'.format(str(vlink_uuid)))

            vlink_name = request.name
            if len(vlink_name) == 0: vlink_name = request.link_id.link_uuid.uuid
            LOGGER.info('[SetVirtualLink] vlink_name={:s}'.format(str(vlink_name)))

            vlink_endpoint_ids = [
                grpc_message_to_json(endpoint_id)
                for endpoint_id in request.link_endpoint_ids
            ]
            LOGGER.info('[SetVirtualLink] vlink_endpoint_ids={:s}'.format(str(vlink_endpoint_ids)))

            total_capacity_gbps = request.attributes.total_capacity_gbps
            LOGGER.info('[SetVirtualLink] total_capacity_gbps={:s}'.format(str(total_capacity_gbps)))

            vlink = Link(**json_link(
                vlink_uuid, vlink_endpoint_ids, name=vlink_name,
                link_type=LinkTypeEnum.LINKTYPE_VIRTUAL,
                total_capacity_gbps=total_capacity_gbps,
            ))
            LOGGER.info('[SetVirtualLink] vlink={:s}'.format(grpc_message_to_json_string(vlink)))

            #device_names, endpoints_data = get_endpoint_names(self.context_client, request.link_endpoint_ids)

            #device_uuid_or_name_a = vlink_endpoint_ids[ 0]['device_id']['device_uuid']['uuid']
            #device_name_a = device_names.get(device_uuid_or_name_a, device_uuid_or_name_a)

            #device_uuid_or_name_b = vlink_endpoint_ids[-1]['device_id']['device_uuid']['uuid']
            #device_name_b = device_names.get(device_uuid_or_name_b, device_uuid_or_name_b)

            #endpoint_uuid_or_name_a = vlink_endpoint_ids[ 0]['endpoint_uuid']['uuid']
            #endpoint_name_a = endpoints_data.get(endpoint_uuid_or_name_a, (endpoint_uuid_or_name_a, None))
            #endpoint_name_a = endpoint_name_a.replace('PORT-', '')

            #endpoint_uuid_or_name_b = vlink_endpoint_ids[-1]['endpoint_uuid']['uuid']
            #endpoint_name_b = endpoints_data.get(endpoint_uuid_or_name_b, (endpoint_uuid_or_name_b, None))
            #endpoint_name_b = endpoint_name_b.replace('PORT-', '')

            #network_instance_name = '-'.join([
            #    device_name_a, endpoint_name_a, device_name_b, endpoint_name_b
            #])
            #configure(
            #    device_name_a, endpoint_name_a, device_name_b, endpoint_name_b, network_instance_name
            #)

            vlink_id = self.context_client.SetLink(vlink)

            MSG = 'Virtual link created, vlink_id={:s}'
            LOGGER.info(MSG.format(grpc_message_to_json_string(vlink_id)))
            return vlink_id
        except: # pylint: disable=bare-except
            MSG = 'Exception setting virtual link={:s}'
            LOGGER.exception(MSG.format(str(request.link_id.link_uuid.uuid)))
            raise

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def RemoveVirtualLink(self, request : LinkId, context : grpc.ServicerContext) -> Empty:
        try:
            LOGGER.info('[RemoveVirtualLink] request={:s}'.format(grpc_message_to_json_string(request)))
            request_key = self.send_vlink_remove(request)
            reply = self.wait_for_reply(request_key)
            LOGGER.info('[RemoveVirtualLink] reply={:s}'.format(str(reply)))

            # At this point, we know the request is processed and an optical connection was removed

            vlink_uuid = request.link_uuid.uuid
            LOGGER.info('[RemoveVirtualLink] vlink_uuid={:s}'.format(str(vlink_uuid)))

            vlink_id = LinkId(**json_link_id(vlink_uuid))
            LOGGER.info('[RemoveVirtualLink] vlink_id={:s}'.format(grpc_message_to_json_string(vlink_id)))

            # deconfigure('CSGW1', 'xe5', 'CSGW2', 'xe5', 'ecoc2024-1')
            self.context_client.RemoveLink(vlink_id)

            MSG = 'Virtual link removed, vlink_id={:s}'
            LOGGER.info(MSG.format(grpc_message_to_json_string(vlink_id)))
            return Empty()
        except: # pylint: disable=bare-except
            MSG = 'Exception removing virtual link={:s}'
            LOGGER.exception(MSG.format(str(request.link_uuid.uuid)))
            raise
