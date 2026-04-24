# SOLUTION: Remediation of 504 Gateway Time-out during Data Ingestion

## Issue Overview
During the **Sovereign Graduation Induction (v3.1)**, data ingestion attempts using large JSON files resulted in a `504 Gateway Time-out` from the NGINX Ingress controller.

## Forensic Diagnosis
- **Symptom**: NGINX timeout after 60 seconds.
- **Root Cause**: **Resource Starvation (CPU Throttling)**.
- **Details**:
    - The Python-based gRPC services (WebUI, Device, and Context) were operating under a strict 125m CPU audit limit.
    - During JSON parsing and gRPC serialization, CPU utilization spiked to **207m** (WebUI) and **160m** (Device).
    - Aggressive GKE throttling induced latency exceeding the 60s NGINX threshold and triggering exponential gRPC retry loops, creating a service deadlock.

## Remediation: Vertical Burst Scaling
The resource baseline was updated to allow for computational bursting during ingestion.
- **CPU**: 250m Request / 500m Limit (1000m for WebUI/Context).
- **Memory**: 128Mi Request / 256Mi Limit.

## Remediation: Ingress Timeout & Bound Controller
Fixed the 504 Gateway Time-out by binding the Ingress to NGINX and increasing the timeout to 3600s.
- **Ingress Class**: Added `spec.ingressClassName: nginx`.
- **Timeouts**: Enforced `proxy-read-timeout` and `proxy-send-timeout` at `3600s`.

## Remediation: Native gRPC Probes
Resolved `NotReady` states by switching to native gRPC probes, as the graduation images were missing the health-probe binary.
- **Affected Services**: `deviceservice`, `automationservice`, `forecasterservice`.

## Remediation: Topology Associations
Enabled `ALLOW_EXPLICIT_ADD_DEVICE_TO_TOPOLOGY=TRUE` in `contextservice` to ensure complex Topologies are correctly populated.

## Verification
- Confirmed successful ingestion of 20+ devices and 25+ links.
- WebUI reachability confirmed at `http://34.68.33.204/webui/`.

## Version Control & Persistence
The environment is now anchored to the `v3.2-stabilized` release.
- **Tag**: `v3.2-stabilized`

## Rollback Procedure
To revert, restore the original resource values in the manifests and ensure the target image contains the `grpc_health_probe` binary before reverting probes.
