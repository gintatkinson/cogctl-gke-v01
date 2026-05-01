#!/bin/bash
# Total Purge Engine: Sovereign Genesis
# Targets compute and persistent storage for Zero-Debt Hibernation.

ZONE="us-central1-a"
CLUSTER_NAME="sovereign-genesis"

echo "--- INITIATING TOTAL PURGE (ZONE: $ZONE) ---"

# 1. Delete Cluster (Wait for completion to identify orphaned disks)
gcloud container clusters delete $CLUSTER_NAME --zone $ZONE --quiet

# 2. Purge Orphaned Persistent Disks (PVCs)
echo "Searching for orphaned PVC disks..."
PVC_DISKS=$(gcloud compute disks list --filter="zone:$ZONE AND name~pvc-.*" --format="value(name)")

if [ -n "$PVC_DISKS" ]; then
    echo "Deleting disks: $PVC_DISKS"
    gcloud compute disks delete $PVC_DISKS --zone $ZONE --quiet
else
    echo "No orphaned disks found."
fi

echo "[SUCCESS] Enclave fully decommissioned. Zero-Debt achieved."
