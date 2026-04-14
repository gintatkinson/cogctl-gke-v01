#!/bin/bash
# foundation_purge.sh - The Sovereign Purge (Hardened Discovery)
# Purges any and all 'sovereign-*' resources from the GCP project.
# Includes deletion of Managed Service peerings and addresses.

set -e

export PATH="/home/parallels/google-cloud-sdk/bin:$PATH"
export PROJECT_ID="cogctl-gke-v01"
export REGION="us-central1"

log() { echo "[PURGE] $1"; }

log "SEARCHING FOR SOVEREIGN CLUSTERS..."
CLUSTERS=$(gcloud container clusters list --project $PROJECT_ID --format="value(name)" --filter="name ~ sovereign-")

for CLUSTER in $CLUSTERS; do
    log "Deleting cluster $CLUSTER..."
    gcloud container clusters delete $CLUSTER --region $REGION --async --quiet --project $PROJECT_ID
done

if [ -n "$CLUSTERS" ]; then
    log "Waiting for cluster deletion to complete..."
    while gcloud container clusters list --project $PROJECT_ID --filter="name ~ sovereign-" --format="value(name)" | grep -q 'sovereign-'; do
        log "Clusters still exist... waiting 30s..."
        sleep 30
    done
fi

log "Clusters are GONE."

log "Deleting Sovereign Routers..."
ROUTERS=$(gcloud compute routers list --project $PROJECT_ID --format="value(name)" --filter="name ~ sovereign-")
for ROUTER in $ROUTERS; do
    gcloud compute routers delete $ROUTER --region $REGION --quiet --project $PROJECT_ID
done

log "Deleting Sovereign Firewalls..."
FIREWALLS=$(gcloud compute firewall-rules list --project $PROJECT_ID --format="value(name)" --filter="name ~ sovereign-")
for FW in $FIREWALLS; do
    gcloud compute firewall-rules delete $FW --quiet --project $PROJECT_ID
done

log "Cleaning up Sovereign VPCs and Managed Dependencies..."
VPCS=$(gcloud compute networks list --project $PROJECT_ID --format="value(name)" --filter="name ~ sovereign-")
for VPC in $VPCS; do
    log "Processing VPC $VPC..."
    
    # 1. Remove Peerings (e.g., Service Networking)
    PEERINGS=$(gcloud compute networks describe $VPC --project $PROJECT_ID --format="value(peerings[].name)")
    for PEERING in $PEERINGS; do
        log "Deleting peering $PEERING from $VPC..."
        gcloud compute networks peerings delete $PEERING --network=$VPC --project $PROJECT_ID --quiet || true
    done

    # 2. Cleanup Subnets
    SUBNETS=$(gcloud compute networks subnets list --network $VPC --project $PROJECT_ID --format="value(name)")
    for SUBNET in $SUBNETS; do
        log "Deleting subnet $SUBNET..."
        gcloud compute networks subnets delete $SUBNET --region $REGION --quiet --project $PROJECT_ID 2>/dev/null || true
    done

    # 3. Release Managed Addresses
    log "Searching for managed addresses tied to $VPC..."
    ADDRESSES=$(gcloud compute addresses list --project $PROJECT_ID --filter="network ~ $VPC" --format="value(name)")
    for ADDR in $ADDRESSES; do
        log "Deleting address $ADDR..."
        gcloud compute addresses delete $ADDR --global --quiet --project $PROJECT_ID 2>/dev/null || true
    done

    # 4. Final VPC Deletion
    log "Deleting VPC $VPC..."
    gcloud compute networks delete $VPC --quiet --project $PROJECT_ID || log "WARNING: VPC deletion retry may be needed."
done

log "TOTAL PURGE COMPLETE (Hardened Discovery)."
