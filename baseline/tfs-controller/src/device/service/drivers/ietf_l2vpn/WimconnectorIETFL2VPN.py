# -*- coding: utf-8 -*-
##
# Copyright 2018 Telefonica
# All Rights Reserved.
#
# Contributors: Oscar Gonzalez de Dios, Manuel Lopez Bravo, Guillermo Pajares Martin
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This work has been performed in the context of the Metro-Haul project -
# funded by the European Commission under Grant number 761727 through the
# Horizon 2020 program.
##
"""The SDN/WIM connector is responsible for establishing wide area network
connectivity.

This SDN/WIM connector implements the standard IETF RFC 8466 "A YANG Data
 Model for Layer 2 Virtual Private Network (L2VPN) Service Delivery"

It receives the endpoints and the necessary details to request
the Layer 2 service.
"""
import requests
import uuid
import logging
import copy
#from osm_ro_plugin.sdnconn import SdnConnectorBase, SdnConnectorError
from .sdnconn import SdnConnectorBase, SdnConnectorError

"""Check layer where we move it"""


class WimconnectorIETFL2VPN(SdnConnectorBase):
    def __init__(self, wim, wim_account, config=None, logger=None):
        """IETF L2VPN WIM connector

        Arguments: (To be completed)
            wim (dict): WIM record, as stored in the database
            wim_account (dict): WIM account record, as stored in the database
        """
        self.logger = logging.getLogger("ro.sdn.ietfl2vpn")
        super().__init__(wim, wim_account, config, logger)
        self.headers = {"Content-Type": "application/json"}
        self.mappings = {
            m["service_endpoint_id"]: m for m in self.service_endpoint_mapping
        }
        self.user = wim_account.get("user")
        self.passwd = wim_account.get("password")

        if self.user is not None and self.passwd is not None:
            self.auth = (self.user, self.passwd)
        else:
            self.auth = None

        self.logger.info("IETFL2VPN Connector Initialized.")

    def check_credentials(self):
        endpoint = "{}/restconf/data/ietf-l2vpn-svc:l2vpn-svc/vpn-services".format(
            self.wim["wim_url"]
        )

        try:
            response = requests.get(endpoint, auth=self.auth)
            http_code = response.status_code
        except requests.exceptions.RequestException as e:
            raise SdnConnectorError(e.response, http_code=503)

        if http_code != 200:
            raise SdnConnectorError("Failed while authenticating", http_code=http_code)

        self.logger.info("Credentials checked")

    def get_connectivity_service_status(self, service_uuid, conn_info=None):
        """Monitor the status of the connectivity service stablished

        Arguments:
            service_uuid: Connectivity service unique identifier

        Returns:
            Examples::
                {'sdn_status': 'ACTIVE'}
                {'sdn_status': 'INACTIVE'}
                {'sdn_status': 'DOWN'}
                {'sdn_status': 'ERROR'}
        """
        try:
            self.logger.info("Sending get connectivity service stuatus")
            servicepoint = "{}/restconf/data/ietf-l2vpn-svc:l2vpn-svc/vpn-services/vpn-service={}/".format(
                self.wim["wim_url"], service_uuid
            )
            response = requests.get(servicepoint, auth=self.auth)
            self.logger.warning('response.status_code={:s}'.format(str(response.status_code)))
            if response.status_code != requests.codes.ok:
                raise SdnConnectorError(
                    "Unable to obtain connectivity servcice status",
                    http_code=response.status_code,
                )

            service_status = {"sdn_status": "ACTIVE"}

            return service_status
        except requests.exceptions.ConnectionError:
            raise SdnConnectorError("Request Timeout", http_code=408)

    def search_mapp(self, connection_point):
        id = connection_point["service_endpoint_id"]
        if id not in self.mappings:
            raise SdnConnectorError("Endpoint {} not located".format(str(id)))
        else:
            return self.mappings[id]

    def create_connectivity_service(self, service_uuid, service_type, connection_points, **kwargs):
        """Stablish WAN connectivity between the endpoints

        Arguments:
            service_type (str): ``ELINE`` (L2), ``ELAN`` (L2), ``ETREE`` (L2),
                ``L3``.
            connection_points (list): each point corresponds to
                an entry point from the DC to the transport network. One
                connection point serves to identify the specific access and
                some other service parameters, such as encapsulation type.
                Represented by a dict as follows::

                    {
                      "service_endpoint_id": ..., (str[uuid])
                      "service_endpoint_encapsulation_type": ...,
                           (enum: none, dot1q, ...)
                      "service_endpoint_encapsulation_info": {
                        ... (dict)
                        "vlan": ..., (int, present if encapsulation is dot1q)
                        "vni": ... (int, present if encapsulation is vxlan),
                        "peers": [(ipv4_1), (ipv4_2)]
                            (present if encapsulation is vxlan)
                      }
                    }

              The service endpoint ID should be previously informed to the WIM
              engine in the RO when the WIM port mapping is registered.

        Keyword Arguments:
            bandwidth (int): value in kilobytes
            latency (int): value in milliseconds

        Other QoS might be passed as keyword arguments.

        Returns:
            tuple: ``conn_info``:
               - *conn_info* (dict or None): Information to be stored at the
                 database (or ``None``). This information will be provided to
                 the :meth:`~.edit_connectivity_service` and :obj:`~.delete`.
                 **MUST** be JSON/YAML-serializable (plain data structures).

        Raises:
            SdnConnectorException: In case of error.
        """
        SETTINGS = {    # min_endpoints, max_endpoints, vpn_service_type
            'ELINE': (2,    2, 'vpws'), # Virtual Private Wire Service
            'ELAN' : (2, None, 'vpls'), # Virtual Private LAN  Service
        }
        settings = SETTINGS.get(service_type)
        if settings is None: raise NotImplementedError('Unsupported service_type({:s})'.format(str(service_type)))
        min_endpoints, max_endpoints, vpn_service_type = settings

        if max_endpoints is not None and len(connection_points) > max_endpoints:
            msg = "Connections between more than {:d} endpoints are not supported for service_type {:s}"
            raise SdnConnectorError(msg.format(max_endpoints, service_type))

        if min_endpoints is not None and len(connection_points) < min_endpoints:
            msg = "Connections must be of at least {:d} endpoints for service_type {:s}"
            raise SdnConnectorError(msg.format(min_endpoints, service_type))

        """First step, create the vpn service"""
        vpn_service = {}
        vpn_service["vpn-id"] = service_uuid
        vpn_service["vpn-svc-type"] = vpn_service_type
        vpn_service["svc-topo"] = "any-to-any"
        vpn_service["customer-name"] = "osm"
        vpn_service_list = []
        vpn_service_list.append(vpn_service)
        vpn_service_l = {"ietf-l2vpn-svc:vpn-service": vpn_service_list}
        response_service_creation = None
        conn_info = []
        self.logger.info("Sending vpn-service :{}".format(vpn_service_l))

        try:
            endpoint_service_creation = (
                "{}/restconf/data/ietf-l2vpn-svc:l2vpn-svc/vpn-services".format(
                    self.wim["wim_url"]
                )
            )
            response_service_creation = requests.post(
                endpoint_service_creation,
                headers=self.headers,
                json=vpn_service_l,
                auth=self.auth,
            )
        except requests.exceptions.ConnectionError:
            raise SdnConnectorError(
                "Request to create service Timeout", http_code=408
            )

        if response_service_creation.status_code == 409:
            raise SdnConnectorError(
                "Service already exists",
                http_code=response_service_creation.status_code,
            )
        elif response_service_creation.status_code != requests.codes.created:
            raise SdnConnectorError(
                "Request to create service not accepted",
                http_code=response_service_creation.status_code,
            )

        self.logger.info('connection_points = {:s}'.format(str(connection_points)))

        # Check if protected paths are requested
        extended_connection_points = []
        for connection_point in connection_points:
            extended_connection_points.append(connection_point)

            connection_point_wan_info = self.search_mapp(connection_point)
            service_mapping_info = connection_point_wan_info.get('service_mapping_info', {})
            redundant_service_endpoint_ids = service_mapping_info.get('redundant')

            if redundant_service_endpoint_ids is None: continue
            if len(redundant_service_endpoint_ids) == 0: continue

            for redundant_service_endpoint_id in redundant_service_endpoint_ids:
                redundant_connection_point = copy.deepcopy(connection_point)
                redundant_connection_point['service_endpoint_id'] = redundant_service_endpoint_id
                extended_connection_points.append(redundant_connection_point)

        self.logger.info('extended_connection_points = {:s}'.format(str(extended_connection_points)))

        """Second step, create the connections and vpn attachments"""
        for connection_point in extended_connection_points:
            connection_point_wan_info = self.search_mapp(connection_point)
            site_network_access = {}
            connection = {}

            if connection_point["service_endpoint_encapsulation_type"] != "none":
                if (
                    connection_point["service_endpoint_encapsulation_type"]
                    == "dot1q"
                ):
                    """The connection is a VLAN"""
                    connection["encapsulation-type"] = "dot1q-vlan-tagged"
                    tagged = {}
                    tagged_interf = {}
                    service_endpoint_encapsulation_info = connection_point[
                        "service_endpoint_encapsulation_info"
                    ]

                    if service_endpoint_encapsulation_info["vlan"] is None:
                        raise SdnConnectorError("VLAN must be provided")

                    tagged_interf["cvlan-id"] = service_endpoint_encapsulation_info[
                        "vlan"
                    ]
                    tagged["dot1q-vlan-tagged"] = tagged_interf
                    connection["tagged-interface"] = tagged
                else:
                    raise NotImplementedError("Encapsulation type not implemented")

            site_network_access["connection"] = connection
            self.logger.info("Sending connection:{}".format(connection))
            vpn_attach = {}
            vpn_attach["vpn-id"] = service_uuid
            vpn_attach["site-role"] = vpn_service["svc-topo"] + "-role"
            site_network_access["vpn-attachment"] = vpn_attach
            self.logger.info("Sending vpn-attachement :{}".format(vpn_attach))
            uuid_sna = str(uuid.uuid4())
            site_network_access["network-access-id"] = uuid_sna
            site_network_access["bearer"] = connection_point_wan_info[
                "service_mapping_info"
            ]["bearer"]

            access_priority = connection_point_wan_info["service_mapping_info"].get("priority")
            if access_priority is not None:
                availability = {}
                availability["access-priority"] = access_priority
                availability["single-active"] = [None]
                site_network_access["availability"] = availability

                constraint = {}
                constraint['constraint-type'] = 'end-to-end-diverse'
                constraint['target'] = {'all-other-accesses': [None]}

                access_diversity = {}
                access_diversity['constraints'] = {'constraint': []}
                access_diversity['constraints']['constraint'].append(constraint)
                site_network_access["access-diversity"] = access_diversity

            site_network_accesses = {}
            site_network_access_list = []
            site_network_access_list.append(site_network_access)
            site_network_accesses[
                "ietf-l2vpn-svc:site-network-access"
            ] = site_network_access_list
            conn_info_d = {}
            conn_info_d["site"] = connection_point_wan_info["service_mapping_info"][
                "site-id"
            ]
            conn_info_d["site-network-access-id"] = site_network_access[
                "network-access-id"
            ]
            conn_info_d["mapping"] = None
            conn_info.append(conn_info_d)

            try:
                endpoint_site_network_access_creation = (
                    "{}/restconf/data/ietf-l2vpn-svc:l2vpn-svc/"
                    "sites/site={}/site-network-accesses/".format(
                        self.wim["wim_url"],
                        connection_point_wan_info["service_mapping_info"][
                            "site-id"
                        ],
                    )
                )
                response_endpoint_site_network_access_creation = requests.post(
                    endpoint_site_network_access_creation,
                    headers=self.headers,
                    json=site_network_accesses,
                    auth=self.auth,
                )

                if (
                    response_endpoint_site_network_access_creation.status_code
                    == 409
                ):
                    self.delete_connectivity_service(vpn_service["vpn-id"])

                    raise SdnConnectorError(
                        "Site_Network_Access with ID '{}' already exists".format(
                            site_network_access["network-access-id"]
                        ),
                        http_code=response_endpoint_site_network_access_creation.status_code,
                    )
                elif (
                    response_endpoint_site_network_access_creation.status_code
                    == 400
                ):
                    self.delete_connectivity_service(vpn_service["vpn-id"])

                    raise SdnConnectorError(
                        "Site {} does not exist".format(
                            connection_point_wan_info["service_mapping_info"][
                                "site-id"
                            ]
                        ),
                        http_code=response_endpoint_site_network_access_creation.status_code,
                    )
                elif (
                    response_endpoint_site_network_access_creation.status_code
                    != requests.codes.created
                    and response_endpoint_site_network_access_creation.status_code
                    != requests.codes.no_content
                ):
                    self.delete_connectivity_service(vpn_service["vpn-id"])

                    raise SdnConnectorError(
                        "Request not accepted",
                        http_code=response_endpoint_site_network_access_creation.status_code,
                    )
            except requests.exceptions.ConnectionError:
                self.delete_connectivity_service(vpn_service["vpn-id"])

                raise SdnConnectorError("Request Timeout", http_code=408)

        return conn_info

    def delete_connectivity_service(self, service_uuid, conn_info=None):
        """Disconnect multi-site endpoints previously connected

        This method should receive as the first argument the UUID generated by
        the ``create_connectivity_service``
        """
        try:
            self.logger.info("Sending delete")
            servicepoint = "{}/restconf/data/ietf-l2vpn-svc:l2vpn-svc/vpn-services/vpn-service={}/".format(
                self.wim["wim_url"], service_uuid
            )
            response = requests.delete(servicepoint, auth=self.auth)

            if response.status_code != requests.codes.no_content:
                raise SdnConnectorError(
                    "Error in the request", http_code=response.status_code
                )
        except requests.exceptions.ConnectionError:
            raise SdnConnectorError("Request Timeout", http_code=408)

    def edit_connectivity_service(
        self, service_uuid, conn_info=None, connection_points=None, **kwargs
    ):
        """Change an existing connectivity service, see
        ``create_connectivity_service``"""
        # sites = {"sites": {}}
        # site_list = []
        vpn_service = {}
        vpn_service["svc-topo"] = "any-to-any"
        counter = 0

        for connection_point in connection_points:
            site_network_access = {}
            connection_point_wan_info = self.search_mapp(connection_point)
            params_site = {}
            params_site["site-id"] = connection_point_wan_info["service_mapping_info"][
                "site-id"
            ]
            params_site["site-vpn-flavor"] = "site-vpn-flavor-single"
            device_site = {}
            device_site["device-id"] = connection_point_wan_info["device-id"]
            params_site["devices"] = device_site
            # network_access = {}
            connection = {}

            if connection_point["service_endpoint_encapsulation_type"] != "none":
                if connection_point["service_endpoint_encapsulation_type"] == "dot1q":
                    """The connection is a VLAN"""
                    connection["encapsulation-type"] = "dot1q-vlan-tagged"
                    tagged = {}
                    tagged_interf = {}
                    service_endpoint_encapsulation_info = connection_point[
                        "service_endpoint_encapsulation_info"
                    ]

                    if service_endpoint_encapsulation_info["vlan"] is None:
                        raise SdnConnectorError("VLAN must be provided")

                    tagged_interf["cvlan-id"] = service_endpoint_encapsulation_info[
                        "vlan"
                    ]
                    tagged["dot1q-vlan-tagged"] = tagged_interf
                    connection["tagged-interface"] = tagged
                else:
                    raise NotImplementedError("Encapsulation type not implemented")

            site_network_access["connection"] = connection
            vpn_attach = {}
            vpn_attach["vpn-id"] = service_uuid
            vpn_attach["site-role"] = vpn_service["svc-topo"] + "-role"
            site_network_access["vpn-attachment"] = vpn_attach
            uuid_sna = conn_info[counter]["site-network-access-id"]
            site_network_access["network-access-id"] = uuid_sna
            site_network_access["bearer"] = connection_point_wan_info[
                "service_mapping_info"
            ]["bearer"]
            site_network_accesses = {}
            site_network_access_list = []
            site_network_access_list.append(site_network_access)
            site_network_accesses[
                "ietf-l2vpn-svc:site-network-access"
            ] = site_network_access_list

            try:
                endpoint_site_network_access_edit = (
                    "{}/restconf/data/ietf-l2vpn-svc:l2vpn-svc/"
                    "sites/site={}/site-network-accesses/".format(
                        self.wim["wim_url"],
                        connection_point_wan_info["service_mapping_info"]["site-id"],
                    )
                )
                response_endpoint_site_network_access_creation = requests.put(
                    endpoint_site_network_access_edit,
                    headers=self.headers,
                    json=site_network_accesses,
                    auth=self.auth,
                )

                if response_endpoint_site_network_access_creation.status_code == 400:
                    raise SdnConnectorError(
                        "Service does not exist",
                        http_code=response_endpoint_site_network_access_creation.status_code,
                    )
                elif (
                    response_endpoint_site_network_access_creation.status_code != 201
                    and response_endpoint_site_network_access_creation.status_code
                    != 204
                ):
                    raise SdnConnectorError(
                        "Request no accepted",
                        http_code=response_endpoint_site_network_access_creation.status_code,
                    )
            except requests.exceptions.ConnectionError:
                raise SdnConnectorError("Request Timeout", http_code=408)

            counter += 1

        return None

    def clear_all_connectivity_services(self):
        """Delete all WAN Links corresponding to a WIM"""
        try:
            self.logger.info("Sending clear all connectivity services")
            servicepoint = (
                "{}/restconf/data/ietf-l2vpn-svc:l2vpn-svc/vpn-services".format(
                    self.wim["wim_url"]
                )
            )
            response = requests.delete(servicepoint, auth=self.auth)

            if response.status_code != requests.codes.no_content:
                raise SdnConnectorError(
                    "Unable to clear all connectivity services",
                    http_code=response.status_code,
                )
        except requests.exceptions.ConnectionError:
            raise SdnConnectorError("Request Timeout", http_code=408)

    def get_all_active_connectivity_services(self):
        """Provide information about all active connections provisioned by a
        WIM
        """
        try:
            self.logger.info("Sending get all connectivity services")
            servicepoint = (
                "{}/restconf/data/ietf-l2vpn-svc:l2vpn-svc/vpn-services".format(
                    self.wim["wim_url"]
                )
            )
            response = requests.get(servicepoint, auth=self.auth)

            if response.status_code != requests.codes.ok:
                raise SdnConnectorError(
                    "Unable to get all connectivity services",
                    http_code=response.status_code,
                )

            return response
        except requests.exceptions.ConnectionError:
            raise SdnConnectorError("Request Timeout", http_code=408)

    def get_connectivity_service(self, service_uuid, conn_info=None):
        """Provide information about a specific connection provisioned by a WIM.

        This method should receive as the first argument the UUID generated by
        the ``create_connectivity_service``
        """
        try:
            self.logger.info("Sending get connectivity service")
            servicepoint = (
                "{}/restconf/data/ietf-l2vpn-svc:l2vpn-svc/vpn-services/vpn-service={}/".format(
                    self.wim["wim_url"], service_uuid
                )
            )
            response = requests.get(servicepoint, auth=self.auth)

            if response.status_code != requests.codes.ok:
                raise SdnConnectorError(
                    "Unable to get connectivity service {:s}".format(str(service_uuid)),
                    http_code=response.status_code,
                )

            return response
        except requests.exceptions.ConnectionError:
            raise SdnConnectorError("Request Timeout", http_code=408)
