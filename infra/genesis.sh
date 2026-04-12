#!/bin/bash
set -e

# SOVEREIGN GENESIS ENGINE v2.0 (IMMUTABLE)
# Reference: SOVEREIGN_SYSTEM_DESIGN.md
# Purpose: Dynamic, NAT-provisioned, and high-entropy GKE bootstrap.

export PATH="/home/parallels/google-cloud-sdk/bin:$PATH"
export PROJECT_ID="cogctl-gke-v01"
export REGION="us-central1"

# IDENTIFIER GENERATION (The "Vacuum" Key)
export ID=$(date +%s)
export VPC_NAME="sovereign-vpc-$ID"
export SUBNET_NAME="sovereign-subnet-$ID"
export CLUSTER_NAME="sovereign-genesis-$ID"
export ROUTER_NAME="sovereign-router-$ID"
export NAT_NAME="sovereign-nat-$ID"

log() { echo "[$(date +%Y-%m-%dT%H:%M:%S%z)] $1"; }

log "STAGE 1: VALIDATING IDENTITY [$ID]..."
gcloud config set project $PROJECT_ID

log "STAGE 2: ENABLING SOVEREIGN APIs..."
gcloud services enable \
    container.googleapis.com \
    compute.googleapis.com \
    servicenetworking.googleapis.com \
    artifactregistry.googleapis.com --project $PROJECT_ID

log "STAGE 3: BUILDING IMMUTABLE VPC [$VPC_NAME]..."
gcloud compute networks create $VPC_NAME \
    --subnet-mode=custom \
    --project=$PROJECT_ID

log "STAGE 4: BUILDING SUBNET FABRIC (RANGE-AWARE)..."
gcloud compute networks subnets create $SUBNET_NAME \
    --network=$VPC_NAME \
    --range=10.10.0.0/24 \
    --secondary-range=gke-pods=10.100.0.0/16,gke-services=10.101.0.0/20 \
    --region=$REGION \
    --enable-private-ip-google-access \
    --project=$PROJECT_ID

log "STAGE 5: PROVISIONING SOVEREIGN EGRESS (CLOUD NAT)..."
gcloud compute routers create $ROUTER_NAME \
    --network=$VPC_NAME \
    --region=$REGION \
    --project=$PROJECT_ID

gcloud compute routers nats create $NAT_NAME \
    --router=$ROUTER_NAME \
    --region=$REGION \
    --auto-allocate-nat-external-ips \
    --nat-all-subnet-ip-ranges \
    --project=$PROJECT_ID

log "STAGE 6: ESTABLISHING SERVICE BRIDGE (PEERING)..."
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

log "STAGE 7: ESTABLISHING SECURITY PERIMETER..."
gcloud compute firewall-rules create sovereign-allow-internal-$ID \
    --network=$VPC_NAME \
    --allow=tcp,udp,icmp \
    --source-ranges=10.10.0.0/16 \
    --project=$PROJECT_ID

log "STAGE 8: IGNITION - CREATING PRIVATE SOVEREIGN CLUSTER..."
gcloud container clusters create-auto $CLUSTER_NAME \
    --region $REGION \
    --network $VPC_NAME \
    --subnetwork $SUBNET_NAME \
    --enable-private-nodes \
    --master-ipv4-cidr 172.16.0.0/28 \
    --cluster-secondary-range-name gke-pods \
    --services-secondary-range-name gke-services \
    --project $PROJECT_ID

log "MISSION SUCCESS: Sovereign Genesis [$ID] is RUNNING."
