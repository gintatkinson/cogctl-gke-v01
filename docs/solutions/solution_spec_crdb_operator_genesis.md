# Solution Brief: CockroachDB Operator Bootstrap (Genesis v3.0)

## Problem Statement
The Sovereign GKE Genesis v3.0 restoration failed during Phase 5 (Foundational Databases). Cloud Build logs for build `b02e8dd4` show the following fatal error:
```
error: resource mapping not found for name: "cockroachdb" namespace: "" from "baseline/tfs-controller/manifests/cockroachdb/cluster.yaml": no matches for kind "CrdbCluster" in version "crdb.cockroachlabs.com/v1alpha1"
```
This indicates that the Kubernetes API does not recognize the `CrdbCluster` resource type because the **CockroachDB Operator** and its associated **Custom Resource Definitions (CRDs)** were not installed prior to applying the database cluster manifest.

## Identified Root Cause
- **Manifest Sequencing**: The automated Cloud Build scripts attempt to deploy the database cluster before the operator is active in the cluster.
- **Empty State**: As this is a fresh cluster ("Re-Birth"), it lacks all non-standard controllers and CRDs.

## Solution: Manual Operator Bootstrap
To unblock the automated restoration, the operator must be birthed manually using the sanctioned baseline manifests.

### 1. Verification of Manifests
Ensure the following files are present in the repository:
- `baseline/tfs-controller/manifests/cockroachdb/crds.yaml`
- `baseline/tfs-controller/manifests/cockroachdb/operator.yaml`

### 2. Execution Path
Run the following commands against the active cluster anchor:
```bash
# 1. Install CRDs
kubectl apply -f baseline/tfs-controller/manifests/cockroachdb/crds.yaml

# 2. Install Operator
kubectl apply -f baseline/tfs-controller/manifests/cockroachdb/operator.yaml
```

### 3. Verification of Fix
Verify the operator is running and the resource mapping is available:
```bash
kubectl get crds | grep cockroach
kubectl get pods -n cockroach-operator-system
```

## Restoration Path
Once the operator is confirmed `READY`, re-trigger the automated deployment:
- **Build**: `infra/cloudbuild_deploy_core.yaml` (or equivalent database mirror script).

---
> [!IMPORTANT]
> This fix is a prerequisite for the completion of **SOP-03 (Foundational Bases)** and **SOP-05 (Core Execution)**.
