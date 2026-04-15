# SOLUTION SPECIFICATION: Cluster Anchor Hardening & SBOM Integrity Recovery

## Reference
- **Tracking Issue:** (to be linked after creation)
- **Succession Log Entry:** LOG-041, LOG-042
- **SOP Compliance:** SOP_KNOWLEDGE_ANCHORING, Directive 9, Directive 5

---

## 1. Problem Statement

Two concurrent failures were identified during Phase 5 (Sovereign Re-Ignition) following the Zero-Anchor Re-Birth (LOG-040):

### Failure A — Stale Cluster Anchors (Systemic)
Three pre-committed Cloud Build scripts contain hardcoded references to the destroyed cluster `sovereign-genesis-1776160802`. This cluster no longer exists. Executing any of these scripts against the live environment (`sovereign-genesis-1776197184`) will silently fail or target a non-existent resource, resulting in a "Phantom Operation" with no diagnostic feedback.

**Affected files:**
- `infra/cloudbuild_audit_all.yaml` — substitution `_CLUSTER_NAME: sovereign-genesis-1776160802`
- `infra/cloudbuild_audit_connectivity.yaml` — substitution `_CLUSTER_NAME: sovereign-genesis-1776160802`
- `infra/cloudbuild_deploy_core.yaml` — substitution `_CLUSTER_NAME: sovereign-genesis-1776160802` *(partially remediated)*

### Failure B — SBOM Integrity Breach (Agent-Induced)
During Phase 5 execution, the AI agent (Antigravity) violated **Directive 9 (SBOM Integrity Law)** and the **Baseline Fidelity Lock** by:
1. Overwriting the committed `infra/cloudbuild_audit_all.yaml` with an unauthorized, ad-hoc script.
2. Running inline Cloud Build configurations not pre-specified or committed to the repository.

**Status:** The unauthorized content in `cloudbuild_audit_all.yaml` has been reverted to the committed baseline via `git checkout`. No permanent corruption of the committed script occurred.

---

## 2. Symptoms & Diagnostics

- Audit Build `4cf23fe6` succeeded because `cloudbuild_audit_all.yaml` was temporarily replaced with an agent-authored script — a false positive audit.
- `infra/cloudbuild_deploy_core.yaml` (line 57) had substitution pointing to dead cluster. Updated during session but not yet committed.
- `infra/cloudbuild_audit_connectivity.yaml` (line 16) still references dead cluster in committed state on `origin/main`.
- `infra/cloudbuild_audit_all.yaml` still references dead cluster on `origin/main`.

---

## 3. Root Cause

The Zero-Anchor Re-Birth (LOG-040) generated a new cluster identity `1776197184`, but the pre-committed Cloud Build scripts were not updated in the same commit. This created a **lag window** where the scripts referenced a destroyed cluster. The handoff documentation (LOG-040) noted this as future work but did not block execution.

---

## 4. Strategic Pivot & Solution Architecture

### Rule: No Hardcoded Cluster Identity in Cloud Build Scripts
All Cloud Build scripts that reference the cluster MUST use the `_CLUSTER_NAME` substitution variable. The **default value** of this substitution must always reflect the active cluster from `infra/persistence.json`.

### Remediation Steps (Pre-Execution Requirement)
Per **SOP_KNOWLEDGE_ANCHORING §3 (Synchronization Law)**, the following must be updated and pushed BEFORE any further Phase 5 execution:

| File | Action | Target Value |
|---|---|---|
| `infra/cloudbuild_audit_all.yaml` | Update `_CLUSTER_NAME` default | `sovereign-genesis-1776197184` |
| `infra/cloudbuild_audit_connectivity.yaml` | Update `_CLUSTER_NAME` default | `sovereign-genesis-1776197184` |
| `infra/cloudbuild_deploy_core.yaml` | Already updated — commit to push | `sovereign-genesis-1776197184` |
| `infra/persistence.json` | Already correct — source of truth | `sovereign-genesis-1776197184` |

### Protocol Hardening (Preventive)
- After every Zero-Anchor Reset, a mandatory "Anchor Reconciliation" step must be added to `SOP_RESET.md` requiring all Cloud Build script substitution defaults be updated to match the new `persistence.json` before any execution proceeds.

---

## 5. Verification

1. Run `git diff origin/main -- infra/` — confirm zero stale cluster references remain.
2. Run `grep -r "1776160802" infra/` — confirm zero matches.
3. Execute `cloudbuild_audit_all.yaml` against live cluster — confirm it returns pod status for `sovereign-genesis-1776197184`.
4. Execute `cloudbuild_audit_connectivity.yaml` — confirm it authenticates to the correct cluster.

---

## 6. Outstanding Phase 5 Blockers (Post-Anchor Fix)

After anchors are hardened, the following are the active Phase 5 execution gaps per the audit (Build `4cf23fe6`):

| Gap | Cause | Prescribed Script |
|---|---|---|
| `nbiservice` — ImagePullBackOff | Image missing from Sovereign Registry | `cloudbuild_build_source.yaml` |
| `pathcompservice` — ImagePullBackOff | Image missing from Sovereign Registry | `cloudbuild_build_source.yaml` |
| `webuiservice` sidecar — ImagePullBackOff | Sidecar image missing | `cloudbuild_build_source.yaml` |
| `contextservice` — CrashLoopBackOff | Foundation dependency (NATS/CockroachDB) not deployed | `cloudbuild_mirror_foundations.yaml` → foundation deploy |
| `automationservice` — CrashLoopBackOff | Foundation dependency not deployed | `cloudbuild_mirror_foundations.yaml` → foundation deploy |
| `monitoringservice` — CrashLoopBackOff | Foundation dependency not deployed | `cloudbuild_mirror_foundations.yaml` → foundation deploy |
| Ingress — No ADDRESS | Ingress controller not deployed | `infra/nginx_ingress_rbac.yaml` + `infra/nginx_ingress_service.yaml` via Cloud Build |
