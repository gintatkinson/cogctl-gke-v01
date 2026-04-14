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

ALLOWED_LINKS_PER_CONTROLLER = {
    'e2e'      : {'L1', 'L2', 'L3', 'L4'},
    'agg'      : {'L7ab', 'L7ba', 'L8ab', 'L8ba', 'L11ab', 'L11ba',
                  'L12ab', 'L12ba', 'L13', 'L14'},
    'trans-pkt': {'L5', 'L6', 'L9', 'L10'},
}
