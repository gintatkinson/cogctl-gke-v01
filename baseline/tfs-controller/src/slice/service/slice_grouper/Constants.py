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

# TODO: define by means of settings
SLICE_GROUPS = [
    ('bronze',   10.0,  10.0), # Bronze   (10%, 10Gb/s)
    ('silver',   30.0,  40.0), # Silver   (30%, 40Gb/s)
    ('gold',     70.0,  50.0), # Gold     (70%, 50Gb/s)
    ('platinum', 99.0, 100.0), # Platinum (99%, 100Gb/s)
]
SLICE_GROUP_NAMES = {slice_group[0] for slice_group in SLICE_GROUPS}
