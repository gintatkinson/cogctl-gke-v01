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

# Add/comment in this file the service handlers to be tested by the unitry tests.

SERVICE_HANDLERS_TO_TEST = []

try:
    from service.tests.ServiceHandler_L3NM_EMU import TEST_SERVICE_HANDLER
    SERVICE_HANDLERS_TO_TEST.append(TEST_SERVICE_HANDLER)
except ImportError:
    pass

#try:
#    from service.tests.ServiceHandler_L3NM_OC import TEST_SERVICE_HANDLER
#    SERVICE_HANDLERS_TO_TEST.append(TEST_SERVICE_HANDLER)
#except ImportError:
#    pass
