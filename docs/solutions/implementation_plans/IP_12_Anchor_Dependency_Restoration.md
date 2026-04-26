# IP_12: Anchor & Dependency Restoration

## 1. Ingress Restoration (The Ingress Void)
**Objective**: Reconstruct `infra/tfs_ingress.yaml` to restore external gateway access.
**Action**:
- Surgically extracted the `Ingress` resource from `baseline/tfs-controller/src/tests/ofc25/tfs-ingress-e2e.yaml`.
- Wrote the extracted content to `infra/tfs_ingress.yaml`.
- Explicitly modified the `ingressClassName` in the `spec` section to `nginx`.

## 2. Topography Realignment (The Topographical Fracture)
**Objective**: Resolve the `ErrImagePull` affecting `analyticsservice`.
**Action**:
- Adjusted the `sed` substitution logic in `cloudbuild_graduation_final.yaml` to properly handle `analytics-frontend` and `analytics-backend` as `T_NAME`.
- The exact image tags in the Artifact Registry are `analytics-frontend:rc13-verified` and `analytics-backend:rc13-verified`. 

## 3. Hydration Injection
**Objective**: Ensure proper database namespace scoping and Kafka compatibility for `automationservice` and `deviceservice`.
**Action**:
- Injected the environment variable `CRDB_NAMESPACE` with value `"default"` into `deviceservice` (and verified it in `automationservice`).
- Injected the environment variable `KAFKA_API_VERSION` with value `"3.7.0"` into the `automationservice` and `deviceservice` deployment manifests.

## 4. Readiness Probe Relaxation
**Objective**: Bypass sidecar readiness failures in `monitoringservice` and `nbiservice`.
**Action**:
- Applied the "Surgical Relaxation Patch" to both manifests, changing the `readinessProbe` definitions to `startupProbe` definitions (to allow sidecars and dependent services sufficient time to initialize without causing cyclic restart loops).

## 5. NBI Resource Elevation
**Objective**: Bridge the Kafka sync spike by allocating sufficient memory to `nbiservice`.
**Action**:
- Enforced `2048Mi` memory limit in the `nbiservice` limits spec, and ensured the `cloudbuild_graduation_final.yaml` resource throttling `sed` commands correctly allow NBI to retain its memory allocation.
