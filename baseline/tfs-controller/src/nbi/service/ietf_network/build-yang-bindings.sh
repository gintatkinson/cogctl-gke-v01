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

BASE_PATH=~/tfs-ctrl/src/nbi/service/ietf_network
IETF_MODELS_PATH=${BASE_PATH}/yang

cd ${BASE_PATH}
export PYBINDPLUGIN=`/usr/bin/env python -c 'import pyangbind; import os; print ("{}/plugin".format(os.path.dirname(pyangbind.__file__)))'`

rm -rf bindings

# -p ${OC_HERCULES_MODELS_PATH}/
# --split-class-dir openconfig_hercules
# --presence
pyang --plugindir $PYBINDPLUGIN -p ${IETF_MODELS_PATH}/ -f pybind --split-class-dir bindings \
    ${IETF_MODELS_PATH}/ietf-network-topology@2018-02-26.yang \
    ${IETF_MODELS_PATH}/ietf-network@2018-02-26.yang          \
    ${IETF_MODELS_PATH}/ietf-te-topology@2020-08-06.yang      \
    ${IETF_MODELS_PATH}/ietf-otn-topology@2023-07-06.yang     \
    ${IETF_MODELS_PATH}/ietf-eth-te-topology@2023-09-28.yang  

#    ${IETF_MODELS_PATH}/iana-routing-types@2017-12-04.yang    \
#    ${IETF_MODELS_PATH}/ietf-inet-types@2013-07-15.yang       \
#    ${IETF_MODELS_PATH}/ietf-layer1-types@2022-10-14.yang     \
#    ${IETF_MODELS_PATH}/ietf-routing-types@2017-12-04.yang    \
#    ${IETF_MODELS_PATH}/ietf-te-packet-types@2020-06-10.yang  \
#    ${IETF_MODELS_PATH}/ietf-te-types@2020-06-10.yang         \
#    ${IETF_MODELS_PATH}/ietf-yang-types@2013-07-15.yang       \
