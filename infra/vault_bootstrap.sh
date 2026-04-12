#!/bin/bash
# SOP-VAULT: Stage I (Secret Management)
# Reference: SOP_VAULT.md
# Purpose: Sync external secrets to the Sovereign GKE cluster.

set -e

# Configuration
PROJECT_ID="cogctl-gke-v01"
NAMESPACE="default"

log() { echo "[$(date +%Y-%m-%dT%H:%M:%S%z)] $1"; }

log "STAGE I: FETCHING GITLAB PAT FROM SECRET MANAGER..."
GITLAB_PAT=$(/home/parallels/google-cloud-sdk/bin/gcloud secrets versions access latest --secret="ETSI_GITLAB_PAT" --project=$PROJECT_ID)

log "STAGE II: CREATING K8S REGISTRY SECRET [tfs-gitlab-auth]..."
# Note: This is used for pulling images from Artifact Registry / GitLab if needed.
# For GKE -> Artifact Registry, IAM is preferred, but for GitLab/etc PAT is needed.
kubectl create secret generic tfs-gitlab-auth \
    --from-literal=token="$GITLAB_PAT" \
    --dry-run=client -o yaml | kubectl apply -f -

log "STAGE III: GENERATING HIGH-ENTROPY INFRASTRUCTURE SECRETS..."
DB_PASS=$(openssl rand -base64 32)
KC_ADMIN_PASS=$(openssl rand -base64 32)

log "STAGE IV: CREATING K8S INFRASTRUCTURE SECRETS..."
kubectl create secret generic tfs-database-creds \
    --from-literal=password="$DB_PASS" \
    --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic tfs-keycloak-creds \
    --from-literal=admin-password="$KC_ADMIN_PASS" \
    --dry-run=client -o yaml | kubectl apply -f -

log "MISSION SUCCESS: SOP-VAULT Stage I Complete."
echo "--------------------------------------------------"
echo "Database Password: [SECURED IN K8S]"
echo "Keycloak Admin Password: [SECURED IN K8S]"
