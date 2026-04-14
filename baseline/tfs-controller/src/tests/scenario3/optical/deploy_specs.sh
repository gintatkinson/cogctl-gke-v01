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


# ----- TeraFlowSDN ------------------------------------------------------------

# Set the list of components, separated by spaces, you want to build images for, and deploy.
export TFS_COMPONENTS="context device ztp monitoring pathcomp service slice nbi webui load_generator"

# addition for the optical cybersecurity component
export TFS_COMPONENTS="${TFS_COMPONENTS} dbscanserving opticalattackmitigator opticalattackdetector opticalattackmanager"

export TFS_EXTRA_MANIFESTS="manifests/nginx_ingress_http.yaml manifests/servicemonitors.yaml"
export TFS_EXTRA_MANIFESTS="${TFS_EXTRA_MANIFESTS} manifests/cachingservice.yaml"


# ----- CockroachDB ------------------------------------------------------------


# Disable flag for dropping database, if it exists.
export CRDB_DROP_DATABASE_IF_EXISTS="YES"



# ----- QuestDB ----------------------------------------------------------------

# Disable flag for dropping tables if they exist.
export QDB_DROP_TABLES_IF_EXIST="YES"

# Disable flag for re-deploying QuestDB from scratch.
export QDB_REDEPLOY=""
