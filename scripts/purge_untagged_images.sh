#!/bin/bash
# AGGRESSIVE PURGE (FINAL): Reclaim storage by iterating through packages
# AUTHORIZED: Directive REFAC_01
REPO="us-central1-docker.pkg.dev/cogctl-gke-v01/sovereign-tfs"

echo "=== SOVEREIGN REGISTRY PURGE (DEEP SCAN - VERSION FIX) ==="
echo "Target Repository: $REPO"

# Stage 1: Get all sub-packages (images) in the repository
PACKAGES=$(gcloud artifacts docker images list "$REPO" --format="value(package)" | uniq)

COUNT=0
for PACKAGE in $PACKAGES; do
    echo "[POD] Scanning package: $PACKAGE"
    # Stage 2: Identify untagged digests using the 'version' field
    DIGESTS=$(gcloud artifacts docker images list "$PACKAGE" --filter="-tags:*" --format="value(version)")
    
    for DIGEST in $DIGESTS; do
        if [ -n "$DIGEST" ]; then
            echo "  [$(date +%T)] Deleting orphan: $DIGEST"
            # Delete with full @digest identifier (the version field contains sha256:...)
            gcloud artifacts docker images delete "$PACKAGE@$DIGEST" --quiet --delete-tags
            
            # Rate-limiting
            sleep 1
            ((COUNT++))
        fi
    done
done

echo "=== PURGE COMPLETE ==="
echo "Total orphan manifests removed: $COUNT"
