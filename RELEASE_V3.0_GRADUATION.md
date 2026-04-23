# Sovereign Genesis v3.0: Graduation Release

This release codifies the total synthesis and graduation of the Sovereign GKE 11-service infrastructure. It is designed for 100% reproducibility by any agent with minimal skill.

## Reproducibility Guide (Zero-to-Graduation)

### 1. Pre-Requisites
- Access to the GKE Cluster (`cogctl-gke-v01`).
- Authenticated `gcloud` and `kubectl` CLI.
- Repository cloned and aligned to the `v3.0-graduation` tag.

### 2. Execution Path (The Graduation Ignition)
To reproduce the entire 11-service stack with all remediations (Kafka, Telemetry, NBI), execute the following command from the root of the repository:

```bash
gcloud builds submit --config infra/cloudbuild_graduation_final.yaml --substitutions=_TAG="v3.0-grad" .
```

### 3. Verification Path
Once the build completes, verify the perimeter accessibility:

```bash
# Retrieve the WebUI IP
kubectl get service webuiservice -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

# Verify 11/11 service stability
kubectl get pods
```

## Included Remediations
- **Namespace Shadowing**: Fixed via Absolute Workdir Enforcement.
- **Kafka Handshake**: Fixed via API Version 3.7.0 alignment.
- **Messaging Identity**: Fixed via ADVERTISED_LISTENERS patching.
- **Telemetry Synthesis**: Fixed via multi-container split.
- **NBI Stability**: Fixed via total dependency saturation.

---
**Sovereign Status**: Graduated & Stable.
**Access URL**: http://34.68.33.204/webui/
