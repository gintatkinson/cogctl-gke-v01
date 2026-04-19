# SOP-04: Application Stack Rollout

## 1. Subprocess: Image Registry Reconciliation
- **Action**: Verify that all 11 core service images are present in the certified project registry.
- **Correction**: Run `infra/cloudbuild_build_source.yaml` if images are missing or stale.

## 2. Subprocess: Service Manifest Application
- **Action**: Apply the TFS controller and service manifests in sequence.
- **Reference**: `infra/cloudbuild_deploy_core.yaml`.

## 3. Subprocess: Rollout Monitoring
- **Action**: Track deployment progress via `kubectl rollout status`.

## 4. Subprocess: Sidecar Injection Verification
- **Action**: Verify that 2-container pods are birthed for services requiring NGINX or Envoy sidecars.

## 5. Subprocess: Pod Integrity Check
- **Action**: Audit pod states for `ImagePullBackOff` or `ConfigError`.

---
**Status**: ACTIVE
**Source Files**: Refactored from `SOP_CORE.md`, `SOP_GENESIS.md`.
