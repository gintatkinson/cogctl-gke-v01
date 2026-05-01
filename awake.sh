#!/bin/bash
# Total Ignition Engine: Sovereign Genesis
# Rebuilds compute and deploys the full service stack.

ZONE="us-central1-a"
CLUSTER_NAME="sovereign-genesis"

echo "--- INITIATING TOTAL IGNITION (ZONE: $ZONE) ---"

# 1. Create the GKE Cluster
gcloud container clusters create $CLUSTER_NAME \
    --zone $ZONE \
    --num-nodes 3 \
    --machine-type n1-standard-4 \
    --quiet

# 2. Get Credentials
gcloud container clusters get-credentials $CLUSTER_NAME --zone $ZONE

# 3. Deploy Backbone (Databases & Messaging)
echo "Deploying backbone infrastructure..."
kubectl apply -f infra/manifests/backbone/

# 4. Wait for CRDs and Operators (Brief pause for stability)
sleep 10

# 5. Deploy Application Services
echo "Deploying application services..."
kubectl apply -f infra/manifests/services/
kubectl apply -f infra/gce_ingress.yaml

echo "[SUCCESS] Enclave is operational."
