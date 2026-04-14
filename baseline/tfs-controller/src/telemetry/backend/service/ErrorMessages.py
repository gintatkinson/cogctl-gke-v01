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

_DEVICE_ID          = 'DeviceId({device_uuid:s})'
_ENDPOINT_ID        = 'EndpointId({endpoint_uuid:s})'
_KPI                = 'Kpi({kpi_uuid:s})'
_DEVICE_ENDPOINT_ID = _DEVICE_ID + '/' + _ENDPOINT_ID
_RESOURCE           = 'Resource({resource_data:s})'
_RESOURCE_KEY       = 'Resource(key={resource_key:s})'
_RESOURCE_KEY_VALUE = 'Resource(key={resource_key:s}, value={resource_value:s})'
_SUBSCRIPTION       = 'Subscription(key={subscr_key:s}, duration={subscr_duration:s}, interval={subscr_interval:s})'
_SAMPLE_TYPE        = 'SampleType({sample_type_id:s}/{sample_type_name:s})'
_ERROR              = 'Error({error:s})'

ERROR_MISSING_DRIVER = _DEVICE_ID + ' has not been added to this Device instance'
ERROR_MISSING_KPI    = _KPI + ' not found'

ERROR_BAD_RESOURCE   = _DEVICE_ID + ': GetConfig retrieved malformed ' + _RESOURCE
ERROR_UNSUP_RESOURCE = _DEVICE_ID + ': GetConfig retrieved unsupported ' + _RESOURCE

ERROR_GET            = _DEVICE_ID + ': Unable to Get ' + _RESOURCE_KEY + '; ' + _ERROR
ERROR_GET_INIT       = _DEVICE_ID + ': Unable to Get Initial ' + _RESOURCE_KEY + '; ' + _ERROR
ERROR_DELETE         = _DEVICE_ID + ': Unable to Delete ' + _RESOURCE_KEY_VALUE + '; ' + _ERROR
ERROR_SET            = _DEVICE_ID + ': Unable to Set ' + _RESOURCE_KEY_VALUE + '; ' + _ERROR

ERROR_SAMPLETYPE     = _DEVICE_ENDPOINT_ID + ': ' + _SAMPLE_TYPE + ' not supported'

ERROR_SUBSCRIBE      = _DEVICE_ID + ': Unable to Subscribe ' + _SUBSCRIPTION + '; ' + _ERROR
ERROR_UNSUBSCRIBE    = _DEVICE_ID + ': Unable to Unsubscribe ' + _SUBSCRIPTION + '; ' + _ERROR
