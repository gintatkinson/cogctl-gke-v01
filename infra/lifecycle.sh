#!/bin/bash
set -e

# THE SOVEREIGN LIFECYCLE MANAGER
# Operations for project: cogctl-gke-v01

PROJECT_ID="cogctl-gke-v01"
CLUSTER_NAME="sovereign-genesis"
REGION="us-central1"

log() {
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] $1"
}

case "$1" in
    up)
        log "Summoning GKE Genesis..."
        ./infra/bootstrap.sh
        ;;
    down)
        log "Dismissing Sovereign Environment (Scale to Zero)..."
        # Since this is a dev/test environment, we delete the cluster to avoid the management fee.
        # Re-creation via 'up' is the standard recovery path.
        gcloud container clusters delete ${CLUSTER_NAME} --region ${REGION} --quiet --project ${PROJECT_ID}
        log "Environment dismissed. No management fees will be incurred."
        ;;
    status)
        log "Querying Sovereign Status..."
        gcloud container clusters list --project ${PROJECT_ID}
        ;;
    *)
        echo "Usage: $0 {up|down|status}"
        exit 1
        ;;
esac
