# SOP-05: Perimeter & Connectivity Stability

## 1. Subprocess: Ingress Controller Deployment
- **Action**: Provision the NGINX Ingress Controller.
- **Reference**: `infra/cloudbuild_final.yaml`.

## 2. Subprocess: Routing Resource Creation
- **Action**: Apply the Ingress rules mapping `/webui`, `/grafana`, and `/restconf` to backend services.

## 3. Subprocess: Readiness Probe Patching
- **Action**: Apply the **Surgical Relaxation Patch** to pods stuck in `1/2 READY` due to sidecar probe failures.
- **Reference**: `infra/cloudbuild_patch_probes.yaml`.

## 4. Subprocess: LoadBalancer Address Birth
- **Action**: Confirm the external IP assignment via `kubectl get svc -n tectonic-system`.
- **Target IP**: `136.112.218.241`.

## 5. Subprocess: Perimeter Connectivity Probe
- **Action**: Perform external `curl` probes against the `/webui/` endpoint.

---
**Status**: ACTIVE
**Source Files**: Refactored from `SOP_INGRESS.md`, `SOP_READINESS_DEADLOCK.md`.
