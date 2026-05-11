# Implementation Plan: IP_11 (Sovereign Golden Restoration & Sterilization)

**Status**: DRAFT (Awaiting Agent Director Approval)
**Author**: Antigravity (Auditor Role)
**Reference**: [SOVEREIGN DIRECTIVES.MD](SOVEREIGN%20DIRECTIVES.MD)

## 1. Objectives
Achieve a flawless **Golden Release** deployment by reconciling the architectural drift and stabilizing the infrastructure on a resilient **3-node** fabric. This plan relies entirely on **Remote GKE/Cloud Build** execution.

## 2. Problems to Overcome
This plan resolves the following documented blockers via remote automation:
- **Resource Starvation**: Systemic OOM on 1-node configurations.
- **Storage Provisioning Failure**: Missing `hardened-storage` StorageClass.
- **Idempotency Failure**: `mv` deadlock in foundation builds.
- **Backbone Induction Failure**: Telemetry crashing due to CockroachDB race conditions.

## 3. Phase 1: Remote Sterilization (Purging Ghost Resources)
**Isolation Requirement**: This phase must be executed via `infra/cloudbuild_forensic_audit.yaml` or a dedicated sterilization worker.

### [REMOTE ACTION] File Sanitization
- **Targets**:
    - `docs/solutions/TSS-RECOVERY-GOLDEN-3.1-MASTER.md` (Unauthorized Spec)
    - `infra/cloudbuild_v3.1.1_customer_release.yaml` (Unauthorized Manifest)
    - `build.log` (Local residue)

### [REMOTE ACTION] Infrastructure Purge
- **Command**: `gcloud builds submit --config infra/cloudbuild_purge_all.yaml`
- **Impact**: Deletes all existing `sovereign-genesis-*` clusters to eliminate topographical duplication.

## 4. Phase 2: Architectural Hardening (Remote Fixes)
### [MODIFY] [infra/genesis.sh](infra/genesis.sh)
- **Change**: Set `--num-nodes 3`.
- **Rationale**: Provides the memory ceiling required for the 11-service stack.

### [MODIFY] [baseline/tfs-controller/manifests/](baseline/tfs-controller/manifests/)
- **Change**: Reconcile resource limits (125m CPU / 64Mi Memory) across all service manifests to match the Golden Baseline.

## 5. Phase 3: Golden Ignition
1. **Trigger**: `gcloud builds submit --config infra/cloudbuild_graduation_final.yaml`
2. **Verification**: Confirm all 11 services achieve **2/2 READY** state in the remote logs.

---
**Verification Gate**: Zero local tool usage during execution. All logs must be retrieved via `gcloud` from the remote worker.
