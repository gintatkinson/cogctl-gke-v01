#!/bin/bash
set -e

CLUSTER_NAME="sovereign-genesis"
ZONE="us-central1-a"
MACHINE_TYPE="n1-standard-4"
NODES=3
REQUIRED_VCPUS=12

echo "--- PHASE 1: PRE-FLIGHT ---"

# 1. Permission Check
gcloud container clusters list --limit=1 > /dev/null

# 2. Quota Check (The "No More Jokes" Version)
# -w ensures we match the WHOLE word 'CPUS' (not 'CPUS_ALL_REGIONS')
# head -n 1 ensures we only get one value if multiple regions report
RAW_CPU=$(gcloud compute project-info describe --format="csv[no-heading](quotas.metric,quotas.limit)" | grep -w "CPUS" | head -n 1 | cut -d',' -f2)

if [ -z "$RAW_CPU" ]; then
    echo "CRITICAL FAILURE: Specific 'CPUS' metric not found."
    exit 1
fi

# Convert float to integer (handles the 12.0 format)
AVAILABLE_CPU=$(printf "%.0f" "$RAW_CPU")

if [ "$AVAILABLE_CPU" -lt "$REQUIRED_VCPUS" ]; then
    echo "CRITICAL FAILURE: Insufficient vCPU quota (Need $REQUIRED_VCPUS, found $AVAILABLE_CPU)."
    exit 1
fi

echo "--- PHASE 2: PROVISIONING ---"
if gcloud container clusters describe "$CLUSTER_NAME" --zone "$ZONE" >/dev/null 2>&1; then
    echo "Cluster detected. Ready."
else
    gcloud container clusters create "$CLUSTER_NAME" \
        --zone "$ZONE" --machine-type "$MACHINE_TYPE" --num-nodes "$NODES" --quiet
fi

echo "--- PHASE 3: INDUCTION ---"
gcloud container clusters get-credentials "$CLUSTER_NAME" --zone "$ZONE"

until kubectl get nodes | grep -q " Ready"; do
  echo "Polling nodes..."
  sleep 5
done

gcloud builds submit --config infra/cloudbuild_graduation_final.yaml --substitutions=_TAG="rc13-verified" .
echo "--- SYSTEM ONLINE ---"
