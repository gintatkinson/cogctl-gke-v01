# ISSUE #37: Regional Node Deadlock (Peering Propagation Failure)

## Status: OPEN
**Severity:** CRITICAL
**Label:** ARCHITECTURE, GKE, NETWORKING

## Description
During multiple recovery attempts, the GKE Autopilot clusters reached a "Ghost State" where the control plane reported `RUNNING` but the system was unable to birth a single compute node. This resulted in a terminal 100% `Pending` state for all pods, including mission-critical monitoring and ingress controllers.

## Symptoms
- **Node Count**: `kubectl get nodes` returns `No resources found`.
- **Pod Status**: 100% of pods in all namespaces remain `Pending`.
- **Events**: `pod didn't trigger scale-up: 1 node(s) didn't fit resource`.
- **Service Status**: `cannot EnsureLoadBalancer() with no hosts`.

## Root Cause
- **Heartbeat Deadlock**: The use of `--enable-private-nodes` combined with Stage 6 `VPC Peering` logic created a race condition. If the peering did not fully propagate before the Autopilot Node Agent attempted to heartbeat to the Master, the nodes were rejected or never provisioned.
- **NAT Lag**: Dependency on Cloud NAT for private nodes added another layer of failure potential during the rapid "Nuclear Ignition" sequence.

## Mandated Resolution
1. **Standard Native Strategy**: Revert to public GKE nodes (secured by firewall) to ensure deterministic heartbeats.
2. **Peering Removal**: Eliminate Managed Service Peering from the foundation script to prevent propagation deadlocks.
3. **IAM Sentry**: Explicitly verify the GKE Robot Service Account permissions before every ignition.

## Audit Trail
- **Detected:** 2026-04-14
- **Researcher:** Antigravity (AI Agent)
- **Reviewer:** Sovereign (USER)
