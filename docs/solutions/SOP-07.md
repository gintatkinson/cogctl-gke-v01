# SOP-07: State Audit (Tabula Rasa Verification)

## 1. Subprocess: Project Registry Audit
- **Action**: Query the Global Project Registry for legacy or unauthorized projects.
- **Verification**: `gcloud projects list --filter="name:cogctl-gke-*"`
- **Success Criteria**: Zero `ACTIVE` projects found. Any `DELETE_REQUESTED` projects must be documented as inert.

## 2. Subprocess: Orphaned Resource Audit
- **Action**: Verify the regional void for compute and network resources.
- **Verification 2.1 (Compute)**: `gcloud compute instances list --project [PROJECT_ID]` (Should be empty).
- **Verification 2.2 (Disks)**: `gcloud compute disks list --project [PROJECT_ID]` (Should be empty).
- **Verification 2.3 (VPC)**: `gcloud compute networks list --project [PROJECT_ID]` (Only `default` permitted if not yet purged).

## 3. Subprocess: Local Configuration Audit
- **Action**: Verify the sterilization of the local SDK and Kubecontext.
- **Verification 3.1**: `gcloud config get-value project` (Must be `unset` or `(unset)`).
- **Verification 3.2**: `ls ~/.kube/config` (Must return `No such file or directory`).

## 4. Subprocess: Credential Audit
- **Action**: Verify the absence of active service account keys.
- **Verification**: `gcloud iam service-accounts list --project [PROJECT_ID]` (Should be empty).

---
**Status**: ACTIVE (Sovereign v4.0)
**Constraint**: Failure of any verification step prohibits the execution of `IP_13` (Project Birth).
