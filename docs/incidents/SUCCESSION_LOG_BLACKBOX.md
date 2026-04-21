# TECHNICAL IMPLEMENTATION LOG: THE BLACK BOX

## 1. System Recovery Records

### REC-001: Toolchain Path Hardening (Succession Regression Audit)
- **Discovery**: SDK binaries (`gcloud`, `gh`) failed to load in non-interactive shells and orchestration scripts due to legacy absolute paths (`/home/parallels/...`).
- **Remediation**: Expanded logic to mandate **Mandatory Script-Level Path Sanitization**. Replaced all absolute calls with relative calls anchored by a reconciled, Homebrew-aware `PATH`.

### REC-002: Service Endpoint Deadlocks
- **Discovery**: GKE Autopilot probes failed for 2nd-container sidecars (NGINX/Envoy), preventing pod readiness.
- **Remediation**: Implemented a Surgical Probe Relaxation Patch (Removing readiness/liveness probes from sidecars).

### REC-003: Core Configuration Gap (CRDB_NAMESPACE)
- **Discovery**: `contextservice` crashed due to missing `CRDB_NAMESPACE` setting.
- **Remediation**: Permanently injected variable into the deployment manifest. Logged in Solution Spec.

### REC-004: Ingress Perimeter Alignment
- **Discovery**: Ingress resource birthed with the wrong selector for the NGINX controller.
- **Remediation**: Corrected deployment labels and updated ingress mapping.

### REC-005: NBI Broker Synchronization OOM Deadlock
- **Discovery**: GKE Autopilot executed an OOM-kill on `nbiservice` during its initial Kafka topic synchronization due to a massive memory spike upon successful broker connection.
- **Remediation**: Surgically elevated the deployment resource limits to `memory=2Gi` to bridge the initialization spike. Logged in Solution Spec.

### REC-006: Readiness Dependency & Manifest Hardening
- **Discovery**: WebUI service failed ignition due to a `ModuleNotFoundError` for `flask-healthz` (missing from unified requirements) and a `Werkzeug 3.0` regression.
- **Remediation**: Anchored exact pins (`flask-healthz==1.0.1`, `Werkzeug==2.3.7`) in the Gold Master foundation.

### REC-007: Perimeter IP Drift & Firewall Deadlock
- **Discovery**: LoadBalancer identity shifted during the v3.0 GKE re-birth, causing 404 deadlocks. VPC firewall rules also isolated external traffic from the NGINX controller.
- **Remediation**: Anchored static IP `34.31.116.202` in persistence metadata and injected public ingress rules (TCP 80/443) into the genesis fabric.

### REC-008: CRD Propagation & Sequential Hardening
- **Discovery**: Build #14 failed due to a race condition where `CrdbCluster` was applied before the CockroachDB Operator was birthed, causing a 'resource mapping not found' error.
- **Remediation**: Implemented deterministic sequencing in `cloudbuild_final.yaml`. Mandatory `kubectl wait` for CRD stability followed by `kubectl rollout status` for the operator manager before applying the database cluster manifest.

### REC-009: Artifact Registry Reconciliation & Latency Buffering
- **Discovery**: Build #15 failed with `ErrImagePull` because foundational images (Cockroach Operator) were missing from the project Artifact Registry. Rollout also timed out due to GKE Autopilot provisioning latency.
- **Remediation**: Triggered `infra/cloudbuild_mirror_foundations.yaml` to vault dependencies in our sanctioned registry. Extended the rollout status gate to **300 seconds** to accommodate background node-provisioning.

---

## 2. Immutable Operational Constraints
- **Constraint 01**: All infrastructure changes MUST be executed via Cloud Build.
- **Constraint 02**: No manual `kubectl` patches are allowed without manifest back-porting.
- **Constraint 03**: Every session must begin with a Technical Health Audit (SOP-01).

---
**Status**: ACTIVE
**Source of Truth**: Aligned with the 1-6 SOP Framework.
docs/incidents/13_SCREEN_AUDIT.md
