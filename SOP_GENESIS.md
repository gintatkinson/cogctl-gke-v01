# SOP: GENESIS (GKE Birth v3.0)

This protocol establishes the Sovereign Foundation on GKE Autopilot.

## Phase 0: The Networking Eyes (MANDATORY)
- **Requirement**: Cloud NAT and Router MUST be provisioned BEFORE cluster creation. 
- **Rationale**: Private nodes require an outbound path to reach the Google Control Plane for initialization. Failure to sequence NAT results in a 'Blind Birth' (Ghost Cluster).

## Phase 1: Infrastructure Birth
- Provision GKE Autopilot cluster with Private Nodes enabled.
- **Verification**: Wait for `Ready` status on all system nodes.
