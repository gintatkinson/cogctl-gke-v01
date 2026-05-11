# TECHNICAL SOLUTION SPEC: Foundation Fidelity Correction

**Issue**: Restoration Mission Failure via Blueprint Violation
**Date**: 2026-04-17
**Status**: DRAFT (Awaiting Approval)
**Reference**: SOP-03, LOG-045, Blueprint Law Rule 7.2

---

## 1. Problem Statement
The automated restoration of the Sovereign GKE Genesis v3.0 infrastructure failed during Phase 5 (Foundation Layer Deployment). The failure was two-fold:
1.  **API Watch Blindness**: The CockroachDB Operator was birthed with an unpatched `%TFS_CRDB_NAMESPACE%` variable, preventing it from discovering the database resources in the `default` namespace.
2.  **Manifest Misclassification**: A Helm values file (`nats/cluster.yaml`) was incorrectly used as a raw Kubernetes manifest, causing a validation failure in the Cloud Build pipeline.

## 2. Root Cause
A violation of **Blueprint Law Rule 7.2 (Shadow Manifest Prohibition)**. I relied on "Tactical Fallbacks" and "Heuristic Guessing" instead of performing a deterministic audit of the `baseline/` directory before designing the automation.

## 3. Proposed Fix: The Fidelity Reconciliation
1.  **Bootstrap Correction**: Update `baseline/tfs-controller/manifests/cockroachdb/operator.yaml` to include the hardcoded `default` namespace (Rule 4.2 Back-port).
2.  **NATS Codification**: Birth a new, native Kubernetes manifest `baseline/tfs-controller/manifests/nats/nats_fidelity.yaml` to replace the unusable Helm config.
3.  **Pipeline Hardening**: Update `infra/cloudbuild_foundations_fidelity.yaml` to point to the corrected baseline files and incorporate a **Post-Patch Placeholder Audit** step to prevent future unpatched variables.

## 4. Verification Criteria
- `kubectl get pods -n default` confirms `cockroachdb-0`, `nats`, and `kafka` are in `RUNNING` status.
- `grep -c "%" baseline/tfs-controller/manifests/` returns `0`.

---
**Author**: Antigravity (Sovereign Infrastructure Agent)
