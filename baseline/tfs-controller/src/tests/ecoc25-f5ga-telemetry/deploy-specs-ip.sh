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
export TFS_COMPONENTS="context device pathcomp service nbi webui"

# Uncomment to activate Monitoring (old)
#export TFS_COMPONENTS="${TFS_COMPONENTS} monitoring"

# Uncomment to activate Monitoring Framework (new)
#export TFS_COMPONENTS="${TFS_COMPONENTS} kpi_manager kpi_value_writer kpi_value_api telemetry analytics automation"

# Uncomment to activate QoS Profiles
#export TFS_COMPONENTS="${TFS_COMPONENTS} qos_profile"

# Uncomment to activate BGP-LS Speaker
#export TFS_COMPONENTS="${TFS_COMPONENTS} bgpls_speaker"

# Uncomment to activate Optical Controller
#   To manage optical connections, "service" requires "opticalcontroller" to be deployed
#   before "service", thus we "hack" the TFS_COMPONENTS environment variable prepending the
#   "opticalcontroller" only if "service" is already in TFS_COMPONENTS, and re-export it.
#if [[ "$TFS_COMPONENTS" == *"service"* ]]; then
#    BEFORE="${TFS_COMPONENTS% service*}"
#    AFTER="${TFS_COMPONENTS#* service}"
#    export TFS_COMPONENTS="${BEFORE} opticalcontroller service ${AFTER}"
#fi

# Uncomment to activate ZTP
#export TFS_COMPONENTS="${TFS_COMPONENTS} ztp"

# Uncomment to activate Policy Manager
#export TFS_COMPONENTS="${TFS_COMPONENTS} policy"

# Uncomment to activate Optical CyberSecurity
#export TFS_COMPONENTS="${TFS_COMPONENTS} dbscanserving opticalattackmitigator opticalattackdetector opticalattackmanager"

# Uncomment to activate L3 CyberSecurity
#export TFS_COMPONENTS="${TFS_COMPONENTS} l3_attackmitigator l3_centralizedattackdetector"

# Uncomment to activate TE
#export TFS_COMPONENTS="${TFS_COMPONENTS} te"

# Uncomment to activate Forecaster
#export TFS_COMPONENTS="${TFS_COMPONENTS} forecaster"

# Uncomment to activate E2E Orchestrator
#export TFS_COMPONENTS="${TFS_COMPONENTS} e2e_orchestrator"

# Uncomment to activate VNT Manager
#export TFS_COMPONENTS="${TFS_COMPONENTS} vnt_manager"

# Uncomment to activate DLT and Interdomain
#export TFS_COMPONENTS="${TFS_COMPONENTS} interdomain dlt"
#if [[ "$TFS_COMPONENTS" == *"dlt"* ]]; then
#    export KEY_DIRECTORY_PATH="src/dlt/gateway/keys/priv_sk"
#    export CERT_DIRECTORY_PATH="src/dlt/gateway/keys/cert.pem"
#    export TLS_CERT_PATH="src/dlt/gateway/keys/ca.crt"
#fi

# Uncomment to activate QKD App
#   To manage QKD Apps, "service" requires "qkd_app" to be deployed
#   before "service", thus we "hack" the TFS_COMPONENTS environment variable prepending the
#   "qkd_app" only if "service" is already in TFS_COMPONENTS, and re-export it.
#if [[ "$TFS_COMPONENTS" == *"service"* ]]; then
#    BEFORE="${TFS_COMPONENTS% service*}"
#    AFTER="${TFS_COMPONENTS#* service}"
#    export TFS_COMPONENTS="${BEFORE} qkd_app service ${AFTER}"
#fi

# Uncomment to activate SIMAP Connector
export TFS_COMPONENTS="${TFS_COMPONENTS} simap_connector"

# Uncomment to activate Load Generator
#export TFS_COMPONENTS="${TFS_COMPONENTS} load_generator"


# Set the tag you want to use for your images.
export TFS_IMAGE_TAG="dev"

# Set the name of the Kubernetes namespace to deploy TFS to.
export TFS_K8S_NAMESPACE="tfs"

# Set additional manifest files to be applied after the deployment
export TFS_EXTRA_MANIFESTS="manifests/nginx_ingress_http.yaml"

# Uncomment to monitor performance of components
#export TFS_EXTRA_MANIFESTS="${TFS_EXTRA_MANIFESTS} manifests/servicemonitors.yaml"

# Uncomment when deploying Optical CyberSecurity
#export TFS_EXTRA_MANIFESTS="${TFS_EXTRA_MANIFESTS} manifests/cachingservice.yaml"

# Set the new Grafana admin password
export TFS_GRAFANA_PASSWORD="admin123+"

# Disable skip-build flag to rebuild the Docker images.
export TFS_SKIP_BUILD=""


# ----- CockroachDB ------------------------------------------------------------

# Set the namespace where CockroackDB will be deployed.
export CRDB_NAMESPACE="crdb"

# Set the external port CockroackDB Postgre SQL interface will be exposed to.
export CRDB_EXT_PORT_SQL="26257"

# Set the external port CockroackDB HTTP Mgmt GUI interface will be exposed to.
export CRDB_EXT_PORT_HTTP="8081"

# Set the database username to be used by Context.
export CRDB_USERNAME="tfs"

# Set the database user's password to be used by Context.
export CRDB_PASSWORD="tfs123"

# Set CockroachDB installation mode to 'single'. This option is convenient for development and testing.
# See ./deploy/all.sh or ./deploy/crdb.sh for additional details
export CRDB_DEPLOY_MODE="single"

# Disable flag for dropping database, if it exists.
export CRDB_DROP_DATABASE_IF_EXISTS="YES"

# Disable flag for re-deploying CockroachDB from scratch.
export CRDB_REDEPLOY=""


# ----- NATS -------------------------------------------------------------------

# Set the namespace where NATS will be deployed.
export NATS_NAMESPACE="nats"

# Set the external port NATS Client interface will be exposed to.
export NATS_EXT_PORT_CLIENT="4222"

# Set the external port NATS HTTP Mgmt GUI interface will be exposed to.
export NATS_EXT_PORT_HTTP="8222"

# Set NATS installation mode to 'single'. This option is convenient for development and testing.
# See ./deploy/all.sh or ./deploy/nats.sh for additional details
export NATS_DEPLOY_MODE="single"

# Disable flag for re-deploying NATS from scratch.
export NATS_REDEPLOY=""


# ----- Apache Kafka -----------------------------------------------------------

# Set the namespace where Apache Kafka will be deployed.
export KFK_NAMESPACE="kafka"

# Set the port Apache Kafka server will be exposed to.
export KFK_EXT_PORT_CLIENT="9092"

# Set Kafka installation mode to 'single'. This option is convenient for development and testing.
# See ./deploy/all.sh or ./deploy/kafka.sh for additional details
export KFK_DEPLOY_MODE="single"

# Disable flag for re-deploying Kafka from scratch.
export KFK_REDEPLOY=""


# ----- QuestDB ----------------------------------------------------------------

# Set the namespace where QuestDB will be deployed.
export QDB_NAMESPACE="qdb"

# Set the external port QuestDB Postgre SQL interface will be exposed to.
export QDB_EXT_PORT_SQL="8812"

# Set the external port QuestDB Influx Line Protocol interface will be exposed to.
export QDB_EXT_PORT_ILP="9009"

# Set the external port QuestDB HTTP Mgmt GUI interface will be exposed to.
export QDB_EXT_PORT_HTTP="9000"

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


# ----- K8s Observability ------------------------------------------------------

# Set the external port Prometheus Mgmt HTTP GUI interface will be exposed to.
export PROM_EXT_PORT_HTTP="9090"

# Set the external port Grafana HTTP Dashboards will be exposed to.
export GRAF_EXT_PORT_HTTP="3000"
