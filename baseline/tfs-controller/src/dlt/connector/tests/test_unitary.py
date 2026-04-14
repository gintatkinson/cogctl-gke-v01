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

#import logging
#from typing import Tuple
#from common.orm.Database import Database
#from common.message_broker.MessageBroker import MessageBroker
#from common.proto.context_pb2 import Context, ContextId, Device, DeviceId, Link, LinkId, Topology, TopologyId
#from context.client.ContextClient import ContextClient
#from .PrepareTestScenario import (
#    # pylint: disable=unused-import
#    dltgateway_service,
#    context_service_a, context_client_a, dltconnector_service_a, dltconnector_client_a,
#    context_service_b, context_client_b, dltconnector_service_b, dltconnector_client_b)
#from .Objects import (
#    DA_CONTEXTS, DA_TOPOLOGIES, DA_DEVICES, DA_LINKS,
#    DB_CONTEXTS, DB_TOPOLOGIES, DB_DEVICES, DB_LINKS)
#
#LOGGER = logging.getLogger(__name__)
#LOGGER.setLevel(logging.DEBUG)
#
#def test_create_events(
#    context_client : ContextClient,                     # pylint: disable=redefined-outer-name
#    context_db_mb : Tuple[Database, MessageBroker]):    # pylint: disable=redefined-outer-name
#
#    for context  in CONTEXTS  : context_client.SetContext (Context (**context ))
#    for topology in TOPOLOGIES: context_client.SetTopology(Topology(**topology))
#    for device   in DEVICES   : context_client.SetDevice  (Device  (**device  ))
#    for link     in LINKS     : context_client.SetLink    (Link    (**link    ))
#
#
#    for link     in LINKS     : context_client.RemoveLink    (LinkId    (**link    ['link_id'    ]))
#    for device   in DEVICES   : context_client.RemoveDevice  (DeviceId  (**device  ['device_id'  ]))
#    for topology in TOPOLOGIES: context_client.RemoveTopology(TopologyId(**topology['topology_id']))
#    for context  in CONTEXTS  : context_client.RemoveContext (ContextId (**context ['context_id' ]))
#
#
#
#    dltgateway_client = DltGatewayClient(host='127.0.0.1', port=50051)
#    dltgateway_collector = DltEventsCollector(dltgateway_client, log_events_received=True)
#    dltgateway_collector.start()
#
#    dltgateway_collector.stop()
#