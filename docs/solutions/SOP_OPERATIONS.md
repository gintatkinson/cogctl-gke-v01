# SOP: Sovereign Genesis Operations (Hermetic Induction)

## Overview
This document defines the procedure for power-cycling the Sovereign GKE Genesis environment. 

**MANDATE: ZERO-LOCAL EXECUTION.**
There is no such thing as "local" for this project. All commands must be "Inducted" via the provided wrappers, which hand off execution to the GKE/Cloud Build environment. 

## 1. Hibernation (Remote Purge)
Use this procedure to achieve **$0.00/month** consumption by safely deconstructing the enclave from the cloud.

### Procedure
1.  Execute the Induction Gateway from the root directory:
    ```bash
    ./hibernate.sh
    ```
2.  **Verification (Remote)**: Monitor the Cloud Build logs. The process will:
    *   Delete the GKE Cluster remotely.
    *   Purge all orphaned Persistent Disks (PVCs) remotely.

### Status
- **Costs**: $0.00 (Total).
- **State**: Permanently Deleted from the infrastructure provider.
- **Immunity**: No local binaries (gcloud/kubectl) are invoked for logic.

## 2. Resurrection (Remote Ignition)
Use this procedure to re-birth the system from a zero-state.

### Procedure
1.  Execute the Ignition Gateway from the root directory:
    ```bash
    ./awake.sh
    ```
2.  **Verification (Remote)**: Monitor the Cloud Build logs. The process will:
    *   Provision the "Hardened Cottage" cluster remotely.
    *   Induct the Software Stack (11 Services) remotely.

### Status
- **Success Criteria**: All services reach `Running` on a fresh, hermetically-sealed cluster.
- **Data State**: Reset to the "rc13-verified" baseline.

## 3. High-Level Orchestration
For full lifecycle management (Restart/Shutdown), use the unified orchestrator:
```bash
./lifecycle.sh {shutdown|restart}
```

## 4. Operational Comparison
| Mode | Local Tools | Execution Env | Cost | Recovery |
| :--- | :--- | :--- | :--- | :--- |
| **Hibernation** | NONE | Cloud Build | $0.00 | 12 mins |
| **Resurrection** | NONE | Cloud Build | Active | 12 mins |
