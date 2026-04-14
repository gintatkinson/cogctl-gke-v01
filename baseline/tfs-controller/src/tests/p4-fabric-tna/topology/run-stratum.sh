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

# You must run this script as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

source "p4-switch-conf-common.sh"

LOG_FILE_DIR="/var/log/stratum/"

sudo mkdir -p "${LOG_FILE_DIR}"

LOG_LEVEL="info"
READ_LOGS_FILE_PATH=${LOG_FILE_DIR}"p4_reads.pb.txt"
WRITE_LOGS_FILE_PATH=${LOG_FILE_DIR}"p4_writes.pb.txt"
CHASSIS_CONFIG="p4-switch-three-port-chassis-config-phy.pb.txt"

[ -f ${CHASSIS_CONFIG} ] || { echo "$CHASSIS_CONFIG not found!" ; exit 1 ;}

touch "${READ_LOGS_FILE_PATH}"
touch "${WRITE_LOGS_FILE_PATH}"

ip netns exec ns-switch stratum_bmv2 \
        -chassis_config_file=${CHASSIS_CONFIG} \
        -read_req_log_file=${READ_LOGS_FILE_PATH} \
        -write_req_log_file=${WRITE_LOGS_FILE_PATH} \
        -external_stratum_urls="0.0.0.0:"${SW_P4RT_GNMI_PORT}",0.0.0.0:"${SW_P4RT_GRPC_PORT} \
        -local_stratum_url="0.0.0.0:"${SW_P4RT_LOCAL_PORT} \
        -bmv2_log_level=${LOG_LEVEL}

exit 0
