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
from device.service.driver_api._Driver import RESOURCE_ENDPOINTS, RESOURCE_SERVICES
from concurrent.futures import ThreadPoolExecutor


LOGGER = logging.getLogger(__name__)

EXECUTOR = ThreadPoolExecutor()

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
    url = '{:s}/restconf/data/tapi-common:context'.format(root_url)
    result = []
    try:
        response = requests.get(url, timeout=timeout, verify=False, auth=auth)
    except requests.exceptions.Timeout:
        LOGGER.exception('Timeout connecting {:s}'.format(url))
        return result
    except Exception as e:  # pylint: disable=broad-except
        LOGGER.exception('Exception retrieving {:s}'.format(resource_key))
        result.append((resource_key, e))
        return result

    try:
        context = json.loads(response.content)
    except Exception as e:  # pylint: disable=broad-except
        LOGGER.warning('Unable to decode reply: {:s}'.format(str(response.content)))
        result.append((resource_key, e))
        return result

    if resource_key == RESOURCE_ENDPOINTS:
        if 'tapi-common:context' in context:
            context = context['tapi-common:context']
        elif 'context' in context:
            context = context['context']

        for sip in context['service-interface-point']:
            layer_protocol_name = sip.get('layer-protocol-name', '?')
            supportable_spectrum = sip.get('tapi-photonic-media:media-channel-service-interface-point-spec', {})
            supportable_spectrum = supportable_spectrum.get('mc-pool', {})
            supportable_spectrum = supportable_spectrum.get('supportable-spectrum', [])
            supportable_spectrum = supportable_spectrum[0] if len(supportable_spectrum) == 1 else {}
            grid_type = supportable_spectrum.get('frequency-constraint', {}).get('grid-type')
            granularity = supportable_spectrum.get('frequency-constraint', {}).get('adjustment-granularity')
            direction = sip.get('direction', '?')

            endpoint_type = [layer_protocol_name, grid_type, granularity, direction]
            str_endpoint_type = ':'.join(filter(lambda i: operator.is_not(i, None), endpoint_type))
            sip_uuid = sip['uuid']

            sip_names = sip.get('name', [])
            sip_name = next(iter([
                sip_name['value']
                for sip_name in sip_names
                if sip_name['value-name'] == 'local-name'
            ]), sip_uuid)

            endpoint_url = '/endpoints/endpoint[{:s}]'.format(sip_uuid)
            endpoint_data = {'uuid': sip_uuid, 'name': sip_name, 'type': str_endpoint_type}
            result.append((endpoint_url, endpoint_data))

    elif resource_key == RESOURCE_SERVICES:
        if 'tapi-common:context' in context:
            context = context['tapi-common:context']
        elif 'context' in context:
            context = context['context']

        if 'tapi-connectivity:connectivity-context' in context:
            context = context['tapi-connectivity:connectivity-context']
        elif 'connectivity-context' in context:
            context = context['connectivity-context']

        for conn_svc in context['connectivity-service']:
            service_uuid = conn_svc['uuid']
            constraints = conn_svc.get('connectivity-constraint', {})
            total_req_cap = constraints.get('requested-capacity', {}).get('total-size', {})

            service_url = '/services/service[{:s}]'.format(service_uuid)
            service_data = {
                'uuid': service_uuid,
                'direction': constraints.get('connectivity-direction', 'UNIDIRECTIONAL'),
                'capacity_unit': total_req_cap.get('unit', '<UNDEFINED>'),
                'capacity_value': total_req_cap.get('value', '<UNDEFINED>'),
            }

            for i,endpoint in enumerate(conn_svc.get('end-point', [])):
                layer_protocol_name = endpoint.get('layer-protocol-name')
                if layer_protocol_name is not None:
                    service_data['layer_protocol_name'] = layer_protocol_name

                layer_protocol_qualifier = endpoint.get('layer-protocol-qualifier')
                if layer_protocol_qualifier is not None:
                    service_data['layer_protocol_qualifier'] = layer_protocol_qualifier

                sip = endpoint['service-interface-point']['service-interface-point-uuid']
                service_data['input_sip' if i == 0 else 'output_sip'] = sip

            result.append((service_url, service_data))

    return result

def create_connectivity_service(
    root_url, uuid, input_sip, output_sip, direction, capacity_value, capacity_unit, layer_protocol_name,
    layer_protocol_qualifier,
    auth : Optional[HTTPBasicAuth] = None, timeout : Optional[int] = None
):

    url = '{:s}/restconf/data/tapi-common:context/tapi-connectivity:connectivity-context'.format(root_url)
    headers = {'content-type': 'application/json'}
    data = {
        'tapi-connectivity:connectivity-service': [
            {
                'uuid': uuid,
                'connectivity-constraint': {
                    'requested-capacity': {
                        'total-size': {
                            'value': capacity_value,
                            'unit': capacity_unit
                        }
                    },
                    'connectivity-direction': direction
                },
                'end-point': [
                    {
                        'service-interface-point': {
                            'service-interface-point-uuid': input_sip
                        },
                        'layer-protocol-name': layer_protocol_name,
                        'layer-protocol-qualifier': layer_protocol_qualifier,
                        'local-id': input_sip
                    },
                    {
                        'service-interface-point': {
                            'service-interface-point-uuid': output_sip
                        },
                        'layer-protocol-name': layer_protocol_name,
                        'layer-protocol-qualifier': layer_protocol_qualifier,
                        'local-id': output_sip
                    }
                ]
            }
        ]
    }
    results = []
    try:
        LOGGER.info('Connectivity service {:s}: {:s}'.format(str(uuid), str(data)))
        response = requests.post(
            url=url, data=json.dumps(data), timeout=timeout, headers=headers, verify=False, auth=auth)
        LOGGER.info('TAPI response: {:s}'.format(str(response)))
    except Exception as e:  # pylint: disable=broad-except
        LOGGER.exception('Exception creating ConnectivityService(uuid={:s}, data={:s})'.format(str(uuid), str(data)))
        results.append(e)
    else:
        if response.status_code not in HTTP_OK_CODES:
            msg = 'Could not create ConnectivityService(uuid={:s}, data={:s}). status_code={:s} reply={:s}'
            LOGGER.error(msg.format(str(uuid), str(data), str(response.status_code), str(response)))
        results.append(response.status_code in HTTP_OK_CODES)
    return results

def delete_connectivity_service(root_url, uuid, auth : Optional[HTTPBasicAuth] = None, timeout : Optional[int] = None):
    url = '{:s}/restconf/data/tapi-common:context/tapi-connectivity:connectivity-context/connectivity-service={:s}'
    url = url.format(root_url, uuid)
    results = []
    try:
        response = requests.delete(url=url, timeout=timeout, verify=False, auth=auth)
    except Exception as e:  # pylint: disable=broad-except
        LOGGER.exception('Exception deleting ConnectivityService(uuid={:s})'.format(str(uuid)))
        results.append(e)
    else:
        if response.status_code not in HTTP_OK_CODES:
            msg = 'Could not delete ConnectivityService(uuid={:s}). status_code={:s} reply={:s}'
            LOGGER.error(msg.format(str(uuid), str(response.status_code), str(response)))
        results.append(response.status_code in HTTP_OK_CODES)
    return results

def tapi_tequest(resource_value):

    services, urls  =  build_tapi_connectivity(resource_value)
    for service, url in zip(services, urls):
        LOGGER.info(f"Services to be processed: {json.dumps(service, indent=2)}")
        LOGGER.info(f"URL to be used: {url}")

        EXECUTOR.submit(process_uuid, service, url)

def process_uuid(service, url):
    headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
    }

    LOGGER.info(f"Processing service {service} to URL: {url}")
    try:
        response = requests.post(url = url, json=service, headers=headers, timeout=300)
        LOGGER.info("Response Status code: %s", response)
    except requests.exceptions.RequestException as e:
        LOGGER.info(f"ERROR equest to {service} failed: {e}")

def build_tapi_connectivity(service_data):
    LOGGER.info(f"Building TAPI connectivity for services data: {service_data}")
    outputs = []
    urls = []
    rules_set = service_data[1]["rule_set"]
    for rule_set in rules_set:
        direction = rule_set["direction"]
        layer_name = rule_set["layer_protocol_name"]
        layer_qualifier = rule_set["layer_protocol_qualifier"]
        urls.append(rule_set["url"])
        cs = {
            "uuid": rule_set["uuid"],
            "connectivity-direction": direction,
            "layer-protocol-name": layer_name,
            "layer-protocol-qualifier": layer_qualifier,
            "end-point": []
        }

        endpoints = []
        if direction == "UNIDIRECTIONAL":
            endpoints.append({
                "layer-protocol-name": layer_name,
                "layer-protocol-qualifier": layer_qualifier,
                "service-interface-point": {"service-interface-point-uuid": rule_set["input_sip"]},
                "direction:": "INPUT",
                "local-id": rule_set["input_sip"]
            })
            endpoints.append({
                "layer-protocol-name": layer_name,
                "layer-protocol-qualifier": layer_qualifier,
                "service-interface-point": {"service-interface-point-uuid": rule_set["output_sip"]},
                "direction:": "OUTPUT",
                "local-id": rule_set["output_sip"]
            })
        else:
            for point in [rule_set["input_sip"], rule_set["output_sip"]]:
                ep = {
                    "layer-protocol-name": layer_name,
                    "layer-protocol-qualifier": layer_qualifier,
                    "service-interface-point": {"service-interface-point-uuid": point},
                    "direction:": "BIDIRECTIONAL",
                    "local-id": point
                }
                if rule_set.get("lower_frequency_mhz") != "NONE":
                    ep["tapi-photonic-media:media-channel-connectivity-service-end-point-spec"] = {
                        "mc-config": {
                            "spectrum": {
                                "frequency-constraint": {
                                    "adjustment-granularity": rule_set.get("granularity", "NONE"),
                                    "grid-type": rule_set.get("grid_type", "NONE")
                                },
                                "lower-frequency": rule_set["lower_frequency_mhz"],
                                "upper-frequency": rule_set["upper_frequency_mhz"]
                            }
                        }
                    }
                endpoints.append(ep)
        cs["end-point"] = endpoints

        route_obj = rule_set.get("route_objective_function", "UNSPECIFIED")
        cs["route-objective-function"] = route_obj if route_obj != "NONE" else "10000"
        capacity_value = rule_set.get("capacity_value", "NONE")
        capacity_unit  = rule_set.get("capacity_unit" , "NONE")

        if capacity_value != "NONE":
            cs["requested-capacity"] = {
                "total-size": {"value": capacity_value, "unit": capacity_unit}
            }
        outputs.append({"tapi-connectivity:connectivity-service": [cs]})
    return outputs, urls
