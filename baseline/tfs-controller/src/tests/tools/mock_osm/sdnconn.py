# -*- coding: utf-8 -*-
##
# Copyright 2018 University of Bristol - High Performance Networks Research
# Group
# All Rights Reserved.
#
# Contributors: Anderson Bravalheri, Dimitrios Gkounis, Abubakar Siddique
# Muqaddas, Navdeep Uniyal, Reza Nejabati and Dimitra Simeonidou
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# For those usages not covered by the Apache License, Version 2.0 please
# contact with: <highperformance-networks@bristol.ac.uk>
#
# Neither the name of the University of Bristol nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# This work has been performed in the context of DCMS UK 5G Testbeds
# & Trials Programme and in the framework of the Metro-Haul project -
# funded by the European Commission under Grant number 761727 through the
# Horizon 2020 and 5G-PPP programmes.
##
"""The SDN connector is responsible for establishing both wide area network connectivity (WIM)
and intranet SDN connectivity.

It receives information from ports to be connected .
"""

import logging
from http import HTTPStatus


class SdnConnectorError(Exception):
    """Base Exception for all connector related errors
    provide the parameter 'http_code' (int) with the error code:
        Bad_Request = 400
        Unauthorized = 401  (e.g. credentials are not valid)
        Not_Found = 404    (e.g. try to edit or delete a non existing connectivity service)
        Forbidden = 403
        Method_Not_Allowed = 405
        Not_Acceptable = 406
        Request_Timeout = 408  (e.g timeout reaching server, or cannot reach the server)
        Conflict = 409
        Service_Unavailable = 503
        Internal_Server_Error = 500
    """

    def __init__(self, message, http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value):
        Exception.__init__(self, message)
        self.http_code = http_code


class SdnConnectorBase(object):
    """Abstract base class for all the SDN connectors

    Arguments:
        wim (dict): WIM record, as stored in the database
        wim_account (dict): WIM account record, as stored in the database
        config
    The arguments of the constructor are converted to object attributes.
    An extra property, ``service_endpoint_mapping`` is created from ``config``.
    """

    def __init__(self, wim, wim_account, config=None, logger=None):
        """
        :param wim: (dict). Contains among others 'wim_url'
        :param wim_account: (dict). Contains among others 'uuid' (internal id), 'name',
            'sdn' (True if is intended for SDN-assist or False if intended for WIM), 'user', 'password'.
        :param config: (dict or None): Particular information of plugin. These keys if present have a common meaning:
            'mapping_not_needed': (bool) False by default or if missing, indicates that mapping is not needed.
            'service_endpoint_mapping': (list) provides the internal endpoint mapping. The meaning is:
                KEY                     meaning for WIM             meaning for SDN assist
                --------                --------                    --------
                device_id               pop_switch_dpid             compute_id
                device_interface_id     pop_switch_port             compute_pci_address
                service_endpoint_id     wan_service_endpoint_id     SDN_service_endpoint_id
                service_mapping_info    wan_service_mapping_info    SDN_service_mapping_info
                    contains extra information if needed. Text in Yaml format
                switch_dpid             wan_switch_dpid             SDN_switch_dpid
                switch_port             wan_switch_port             SDN_switch_port
                datacenter_id           vim_account                 vim_account
            id: (internal, do not use)
            wim_id: (internal, do not use)
        :param logger (logging.Logger): optional logger object. If none is passed 'openmano.sdn.sdnconn' is used.
        """
        self.logger = logger or logging.getLogger("ro.sdn")
        self.wim = wim
        self.wim_account = wim_account
        self.config = config or {}
        self.service_endpoint_mapping = self.config.get("service_endpoint_mapping", [])

    def check_credentials(self):
        """Check if the connector itself can access the SDN/WIM with the provided url (wim.wim_url),
            user (wim_account.user), and password (wim_account.password)

        Raises:
            SdnConnectorError: Issues regarding authorization, access to
                external URLs, etc are detected.
        """
        raise NotImplementedError

    def get_connectivity_service_status(self, service_uuid, conn_info=None):
        """Monitor the status of the connectivity service established

        Arguments:
            service_uuid (str): UUID of the connectivity service
            conn_info (dict or None): Information returned by the connector
                during the service creation/edition and subsequently stored in
                the database.

        Returns:
            dict: JSON/YAML-serializable dict that contains a mandatory key
                ``sdn_status`` associated with one of the following values::

                    {'sdn_status': 'ACTIVE'}
                        # The service is up and running.

                    {'sdn_status': 'INACTIVE'}
                        # The service was created, but the connector
                        # cannot determine yet if connectivity exists
                        # (ideally, the caller needs to wait and check again).

                    {'sdn_status': 'DOWN'}
                        # Connection was previously established,
                        # but an error/failure was detected.

                    {'sdn_status': 'ERROR'}
                        # An error occurred when trying to create the service/
                        # establish the connectivity.

                    {'sdn_status': 'BUILD'}
                        # Still trying to create the service, the caller
                        # needs to wait and check again.

                Additionally ``error_msg``(**str**) and ``sdn_info``(**dict**)
                keys can be used to provide additional status explanation or
                new information available for the connectivity service.
        """
        raise NotImplementedError

    def create_connectivity_service(self, service_type, connection_points, **kwargs):
        """
        Establish SDN/WAN connectivity between the endpoints
        :param service_type: (str): ``ELINE`` (L2), ``ELAN`` (L2), ``ETREE`` (L2), ``L3``.
        :param connection_points:  (list): each point corresponds to
            an entry point to be connected. For WIM: from the DC to the transport network.
            For SDN: Compute/PCI to the transport network. One
            connection point serves to identify the specific access and
            some other service parameters, such as encapsulation type.
            Each item of the list is a dict with:
                "service_endpoint_id": (str)(uuid)  Same meaning that for 'service_endpoint_mapping' (see __init__)
                    In case the config attribute mapping_not_needed is True, this value is not relevant. In this case
                    it will contain the string "device_id:device_interface_id"
                "service_endpoint_encapsulation_type": None, "dot1q", ...
                "service_endpoint_encapsulation_info": (dict) with:
                    "vlan": ..., (int, present if encapsulation is dot1q)
                    "vni": ... (int, present if encapsulation is vxlan),
                    "peers": [(ipv4_1), (ipv4_2)] (present if encapsulation is vxlan)
                    "mac": ...
                    "device_id": ..., same meaning that for 'service_endpoint_mapping' (see __init__)
                    "device_interface_id": same meaning that for 'service_endpoint_mapping' (see __init__)
                    "switch_dpid": ..., present if mapping has been found for this device_id,device_interface_id
                    "swith_port": ... present if mapping has been found for this device_id,device_interface_id
                    "service_mapping_info": present if mapping has been found for this device_id,device_interface_id
        :param kwargs: For future versions:
            bandwidth (int): value in kilobytes
            latency (int): value in milliseconds
            Other QoS might be passed as keyword arguments.
        :return: tuple: ``(service_id, conn_info)`` containing:
            - *service_uuid* (str): UUID of the established connectivity service
            - *conn_info* (dict or None): Information to be stored at the database (or ``None``).
                This information will be provided to the :meth:`~.edit_connectivity_service` and :obj:`~.delete`.
                **MUST** be JSON/YAML-serializable (plain data structures).
        :raises: SdnConnectorException: In case of error. Nothing should be created in this case.
            Provide the parameter http_code
        """
        raise NotImplementedError

    def delete_connectivity_service(self, service_uuid, conn_info=None):
        """
        Disconnect multi-site endpoints previously connected

        :param service_uuid: The one returned by create_connectivity_service
        :param conn_info: The one returned by last call to 'create_connectivity_service' or 'edit_connectivity_service'
            if they do not return None
        :return: None
        :raises: SdnConnectorException: In case of error. The parameter http_code must be filled
        """
        raise NotImplementedError

    def edit_connectivity_service(
        self, service_uuid, conn_info=None, connection_points=None, **kwargs
    ):
        """Change an existing connectivity service.

        This method's arguments and return value follow the same convention as
        :meth:`~.create_connectivity_service`.

        :param service_uuid: UUID of the connectivity service.
        :param conn_info: (dict or None): Information previously returned by last call to create_connectivity_service
            or edit_connectivity_service
        :param connection_points: (list): If provided, the old list of connection points will be replaced.
        :param kwargs: Same meaning that create_connectivity_service
        :return: dict or None: Information to be updated and stored at the database.
                When ``None`` is returned, no information should be changed.
                When an empty dict is returned, the database record will be deleted.
                **MUST** be JSON/YAML-serializable (plain data structures).
        Raises:
            SdnConnectorException: In case of error.
        """

    def clear_all_connectivity_services(self):
        """Delete all WAN Links in a WIM.

        This method is intended for debugging only, and should delete all the
        connections controlled by the WIM/SDN, not only the  connections that
        a specific RO is aware of.

        Raises:
            SdnConnectorException: In case of error.
        """
        raise NotImplementedError

    def get_all_active_connectivity_services(self):
        """Provide information about all active connections provisioned by a
        WIM.

        Raises:
            SdnConnectorException: In case of error.
        """
        raise NotImplementedError
