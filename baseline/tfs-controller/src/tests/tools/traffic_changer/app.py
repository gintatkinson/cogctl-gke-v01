#!/bin/bash
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


import enum, json, logging, requests, secrets, time
from flask import Flask, render_template, request, flash


logging.basicConfig(
    level=logging.INFO,
    format='[Worker-%(process)d][%(asctime)s] %(levelname)s:%(name)s:%(message)s',
)

NETWORK_ID = 'admin'

class Controller(enum.Enum):
    TFS_E2E = 'TFS-E2E'
    TFS_AGG = 'TFS-AGG'
    TFS_IP  = 'TFS-IP'

CONTROLLER_TO_ADDRESS_PORT = {
    Controller.TFS_E2E : ('10.254.0.10', 80),
    Controller.TFS_AGG : ('10.254.0.11', 80),
    Controller.TFS_IP  : ('10.254.0.12', 80),
}

LINK_ID_TO_CONTROLLER = {
    'L1'    : Controller.TFS_E2E,
    'L2'    : Controller.TFS_E2E,
    'L3'    : Controller.TFS_E2E,
    'L4'    : Controller.TFS_E2E,
    'L5'    : Controller.TFS_IP,
    'L6'    : Controller.TFS_IP,
    'L7ab'  : Controller.TFS_AGG,
    'L7ba'  : Controller.TFS_AGG,
    'L8ab'  : Controller.TFS_AGG,
    'L8ba'  : Controller.TFS_AGG,
    'L9'    : Controller.TFS_IP,
    'L10'   : Controller.TFS_IP,
    'L11ab' : Controller.TFS_AGG,
    'L11ba' : Controller.TFS_AGG,
    'L12ab' : Controller.TFS_AGG,
    'L12ba' : Controller.TFS_AGG,
    'L13'   : Controller.TFS_AGG,
    'L14'   : Controller.TFS_AGG,
}

TARGET_URL = 'http://{:s}:{:d}/restconf/operations/affect_sample_synthesizer'


LOGGER = logging.getLogger(__name__)

def log_request(response):
    timestamp = time.strftime('[%Y-%b-%d %H:%M]')
    LOGGER.info(
        '%s %s %s %s %s', timestamp, request.remote_addr, request.method,
        request.full_path, response.status
    )
    return response


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(64)
app.after_request(log_request)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('affect_form.html', payload=None, response=None)

    link_id          = request.form.get('link_id',          '').strip()
    bandwidth_factor = request.form.get('bandwidth_factor', '').strip()
    latency_factor   = request.form.get('latency_factor',   '').strip()

    controller = LINK_ID_TO_CONTROLLER.get(link_id)
    if controller is None:
        MSG = 'link_id({:s}) not allowed. Must be one of {:s}'
        allowed_link_ids = set(LINK_ID_TO_CONTROLLER.keys())
        flash(MSG.format(str(link_id), str(allowed_link_ids)), category='error')
        return render_template('affect_form.html', payload=None, response=None)

    try:
        bandwidth_factor = float(bandwidth_factor)
        if bandwidth_factor < 0.01 or bandwidth_factor > 100.0: raise ValueError()
    except Exception:
        MSG = 'bandwidth_factor({:s}) must be a float in range [0.01..100.0]'
        flash(MSG.format(str(bandwidth_factor)), category='error')
        return render_template('affect_form.html', payload=None, response=None)

    try:
        latency_factor = float(latency_factor)
        if latency_factor < 0.01 or latency_factor > 100.0: raise ValueError()
    except Exception:
        MSG = 'latency_factor({:s}) must be a float in range [0.01..100.0]'
        flash(MSG.format(str(latency_factor)), category='error')
        return render_template('affect_form.html', payload=None, response=None)

    payload = {
        'network_id'      : NETWORK_ID,
        'link_id'         : link_id,
        'bandwidth_factor': bandwidth_factor,
        'latency_factor'  : latency_factor,
    }

    controller_address, controller_port = CONTROLLER_TO_ADDRESS_PORT.get(controller)
    target_url = TARGET_URL.format(controller_address, controller_port)

    try:
        resp = requests.post(target_url, json=payload, timeout=10)
        try:
            resp_content = resp.json()
        except Exception:
            resp_content = resp.text

        response = {'status_code': resp.status_code, 'body': resp_content, 'ok': resp.ok}
    except Exception as e:
        flash('Error sending request: {:s}'.format(str(e)), category='error')
        response = None

    str_payload = json.dumps(payload)
    return render_template('affect_form.html', payload=str_payload, response=response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
