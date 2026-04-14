#!/bin/bash
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

PROJECTDIR=`pwd`

cd $PROJECTDIR/src

# test DSCM NBI functions
python3 -m pytest --log-level=INFO --log-cli-level=INFO --verbose \
    nbi/tests/test_dscm_restconf.py::test_post_get_delete_leaf_optical_channel_frequency

# # test JSON to Proto conversion functions
# python3 -m pytest --log-level=INFO --log-cli-level=INFO --verbose \
#     nbi/tests/test_json_to_proto.py::test_create_pluggable_request_hub_format \
#     nbi/tests/test_json_to_proto.py::test_create_pluggable_request_leaf_format \
#     nbi/tests/test_json_to_proto.py::test_configure_pluggable_request_hub_format \
#     nbi/tests/test_json_to_proto.py::test_configure_pluggable_request_leaf_format \
#     nbi/tests/test_json_to_proto.py::test_empty_payload
