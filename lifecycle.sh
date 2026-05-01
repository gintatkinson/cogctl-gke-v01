#!/bin/bash
set -e

COMMAND=$1
CLUSTER="sovereign-genesis"
ZONE="us-central1-a"

case $COMMAND in
  shutdown)
    echo "[SHUTDOWN] Initiating graceful termination of $CLUSTER..."
    gcloud container clusters delete "$CLUSTER" --zone "$ZONE" --quiet --async
    echo "[SHUTDOWN] Deletion requested. Billing will cease once Google completes the background task."
    ;;
  
  restart)
    echo "[RESTART] Ensuring clean slate..."
    if gcloud container clusters describe "$CLUSTER" --zone "$ZONE" >/dev/null 2>&1; then
        echo "[RESTART] Active cluster detected. Triggering deep purge first."
        gcloud container clusters delete "$CLUSTER" --zone "$ZONE" --quiet
    fi
    echo "[RESTART] Provisioning fresh infrastructure..."
    gcloud container clusters create "$CLUSTER" --zone "$ZONE" \
        --machine-type n1-standard-4 --num-nodes 3 --quiet
    
    echo "[RESTART] Authenticating..."
    gcloud container clusters get-credentials "$CLUSTER" --zone "$ZONE"
    
    echo "[RESTART] Inducing 11 Core Services..."
    gcloud builds submit --config infra/cloudbuild_graduation_final.yaml --substitutions=_TAG="rc13-verified" .
    ;;

  *)
    echo "Usage: ./lifecycle.sh {shutdown|restart}"
    exit 1
    ;;
esac
