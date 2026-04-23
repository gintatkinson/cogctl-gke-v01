# Sovereign Genesis v3.0: Customer Onboarding Guide

This guide provides the instructions for customers to deploy the Sovereign GKE 11-service infrastructure into their own Google Cloud environment.

## 1. Prerequisites (GCP Preparation)
Before deployment, ensure the following are configured in your Google Cloud Project:
- **Enable APIs**:
  - Cloud Build API (`cloudbuild.googleapis.com`)
  - Artifact Registry API (`artifactregistry.googleapis.com`)
  - GKE API (`container.googleapis.com`)
- **GKE Cluster**: A running GKE Autopilot or Standard cluster.
- **CLI Tools**: `gcloud` and `kubectl` authenticated to your project and cluster.

## 2. Infrastructure Deployment
To deploy the full Sovereign stack (including messaging and persistence backbones), clone this repository and execute the graduation synthesis from the root directory:

```bash
# Ignite the 11-service Graduation
gcloud builds submit --config infra/cloudbuild_graduation_final.yaml --substitutions=_TAG="v3.0-customer" .
```

## 3. Post-Deployment Verification
Once the Cloud Build process completes successfully, perform the following verification:

### A. Connectivity Audit
Retrieve the public IP address for your Sovereign WebUI:
```bash
kubectl get service webuiservice -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```
Access the dashboard at: `http://<YOUR_IP>/webui/`

### B. Health Audit
Verify that all 11 services are in a healthy `Running` state:
```bash
kubectl get pods
```

## 4. Key Architectural Notes
- **Namespace**: This deployment is optimized for the `default` namespace fabric.
- **Persistence**: Includes pre-configured Kafka and QuestDB instances namespace-aligned for internal DNS resolution.
- **Remediations**: Automatically applies all Phase 7.95 remediations (Handshake reconciliation, Multi-container synthesis, etc.).

---
**Sovereign Support**: For forensic details on specific deadlocks, refer to the [REMEDIATION Documents](https://github.com/gintatkinson/cogctl-gke-v01/blob/main/RELEASE_V3.0_GRADUATION.md) in this repository.
