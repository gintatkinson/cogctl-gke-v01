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

## 3. Zero-Consumption Termination (Total Destruction)
Use this procedure to achieve **$0.00/month** consumption. This deletes the cluster and all persistent disks.

### Procedure
1. Destroy the cluster:
   ```bash
   gcloud container clusters delete sovereign-genesis --zone us-central1-a --quiet
   ```
2. Verify no orphaned disks remain:
   ```bash
   gcloud compute disks list --filter="name~'sovereign-genesis'"
   ```

### Status
- **Costs**: $0.00 (Total).
- **State**: Permanently Deleted.
- **Restart**: Requires a full "Resurrection" build.

## 4. Resurrection (Restoring from Zero)
Use this procedure to re-birth the system after a Total Termination.

### Phase 1: Infra-Provisioning (Re-building the Foundation)
Execute the command to provision the "Hardened Cottage" cluster:
```bash
gcloud container clusters create sovereign-genesis \
    --zone us-central1-a \
    --machine-type e2-standard-4 \
    --num-nodes 3 \
    --disk-type pd-balanced \
    --disk-size 100 \
    --project cogctl-gke-v01
```

### Phase 2: Software Induction (Restoring the Enclave)
Once the cluster is healthy, execute the graduation pipeline:
```bash
gcloud builds submit --config infra/cloudbuild_graduation_final.yaml .
```

### Status
- **Success Criteria**: All 11 services reach `Running` on a fresh cluster.
- **Data State**: Reset to the "rc13-verified" baseline.

## 5. Comparison Matrix
| Mode | Compute | Storage | Mgmt Fee | State | Restart |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hibernation** | $0 | Yes | Yes | Preserved | 3 mins |
| **Termination** | $0 | $0 | $0 | Wiped | 12 mins |
