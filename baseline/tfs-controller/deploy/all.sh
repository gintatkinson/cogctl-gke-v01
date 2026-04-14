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


########################################################################################################################
# Read deployment settings
########################################################################################################################


# ----- TeraFlowSDN ------------------------------------------------------------

# If not already set, set the URL of the Docker registry where the images will be uploaded to.
# By default, assume internal MicroK8s registry is used.
export TFS_REGISTRY_IMAGES=${TFS_REGISTRY_IMAGES:-"http://localhost:32000/tfs/"}

# If not already set, set the list of components, separated by spaces, you want to build images for, and deploy.
# By default, only basic components are deployed
export TFS_COMPONENTS=${TFS_COMPONENTS:-"context device pathcomp service slice nbi webui load_generator"}

# Uncomment to activate Monitoring (old)
#export TFS_COMPONENTS="${TFS_COMPONENTS} monitoring"

# Uncomment to activate Monitoring Framework (new)
#export TFS_COMPONENTS="${TFS_COMPONENTS} kpi_manager kpi_value_writer kpi_value_api telemetry analytics"

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

# Uncomment to activate Pluggables Component
#export TFS_COMPONENTS="${TFS_COMPONENTS} pluggables"

# If not already set, set the tag you want to use for your images.
export TFS_IMAGE_TAG=${TFS_IMAGE_TAG:-"dev"}

# If not already set, set the name of the Kubernetes namespace to deploy TFS to.
export TFS_K8S_NAMESPACE=${TFS_K8S_NAMESPACE:-"tfs"}

# If not already set, set additional manifest files to be applied after the deployment
export TFS_EXTRA_MANIFESTS=${TFS_EXTRA_MANIFESTS:-""}

# If not already set, set the new Grafana admin password
export TFS_GRAFANA_PASSWORD=${TFS_GRAFANA_PASSWORD:-"admin123+"}

# If not already set, disable skip-build flag to rebuild the Docker images.
# If TFS_SKIP_BUILD is "YES", the containers are not rebuilt-retagged-repushed and existing ones are used.
export TFS_SKIP_BUILD=${TFS_SKIP_BUILD:-""}


# ----- CockroachDB ------------------------------------------------------------

# If not already set, set the namespace where CockroackDB will be deployed.
export CRDB_NAMESPACE=${CRDB_NAMESPACE:-"crdb"}

# If not already set, set the external port CockroackDB Postgre SQL interface will be exposed to.
export CRDB_EXT_PORT_SQL=${CRDB_EXT_PORT_SQL:-"26257"}

# If not already set, set the external port CockroackDB HTTP Mgmt GUI interface will be exposed to.
export CRDB_EXT_PORT_HTTP=${CRDB_EXT_PORT_HTTP:-"8081"}

# If not already set, set the database username to be used by Context.
export CRDB_USERNAME=${CRDB_USERNAME:-"tfs"}

# If not already set, set the database user's password to be used by Context.
export CRDB_PASSWORD=${CRDB_PASSWORD:-"tfs123"}

# If not already set, set CockroachDB installation mode. Accepted values are: 'single' and 'cluster'.
# - If CRDB_DEPLOY_MODE is "single", CockroachDB is deployed in single node mode. It is convenient for
#   development and testing purposes and should fit in a VM. IT SHOULD NOT BE USED IN PRODUCTION ENVIRONMENTS.
# - If CRDB_DEPLOY_MODE is "cluster", CockroachDB is deployed in cluster mode, and an entire CockroachDB cluster
#   with 3 replicas and version v22.2 (set by default) will be deployed. It is convenient for production and
#   provides scalability features. If you are deploying for production, also read the following link providing
#   details on deploying CockroachDB for production environments:
#   Ref: https://www.cockroachlabs.com/docs/stable/recommended-production-settings.html
export CRDB_DEPLOY_MODE=${CRDB_DEPLOY_MODE:-"single"}

# If not already set, disable flag for dropping database, if it exists.
# WARNING: ACTIVATING THIS FLAG IMPLIES LOOSING THE DATABASE INFORMATION!
# If CRDB_DROP_DATABASE_IF_EXISTS is "YES", the databases starting with "tfs_" will be dropped while
# checking/deploying CockroachDB.
export CRDB_DROP_DATABASE_IF_EXISTS=${CRDB_DROP_DATABASE_IF_EXISTS:-""}

# If not already set, disable flag for re-deploying CockroachDB from scratch.
# WARNING: ACTIVATING THIS FLAG IMPLIES LOOSING THE DATABASE INFORMATION!
# WARNING: THE REDEPLOY MIGHT TAKE FEW MINUTES TO COMPLETE GRACEFULLY IN CLUSTER MODE
# If CRDB_REDEPLOY is "YES", the database will be dropped while checking/deploying CockroachDB.
export CRDB_REDEPLOY=${CRDB_REDEPLOY:-""}


# ----- NATS -------------------------------------------------------------------

# If not already set, set the namespace where NATS will be deployed.
export NATS_NAMESPACE=${NATS_NAMESPACE:-"nats"}

# If not already set, set the external port NATS Client interface will be exposed to.
export NATS_EXT_PORT_CLIENT=${NATS_EXT_PORT_CLIENT:-"4222"}

# If not already set, set the external port NATS HTTP Mgmt GUI interface will be exposed to.
export NATS_EXT_PORT_HTTP=${NATS_EXT_PORT_HTTP:-"8222"}

# If not already set, set NATS installation mode. Accepted values are: 'single' and 'cluster'.
# - If NATS_DEPLOY_MODE is "single", NATS is deployed in single node mode. It is convenient for
#   development and testing purposes and should fit in a VM. IT SHOULD NOT BE USED IN PRODUCTION ENVIRONMENTS.
# - If NATS_DEPLOY_MODE is "cluster", NATS is deployed in cluster mode, and an entire NATS cluster
#   with 3 replicas (set by default) will be deployed. It is convenient for production and
#   provides scalability features.
export NATS_DEPLOY_MODE=${NATS_DEPLOY_MODE:-"single"}

# If not already set, disable flag for re-deploying NATS from scratch.
# WARNING: ACTIVATING THIS FLAG IMPLIES LOOSING THE MESSAGE BROKER INFORMATION!
# If NATS_REDEPLOY is "YES", the message broker will be dropped while checking/deploying NATS.
export NATS_REDEPLOY=${NATS_REDEPLOY:-""}


# ----- Apache Kafka -----------------------------------------------------------

# If not already set, set the namespace where Kafka will be deployed.
export KFK_NAMESPACE=${KFK_NAMESPACE:-"kafka"}

# If not already set, set the external port Kafka Client interface will be exposed to.
export KFK_EXT_PORT_CLIENT=${KFK_EXT_PORT_CLIENT:-"9092"}

# If not already set, set Kafka installation mode. Accepted values are: 'single'.
# - If KFK_DEPLOY_MODE is "single", Kafka is deployed in single node mode. It is convenient for
#   development and testing purposes and should fit in a VM. IT SHOULD NOT BE USED IN PRODUCTION ENVIRONMENTS.
# NOTE: Production mode is still not supported. Will be provided in the future.
export KFK_DEPLOY_MODE=${KFK_DEPLOY_MODE:-"single"}

# If not already set, disable flag for re-deploying Kafka from scratch.
# WARNING: ACTIVATING THIS FLAG IMPLIES LOOSING THE MESSAGE BROKER INFORMATION!
# If KFK_REDEPLOY is "YES", the message broker will be dropped while checking/deploying Kafka.
export KFK_REDEPLOY=${KFK_REDEPLOY:-""}


# ----- QuestDB ----------------------------------------------------------------

# If not already set, set the namespace where QuestDB will be deployed.
export QDB_NAMESPACE=${QDB_NAMESPACE:-"qdb"}

# If not already set, set the external port QuestDB Postgre SQL interface will be exposed to.
export QDB_EXT_PORT_SQL=${QDB_EXT_PORT_SQL:-"8812"}

# If not already set, set the external port QuestDB Influx Line Protocol interface will be exposed to.
export QDB_EXT_PORT_ILP=${QDB_EXT_PORT_ILP:-"9009"}

# If not already set, set the external port QuestDB HTTP Mgmt GUI interface will be exposed to.
export QDB_EXT_PORT_HTTP=${QDB_EXT_PORT_HTTP:-"9000"}

# If not already set, set the database username to be used for QuestDB.
export QDB_USERNAME=${QDB_USERNAME:-"admin"}

# If not already set, set the database user's password to be used for QuestDB.
export QDB_PASSWORD=${QDB_PASSWORD:-"quest"}

# If not already set, set the table name to be used by Monitoring for KPIs.
export QDB_TABLE_MONITORING_KPIS=${QDB_TABLE_MONITORING_KPIS:-"tfs_monitoring_kpis"}

# If not already set, set the table name to be used by Slice for plotting groups.
export QDB_TABLE_SLICE_GROUPS=${QDB_TABLE_SLICE_GROUPS:-"tfs_slice_groups"}

# If not already set, disable flag for dropping tables if they exist.
# WARNING: ACTIVATING THIS FLAG IMPLIES LOOSING THE TABLE INFORMATION!
# If QDB_DROP_TABLES_IF_EXIST is "YES", the tables pointed by variables
# QDB_TABLE_MONITORING_KPIS and QDB_TABLE_SLICE_GROUPS will be dropped while
# checking/deploying QuestDB.
export QDB_DROP_TABLES_IF_EXIST=${QDB_DROP_TABLES_IF_EXIST:-""}

# If not already set, disable flag for re-deploying QuestDB from scratch.
# WARNING: ACTIVATING THIS FLAG IMPLIES LOOSING THE DATABASE INFORMATION!
# If QDB_REDEPLOY is "YES", the database will be dropped while checking/deploying QuestDB.
export QDB_REDEPLOY=${QDB_REDEPLOY:-""}


# ----- Time Series Storage - Prometheus / Grafana Mimir -----------------------

# If not already set, set Time Series Storage installation mode. Accepted values are:
# 'single' and 'cluster'.
# - If TSDB_DEPLOY_MODE is "single", Time Series Storage is deployed in single node
#   mode and features a basic Prometheus instance. It is convenient for development and
#   testing purposes and should fit in a VM.
#   IT SHOULD NOT BE USED IN PRODUCTION ENVIRONMENTS.
# - If TSDB_DEPLOY_MODE is "cluster", Time Series Storage is deployed in cluster mode
#   and a Grafana Mimir database in cluster mode will be deployed. It is convenient for
#   production and provides scalability features. If you are deploying for production,
#   also read the following link providing details on deploying Grafana Mimir for
#   production environments:
#   Ref: https://grafana.com/docs/mimir/latest/manage/run-production-environment/
export TSDB_DEPLOY_MODE=${TSDB_DEPLOY_MODE:-"single"}


# ----- K8s Observability ------------------------------------------------------

# If not already set, set the external port Prometheus Mgmt HTTP GUI interface will be exposed to.
export PROM_EXT_PORT_HTTP=${PROM_EXT_PORT_HTTP:-"9090"}

# If not already set, set the external port Grafana HTTP Dashboards will be exposed to.
export GRAF_EXT_PORT_HTTP=${GRAF_EXT_PORT_HTTP:-"3000"}


########################################################################################################################
# Automated steps start here
########################################################################################################################

# Deploy CockroachDB
./deploy/crdb.sh

# Deploy NATS
./deploy/nats.sh

# Deploy QuestDB
./deploy/qdb.sh

# Deploy Apache Kafka
./deploy/kafka.sh

#Deploy Monitoring (Prometheus Gateway, Prometheus)
# ./deploy/monitoring.sh

# Expose Dashboard
./deploy/expose_dashboard.sh

# Deploy TeraFlowSDN
./deploy/tfs.sh

# Show deploy summary
./deploy/show.sh

echo "Done!"
