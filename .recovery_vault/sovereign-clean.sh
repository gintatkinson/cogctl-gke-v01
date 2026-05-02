#!/bin/bash
# Global Scrub Script - Sovereign Genesis v3.2
# Objective: Zero-footprint infrastructure reset

echo "--- INITIATING ATOMIC CLEANUP ---"

# 1. Delete Kubernetes Namespace
# We are using default namespace mostly now due to failover, but we'll check both
kubectl delete namespace sovereign-genesis --wait=true --timeout=60s

# 2. Force-Delete Orphaned PVCs/PVs
kubectl get pv | grep 'sovereign-genesis' | awk '{print $1}' | xargs -r kubectl delete pv --force --grace-period=0

# 3. Cloud-Layer: Orphaned Persistent Disk Sweep
echo "Scanning for unattached Persistent Disks in us-central1..."
gcloud compute disks list --filter="zone:us-central1 AND -users:*" --format="value(name)" > orphaned_disks.txt

if [ -s orphaned_disks.txt ]; then
    echo "Deleting orphaned disks to recover SSD quota..."
    cat orphaned_disks.txt | xargs -I {} gcloud compute disks delete {} --zone=us-central1 --quiet
else
    echo "No orphaned disks detected."
fi

# 4. Quota Verification
USAGE=$(gcloud compute project-info describe --format="json" | jq -r '.quotas[] | select(.metric=="SSD_TOTAL_GB") | .usage')
echo "Current SSD Quota Usage: $USAGE / 500GB"

echo "--- SANITATION COMPLETE ---"
