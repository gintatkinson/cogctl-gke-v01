# Sovereign Resurrection v3.3 Implementation Plan

**Goal:** Secure the Sovereign Enclave by resolving Namespace Leakage (REC-049) and Monitoring CRD Deadlocks (REC-050) while achieving a stable 11-service resurrection.

**Architecture:** Forensic sanitation of the `default` namespace, hardened Cloud Build orchestration with explicit enclave scoping, and manifest filtering for graduation-critical services only.

**Tech Stack:** GKE, Google Cloud Build, Kubectl, GitHub CLI.

---

### Task 1: Environment Sterilization (REC-049 Cleanup)
**Goal:** Purge all leaked resources from the `default` namespace to restore forensic purity.

**Steps:**
1. **Identify Leaks**: List all deployments, services, and HPAs in the `default` namespace.
2. **Execute Purge**: 
   ```bash
   kubectl delete deployment,service,hpa --all -n default
   ```
3. **Verify Sterility**: Confirm `kubectl get all -n default` returns zero Sovereign resources.

### Task 2: Ignition Engine Hardening
**Goal:** Permanently prevent namespace leakage and dependency deadlocks in `awake.yaml`.

**Files:**
- Modify: `infra/awake.yaml`

**Step 1: Enforce Enclave Scoping**
Append `-n "${_NAMESPACE}"` to the `kubectl apply` commands in the `induct-backbone` and `induct-services` steps.

**Step 2: Implement Manifest Filtering (REC-050)**
Update the `induct-services` step to explicitly exclude `servicemonitors.yaml` from the bulk induction to prevent build failure.
```bash
# Example logic:
# find baseline/tfs-controller/manifests/ -name "*.yaml" ! -name "servicemonitors.yaml" | xargs kubectl apply -f - -n "${_NAMESPACE}"
```

**Step 3: Commit & Push**
```bash
git add infra/awake.yaml
git add docs/plans/2026-05-08-sovereign-resurrection-v3.3.md
git commit -m "fix: resolve REC-049 (leakage) and REC-050 (deadlock) in ignition engine"
git push origin main
```

### Task 3: Execute Hardened Resurrection
**Goal:** Trigger the final stable build and verify service ignition.

**Step 1: Trigger Build**
Run: `bash awake.sh`

**Step 2: Monitor Enclave Readiness**
Run: `kubectl rollout status deployment/contextservice -n sovereign-genesis --timeout=300s`

### Task 4: Forensic Post-Audit
**Goal:** Prove 100% enclave isolation.

**Step 1: Cross-Namespace Audit**
- Run: `kubectl get pods -n sovereign-genesis` (Expected: 11 services Running)
- Run: `kubectl get pods -n default` (Expected: Zero Sovereign services)

**Step 2: Close Incident**
Update GitHub Issue #22 with final logs and status.
