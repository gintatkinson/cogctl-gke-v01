#!/bin/bash
echo "[PURGE] Hunting for orphaned Sovereign disks..."
ORPHAN_DISKS=$(gcloud compute disks list --filter="name ~ gke-sovereign-genesis AND users ~ none" --format="value(name)")

if [ -n "$ORPHAN_DISKS" ]; then
    echo "[PURGE] Found orphans: $ORPHAN_DISKS"
    for DISK in $ORPHAN_DISKS; do
        echo "[PURGE] Neutralizing $DISK..."
        gcloud compute disks delete "$DISK" --zone "us-central1-a" --quiet
    done
else
    echo "[PURGE] No orphaned disks found. Clean state verified."
fi
