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

import json, logging, operator, requests
from requests.auth import HTTPBasicAuth
from typing import Optional
#from device.service.driver_api._Driver import RESOURCE_ENDPOINTS, RESOURCE_SERVICES, RESOURCE_INTERFACES


import logging
from typing import Any, Dict, Optional, Tuple
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.type_checkers.Checkers import chk_attribute, chk_string, chk_type
from device.service.driver_api._Driver import RESOURCE_ENDPOINTS, RESOURCE_INTERFACES

LOGGER = logging.getLogger(__name__)


SPECIAL_RESOURCE_MAPPINGS = {
    RESOURCE_ENDPOINTS        : '/endpoints',
    RESOURCE_INTERFACES       : '/interfaces'
}

HTTP_OK_CODES = {
    200,    # OK
    201,    # Created
    202,    # Accepted
    204,    # No Content
}

def find_key(resource, key):
    return json.loads(resource[1])[key]


def config_getter(
    root_url : str, resource_key : str, auth : Optional[HTTPBasicAuth] = None, timeout : Optional[int] = None
):
    url = '{:s}/manage-probe/ports'.format(root_url)
    result = []
    try:
        response = requests.get(url, timeout=timeout, verify=False)
        data = response.json()
        for item in data:
            tupla = ('/endpoints/endpoint', item)
            result.append(tupla)
        return result
    except requests.exceptions.Timeout:
        LOGGER.exception('Timeout connecting {:s}'.format(url))
        return result
    except Exception as e:  # pylint: disable=broad-except
        LOGGER.exception('Exception retrieving {:s}'.format(resource_key))
        result.append((resource_key, e))
        return result

    # try:
    #     context = json.loads(response.content)
    # except Exception as e:  # pylint: disable=broad-except
    #     LOGGER.warning('Unable to decode reply: {:s}'.format(str(response.content)))
    #     result.append((resource_key, e))
    #     return result



def create_connectivity_service(
    root_url, config_rules, timeout : Optional[int] = None, auth : Optional[HTTPBasicAuth] = None 
):

    url = '{:s}/manage-probe/configure'.format(root_url)
    headers = {'content-type': 'application/json'}
    results = []
    try:
        LOGGER.info('Configuring Smartnic rules')
        response = requests.post(
            url=url, data=config_rules, timeout=timeout, headers=headers, verify=False)
        LOGGER.info('SmartNIC Probes response: {:s}'.format(str(response)))
    except Exception as e:  # pylint: disable=broad-except
        LOGGER.exception('Exception creating ConfigRule')
        results.append(e)
    else:
        if response.status_code not in HTTP_OK_CODES:
            msg = 'Could not create ConfigRule status_code={:s} reply={:s}'
            LOGGER.error(msg.format(str(response.status_code), str(response)))
        results.append(response.status_code in HTTP_OK_CODES)
    return results

def delete_connectivity_service(root_url, config_rules, timeout : Optional[int] = None, auth : Optional[HTTPBasicAuth] = None 
):
    url = '{:s}/manage-probe/configure'.format(root_url)
    results = []
    try:
        response = requests.delete(url=url, data=config_rules, timeout=timeout, verify=False)
    except Exception as e:  # pylint: disable=broad-except
        LOGGER.exception('Exception deleting ConfigRule')
        results.append(e)
    else:
        if response.status_code not in HTTP_OK_CODES:
            msg = 'Could not delete ConfigRule status_code={:s} reply={:s}'
            LOGGER.error(msg.format(str(response.status_code), str(response)))
        results.append(response.status_code in HTTP_OK_CODES)
    return results

def process_optional_string_field(
    endpoint_data : Dict[str, Any], field_name : str, endpoint_resource_value : Dict[str, Any]
) -> None:
    field_value = chk_attribute(field_name, endpoint_data, 'endpoint_data', default=None)
    if field_value is None: return
    chk_string('endpoint_data.{:s}'.format(field_name), field_value)
    if len(field_value) > 0: endpoint_resource_value[field_name] = field_value

def compose_resource_endpoint(endpoint_data : Dict[str, Any]) -> Optional[Tuple[str, Dict]]:
    try:
        # Check type of endpoint_data
        chk_type('endpoint_data', endpoint_data, dict)

        # Check endpoint UUID (mandatory)
        endpoint_uuid = chk_attribute('uuid', endpoint_data, 'endpoint_data')
        chk_string('endpoint_data.uuid', endpoint_uuid, min_length=1)
        endpoint_resource_path = SPECIAL_RESOURCE_MAPPINGS.get(RESOURCE_ENDPOINTS)
        endpoint_resource_key = '{:s}/endpoint[{:s}]'.format(endpoint_resource_path, endpoint_uuid)
        endpoint_resource_value = {'uuid': endpoint_uuid}

        # Check endpoint optional string fields
        process_optional_string_field(endpoint_data, 'name', endpoint_resource_value)
        process_optional_string_field(endpoint_data, 'type', endpoint_resource_value)
        process_optional_string_field(endpoint_data, 'context_uuid', endpoint_resource_value)
        process_optional_string_field(endpoint_data, 'topology_uuid', endpoint_resource_value)

        # Check endpoint sample types (optional)
        endpoint_sample_types = chk_attribute('sample_types', endpoint_data, 'endpoint_data', default=[])
        chk_type('endpoint_data.sample_types', endpoint_sample_types, list)
        sample_types = {}
        sample_type_errors = []
        for i,endpoint_sample_type in enumerate(endpoint_sample_types):
            field_name = 'endpoint_data.sample_types[{:d}]'.format(i)
            try:
                chk_type(field_name, endpoint_sample_type, (int, str))
                if isinstance(endpoint_sample_type, int):
                    metric_name = KpiSampleType.Name(endpoint_sample_type)
                    metric_id = endpoint_sample_type
                elif isinstance(endpoint_sample_type, str):
                    metric_id = KpiSampleType.Value(endpoint_sample_type)
                    metric_name = endpoint_sample_type
                else:
                    str_type = str(type(endpoint_sample_type))
                    raise Exception('Bad format: {:s}'.format(str_type)) # pylint: disable=broad-exception-raised
            except Exception as e: # pylint: disable=broad-exception-caught
                MSG = 'Unsupported {:s}({:s}) : {:s}'
                sample_type_errors.append(MSG.format(field_name, str(endpoint_sample_type), str(e)))

            metric_name = metric_name.lower().replace('kpisampletype_', '')
            monitoring_resource_key = '{:s}/state/{:s}'.format(endpoint_resource_key, metric_name)
            sample_types[metric_id] = monitoring_resource_key

        if len(sample_type_errors) > 0:
            # pylint: disable=broad-exception-raised
            raise Exception('Malformed Sample Types:\n{:s}'.format('\n'.join(sample_type_errors)))

        if len(sample_types) > 0:
            endpoint_resource_value['sample_types'] = sample_types
    
        if 'location' in endpoint_data:
            endpoint_resource_value['location'] = endpoint_data['location']
            
        return endpoint_resource_key, endpoint_resource_value
    except: # pylint: disable=bare-except
        LOGGER.exception('Problem composing endpoint({:s})'.format(str(endpoint_data)))
        return None
