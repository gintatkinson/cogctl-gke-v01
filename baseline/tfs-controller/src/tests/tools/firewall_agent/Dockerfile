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


FROM python:3.11-slim

ENV PYTHONUNBUFFERED=0

RUN apt-get --yes --quiet --quiet update && \
    apt-get --yes --quiet --quiet install --no-install-recommends libxtables-dev iptables gcc libc6-dev python3-nftables && \
    apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY firewall_agent ./firewall_agent

EXPOSE 8888
CMD ["python", "-m", "firewall_agent.app"]
