#!/bin/bash
set -e

# THE SOVEREIGN GENESIS BOOTSTRAP
# Project: cogctl-gke-v01

PROJECT_ID="cogctl-gke-v01"
CLUSTER_NAME="sovereign-genesis"
REGION="us-central1"
ZONE="us-central1-a"

log() {
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] $1"
}

log "Initiating Sovereign Genesis Protocol..."

# 1. Enable Required APIs
log "Phase 1: Enabling Google Cloud APIs..."
gcloud services enable \
    container.googleapis.com \
    secretmanager.googleapis.com \
    compute.googleapis.com \
    logging.googleapis.com \
    monitoring.googleapis.com \
    --project ${PROJECT_ID}

# 2. Infrastructure Creation
log "Phase 2: Creating Sovereign GKE Cluster..."
# Using GKE Autopilot for Phase 1 to ensure production-grade security defaults (Shielded Nodes, Workload Identity, etc.)
gcloud container clusters create-auto ${CLUSTER_NAME} \
    --project ${PROJECT_ID} \
    --region ${REGION} \
    --release-channel "regular"

# 3. Connectivity Hand-off
log "Phase 3: Authenticating kubectl..."
gcloud container clusters get-credentials ${CLUSTER_NAME} \
    --region ${REGION} \
    --project ${PROJECT_ID}

log "Genesis Bootstrap Complete. Cluster is ready for Sovereign Directives integration."
