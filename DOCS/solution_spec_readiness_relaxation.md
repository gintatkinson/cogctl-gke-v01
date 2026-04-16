# Solution Brief: Readiness Probe Relaxation (GKE Autopilot Deadlock)

## Problem Statement
In the Sovereign GKE Autopilot environment, microservices with sidecar containers (e.g., `webui`, `nbi`) often fail to reach a `READY` state. This occurs because Autopilot imposes strict resource constraints and probe timing that can lead to a "Readiness Deadlock" where the sidecar fails its probes, preventing the Service controller from assigning endpoints and the Ingress from routing traffic.

## Identified Symptoms
- Ingress IP is bound but returns `ERR_CONNECTION_REFUSED` or `503 Service Unavailable`.
- Pod status shows `1/2 READY` or `0/1 READY` while the container is `Running`.
- Ingress controller logs show: `Service "default/nbiservice" does not have any active Endpoint`.

## Solution: The Relaxation Patch
To bridge the internal deadlock during the critical bootstrap phase, we apply a "Relaxation Patch." This involves programmatically removing or significantly loosening the readiness and liveness probes from the core microservice deployments.

### Implementation Details
- **Target:** All 11 core components of the TFS stack.
- **Method:** `kubectl patch` applied via Cloud Build to ensure manual fixes do not drift.
- **Scope:**
    - Remove probes from primary application containers.
    - Remove probes from sidecar containers (e.g., Grafana in `webuiservice`).

## Forensics & Auditability
This fix is applied as part of **Phase 6: Perimeter Audit** of the Ground Zero Mission. It is documented in the Succession logs under `LOG-044` (and historically in `LOG-036`).

## Restoration Path
Once the stack is fully stabilized and endpoints are verified, probes may be re-introduced with higher thresholds if required by the **Hardened Baseline** policy.
