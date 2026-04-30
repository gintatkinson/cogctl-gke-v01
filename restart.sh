#!/bin/bash
set -e

# --- CONFIGURATION ---
CLUSTER_NAME="sovereign-genesis"
ZONE="us-central1-a"
MACHINE_TYPE="n1-standard-4"
NODES=3
REQUIRED_VCPUS=12

echo "--- PHASE 1: PRE-FLIGHT SAFETY CHECKS ---"

# 1. Permission Check
echo "[Check] Verifying GCP Permissions..."
gcloud container clusters list --limit=1 > /dev/null

# 2. Quota Check (CPU)
echo "[Check] Verifying vCPU Quota..."
# Fetches the specific CPU limit using projection filtering
AVAILABLE_CPU=$(gcloud compute project-info describe --format="value(quotas.filter(metric:CPUS).limit)")

if [ -z "$AVAILABLE_CPU" ] || [ "${AVAILABLE_CPU%.*}" -lt "$REQUIRED_VCPUS" ]; then
    echo "ERROR: Insufficient vCPU quota (Need $REQUIRED_VCPUS, found $AVAILABLE_CPU)."
    exit 1
fi

# 3. Manifest Check
echo "[Check] Verifying Service Manifests..."
if [ ! -f "infra/cloudbuild_graduation_final.yaml" ]; then
    echo "ERROR: Deployment manifest missing at infra/cloudbuild_graduation_final.yaml"
    exit 1
fi

echo "--- PHASE 2: INFRASTRUCTURE PROVISIONING ---"
# Check if cluster already exists to prevent 400 errors
if gcloud container clusters describe "$CLUSTER_NAME" --zone "$ZONE" >/dev/null 2>&1; then
    echo "Cluster already exists. Skipping creation."
else
    gcloud container clusters create "$CLUSTER_NAME" \
        --zone "$ZONE" --machine-type "$MACHINE_TYPE" --num-nodes "$NODES" --quiet
fi

echo "--- PHASE 3: VITALITY & INDUCTION ---"
gcloud container clusters get-credentials "$CLUSTER_NAME" --zone "$ZONE"

echo "Waiting for Kubernetes API and Node Pool..."
until kubectl get nodes | grep -q " Ready"; do
  sleep 5
done

echo "Triggering Final Service Induction..."
gcloud builds submit --config infra/cloudbuild_graduation_final.yaml --substitutions=_TAG="rc13-verified" .

echo "--- PROTOCOL COMPLETE: SYSTEM ONLINE ---"
