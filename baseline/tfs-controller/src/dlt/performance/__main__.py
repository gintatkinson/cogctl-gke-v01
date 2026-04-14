# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
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

import functools, logging, pathlib, sys, time
from common.proto.dlt_gateway_pb2 import DltRecordEvent
from dlt.connector.client.DltGatewayClient import DltGatewayClient
from dlt.connector.client.DltEventsCollector import DltEventsCollector
from .play_ground.Enums import CONTEXT_EVENT_TYPE_TO_ACTION, RECORD_TYPE_TO_ENUM
from .play_ground import PlayGround

DLT_GATEWAY_HOST     = '172.254.254.2'
DLT_GATEWAY_PORT     = 50051

NUM_INITIAL_DEVICES  = 20
NUM_INITIAL_LINKS    = 20
NUM_INITIAL_SERVICES = 20
NUM_INITIAL_SLICES   = 20

NUM_ACTIONS          = 1000
REPORT_EVERY         = 5
DELAY_FOR_EVENTS     = 5
DOMAIN_UUID          = 'perf-test-fake-domain'

OUTPUT_FOLDER        = 'data/perf/scenario_2/dlt/2023-05May-31'
CSV_FILEPATH         = OUTPUT_FOLDER + '/response_time.csv'

LOG_FORMAT = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
LOGGER = logging.getLogger(__name__)

def _event_handler(play_ground : PlayGround, event : DltRecordEvent) -> None:
    # Filter undesired/unsupported/wrong domain_uuids, actions, and record types
    # Update notification time in PlayGround.PerfPoints
    # Return None to prevent storing the events in the DLT Events' Collector internal queue

    domain_uuid = event.record_id.domain_uuid.uuid
    if domain_uuid != DOMAIN_UUID: return None

    action = CONTEXT_EVENT_TYPE_TO_ACTION.get(event.event.event_type)
    if action is None: return None

    record_type = RECORD_TYPE_TO_ENUM.get(event.record_id.type)
    if record_type is None: return None

    #event_time = event.event.timestamp.timestamp
    record_uuid = event.record_id.record_uuid.uuid
    play_ground.perf_data.add_notif_time(action, record_type, record_uuid, time.time())
    return None

def main() -> None:
    dltgateway_client = DltGatewayClient(host=DLT_GATEWAY_HOST, port=DLT_GATEWAY_PORT)

    play_ground = PlayGround(dltgateway_client, DOMAIN_UUID)
    event_handler = functools.partial(_event_handler, play_ground)

    dltgateway_collector = DltEventsCollector(
        dltgateway_client, log_events_received=False, event_handler=event_handler)
    dltgateway_collector.start()

    time.sleep(3)

    LOGGER.info('Adding {:d} initial devices...'.format(NUM_INITIAL_DEVICES))
    for _ in range(NUM_INITIAL_DEVICES):
        play_ground.create_device()

    LOGGER.info('Adding {:d} initial links...'.format(NUM_INITIAL_LINKS))
    for _ in range(NUM_INITIAL_LINKS):
        play_ground.create_link()

    LOGGER.info('Adding {:d} initial services...'.format(NUM_INITIAL_SERVICES))
    for _ in range(NUM_INITIAL_SERVICES):
        play_ground.create_service()

    LOGGER.info('Adding {:d} initial slices...'.format(NUM_INITIAL_SLICES))
    for _ in range(NUM_INITIAL_SLICES):
        play_ground.create_slice()

    # Otherwise, only get/update/delete is performed and play_ground becomes empty
    play_ground.perf_data.clear_operation_counters()

    LOGGER.info('Starting {:d} actions...'.format(NUM_ACTIONS))
    num_action = 0
    while num_action < NUM_ACTIONS:
        if num_action > 0 and num_action % REPORT_EVERY == 0:
            str_stats = play_ground.perf_data.stats_to_str()
            MSG = 'Running action {:d}/{:d}...\n{:s}'
            LOGGER.info(MSG.format(num_action, NUM_ACTIONS, str_stats))
        completed = play_ground.run_random_operation()
        if completed: num_action += 1

    str_stats = play_ground.perf_data.stats_to_str()
    LOGGER.info('Completed {:d} actions!\n{:s}'.format(NUM_ACTIONS, str_stats))

    LOGGER.info('Waiting {:f} for last events...'.format(DELAY_FOR_EVENTS))
    time.sleep(DELAY_FOR_EVENTS)

    dltgateway_collector.stop()

    LOGGER.info('Writing results...')
    pathlib.Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
    play_ground.perf_data.to_csv(CSV_FILEPATH)
    return 0

if __name__ == '__main__':
    sys.exit(main())
