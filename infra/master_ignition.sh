#!/bin/bash
set -e
export PATH="/home/parallels/google-cloud-sdk/bin:$PATH"
export PROJECT_ID="cogctl-gke-v01"
export REGION="us-central1"

log() { echo "[MASTER_IGNITION] $(date +%Y-%m-%dT%H:%M:%S%z) $1"; }

log "PHASE 1: NUCLEAR PURGE..."
bash infra/foundation_purge.sh

log "PHASE 2: FOUNDATION IGNITION..."
bash infra/genesis.sh

CLUSTER_NAME=$(cat /tmp/last_cluster_name.txt)
log "PHASE 3: LINKING CLUSTER [$CLUSTER_NAME]..."
gcloud container clusters get-credentials "$CLUSTER_NAME" --region "$REGION" --project "$PROJECT_ID"

log "PHASE 4: SECRET BOOTSTRAP..."
sleep 60
export CLUSTER_NAME=$CLUSTER_NAME
bash infra/vault_bootstrap.sh

log "PHASE 5: FINAL DEPLOYMENT..."
# Parameterize the build file
sed -i "s/\$CLUSTER_NAME/$CLUSTER_NAME/g" infra/cloudbuild_final.yaml
gcloud builds submit --config infra/cloudbuild_final.yaml --project "$PROJECT_ID"

log "=== GLOBAL IGNITION COMPLETE ==="
