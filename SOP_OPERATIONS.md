# SOP: Sovereign Genesis Operations (Hibernation & Restart)

## Overview
This document defines the procedure for power-cycling the Sovereign GKE Genesis environment to optimize costs while maintaining architectural integrity.

## 1. Hibernation (Scaling to Zero)
Use this procedure to stop all compute charges while preserving the system state (disks, config, secrets).

### Procedure
1. Verify the current cluster context:
   ```bash
   gcloud container clusters get-credentials sovereign-genesis --zone us-central1-a
   ```
2. Scale the node pool to 0:
   ```bash
   gcloud container clusters resize sovereign-genesis --node-pool default-pool --num-nodes 0 --zone us-central1-a --quiet
   ```

### Status
- **Compute (VMs)**: Stopped ($0/hr).
- **Control Plane**: Active (Metadata preserved).
- **Storage (PVCs)**: Persistent (Storage costs apply).
- **Public IP**: Preserved.

## 2. Restoration (Restarting the Enclave)
Use this procedure to return the system to an operational state.

### Procedure
1. Scale the node pool back to the graduation baseline (3 nodes):
   ```bash
   gcloud container clusters resize sovereign-genesis --node-pool default-pool --num-nodes 3 --zone us-central1-a --quiet
   ```
2. Monitor the self-healing sequence:
   ```bash
   kubectl get pods -w
   ```

### Recovery Sequence (Automatic)
1. **Backbone Layer**: CockroachDB and NATS will mount their disks and reach `Running`.
2. **Init Containers**: Microservices will resolve `nats-client` and `kafka-public`.
3. **Core Layer**: All 11 services will transition to `Running`.
4. **Ingress**: The LoadBalancer will resume traffic routing once the `webuiservice` passes readiness probes.

## 3. Troubleshooting
If services remain in `CrashLoopBackOff` after 5 minutes:
- Force a resource release: `kubectl delete pods --all`
- Verify storage binding: `kubectl get pvc`
