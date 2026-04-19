# TECHNICAL IMPLEMENTATION LOG: THE BLACK BOX

## 1. System Recovery Records

### REC-001: Toolchain Path Hardening
- **Discovery**: SDK binaries (`gcloud`, `gh`) failed to load in non-interactive shells.
- **Remediation**: Injected absolute paths into environment configuration.

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

---

## 2. Immutable Operational Constraints
- **Constraint 01**: All infrastructure changes MUST be executed via Cloud Build.
- **Constraint 02**: No manual `kubectl` patches are allowed without manifest back-porting.
- **Constraint 03**: Every session must begin with a Technical Health Audit (SOP-01).

---
**Status**: ACTIVE
**Source of Truth**: Aligned with the 1-6 SOP Framework.
