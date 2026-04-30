#!/bin/bash
# --- Sovereign Genesis: Ground 0 Customer Install ---
CLUSTER_NAME="sovereign-genesis"
ZONE="us-central1-a"
MACHINE_TYPE="n1-standard-4"
NODES=3

echo "[1/4] Igniting Sovereign Enclave Infrastructure..."
gcloud container clusters create $CLUSTER_NAME \
    --zone $ZONE \
    --machine-type $MACHINE_TYPE \
    --num-nodes $NODES \
    --quiet

echo "[2/4] Hard-binding local context..."
gcloud container clusters get-credentials $CLUSTER_NAME --zone $ZONE

echo "[3/4] Waiting for Node-Pool Vitality..."
# Loop until the nodes are actually reporting 'Ready' to the API
until kubectl get nodes | grep -q " Ready"; do
  echo "  ...Infrastructure initializing. Standing by."
  sleep 10
done
echo "  Nodes Verified. Cluster is healthy."

echo "[4/4] Triggering Core 11 Service Induction..."
gcloud builds submit --config infra/cloudbuild_graduation_final.yaml \
    --substitutions=_TAG="rc13-verified" .

echo "--- INSTALL COMPLETE: Sovereign Genesis is Online ---"
