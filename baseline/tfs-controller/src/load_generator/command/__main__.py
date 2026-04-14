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

import logging, sys
from apscheduler.schedulers.blocking import BlockingScheduler
from load_generator.load_gen.Constants import RequestType
from load_generator.load_gen.Parameters import Parameters
from load_generator.load_gen.RequestGenerator import RequestGenerator
from load_generator.load_gen.RequestScheduler import RequestScheduler

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def main():
    LOGGER.info('Starting...')
    parameters = Parameters(
        num_requests = 100,
        request_types = [
            RequestType.SERVICE_L2NM,
            RequestType.SERVICE_L3NM,
            #RequestType.SERVICE_MW,
            #RequestType.SERVICE_TAPI,
            RequestType.SLICE_L2NM,
            RequestType.SLICE_L3NM,
        ],
        device_regex=r'.+',
        endpoint_regex=r'.+',
        offered_load  = 50,
        holding_time  = 10,
        availability_ranges   = [[0.0, 99.9999]],
        capacity_gbps_ranges  = [[0.1, 100.00]],
        e2e_latency_ms_ranges = [[5.0, 100.00]],
        max_workers   = 10,
        dry_mode      = False,           # in dry mode, no request is sent to TeraFlowSDN
        record_to_dlt = False,           # if record_to_dlt, changes in device/link/service/slice are uploaded to DLT
        dlt_domain_id = 'dlt-perf-eval', # domain used to uploaded entities, ignored when record_to_dlt = False
    )

    LOGGER.info('Initializing Generator...')
    generator = RequestGenerator(parameters)
    generator.initialize()

    LOGGER.info('Running Schedule...')
    scheduler = RequestScheduler(parameters, generator, scheduler_class=BlockingScheduler)
    scheduler.start()

    LOGGER.info('Done!')
    return 0

if __name__ == '__main__':
    sys.exit(main())
