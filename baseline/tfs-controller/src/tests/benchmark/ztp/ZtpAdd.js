/**
 * Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import grpc from 'k6/net/grpc';
import exec from "k6/execution";
import { check, sleep } from 'k6';

const client = new grpc.Client();
client.load(['../../../../proto'], 'ztp.proto');

export const data = [];
for (let i = 1; i < 801; i++) {
  data.push({
    "devRoleType": "DEV_CONF",
    "devRoleId": {
        "devId": {"device_uuid": {"uuid": "EMU-" + i}},
        "devRoleId": {"uuid": "EMU-" + i}
    }
  });
};

export const options = {
  scenarios :{

    "ZtpAdd-scenario": {
      executor: "shared-iterations",
      vus: 800,
      iterations: data.length,
      maxDuration: "1h"
    }
  }
};

export default () => {
  client.connect('10.1.255.239:5050', {
    plaintext: true,
    timeout: 10000
  });

  var item = data[exec.scenario.iterationInInstance];
  const response = client.invoke('ztp.ZTPService/ZtpAdd', item);

  check(response, {
    'status is OK': (r) => r && r.status === grpc.StatusOK,
  });

  console.log(JSON.stringify(response.message));

  client.close();
  sleep(1);
};

export function handleSummary(data) {

  return {
    'summary_add_800.json': JSON.stringify(data.metrics.grpc_req_duration.values), //the default data object
  };
}
