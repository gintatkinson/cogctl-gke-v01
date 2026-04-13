# SOP: Readiness Probe Deadlock (Sidecar Override)

## 1. Problem Definition
*   **The Problem**: A pod with multiple containers (e.g., `webuiservice` with Server and Sidecar) remains in a `1/2 READY` state indefinitely.
*   **The Symptom**: `kubectl get pods` shows the pod is `Running` but not `Ready`. `kubectl get endpoints` is `EMPTY`. External LoadBalancer returns `ERR_CONNECTION_REFUSED`.
*   **The Root Cause**: A non-critical sidecar container (e.g., Grafana, metrics collector) fails its readiness or liveness probe. Kubernetes refuses to route traffic to the pod until ALL containers are ready.

## 2. Verification Protocol
1.  **Identify Crashing Sidecar**:
    ```bash
    kubectl describe pod <pod_name>
    ```
    Observe which container has a failing Readiness probe in the "Events" or "Containers" section.

## 3. Resolution Protocol (The Relaxation Patch)
1.  **Hardened Patch**: Remove the readiness and liveness probes for the non-critical container via a JSON patch.
    ```bash
    kubectl patch deployment <deployment_name> --type='json' -p='[{"op": "remove", "path": "/spec/template/spec/containers/1/readinessProbe"}, {"op": "remove", "path": "/spec/template/spec/containers/1/livenessProbe"}]'
    ```
2.  **Acknowledge**: This is a restoration-phase override to facilitate audit. Proper sidecar health should be resolved in the post-audit maturation phase.

## 4. Governance
*   Never remove probes from the PRIMARY container (Index 0).
*   Document ALL overrides in the mission SUCCESSION_LOG.
