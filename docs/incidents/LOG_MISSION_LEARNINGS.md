# MISSION LEARNINGS: Sovereign GKE Foundation Restoration

This document archives the critical technical hurdles and solutions identified during the "Ground Zero Reset" missions (Issues #26, #27). These patterns are mandatory for all future restoration cycles.

## 1. The "Blind Birth" Deadlock (Network Architecture)
- **Problem**: GKE Autopilot clusters with Private Nodes but no Cloud NAT would "birth" a control plane but fail to provision any worker nodes. This was a "Metadata Blackout" where nodes could not call home to the GCP orchestrator.
- **Learning**: Cloud NAT is not a "post-install" convenience; it is a Mission Prerequisite. Node pool orchestration in Private Node clusters requires outbound reachability to the GCP Metadata servers.
- **Fix**: Provision the VPC -> Router -> Cloud NAT GATEWAY before the GKE ignition. Verified via the SOP_GENESIS.md "Hardened Start" protocol.

## 2. The API Gateway Deadlock (Identity & Access)
- **Problem**: Enabling "enablePrivateEndpoint: true" completely blocks external AI Agent access even if the Agent IP is added to the Master Authorized Networks.
- **Learning**: Private Endpoints are strictly VPC-internal. For "Sovereign but Automated" missions, the Control Plane must have a Public Endpoint enabled but restricted via Master Authorized Networks to only the Agent and User IPs.
- **Fix**: Use "Public Master / Private Nodes" architecture for automated restoration.

## 3. The "Warden" Policy Initiation Window
- **Problem**: Immediately after a cluster hits 'RUNNING', kubectl commands are often rejected with 'GKE Warden authz [denied by required-webhooks-limitation]'.
- **Learning**: Autopilot has a background policy propagation phase that lasts ~2-3 minutes.
- **Fix**: Implement a 120-second Mandatory Idle in all bootstrap scripts after cluster readiness is confirmed.

## 4. Legacy Secret Reliance (TFS Microservices)
- **Problem**: TFS Core services (Monitoring, KPI-Manager) threw 'CreateContainerConfigError' despite the database being alive.
- **Learning**: The official ETSI TFS manifests rely on legacy secret names (e.g., 'qdb-data' for QuestDB) that are not automatically birthed by the standard secret sync.
- **Fix**: Codified the legacy secret injection into infra/vault_bootstrap.sh and manually initialized the 'qdb-data' baseline.
