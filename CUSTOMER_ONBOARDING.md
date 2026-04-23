# Sovereign Genesis v3.0: Customer Onboarding Guide

This guide provides the instructions for customers to deploy the Sovereign GKE 11-service infrastructure into their own Google Cloud environment, starting from a raw project.

## 0. The Sovereign Genesis (Cluster Creation)
If you do not have a GKE cluster, execute the following to create a Sovereign-ready Autopilot cluster:

```bash
# Set your project ID
gcloud config set project [YOUR_PROJECT_ID]

# Enable Required Services
gcloud services enable container.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com

# Create the GKE Autopilot Cluster
gcloud container clusters create-auto sovereign-genesis     --region us-central1     --project [YOUR_PROJECT_ID]

# Authenticate kubectl to the new cluster
gcloud container clusters get-credentials sovereign-genesis --region us-central1
```

## 1. Prerequisites (GCP Preparation)
Ensure the following are confirmed in your authenticated environment:
- **Project Identity**: `gcloud config get-value project` should match your target project.
- **Cluster Context**: `kubectl config current-context` should point to `sovereign-genesis`.

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
Access the dashboard at: `http://<YOUR_IP>:8004/webui/`

### B. Health Audit
Verify that all 11 services are in a healthy `Running` state:
```bash
kubectl get pods
```

## 4. Key Architectural Notes
- **Namespace**: This deployment is optimized for the `default` namespace fabric.
- **Autopilot Compatibility**: Fully tested on GKE Autopilot with Phase 7.95 "Relaxation Patches" included.
- **Remediations**: Automatically applies all forensic remediations for Kafka and Telemetry synthesis.

---
**Sovereign Support**: For forensic details on specific deadlocks, refer to the [REMEDIATION Documents](https://github.com/gintatkinson/cogctl-gke-v01/blob/main/RELEASE_V3.0_GRADUATION.md) in this repository.
