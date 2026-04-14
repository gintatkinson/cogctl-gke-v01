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

set -euo pipefail


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


# -----------------------------------------------------------
# Global namespace for all deployments
# -----------------------------------------------------------
NAMESPACE="monitoring"
VALUES_FILE_PATH="manifests/monitoring"

# -----------------------------------------------------------
# Prometheus Configuration
# -----------------------------------------------------------
RELEASE_NAME_PROM="mon-prometheus"
CHART_REPO_NAME_PROM="prometheus-community"
CHART_REPO_URL_PROM="https://prometheus-community.github.io/helm-charts"
CHART_NAME_PROM="prometheus"
VALUES_FILE_PROM="$VALUES_FILE_PATH/prometheus_values.yaml"

# -----------------------------------------------------------
# Mimir Configuration
# -----------------------------------------------------------
RELEASE_NAME_MIMIR="mon-mimir"
CHART_REPO_NAME_MIMIR="grafana"
CHART_REPO_URL_MIMIR="https://grafana.github.io/helm-charts"
CHART_NAME_MIMIR="mimir-distributed"
VALUES_FILE_MIMIR="$VALUES_FILE_PATH/mimir_values.yaml"

# -----------------------------------------------------------
# Grafana Configuration
# -----------------------------------------------------------
# RELEASE_NAME_GRAFANA="mon-grafana"
# CHART_REPO_NAME_GRAFANA="grafana"
# CHART_REPO_URL_GRAFANA="https://grafana.github.io/helm-charts"
# CHART_NAME_GRAFANA="grafana"
# VALUES_FILE_GRAFANA="$VALUES_FILE_PATH/grafana_values.yaml"


# -----------------------------------------------------------
# Function to deploy or upgrade a Helm chart
# -----------------------------------------------------------
deploy_chart() {
  local release_name="$1"
  local chart_repo_name="$2"
  local chart_repo_url="$3"
  local chart_name="$4"
  local values_file="$5"
  local namespace="$6"

  echo ">>> Deploying [${release_name}] from repo [${chart_repo_name}]..."

  # Add or update the Helm repo
  echo "Adding/updating Helm repo: $chart_repo_name -> $chart_repo_url"
  helm repo add "$chart_repo_name" "$chart_repo_url" || true
  helm repo update

  # Create namespace if needed
  echo "Creating namespace '$namespace' if it doesn't exist..."
  kubectl get namespace "$namespace" >/dev/null 2>&1 || kubectl create namespace "$namespace"

  # Install or upgrade the chart
  if [ -n "$values_file" ] && [ -f "$values_file" ]; then
    echo "Installing/Upgrading $release_name using custom values from $values_file..."
    helm upgrade --install "$release_name" "$chart_repo_name/$chart_name" \
      --namespace "$namespace" \
      --values "$values_file"
  else
    echo "Installing/Upgrading $release_name with default chart values..."
    helm upgrade --install "$release_name" "$chart_repo_name/$chart_name" \
      --namespace "$namespace"
  fi

  echo "<<< Deployment initiated for [$release_name]."
  echo
}


# -----------------------------------------------------------
# Actual Deployments
# -----------------------------------------------------------

# 1) Deploy Prometheus
deploy_chart "$RELEASE_NAME_PROM" \
             "$CHART_REPO_NAME_PROM" \
             "$CHART_REPO_URL_PROM" \
             "$CHART_NAME_PROM" \
             "$VALUES_FILE_PROM" \
             "$NAMESPACE"

# Optionally wait for Prometheus server pod to become ready
kubectl rollout status deployment/"$RELEASE_NAME_PROM-server" -n "$NAMESPACE" || true


# 2) Deploy Mimir
if [ "$TSDB_DEPLOY_MODE" == "cluster" ]; then
    echo "Deploying Mimir in production mode."
    # You can add any production-specific configurations here if needed
    deploy_chart "$RELEASE_NAME_MIMIR" \
                "$CHART_REPO_NAME_MIMIR" \
                "$CHART_REPO_URL_MIMIR" \
                "$CHART_NAME_MIMIR" \
                "$VALUES_FILE_MIMIR" \
                "$NAMESPACE"

    # you can wait for the resource to be ready.
    kubectl rollout status statefulset/"$RELEASE_NAME_MIMIR-distributor" -n "$NAMESPACE" || true
fi


# 3) Deploy Grafana
# deploy_chart "$RELEASE_NAME_GRAFANA" \
#              "$CHART_REPO_NAME_GRAFANA" \
#              "$CHART_REPO_URL_GRAFANA" \
#              "$CHART_NAME_GRAFANA" \
#              "$VALUES_FILE_GRAFANA" \
#              "$NAMESPACE"

# kubectl rollout status deployment/"$RELEASE_NAME_GRAFANA" -n "$NAMESPACE" || true

# -----------------------------------------------------------
echo "All deployments completed!"

