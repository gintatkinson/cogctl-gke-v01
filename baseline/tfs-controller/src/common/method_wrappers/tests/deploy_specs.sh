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

# Set the URL of the internal MicroK8s Docker registry where the images will be uploaded to.
export TFS_REGISTRY_IMAGES="http://localhost:32000/tfs/"

# Set the list of components, separated by spaces, you want to build images for, and deploy.
export TFS_COMPONENTS="context device pathcomp service slice webui load_generator"

# Set the tag you want to use for your images.
export TFS_IMAGE_TAG="dev"

# Set the name of the Kubernetes namespace to deploy TFS to.
export TFS_K8S_NAMESPACE="tfs"

# Set additional manifest files to be applied after the deployment
export TFS_EXTRA_MANIFESTS="manifests/nginx_ingress_http.yaml manifests/servicemonitors.yaml"

# Set the new Grafana admin password
export TFS_GRAFANA_PASSWORD="admin123+"

# Disable skip-build flag to rebuild the Docker images.
export TFS_SKIP_BUILD=""


# ----- CockroachDB ------------------------------------------------------------

# Set the namespace where CockroackDB will be deployed.
export CRDB_NAMESPACE="crdb"

# Set the database username to be used by Context.
export CRDB_USERNAME="tfs"

# Set the database user's password to be used by Context.
export CRDB_PASSWORD="tfs123"

# Set CockroachDB installation mode to 'single'. This option is convenient for development and testing.
# See ./deploy/all.sh or ./deploy/crdb.sh for additional details
export CRDB_DEPLOY_MODE="single"

# Disable flag for dropping database, if it exists.
export CRDB_DROP_DATABASE_IF_EXISTS=""

# Disable flag for re-deploying CockroachDB from scratch.
export CRDB_REDEPLOY=""


# ----- NATS -------------------------------------------------------------------

# Set the namespace where NATS will be deployed.
export NATS_NAMESPACE="nats"

# Disable flag for re-deploying NATS from scratch.
export NATS_REDEPLOY=""


# ----- QuestDB ----------------------------------------------------------------

# Set the namespace where QuestDB will be deployed.
export QDB_NAMESPACE="qdb"

# Set the database username to be used for QuestDB.
export QDB_USERNAME="admin"

# Set the database user's password to be used for QuestDB.
export QDB_PASSWORD="quest"

# Set the table name to be used by Monitoring for KPIs.
export QDB_TABLE_MONITORING_KPIS="tfs_monitoring_kpis"

# Set the table name to be used by Slice for plotting groups.
export QDB_TABLE_SLICE_GROUPS="tfs_slice_groups"

# Disable flag for dropping tables if they exist.
export QDB_DROP_TABLES_IF_EXIST=""

# Disable flag for re-deploying QuestDB from scratch.
export QDB_REDEPLOY=""
