#!/bin/bash
# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list
sed -i 's|security.debian.org|archive.debian.org/debian-security/|g' /etc/apt/sources.list
sed -i '/stretch-updates/d' /etc/apt/sources.list
chmod 1777 /tmp
apt update
apt install -y python-scapy
