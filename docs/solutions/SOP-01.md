# SOP-01: Environment & Fabric Initialization

## 1. Subprocess: Shell & SDK Authentication
- **Action**: Authenticate with the Google Cloud SDK and GitHub CLI.
- **Verification**: `gcloud auth list` and `gh auth status` must confirm valid credentials for the target project.

## 2. Subprocess: Project & Region Mapping
- **Action**: Verify the active property anchor.
- **Status**: Target Project: `[CUSTOMER_PROJECT_ID]` | Target Region: `us-central1`.

## 3. Subprocess: Infrastructure Orchestration (The Engine)
- **Action**: The entire environment (VPC, Network, and GKE Cluster) is provisioned declaratively via the `infra/awake.yaml` orchestrator.
- **Reference**: Do NOT run Terraform manually. The pipeline will invoke `infra/terraform/main.tf`.

## 4. Subprocess: VPC & Network Provisioning (Internal Pipeline Step)
- **Action**: Create the isolated network fabric if non-existent or corrupted.
- **Anchor**: `infra/terraform/main.tf`

## 5. Subprocess: Cloud NAT Configuration (Internal Pipeline Step)
- **Action**: Deploy Cloud NAT to ensure private node outbound connectivity.
- **Requirement**: Mandatory for all GKE Genesis clusters to prevent "Blind Birth" (stalled nodes).

## 6. Subprocess: GKE Cluster Provisioning (Internal Pipeline Step)
- **Action**: Provision the target GKE cluster via declarative Terraform.
- **Anchor**: `infra/terraform/main.tf`
- **Namespace Anchor**: `sovereign-genesis`

## 7. Subprocess: Node Fabric Verification
- **Action**: Verify that nodes are `Ready` and have registered with the control plane post-ignition.
- **Verification**: `kubectl get nodes` (Expected: 3 Nodes).

---
**Status**: ACTIVE (v4.0 Re-Forge)
**Source Files**: Anchored to `infra/awake.yaml` and `infra/terraform/main.tf`.
