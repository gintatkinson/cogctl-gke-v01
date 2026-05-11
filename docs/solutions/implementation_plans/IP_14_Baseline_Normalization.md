# Implementation Plan: IP_14 (Baseline Normalization & Portability)

**Status**: DRAFT (Awaiting Approval)
**Author**: Sovereign AI (Karpathy Skill Active)
**Reference**: [SOVEREIGN DIRECTIVES.MD](../../solutions/SOVEREIGN%20DIRECTIVES.MD)

## 1. Objectives
- Remove all hardcoded `cogctl-gke-v01` references from the `baseline/` manifests.
- Standardize all sidecar images to `busybox:1.36`.
- Implement a **Kustomize Overlay** to allow customers to inject their `PROJECT_ID` and `NAMESPACE` without mutating the source YAMLs.

## 2. Problems to Overcome
- **Static Registry Paths**: Hardcoded paths prevent cross-project image pulling.
- **`sed` Prohibition**: Rule 4.2 prohibits the previous "hacky" solution of patching at runtime.
- **Tag Inconsistency**: `localhost:32000` and `dev` tags are still present in some production baseline files.

## 3. Phase 1: Baseline Tokenization
- **Action**: Replace all `us-central1-docker.pkg.dev/cogctl-gke-v01/sovereign-tfs/` strings with a standard image name (e.g., `sovereign-tfs/[SERVICE_NAME]`).
- **Target**: All 40+ files in `baseline/tfs-controller/manifests/`.

## 4. Phase 2: Kustomize Orchestration
- **Action**: Create `baseline/tfs-controller/manifests/kustomization.yaml`.
- **Action**: Configure `images` section to map the generic service names to the customer's specific registry.

## 5. Phase 3: Pipeline Evolution
- **Action**: Update `infra/awake.yaml` to use `kubectl apply -k` (Kustomize) instead of `kubectl apply -f`.
- **Verification Gate**: `kubectl kustomize baseline/tfs-controller/manifests/` must produce a valid, project-correct output.

---
**Verification Gate**: Zero `v01` strings permitted in the `baseline/` directory after execution.
