# ISSUE #36: Ingress LoadBalancer Deadlock (Autopilot Constraint)

## Status: OPEN
**Severity:** CRITICAL
**Label:** NETWORKING, GKE, AUTOPILOT

## Description
During the "Final Ignition" phase (Build fd234ef1), the system failed to retrieve a public LoadBalancer IP for the WebUI. The `nginx-ingress-sovereign` service remained in a `<pending>` state indefinitely, causing a build timeout.

## Symptoms
- **Build Log**: `CRITICAL: Public IP allocation timed out.`
- **Service Status**: `SyncLoadBalancerFailed` event.
- **Diagnostics**: `cannot EnsureLoadBalancer() with no hosts`.
- **Pod Status**: `kubectl get pods -n ingress` returns zero resources.

## Root Cause
- **Autopilot Policy Violation**: The ETSI `ofc25` NGINX manifest defines a `DaemonSet` using `hostPort` (8003, 4433, etc.).
- **Scheduling Prohibition**: GKE Autopilot prohibits the use of `hostPort` and limits the deployment of `DaemonSets` that require host-level networking access. As a result, the controller pods were never birthed, leaving the LoadBalancer with no healthy backends to target.

## Mandated Resolution
1. **GKE Adaptation**: Refactor the NGINX Ingress Controller from a `DaemonSet` to a GKE-friendly `Deployment`.
2. **Network Decoupling**: Remove all `hostPort` references and rely strictly on the `LoadBalancer` service for port mapping.
3. **Resource Provisioning**: Explicitly define resource requests to satisfy Autopilot's scheduling requirements.

## Audit Trail
- **Detected:** 2026-04-14
- **Researcher:** Antigravity (AI Agent)
- **Reviewer:** Sovereign (USER)
