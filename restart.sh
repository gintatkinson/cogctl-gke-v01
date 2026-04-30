#!/bin/bash
# --- Sovereign Genesis: Ground 0 Install ---
CLUSTER_NAME="sovereign-genesis"
ZONE="us-central1-a"
MACHINE_TYPE="n1-standard-4"
NODES=3

echo "[1/4] Igniting Infrastructure..."
gcloud container clusters create $CLUSTER_NAME \
    --zone $ZONE \
    --machine-type $MACHINE_TYPE \
    --num-nodes $NODES \
    --quiet

echo "[2/4] Binding Context..."
gcloud container clusters get-credentials $CLUSTER_NAME --zone $ZONE

echo "[3/4] Waiting for Node Vitality..."
until kubectl get nodes | grep -q " Ready"; do
  echo "  ...Initializing. Standing by."
  sleep 10
done

echo "[4/4] Triggering Service Induction..."
gcloud builds submit --config infra/cloudbuild_graduation_final.yaml \
    --substitutions=_TAG="rc13-verified" .
