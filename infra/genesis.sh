#!/bin/bash
set -e

# SOVEREIGN GENESIS ENGINE v1.0
# Reference: SUCCESSION_LOG_BLACKBOX.md -> BB-011, BB-012
# Purpose: Atomic, range-aware, and isolated GKE bootstrap.

export PATH="/home/parallels/google-cloud-sdk/bin:$PATH"
export PROJECT_ID="cogctl-gke-v01"
export REGION="us-central1"
export VPC_NAME="sovereign-vpc"
export SUBNET_NAME="sovereign-subnet-us-central"
export CLUSTER_NAME="sovereign-genesis"

log() { echo "[$(date +%Y-%m-%dT%H:%M:%S%z)] $1"; }

log "Phase 1: Validating Project Environment..."
gcloud config set project $PROJECT_ID

log "Phase 2: Enabling Sovereign APIs..."
gcloud services enable \
    container.googleapis.com \
    compute.googleapis.com \
    servicenetworking.googleapis.com \
    artifactregistry.googleapis.com --project $PROJECT_ID

log "Phase 3: Building Isolated Foundation (VPC)..."
gcloud compute networks create $VPC_NAME \
    --subnet-mode=custom \
    --project=$PROJECT_ID

log "Phase 4: Establishing Subnet Fabric (Range-Aware)..."
gcloud compute networks subnets create $SUBNET_NAME \
    --network=$VPC_NAME \
    --range=10.10.0.0/24 \
    --secondary-range=gke-pods=10.100.0.0/16,gke-services=10.101.0.0/20 \
    --region=$REGION \
    --enable-private-ip-google-access \
    --project=$PROJECT_ID

log "Phase 5: Establishing Service Bridge (Peering)..."
gcloud compute addresses create google-managed-services-$VPC_NAME \
    --global \
    --purpose=VPC_PEERING \
    --prefix-length=24 \
    --network=$VPC_NAME \
    --project=$PROJECT_ID

gcloud services vpc-peerings connect \
    --service=servicenetworking.googleapis.com \
    --ranges=google-managed-services-$VPC_NAME \
    --network=$VPC_NAME \
    --project=$PROJECT_ID

log "Phase 6: Establishing Security Perimeter..."
gcloud compute firewall-rules create sovereign-allow-internal \
    --network=$VPC_NAME \
    --allow=tcp,udp,icmp \
    --source-ranges=10.10.0.0/16 \
    --project=$PROJECT_ID

log "Phase 7: IGNITION - Creating Sovereign GKE Cluster..."
gcloud container clusters create-auto $CLUSTER_NAME \
    --region $REGION \
    --network $VPC_NAME \
    --subnetwork $SUBNET_NAME \
    --cluster-secondary-range-name gke-pods \
    --services-secondary-range-name gke-services \
    --project $PROJECT_ID

log "MISSION SUCCESS: Sovereign Genesis Complete."
