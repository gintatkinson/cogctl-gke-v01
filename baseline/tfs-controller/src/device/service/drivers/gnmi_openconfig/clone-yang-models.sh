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

BASE_PATH=~/tfs-ctrl/src/device/service/drivers/gnmi_openconfig
GIT_BASE_PATH=${BASE_PATH}/git/openconfig

rm -rf ${GIT_BASE_PATH}

OC_PUBLIC_PATH=${GIT_BASE_PATH}/public
mkdir -p ${OC_PUBLIC_PATH}
git clone https://github.com/openconfig/public.git ${OC_PUBLIC_PATH}

#OC_HERCULES_PATH=${GIT_BASE_PATH}/hercules
#mkdir -p ${OC_HERCULES_PATH}
#git clone https://github.com/openconfig/hercules.git ${OC_HERCULES_PATH}
