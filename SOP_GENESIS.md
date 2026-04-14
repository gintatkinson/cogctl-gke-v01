# SOP: GENESIS (GKE Birth v3.0 - Hardened Native)

This protocol establishes the Sovereign Foundation on GKE Autopilot, using a **Hardened Native** architecture to resolve the 'Blind Birth' and 'Heartbeat Deadlock' failure modes.

## Phase 0: Networking (The Eyes) - MANDATORY
GKE Autopilot requires an outbound path for nodes to initialize and reach the Google-managed Control Plane.
- **Cloud Router**: Create `sovereign-router` in region `us-central1` for network `sovereign-vpc`.
- **Cloud NAT**: Create `sovereign-nat` on the router. 
- **Verification Command**: `gcloud compute routers nats describe sovereign-nat --router=sovereign-router --region=us-central1`

## Phase 1: Subnet & VPC Alignment
The network fabric must be prepared with secondary ranges for Pods and Services:
- **Primary Subnet**: `sovereign-subnet` (`10.10.0.0/24`)
- **Secondary Range (Pods)**: `gke-pods` (`10.100.0.0/16`)
- **Secondary Range (Services)**: `gke-services` (`10.101.0.0/20`)

## Phase 2: Infrastructure Birth (Hardened Native)
Provision GKE Autopilot cluster utilizing high-entropy naming (e.g., `sovereign-genesis-1776017190`) to bypass legacy metadata locks.
- **Security Posture**: Standard Native nodes (Public IP enabled for heartbeats) secured by VPC-level firewall rules.
- **Sequence**: Network -> Subnet -> Router -> NAT -> **Cluster**.

## Phase 3: Fabric Readiness (The Gateway)
- **Mandatory verification gate**: Minimum 5-minute wait post-creation.
- **Blocking Guardrail**: Fabric audit (via Cloud Console or Cloud Build) MUST return at least 2 `Ready` nodes. 
- **System Service Health**: System pods in `kube-system` MUST show `Running` status for `kube-dns` and `konnectivity-agent` (Verify via Console). 

**DO NOT proceed to application-layer deployment (TFS) until Phase 3 is 100% Green.**
