#!/bin/bash
# SOVEREIGN FINAL PERIMETER AUDIT
set -e

CLUSTER_NAME=$(grep "cluster_name" infra/persistence.json | cut -d'"' -f4)
REGION="us-central1"

echo "[AUDIT] Authenticating to cluster: $CLUSTER_NAME..."
gcloud container clusters get-credentials "$CLUSTER_NAME" --region "$REGION"

echo "[AUDIT] 1. INGRESS RESOURCE STATUS:"
kubectl get ingress tfs-ingress-opt

TARGET_IP=$(kubectl get ingress tfs-ingress-opt -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "Target IP: $TARGET_IP"

if [ -z "$TARGET_IP" ]; then
    echo "FAIL: Ingress IP not assigned."
    exit 1
fi

echo "[AUDIT] 2. POD READINESS CHECK:"
kubectl get pods

echo "[AUDIT] 3. CONNECTIVITY TEST (HTTP 200/302 CHECK):"
# Attempt to curl the WebUI. We expect a redirect or 200.
# We retry a few times to allow for load balancer propagation
for i in {1..5}; do
  echo "Attempt $i..."
  if curl -I -L --connect-timeout 5 --max-time 10 "http://$TARGET_IP/webui/" | grep "200 OK"; then
    echo "SUCCESS: WebUI is reachable."
    exit 0
  fi
  sleep 10
done

echo "FAIL: WebUI still unreachable after retries."
exit 1
