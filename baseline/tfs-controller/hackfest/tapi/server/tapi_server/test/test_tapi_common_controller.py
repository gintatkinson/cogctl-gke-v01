# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from tapi_server.models.operations_tapicommongetserviceinterfacepointdetails_body import OperationsTapicommongetserviceinterfacepointdetailsBody  # noqa: E501
from tapi_server.models.operations_tapicommonupdateserviceinterfacepoint_body import OperationsTapicommonupdateserviceinterfacepointBody  # noqa: E501
from tapi_server.models.tapi_common_bandwidth_profile_wrapper import TapiCommonBandwidthProfileWrapper  # noqa: E501
from tapi_server.models.tapi_common_capacity_value_wrapper import TapiCommonCapacityValueWrapper  # noqa: E501
from tapi_server.models.tapi_common_capacity_wrapper import TapiCommonCapacityWrapper  # noqa: E501
from tapi_server.models.tapi_common_context_wrapper import TapiCommonContextWrapper  # noqa: E501
from tapi_server.models.tapi_common_get_service_interface_point_details import TapiCommonGetServiceInterfacePointDetails  # noqa: E501
from tapi_server.models.tapi_common_get_service_interface_point_list import TapiCommonGetServiceInterfacePointList  # noqa: E501
from tapi_server.models.tapi_common_name_and_value_wrapper import TapiCommonNameAndValueWrapper  # noqa: E501
from tapi_server.models.tapi_common_service_interface_point_wrapper import TapiCommonServiceInterfacePointWrapper  # noqa: E501
from tapi_server.test import BaseTestCase


class TestTapiCommonController(BaseTestCase):
    """TapiCommonController integration test stubs"""

    def test_data_tapi_commoncontext_delete(self):
        """Test case for data_tapi_commoncontext_delete

        removes tapi.common.Context
        """
        response = self.client.open(
            '/data/tapi-common:context/',
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_get(self):
        """Test case for data_tapi_commoncontext_get

        returns tapi.common.Context
        """
        response = self.client.open(
            '/data/tapi-common:context/',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_name_post(self):
        """Test case for data_tapi_commoncontext_name_post

        creates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/name/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_namevalue_name_delete(self):
        """Test case for data_tapi_commoncontext_namevalue_name_delete

        removes tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/name={value-name}/'.format(value_name='value_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/name={value-name}/'.format(value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_namevalue_name_put(self):
        """Test case for data_tapi_commoncontext_namevalue_name_put

        creates or updates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/name={value-name}/'.format(value_name='value_name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_post(self):
        """Test case for data_tapi_commoncontext_post

        creates tapi.common.Context
        """
        body = TapiCommonContextWrapper()
        response = self.client.open(
            '/data/tapi-common:context/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_put(self):
        """Test case for data_tapi_commoncontext_put

        creates or updates tapi.common.Context
        """
        body = TapiCommonContextWrapper()
        response = self.client.open(
            '/data/tapi-common:context/',
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_point_post(self):
        """Test case for data_tapi_commoncontext_service_interface_point_post

        creates tapi.common.ServiceInterfacePoint
        """
        body = TapiCommonServiceInterfacePointWrapper()
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_available_capacity_bandwidth_profile_committed_burst_size_get(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_available_capacity_bandwidth_profile_committed_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/available-capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_available_capacity_bandwidth_profile_committed_information_rate_get(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_available_capacity_bandwidth_profile_committed_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/available-capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_available_capacity_bandwidth_profile_get(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_available_capacity_bandwidth_profile_get

        returns tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/available-capacity/bandwidth-profile/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_available_capacity_bandwidth_profile_peak_burst_size_get(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_available_capacity_bandwidth_profile_peak_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/available-capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_available_capacity_bandwidth_profile_peak_information_rate_get(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_available_capacity_bandwidth_profile_peak_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/available-capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_available_capacity_get(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_available_capacity_get

        returns tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/available-capacity/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_available_capacity_total_size_get(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_available_capacity_total_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/available-capacity/total-size/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_delete(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_delete

        removes tapi.common.ServiceInterfacePoint
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/'.format(uuid='uuid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_get(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_get

        returns tapi.common.ServiceInterfacePoint
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_name_post(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_name_post

        creates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/name/'.format(uuid='uuid_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_namevalue_name_delete(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_namevalue_name_delete

        removes tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_namevalue_name_get(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_namevalue_name_get

        returns tapi.common.NameAndValue
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_namevalue_name_put(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_namevalue_name_put

        creates or updates tapi.common.NameAndValue
        """
        body = TapiCommonNameAndValueWrapper()
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/name={value-name}/'.format(uuid='uuid_example', value_name='value_name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_put(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_put

        creates or updates tapi.common.ServiceInterfacePoint
        """
        body = TapiCommonServiceInterfacePointWrapper()
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/'.format(uuid='uuid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_bandwidth_profile_committed_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/total-potential-capacity/bandwidth-profile/committed-burst-size/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_bandwidth_profile_committed_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/total-potential-capacity/bandwidth-profile/committed-information-rate/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_bandwidth_profile_get(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_bandwidth_profile_get

        returns tapi.common.BandwidthProfile
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/total-potential-capacity/bandwidth-profile/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_bandwidth_profile_peak_burst_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/total-potential-capacity/bandwidth-profile/peak-burst-size/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_bandwidth_profile_peak_information_rate_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/total-potential-capacity/bandwidth-profile/peak-information-rate/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_get(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_get

        returns tapi.common.Capacity
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/total-potential-capacity/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_total_size_get(self):
        """Test case for data_tapi_commoncontext_service_interface_pointuuid_total_potential_capacity_total_size_get

        returns tapi.common.CapacityValue
        """
        response = self.client.open(
            '/data/tapi-common:context/service-interface-point={uuid}/total-potential-capacity/total-size/'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_commonget_service_interface_point_details_post(self):
        """Test case for operations_tapi_commonget_service_interface_point_details_post

        operates on tapi.common.GetServiceInterfacePointDetails
        """
        body = OperationsTapicommongetserviceinterfacepointdetailsBody()
        response = self.client.open(
            '/operations/tapi-common:get-service-interface-point-details/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_commonget_service_interface_point_list_post(self):
        """Test case for operations_tapi_commonget_service_interface_point_list_post

        
        """
        response = self.client.open(
            '/operations/tapi-common:get-service-interface-point-list/',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_operations_tapi_commonupdate_service_interface_point_post(self):
        """Test case for operations_tapi_commonupdate_service_interface_point_post

        operates on tapi.common.UpdateServiceInterfacePoint
        """
        body = OperationsTapicommonupdateserviceinterfacepointBody()
        response = self.client.open(
            '/operations/tapi-common:update-service-interface-point/',
            method='POST',
            data=json.dumps(body),
            content_type='application/yang-data+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
