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
# limitations under the License


PRODUCT_NAME=$(show version | grep 'Platform' | awk '{print $2}')
SERIAL_NUMBER=$(show version | grep 'Serial Number' | awk '{print $3}')
BASE_MAC_ADDRESS=$(show platform syseeprom | grep 'Base MAC Address' | awk '{print $6}')
SONIC_VERSION=$(show version | grep 'SONiC Software Version' | awk '{print $4}')

# URL of the config_db.json file
CONFIG_DB_URL="http://10.1.1.119:9001/config/config_db.json"

# Directory where the file will be saved
DEST_DIR="/etc/sonic"
DEST_FILE="$DEST_DIR/config_db.json"

# Download the config_db.json file
curl -o $DEST_FILE -H "User-Agent: SONiC-ZTP/0.1" \
                     -H "PRODUCT-NAME: $PRODUCT_NAME" \
                     -H "SERIAL-NUMBER: $SERIAL_NUMBER" \
                     -H "BASE-MAC-ADDRESS: $BASE_MAC_ADDRESS" \
                     -H "SONiC-VERSION: $SONIC_VERSION" \
                     $CONFIG_DB_URL
if [ $? -ne 0 ]; then
    logger "Error: Failed to download the file from $CONFIG_DB_URL"
    exit 1
fi

# Reload the configuration database
sudo config reload -y

# Check if the reload was successful
if [ $? -eq 0 ]; then
    logger "The configuration database reloaded successfully."
else
    logger "Error: Failed to reload the configuration database."
    exit 1
fi

logger "Plugin executed successfully."
