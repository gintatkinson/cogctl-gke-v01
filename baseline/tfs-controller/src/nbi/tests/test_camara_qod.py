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


# Enable eventlet for async networking
# NOTE: monkey_patch needs to be executed before importing any other module.
import eventlet
eventlet.monkey_patch()

#pylint: disable=wrong-import-position
import deepdiff, logging, pytest
from decimal import ROUND_HALF_UP, Decimal
from typing import Dict
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.proto.context_pb2 import ContextId
from common.tools.descriptor.Loader import (
    DescriptorLoader, check_descriptor_load_results, validate_empty_scenario
)
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from nbi.service.NbiApplication import NbiApplication
from .PrepareTestScenario import ( # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    nbi_application, context_client,
    do_rest_delete_request, do_rest_get_request, do_rest_post_request, do_rest_put_request,
)


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

DESCRIPTOR_FILE = 'nbi/tests/data/tfs_api_dummy.json'

JSON_ADMIN_CONTEXT_ID = json_context_id(DEFAULT_CONTEXT_NAME)
ADMIN_CONTEXT_ID = ContextId(**JSON_ADMIN_CONTEXT_ID)


@pytest.fixture(scope='session')
def storage() -> Dict:
    yield dict()


# ----- Prepare Environment --------------------------------------------------------------------------------------------

def test_prepare_environment(context_client : ContextClient) -> None: # pylint: disable=redefined-outer-name
    validate_empty_scenario(context_client)
    descriptor_loader = DescriptorLoader(descriptors_file=DESCRIPTOR_FILE, context_client=context_client)
    results = descriptor_loader.process()
    check_descriptor_load_results(results, descriptor_loader)
    descriptor_loader.validate()

    # Verify the scenario has no services/slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.topology_ids) == 1
    assert len(response.service_ids ) == 3
    assert len(response.slice_ids   ) == 1


# ----- Run tests ------------------------------------------------------------------------------------------------------

def test_create_profile(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    qos_profile_data = {
        "name"                   : "QCI_2_voice",
        "description"            : "QoS profile for video streaming",
        "status"                 : "ACTIVE",
        "priority"               : 20,
        "targetMinUpstreamRate"  : {"value": 10, "unit": "bps"},
        "maxUpstreamRate"        : {"value": 10, "unit": "bps"},
        "maxUpstreamBurstRate"   : {"value": 10, "unit": "bps"},
        "targetMinDownstreamRate": {"value": 10, "unit": "bps"},
        "maxDownstreamRate"      : {"value": 10, "unit": "bps"},
        "maxDownstreamBurstRate" : {"value": 10, "unit": "bps"},
        "minDuration"            : {"value": 12, "unit": "Minutes"},
        "maxDuration"            : {"value": 12, "unit": "Minutes"},
        "packetDelayBudget"      : {"value": 12, "unit": "Minutes"},
        "jitter"                 : {"value": 12, "unit": "Minutes"},
        "packetErrorLossRate"    : 3,
    }
    post_response = do_rest_post_request(
        '/camara/qod/v0/profiles', body=qos_profile_data,
        expected_status_codes={201}
    )
    assert 'qos_profile_id' in post_response
    qos_profile_data['qos_profile_id'] = post_response['qos_profile_id']

    diff_data = deepdiff.DeepDiff(qos_profile_data, post_response)
    LOGGER.error('Differences:\n{:s}'.format(str(diff_data.pretty())))
    assert len(diff_data) == 0

    storage['qos_profile'] = post_response

def test_get_profile_before_update(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    qos_profile = storage['qos_profile']
    assert 'qos_profile_id' in qos_profile
    qos_profile_id = qos_profile['qos_profile_id']

    get_response = do_rest_get_request(
        '/camara/qod/v0/profiles/{:s}'.format(str(qos_profile_id)),
        expected_status_codes={200}
    )

    diff_data = deepdiff.DeepDiff(qos_profile, get_response)
    LOGGER.error('Differences:\n{:s}'.format(str(diff_data.pretty())))
    assert len(diff_data) == 0

def test_update_profile(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    qos_profile = storage['qos_profile']
    assert 'qos_profile_id' in qos_profile
    qos_profile_id = qos_profile['qos_profile_id']

    qos_profile_update = {
        "qos_profile_id"         : qos_profile_id,
        "name"                   : "Updated Name",
        "description"            : "NEW GAMING PROFILE",
        "status"                 : "ACTIVE",
        "targetMinUpstreamRate"  : {"value": 20, "unit": "bps"},
        "maxUpstreamRate"        : {"value": 50, "unit": "bps"},
        "maxUpstreamBurstRate"   : {"value": 60, "unit": "bps"},
        "targetMinDownstreamRate": {"value": 30, "unit": "bps"},
        "maxDownstreamRate"      : {"value": 100, "unit": "bps"},
        "maxDownstreamBurstRate" : {"value": 70, "unit": "bps"},
        "minDuration"            : {"value": 15, "unit": "Minutes"},
        "maxDuration"            : {"value": 25, "unit": "Minutes"},
        "priority"               : 15,
        "packetDelayBudget"      : {"value": 10, "unit": "Minutes"},
        "jitter"                 : {"value": 10, "unit": "Minutes"},
        "packetErrorLossRate"    : 1
    }
    put_response = do_rest_put_request(
        '/camara/qod/v0/profiles/{:s}'.format(str(qos_profile_id)), body=qos_profile_update,
        expected_status_codes={202}
    )

    diff_data = deepdiff.DeepDiff(qos_profile_update, put_response)
    LOGGER.error('Differences:\n{:s}'.format(str(diff_data.pretty())))
    assert len(diff_data) == 0

    storage['qos_profile'] = put_response

def test_get_profile_after_update(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    qos_profile = storage['qos_profile']
    assert 'qos_profile_id' in qos_profile
    qos_profile_id = qos_profile['qos_profile_id']

    get_response = do_rest_get_request(
        '/camara/qod/v0/profiles/{:s}'.format(str(qos_profile_id)),
        expected_status_codes={200}
    )

    diff_data = deepdiff.DeepDiff(qos_profile, get_response)
    LOGGER.error('Differences:\n{:s}'.format(str(diff_data.pretty())))
    assert len(diff_data) == 0

def test_create_session(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    qos_profile = storage['qos_profile']
    assert 'qos_profile_id' in qos_profile
    qos_profile_id = qos_profile['qos_profile_id']

    session_data = {
        "device"           : {"ipv4Address": "84.75.11.12/25"},
        "applicationServer": {"ipv4Address": "192.168.0.1/26"},
        "duration"         : float(10), # 10 days
        "qos_profile_id"   : qos_profile_id,
    }
    post_response = do_rest_post_request(
        '/camara/qod/v0/sessions', body=session_data,
        expected_status_codes={201}
    )

    assert 'session_id' in post_response
    session_data['session_id'] = post_response['session_id']

    del post_response['duration']
    del session_data['duration']
    del post_response['startedAt']
    del post_response['expiresAt']

    diff_data = deepdiff.DeepDiff(session_data, post_response)
    LOGGER.error('Differences:\n{:s}'.format(str(diff_data.pretty())))
    assert len(diff_data) == 0

    storage['session'] = post_response

def test_get_session_before_update(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    session = storage['session']
    assert 'session_id' in session
    session_id = session['session_id']

    get_response = do_rest_get_request(
        '/camara/qod/v0/sessions/{:s}'.format(str(session_id)),
        expected_status_codes={200}
    )

    del get_response['duration']
    del get_response['startedAt']
    del get_response['expiresAt']

    diff_data = deepdiff.DeepDiff(session, get_response)
    LOGGER.error('Differences:\n{:s}'.format(str(diff_data.pretty())))
    assert len(diff_data) == 0

def test_update_session(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    session = storage['session']
    assert 'session_id' in session
    session_id = session['session_id']

    qos_profile = storage['qos_profile']
    assert 'qos_profile_id' in qos_profile
    qos_profile_id = qos_profile['qos_profile_id']

    session_update = {
        "session_id"       : session_id,
        "device"           : {"ipv4Address": "84.75.11.12/25"},
        "applicationServer": {"ipv4Address": "192.168.0.1/26"},
        "duration"         : float(20), # 20 days
        "qos_profile_id"   : qos_profile_id,
    }
    put_response = do_rest_put_request(
        '/camara/qod/v0/sessions/{:s}'.format(str(session_id)), body=session_update,
        expected_status_codes={202}
    )

    del put_response['duration']
    del session_update['duration']
    del put_response['startedAt']
    del put_response['expiresAt']

    diff_data = deepdiff.DeepDiff(session_update, put_response)
    LOGGER.error('Differences:\n{:s}'.format(str(diff_data.pretty())))
    assert len(diff_data) == 0

    storage['session'] = put_response

def test_get_session_after_update(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    session = storage['session']
    assert 'session_id' in session
    session_id = session['session_id']

    get_response = do_rest_get_request(
        '/camara/qod/v0/sessions/{:s}'.format(str(session_id)),
        expected_status_codes={200}
    )

    del get_response['duration']
    del get_response['startedAt']
    del get_response['expiresAt']

    diff_data = deepdiff.DeepDiff(session, get_response)
    LOGGER.error('Differences:\n{:s}'.format(str(diff_data.pretty())))
    assert len(diff_data) == 0

def test_delete_session(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    session = storage['session']
    assert 'session_id' in session
    session_id = session['session_id']
    do_rest_delete_request(
        '/camara/qod/v0/sessions/{:s}'.format(str(session_id)),
        expected_status_codes={204}
    )
    storage.pop('session')

def test_delete_profile(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    qos_profile = storage['qos_profile']
    assert 'qos_profile_id' in qos_profile
    qos_profile_id = qos_profile['qos_profile_id']
    do_rest_delete_request(
        '/camara/qod/v0/profiles/{:s}'.format(str(qos_profile_id)),
        expected_status_codes={204}
    )
    storage.pop('qos_profile')

# ----- Cleanup Environment --------------------------------------------------------------------------------------------

def test_cleanup_environment(context_client : ContextClient) -> None: # pylint: disable=redefined-outer-name
    # Verify the scenario has no services/slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.topology_ids) == 1
    assert len(response.service_ids ) == 3
    assert len(response.slice_ids   ) == 1

    # Load descriptors and validate the base scenario
    descriptor_loader = DescriptorLoader(descriptors_file=DESCRIPTOR_FILE, context_client=context_client)
    descriptor_loader.validate()
    descriptor_loader.unload()
    validate_empty_scenario(context_client)
