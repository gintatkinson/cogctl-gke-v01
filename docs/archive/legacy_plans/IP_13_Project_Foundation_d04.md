# Implementation Plan: IP_13 (Project Foundation - d04 Genesis)

**Status**: DRAFT (Awaiting Ignition Authorization)
**Author**: Sovereign AI Agent (Disciplined Alignment)
**Reference**: [SOVEREIGN DIRECTIVES.MD](../../solutions/SOVEREIGN%20DIRECTIVES.MD)

## 1. Objectives
Establish a pristine GCP Project foundation (`cogctl-gke-d04`) to host the Sovereign v4.0 infrastructure, ensuring total isolation from legacy metadata.

## 2. Problems to Overcome
- **Metadata Contamination**: Persistent pointers to `v01` in local configs.
- **Billing Deadlocks**: Inability to link a project without an authenticated Billing Account ID.
- **API Latency**: GKE/Cloud Build failures caused by un-propagated API permissions.

## 3. Phase 1: Project Birth (The D04 Container)
- **Action**: Create the project `cogctl-gke-d04`.
- **Command**: `gcloud projects create cogctl-gke-d04 --name="Sovereign Genesis v4.0"`
- **Verification Gate**: `gcloud projects describe cogctl-gke-d04` must return `lifecycleState: ACTIVE`.

## 4. Phase 2: Billing & API Hydration
- **Action**: Link the project to the master billing account (`0122A4-0EC04A-79B42F`) and enable core GKE/Build APIs.
- **Command (Billing)**: `gcloud billing projects link cogctl-gke-d04 --billing-account=0122A4-0EC04A-79B42F`
- **Command (APIs)**: `gcloud services enable container.googleapis.com compute.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com --project cogctl-gke-d04`
- **Verification Gate**: `gcloud services list --enabled --project cogctl-gke-d04` must confirm `container.googleapis.com` and `cloudbuild.googleapis.com` are enabled.

## 5. Phase 3: Resource Anchoring
- **Action**: Create Artifact Registry for induction.
- **Command**: `gcloud artifacts repositories create sovereign-tfs --repository-format=docker --location=us-central1 --project cogctl-gke-d04`

---
**Verification Gate**: Absolute Zero state must be maintained until Phase 1 ignition. No `v01` context permitted.
