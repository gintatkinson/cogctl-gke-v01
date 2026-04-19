#!/bin/bash
# SOP-VAULT: Stage I (Secret Management) - REMOTE-NATIVE
# Purpose: Delegate secret orchestration to Cloud Build to ensure Viewport Purity.

set -e

PROJECT_ID="cogctl-gke-v01"
CLUSTER_NAME="${CLUSTER_NAME:-$CLUSTER_NAME}"
REGION="${REGION:-us-central1}"

log() { echo "[$(date +%Y-%m-%dT%H:%M:%S%z)] $1"; }

log "STAGE I: DELEGATING VAULT ORCHESTRATION TO CLOUD BUILD [Cluster: $CLUSTER_NAME]..."

/home/parallels/google-cloud-sdk/bin/gcloud builds submit . \
    --config infra/cloudbuild_vault.yaml \
    --substitutions=_CLUSTER_NAME=$CLUSTER_NAME,_REGION=$REGION \
    --project $PROJECT_ID

log "MISSION SUCCESS: Vault orchestration delegated and completed."
