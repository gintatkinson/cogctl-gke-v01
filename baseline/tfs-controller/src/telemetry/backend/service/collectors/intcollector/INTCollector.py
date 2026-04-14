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


import pytz
import queue
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from datetime import datetime
from telemetry.backend.service.collector_api._Collector import _Collector

from scapy.all import *
import struct
import socket
import ipaddress

from .INTCollectorCommon import IntDropReport, IntLocalReport, IntFixedReport, FlowInfo
from common.proto.kpi_manager_pb2 import KpiId, KpiDescriptor
from confluent_kafka import Producer as KafkaProducer
from common.tools.kafka.Variables import KafkaConfig, KafkaTopic
from uuid import uuid4
from typing import Dict
from datetime import datetime, timezone
import json

from kpi_manager.client.KpiManagerClient import KpiManagerClient
from common.proto.analytics_frontend_pb2 import Analyzer, AnalyzerId
from context.client.ContextClient import ContextClient
from analytics.frontend.client.AnalyticsFrontendClient import AnalyticsFrontendClient
from common.proto.kpi_sample_types_pb2 import KpiSampleType
import time
import logging

LOGGER = logging.getLogger(__name__)

class INTCollector(_Collector):

    last_packet_time = time.time() # Track last packet time

    max_idle_time = 5  # for how long we tolerate inactivity
    sniff_timeout = 3   # how often we stop sniffing to check for inactivity

    """
    INTCollector is a class that simulates a network collector for testing purposes.
    It provides functionalities to manage configurations, state subscriptions, and synthetic data generation.
    """
    def __init__(self, collector_id: str , address: str, interface: str, port: str, kpi_id: str, service_id: str, context_id: str, **settings):
        super().__init__('int_collector', address, port, **settings)
        self._out_samples    = queue.Queue()                # Queue to hold synthetic state samples
        self._scheduler      = BackgroundScheduler(daemon=True)
        self._scheduler.configure(
            jobstores = {'default': MemoryJobStore()},
            executors = {'default': ThreadPoolExecutor(max_workers=1)},
            timezone  = pytz.utc
        )
        self.kafka_producer = KafkaProducer({'bootstrap.servers': KafkaConfig.get_kafka_address()})
        self.collector_id    = collector_id
        self.interface    = interface
        self.kpi_manager_client = KpiManagerClient()
        self.analytics_frontend_client = AnalyticsFrontendClient()
        self.context_client = ContextClient()
        self.kpi_id     = kpi_id
        self.service_id = service_id
        self.context_id = context_id
        self.table = {}
        self.connected = False          # To track connection state
        LOGGER.info("INT Collector initialized")

    def Connect(self) -> bool:
        LOGGER.info(f"Connecting to {self.interface}:{self.port}")
        self.connected = True

        self._scheduler.add_job(self.sniff_with_restarts_on_idle, id=self.kpi_id ,args=[self.interface , self.port , self.service_id, self.context_id])

        self._scheduler.start()
        LOGGER.info(f"Successfully connected to {self.interface}:{self.port}")
        return True

    def Disconnect(self) -> bool:
        LOGGER.info(f"Disconnecting from {self.interface}:{self.port}")
        if not self.connected:
            LOGGER.warning("INT Collector is not connected. Nothing to disconnect.")
            return False

        self._scheduler.remove_job(self.kpi_id)
        self._scheduler.shutdown()

        self.connected = False
        LOGGER.info(f"Successfully disconnected from {self.interface}:{self.port}")
        return True

    def on_idle_timeout(self):
        LOGGER.info(f"Sniffer idle for more than {self.max_idle_time} seconds.")
        LOGGER.debug(f"last_packet_time {self.last_packet_time} seconds.")

        values = [0]
        for sw_id in range(1, 6):
            sw = self.table.get(sw_id)
            self.overwrite_switch_values(sw , values)

    def overwrite_switch_values(self, switch, values):
        if not switch:
            return

        # Overwrite values using zip
        for key, new_value in zip(switch, values):
            switch[key] = new_value

        for key, value in switch.items():
            self.send_message_to_kafka(key, value)

    def process_packet(self , packet, port, service_id , context_id):
        # global last_packet_time

        # Check for IP layer
        if IP not in packet:
            return None
        ip_layer = packet[IP]
        # ip_pkt = IPPacket(ip_layer[:20])
        # ip_pkt.show()

        # Check for UDP
        if UDP not in ip_layer:
            return None
        udp_layer = ip_layer[UDP]

        # Only the INT port
        if udp_layer.dport != port:
            return None
        # udp_dgram = UDPPacket(bytes(udp_layer))
        # udp_dgram.show()

        src_ip = socket.ntohl(struct.unpack('<I', socket.inet_aton(ip_layer.src))[0])
        src_ip_str = str(ipaddress.IPv4Address(src_ip))
        LOGGER.debug("ip src: {}".format(src_ip_str))

        dst_ip = socket.ntohl(struct.unpack('<I', socket.inet_aton(ip_layer.dst))[0])
        dst_ip_str = str(ipaddress.IPv4Address(dst_ip))
        LOGGER.debug("ip dst: {}".format(dst_ip_str))
        LOGGER.debug("ip-proto: {}".format(ip_layer.proto))

        LOGGER.debug("port src: {}".format(udp_layer.sport))
        LOGGER.debug("port dst: {}".format(udp_layer.dport))

        # Get the INT report data (after UDP header)
        int_data = bytes(udp_layer.payload)

        # Parse fixed report (first 20 bytes)
        offset = 20
        fixed_report = IntFixedReport(int_data[:offset])
        # fixed_report.show()

        drop_report = None
        local_report = None
        lat = 0

        if fixed_report.d == 1:
            drop_report = IntDropReport(int_data[offset:offset + 4])
            offset += 4
            # drop_report.show()
        elif fixed_report.f == 1 or fixed_report.q == 1:
            local_report = IntLocalReport(int_data[offset:offset + 8])
            offset += 8
            lat = local_report.egress_timestamp - fixed_report.ingress_timestamp
            assert lat > 0, "Egress timestamp must be > ingress timestamp"
            # local_report.show()

        # Create flow info
        flow_info = FlowInfo(
            src_ip=src_ip,
            dst_ip=dst_ip,
            src_port=udp_layer.sport,
            dst_port=udp_layer.dport,
            ip_proto=ip_layer.proto,
            flow_sink_time=fixed_report.ingress_timestamp,
            num_int_hop=1,
            seq_num=fixed_report.seq_num,
            switch_id=fixed_report.switch_id,
            ingress_timestamp=fixed_report.ingress_timestamp,
            ingress_port_id=fixed_report.ingress_port_id,
            egress_port_id=fixed_report.egress_port_id,
            queue_id=local_report.queue_id if local_report else 0,
            queue_occupancy=local_report.queue_occupancy if local_report else 0,
            egress_timestamp=local_report.egress_timestamp if local_report else 0,
            is_drop=1 if drop_report else 0,
            drop_reason=drop_report.drop_reason if drop_report else 0,
            hop_latency=lat
        )
        LOGGER.debug(f"Flow info: {flow_info}")

        self.create_descriptors_and_send_to_kafka(flow_info , service_id , context_id)

        self.last_packet_time = time.time()
        return flow_info

    def set_kpi_descriptor(self , kpi_uuid , service_id , device_id , endpoint_id , sample_type):
        kpi_descriptor = KpiDescriptor()
        kpi_descriptor.kpi_sample_type = sample_type
        kpi_descriptor.service_id.service_uuid.uuid = service_id
        # kpi_descriptor.device_id.device_uuid.uuid = device_id
        # kpi_descriptor.endpoint_id.endpoint_uuid.uuid = endpoint_id
        kpi_descriptor.kpi_id.kpi_id.uuid = kpi_uuid

        kpi_id: KpiId = self.kpi_manager_client.SetKpiDescriptor(kpi_descriptor)

        return kpi_id

    def create_descriptors_and_send_to_kafka(self, flow_info , service_id , context_id):
        LOGGER.debug(f"PACKET FROM SWITCH: {flow_info.switch_id} LATENCY: {flow_info.hop_latency}")
        if(self.table.get(flow_info.switch_id) == None):
            seq_num_kpi_id     = str(uuid4())
            ingress_ts_kpi_id  = str(uuid4())
            egress_ts_kpi_id   = str(uuid4())
            hop_lat_kpi_id     = str(uuid4())
            ing_port_id_kpi_id = str(uuid4())
            egr_port_id_kpi_id = str(uuid4())
            queue_occup_kpi_id = str(uuid4())
            is_drop_kpi_id     = str(uuid4())
            sw_lat_kpi_id      = str(uuid4())

            LOGGER.debug(f"seq_num_kpi_id     for switch {flow_info.switch_id}: {seq_num_kpi_id}")
            LOGGER.debug(f"ingress_ts_kpi_id  for switch {flow_info.switch_id}: {ingress_ts_kpi_id}")
            LOGGER.debug(f"egress_ts_kpi_id   for switch {flow_info.switch_id}: {egress_ts_kpi_id}")
            LOGGER.debug(f"hop_lat_kpi_id     for switch {flow_info.switch_id}: {hop_lat_kpi_id}")
            LOGGER.debug(f"ing_port_id_kpi_id for switch {flow_info.switch_id}: {ing_port_id_kpi_id}")
            LOGGER.debug(f"egr_port_id_kpi_id for switch {flow_info.switch_id}: {egr_port_id_kpi_id}")
            LOGGER.debug(f"queue_occup_kpi_id for switch {flow_info.switch_id}: {queue_occup_kpi_id}")
            LOGGER.debug(f"is_drop_kpi_id     for switch {flow_info.switch_id}: {is_drop_kpi_id}")
            LOGGER.debug(f"sw_lat_kpi_id      for switch {flow_info.switch_id}: {sw_lat_kpi_id}")

            seq_num_kpi           = self.set_kpi_descriptor(seq_num_kpi_id,     service_id ,'', '', KpiSampleType.KPISAMPLETYPE_INT_SEQ_NUM)
            ingress_timestamp_kpi = self.set_kpi_descriptor(ingress_ts_kpi_id,  service_id, '', '', KpiSampleType.KPISAMPLETYPE_INT_TS_ING)
            egress_timestamp_kpi  = self.set_kpi_descriptor(egress_ts_kpi_id,   service_id, '', '', KpiSampleType.KPISAMPLETYPE_INT_TS_EGR)
            hop_latency_kpi       = self.set_kpi_descriptor(hop_lat_kpi_id,     service_id, '', '', KpiSampleType.KPISAMPLETYPE_INT_HOP_LAT)
            ingress_port_id_kpi   = self.set_kpi_descriptor(ing_port_id_kpi_id, service_id, '', '', KpiSampleType.KPISAMPLETYPE_INT_PORT_ID_ING)
            egress_port_id_kpi    = self.set_kpi_descriptor(egr_port_id_kpi_id, service_id, '', '', KpiSampleType.KPISAMPLETYPE_INT_PORT_ID_EGR)
            queue_occup_kpi       = self.set_kpi_descriptor(queue_occup_kpi_id, service_id, '', '', KpiSampleType.KPISAMPLETYPE_INT_QUEUE_OCCUP)
            is_drop_kpi           = self.set_kpi_descriptor(is_drop_kpi_id,     service_id, '', '', KpiSampleType.KPISAMPLETYPE_INT_IS_DROP)

            # Set a dedicated KPI descriptor for every switch
            sw_lat_kpi = None
            sw_sample_types = [
                KpiSampleType.KPISAMPLETYPE_INT_HOP_LAT_SW01, KpiSampleType.KPISAMPLETYPE_INT_HOP_LAT_SW02,
                KpiSampleType.KPISAMPLETYPE_INT_HOP_LAT_SW03, KpiSampleType.KPISAMPLETYPE_INT_HOP_LAT_SW04,
                KpiSampleType.KPISAMPLETYPE_INT_HOP_LAT_SW05, KpiSampleType.KPISAMPLETYPE_INT_HOP_LAT_SW06,
                KpiSampleType.KPISAMPLETYPE_INT_HOP_LAT_SW07, KpiSampleType.KPISAMPLETYPE_INT_HOP_LAT_SW08,
                KpiSampleType.KPISAMPLETYPE_INT_HOP_LAT_SW09, KpiSampleType.KPISAMPLETYPE_INT_HOP_LAT_SW10
            ]
            for i, sw_id in enumerate(range(1, 11)):
                if flow_info.switch_id == sw_id:
                    LOGGER.debug(f"SET KPI : seq_num_kpi_id for switch {flow_info.switch_id}: {sw_lat_kpi_id}")
                    sw_lat_kpi = self.set_kpi_descriptor(sw_lat_kpi_id, service_id, '', '', sw_sample_types[i])

            # Gather keys and values
            keys   = [
                seq_num_kpi.kpi_id.uuid,
                ingress_timestamp_kpi.kpi_id.uuid,
                egress_timestamp_kpi.kpi_id.uuid,
                hop_latency_kpi.kpi_id.uuid,
                ingress_port_id_kpi.kpi_id.uuid,
                egress_port_id_kpi.kpi_id.uuid,
                queue_occup_kpi.kpi_id.uuid,
                is_drop_kpi.kpi_id.uuid,
                sw_lat_kpi.kpi_id.uuid
            ]
            values = [
                flow_info.seq_num,
                flow_info.ingress_timestamp,
                flow_info.egress_timestamp,
                flow_info.hop_latency,
                flow_info.ingress_port_id,
                flow_info.egress_port_id,
                flow_info.queue_occupancy,
                flow_info.is_drop,
                flow_info.hop_latency
            ]
            assert len(keys) == len(values), "KPI keys and values must agree"
            switch = {keys[i]: values[i] for i in range(len(keys))}

            self.table[flow_info.switch_id] = switch

            # Dispatch to Kafka
            for key, value in switch.items():
                self.send_message_to_kafka(key, value)
        else:
            values = [
                flow_info.seq_num,
                flow_info.ingress_timestamp,
                flow_info.egress_timestamp,
                flow_info.hop_latency,
                flow_info.ingress_port_id,
                flow_info.egress_port_id,
                flow_info.queue_occupancy,
                flow_info.is_drop,
                flow_info.hop_latency
            ]
            switch = self.table.get(flow_info.switch_id)

            # Overwrite values using zip
            self.overwrite_switch_values(switch , values)

    def send_message_to_kafka(self , kpi_id , measured_kpi_value):
        producer = self.kafka_producer
        kpi_value: Dict = {
            "time_stamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "kpi_id": kpi_id,
            "kpi_value": measured_kpi_value
        }
        producer.produce(
            KafkaTopic.VALUE.value,
            key=self.collector_id,
            value=json.dumps(kpi_value),
            callback=self.delivery_callback
        )
        producer.flush()
        LOGGER.debug(f"Message with kpi_id: {kpi_id} was send to kafka!")

    def packet_callback(self, packet, port , service_id,context_id):
        flow_info = self.process_packet(packet , port , service_id, context_id)
        if flow_info:
            LOGGER.debug(f"Flow info: {flow_info}")

    def sniff_with_restarts_on_idle(self, interface, port, service_id , context_id):
        while True:
            # Run sniff for a short period to periodically check for idle timeout
            sniff(
                iface=interface,
                filter=f"udp port {port}",
                prn=lambda pkt: self.packet_callback(pkt, port, service_id , context_id),
                timeout=self.sniff_timeout
            )

            if not self.connected:
                break

            # Check if idle period has been exceeded
            now = time.time()
            if (now - self.last_packet_time) > self.max_idle_time:
                self.on_idle_timeout()
                self.last_packet_time = now  # Reset timer after action

    def delivery_callback(self, err, msg):
        if err:
            LOGGER.error('Message delivery failed: {:s}'.format(str(err)))
