#!/bin/bash
# Detected Metadata
CLUSTER="sovereign-genesis"
REGION="us-central1-a"
NAMESPACE="sovereign-genesis"

echo "[STARTUP] Executing Sovereign Activation Sequence..."

# 1. Restore Core 11
while read -r manifest; do
    echo "[STARTUP] Applying $manifest..."
    kubectl apply -f "$manifest" -n $NAMESPACE
done < infra/CORE_11_LIST.txt

# 2. Scaling up (Redundant if apply works, but ensures state)
kubectl scale deployment --all --replicas=1 -n $NAMESPACE
kubectl scale statefulset --all --replicas=1 -n $NAMESPACE

# 4. Monitoring
echo "[STARTUP] Monitoring Pod Induction..."
kubectl get pods -n $NAMESPACE

echo "[STARTUP] Sovereign Genesis is now ACTIVE."
