# SOP-02: Security & Identity Orchestration

## 1. Subprocess: Secret Manager Integration
- **Action**: Sync project-level secrets (GitHub PATs, API keys) into the local VPC scope.
- **Reference**: `gcloud secrets versions access latest --secret="ETSI_GITLAB_PAT"`.

## 2. Subprocess: Kubernetes Secret Mirroring
- **Action**: Inject vaulted secrets into the target GKE namespace.
- **Reference**: `infra/cloudbuild_vault.yaml`.

## 3. Subprocess: RBAC & IAM Mapping
- **Action**: Configure Kubernetes Role-Based Access Control and Bind GSA (Google Service Accounts) to KSA (Kubernetes Service Accounts) via Workload Identity.

## 4. Subprocess: Database Credential Generation
- **Action**: Generate high-entropy credentials for foundation services (CockroachDB, NATS, Kafka).

## 5. Subprocess: Image Registry Authentication
- **Action**: Create `regcred` secrets for the GCR/Artifact Registry to allow pod image pulls.

---
**Status**: ACTIVE
**Source Files**: Refactored from `SOP_VAULT.md`, `SOP_IDENTITY_STALL.md`.
