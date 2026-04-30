#!/bin/bash
# --- Sovereign Genesis: Full Deconstruction ---
CLUSTER_NAME="sovereign-genesis"
ZONE="us-central1-a"

echo "[1/2] Terminating Cluster: $CLUSTER_NAME..."
gcloud container clusters delete $CLUSTER_NAME --zone $ZONE --quiet

echo "[2/2] Vaporizing Orphaned Disks..."
DISK_LIST=$(gcloud compute disks list --filter="zone:($ZONE)" --format="value(name)")
if [ -n "$DISK_LIST" ]; then
  gcloud compute disks delete $DISK_LIST --zone $ZONE --quiet
else
  echo "No orphaned disks found."
fi

echo "--- SHUTDOWN COMPLETE: Environment Zeroed ---"
