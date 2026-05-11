# CUSTOMER README: Sovereign Genesis Enclave v3.2.0

## Preamble
This repository contains the **Sovereign Genesis v3.2.0 Sovereign-Release**, a fully parameterized, environment-agnostic blueprint for deploying a hardened GKE Enclave. All legacy project references have been eradicated to allow for clean, multi-tenant installation on customer-owned infrastructure.

## Operational Prerequisites
- **GCP Project**: A blank Google Cloud project with billing enabled.
- **Authentication**: Local environment must be authenticated via `gcloud auth login` and `gcloud auth application-default login`.
- **APIs**: The following APIs must be enabled in the target project:
  - `compute.googleapis.com`
  - `container.googleapis.com`
  - `cloudbuild.googleapis.com`
  - `artifactregistry.googleapis.com`

## Customer Ignition Payload

### 1. Cloud Build Ignition (Infrastructure & Application)
Execute the following command from the root of this repository to initiate the cold start:

```bash
gcloud builds submit --config infra/awake.yaml \
  --project="<CUSTOMER_PROJECT_ID>" \
  --substitutions=\
_CUSTOMER_PROJECT_ID="<CUSTOMER_PROJECT_ID>",\
_CUSTOMER_REGISTRY="<TARGET_REGION>-docker.pkg.dev/<CUSTOMER_PROJECT_ID>/sovereign-tfs",\
_TARGET_REGION="<TARGET_REGION>",\
_TARGET_ZONE="<TARGET_ZONE>",\
_CLUSTER_NAME="sovereign-genesis"
```

### 2. Terraform Variable Injection
Create a file named `infra/terraform/terraform.tfvars` with the following content:

```hcl
project_id   = "<CUSTOMER_PROJECT_ID>"
region       = "<TARGET_REGION>"
zone         = "<TARGET_ZONE>"
cluster_name = "sovereign-genesis"
```

## System Stewardship
Following ignition, the system state will be tracked in `infra/persistence.template.json` (transitioned to `active`). Refer to the `docs/` directory for operational SOPs and the Sovereign Directives.

---
**Build Anchor**: b4748ed
**Release**: v3.2.0-Sovereign-Release
