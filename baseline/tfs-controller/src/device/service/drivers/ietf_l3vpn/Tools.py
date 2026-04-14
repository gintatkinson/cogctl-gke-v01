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
import logging
from typing import Any, Dict, Optional, Tuple, TypedDict

import requests

from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.type_checkers.Checkers import chk_attribute, chk_string, chk_type
from device.service.driver_api._Driver import RESOURCE_ENDPOINTS

from .Constants import SPECIAL_RESOURCE_MAPPINGS


class LANPrefixesDict(TypedDict):
    lan: str
    lan_tag: str


LOGGER = logging.getLogger(__name__)

SITE_NETWORK_ACCESS_TYPE = "ietf-l3vpn-svc:multipoint"


def service_exists(wim_url: str, auth, service_uuid: str) -> bool:
    try:
        get_connectivity_service(wim_url, auth, service_uuid)
        return True
    except:  # pylint: disable=bare-except
        return False


def get_all_active_connectivity_services(wim_url: str, auth):
    try:
        LOGGER.info("Sending get all connectivity services")
        servicepoint = f"{wim_url}/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services"
        response = requests.get(servicepoint, auth=auth)

        if response.status_code != requests.codes.ok:
            raise Exception(
                "Unable to get all connectivity services",
                http_code=response.status_code,
            )

        return response
    except requests.exceptions.ConnectionError:
        raise Exception("Request Timeout", http_code=408)


def get_connectivity_service(wim_url, auth, service_uuid):
    try:
        LOGGER.info("Sending get connectivity service")
        servicepoint = f"{wim_url}/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services/vpn-service={service_uuid}"

        response = requests.get(servicepoint)

        if response.status_code != requests.codes.ok:
            raise Exception(
                "Unable to get connectivity service{:s}".format(str(service_uuid)),
                http_code=response.status_code,
            )

        return response
    except requests.exceptions.ConnectionError:
        raise Exception("Request Timeout", http_code=408)


def process_optional_string_field(
    endpoint_data: Dict[str, Any],
    field_name: str,
    endpoint_resource_value: Dict[str, Any],
) -> None:
    field_value = chk_attribute(
        field_name, endpoint_data, "endpoint_data", default=None
    )
    if field_value is None:
        return
    chk_string("endpoint_data.{:s}".format(field_name), field_value)
    if len(field_value) > 0:
        endpoint_resource_value[field_name] = field_value


def compose_resource_endpoint(
    endpoint_data: Dict[str, Any],
) -> Optional[Tuple[str, Dict]]:
    try:
        # Check type of endpoint_data
        chk_type("endpoint_data", endpoint_data, dict)

        # Check endpoint UUID (mandatory)
        endpoint_uuid = chk_attribute("uuid", endpoint_data, "endpoint_data")
        chk_string("endpoint_data.uuid", endpoint_uuid, min_length=1)
        endpoint_resource_path = SPECIAL_RESOURCE_MAPPINGS.get(RESOURCE_ENDPOINTS)
        endpoint_resource_key = "{:s}/endpoint[{:s}]".format(
            endpoint_resource_path, endpoint_uuid
        )
        endpoint_resource_value = {"uuid": endpoint_uuid}

        # Check endpoint optional string fields
        process_optional_string_field(endpoint_data, "name", endpoint_resource_value)
        process_optional_string_field(
            endpoint_data, "site_location", endpoint_resource_value
        )
        process_optional_string_field(endpoint_data, "ce-ip", endpoint_resource_value)
        process_optional_string_field(
            endpoint_data, "address_ip", endpoint_resource_value
        )
        process_optional_string_field(
            endpoint_data, "address_prefix", endpoint_resource_value
        )
        process_optional_string_field(endpoint_data, "mtu", endpoint_resource_value)
        process_optional_string_field(
            endpoint_data, "ipv4_lan_prefixes", endpoint_resource_value
        )
        process_optional_string_field(endpoint_data, "type", endpoint_resource_value)
        process_optional_string_field(
            endpoint_data, "context_uuid", endpoint_resource_value
        )
        process_optional_string_field(
            endpoint_data, "topology_uuid", endpoint_resource_value
        )

        # Check endpoint sample types (optional)
        endpoint_sample_types = chk_attribute(
            "sample_types", endpoint_data, "endpoint_data", default=[]
        )
        chk_type("endpoint_data.sample_types", endpoint_sample_types, list)
        sample_types = {}
        sample_type_errors = []
        for i, endpoint_sample_type in enumerate(endpoint_sample_types):
            field_name = "endpoint_data.sample_types[{:d}]".format(i)
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
                    raise Exception("Bad format: {:s}".format(str_type))  # pylint: disable=broad-exception-raised
            except Exception as e:  # pylint: disable=broad-exception-caught
                MSG = "Unsupported {:s}({:s}) : {:s}"
                sample_type_errors.append(
                    MSG.format(field_name, str(endpoint_sample_type), str(e))
                )

            metric_name = metric_name.lower().replace("kpisampletype_", "")
            monitoring_resource_key = "{:s}/state/{:s}".format(
                endpoint_resource_key, metric_name
            )
            sample_types[metric_id] = monitoring_resource_key

        if len(sample_type_errors) > 0:
            # pylint: disable=broad-exception-raised
            raise Exception(
                "Malformed Sample Types:\n{:s}".format("\n".join(sample_type_errors))
            )

        if len(sample_types) > 0:
            endpoint_resource_value["sample_types"] = sample_types

        if "site_location" in endpoint_data:
            endpoint_resource_value["site_location"] = endpoint_data["site_location"]

        if "ce-ip" in endpoint_data:
            endpoint_resource_value["ce-ip"] = endpoint_data["ce-ip"]

        if "address_ip" in endpoint_data:
            endpoint_resource_value["address_ip"] = endpoint_data["address_ip"]

        if "address_prefix" in endpoint_data:
            endpoint_resource_value["address_prefix"] = endpoint_data["address_prefix"]

        if "mtu" in endpoint_data:
            endpoint_resource_value["mtu"] = endpoint_data["mtu"]

        if "ipv4_lan_prefixes" in endpoint_data:
            endpoint_resource_value["ipv4_lan_prefixes"] = endpoint_data[
                "ipv4_lan_prefixes"
            ]

        return endpoint_resource_key, endpoint_resource_value
    except:  # pylint: disable=bare-except
        LOGGER.exception("Problem composing endpoint({:s})".format(str(endpoint_data)))
        return None
