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


import json, logging, time
from common.tools.rest_conf.client.RestConfClient import RestConfClient
from .SimapClient import SimapClient
from .Tools import create_simap_aggnet, create_simap_e2enet, create_simap_te, create_simap_trans


logging.basicConfig(level=logging.INFO)
logging.getLogger('RestConfClient').setLevel(logging.WARN)
LOGGER = logging.getLogger(__name__)


def main() -> None:
    restconf_client = RestConfClient(
        '127.0.0.1', port=8080,
        logger=logging.getLogger('RestConfClient')
    )
    simap_client = SimapClient(restconf_client)

    create_simap_te(simap_client)
    create_simap_trans(simap_client)
    create_simap_aggnet(simap_client)
    create_simap_e2enet(simap_client)

    print('networks=', json.dumps(simap_client.networks()))

    trans_link = simap_client.network('simap-trans').link('Trans-L1')
    trans_node_site1 = simap_client.network('simap-trans').node('site1')
    trans_node_site2 = simap_client.network('simap-trans').node('site2')

    related_service_ids = ['trans-svc1', 'trans-svc2', 'trans-svc3']

    for i in range(1000):
        trans_link.telemetry.update(float(i), float(i), related_service_ids=related_service_ids)
        trans_node_site1.telemetry.update(float(i), related_service_ids=related_service_ids)
        trans_node_site2.telemetry.update(float(i), related_service_ids=related_service_ids)

        print('trans link  telemetry =', json.dumps(trans_link.telemetry.get()))
        print('trans site1 telemetry =', json.dumps(trans_node_site1.telemetry.get()))
        print('trans site2 telemetry =', json.dumps(trans_node_site2.telemetry.get()))

        time.sleep(10)


if __name__ == '__main__':
    main()
