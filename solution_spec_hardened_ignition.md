# Solution Specification: Hardened Ignition Protocol

## 1. Goal: Breaking the "0 Nodes" Cycle
Transition the GKE Genesis engine from a complex "Private Peering" model to a "Standard Native" model that guarantees node birthing and connectivity on GKE Autopilot.

## 2. Technical Modifications
### 2.1 Genesis Refactoring
- **Removal of `--enable-private-nodes`**: Nodes will be birthed with public IPs but remain locked behind VPC firewalls (`sovereign-allow-internal`).
- **Removal of `vpc-peerings`**: Stage 6 is eliminated to remove propagation lag as a failure variable.
- **Subnet Hardening**: Preserve Private Google Access to allow internal API communication without NAT dependency.

### 2.2 Ignition Sequence
- **Phase 1 (Purge)**: Hard reset of all `sovereign-*` resources.
- **Phase 2 (Birth)**: Execute the refactored `genesis.sh`.
- **Phase 3 (Verify)**: Mandatory confirmation of `kubectl get nodes` > 0 before proceeding to application deployment.

## 3. Verification Protocol
- **Stage I**: Node Visibility Audit.
- **Stage II**: Ingress IP Birth.
- **Stage III**: Browser-Subagent Visual Handshake (The "Gold Standard" of success).
