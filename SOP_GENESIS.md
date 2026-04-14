# SOP: GENESIS (GKE Birth v3.0)

This protocol establishes the Sovereign Foundation on GKE Autopilot, hardened against the 'Blind Birth' failure mode.

## Phase 0: Networking (The Eyes) - MANDATORY
GKE Autopilot with Private Nodes requires an outbound path to reach the Google-managed Control Plane for initialization.
- **Cloud Router**: Create `sovereign-router` in region `us-central1` for network `sovereign-vpc`.
- **Cloud NAT**: Create `sovereign-nat` on the router. 
- **Verification Command**: `gcloud compute routers nats describe sovereign-nat --router=sovereign-router --region=us-central1`
- **Rationale**: Failure to sequence NAT results in nodes that are created but cannot bootstrap, leading to a permanent 'Pending' state for system pods.

## Phase 1: Subnet & VPC Alignment
The network fabric must be prepared with secondary ranges for Pods and Services:
- **Primary Subnet**: `sovereign-subnet` (`10.0.0.0/20`)
- **Secondary Range (Pods)**: `gke-pods` (`10.100.0.0/16`)
- **Secondary Range (Services)**: `gke-services` (`10.101.0.0/20`)

## Phase 2: Infrastructure Birth (The Vacuum Shift)
Provision GKE Autopilot cluster utilizing high-entropy naming (e.g., `sovereign-genesis-1776017190`) to bypass legacy metadata locks.
- **Security Posture**: Enable Private Nodes and Private Endpoint.
- **Sequence**: Network -> Subnet -> Router -> NAT -> **Cluster**.

## Phase 3: Fabric Readiness (The Gateway)
- **Mandatory verification gate**: Minimum 5-minute wait post-creation.
- **Blocking Guardrail**: Fabric audit (via Cloud Console or Cloud Build) MUST return at least 2 `Ready` nodes. 
- **System Service Health**: System pods in `kube-system` MUST show `Running` status for `kube-dns` and `konnectivity-agent` (Verify via Console). 

**DO NOT proceed to application-layer deployment (TFS) until Phase 3 is 100% Green.**
