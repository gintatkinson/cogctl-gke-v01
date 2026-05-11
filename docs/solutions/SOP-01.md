# SOP-01: Environment & Fabric Initialization

## 1. Subprocess: Shell & SDK Authentication
- **Action**: Authenticate with the Google Cloud SDK and GitHub CLI.
- **Verification**: `gcloud auth list` and `gh auth status` must confirm valid credentials for $(gcloud config get-value project).

## 2. Subprocess: Project & Region Mapping
- **Action**: Verify the active property anchor.
- **Status**: Target Project: `cogctl-gke-v01` | Target Region: `us-central1`.

## 3. Subprocess: VPC & Network Provisioning
- **Action**: Create the isolated network fabric if non-existent or corrupted.
- **Reference**: `infra/master_ignition.sh`.

## 4. Subprocess: Cloud NAT Configuration
- **Action**: Deploy Cloud NAT to ensure private node outbound connectivity.
- **Requirement**: Mandatory for all GKE Genesis clusters to prevent "Blind Birth" (stalled nodes).

## 5. Subprocess: GKE Cluster Provisioning
- **Action**: Provision the target GKE cluster via declarative Terraform.
- **Reference**: `infra/terraform/main.tf`.
- **Current Anchor**: `sovereign-genesis`.

## 6. Subprocess: Node Fabric Verification
- **Action**: Verify that nodes are `Ready` and have registered with the control plane.
- **Verification**: `kubectl get nodes` (Expected: 3 Nodes).

---
**Status**: ACTIVE (v4.0 Re-Forge)
**Source Files**: Refactored from `awake.yaml` and `terraform`.
