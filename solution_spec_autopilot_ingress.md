# Solution Specification: Autopilot Ingress Adaptation

## 1. Problem Definition: Ingress Deadlock
GKE Autopilot prevents the use of `DaemonSets` with `hostPort` (8003, 4433, etc.), resulting in zero-capacity for the NGINX Ingress controller and indefinite LoadBalancer IP pending status.

## 2. Strategic Resolution: GKE-Native Migration
To ensure compatibility with Autopilot's hardened networking and security fabric, we will refactor the ingress layer as follows:

### 2.1 Deployment Conversion
The NGINX Ingress Controller will be migrated from `DaemonSet` to `Deployment`. This allows the scheduler to place pods on nodes with sufficient resource headroom.

### 2.2 Network Decoupling
- **Removal of hostPort**: Standard TCP Port 80/443 mapping will be handled by the Cloud LoadBalancer service, not on the individual node host network.
- **Autopilot Compliance**: Resource requests will be added to ensure the pods satisfy the mandatory Autopilot scheduling policy.

### 2.3 Bridge Restoration
The `nginx-ingress-sovereign` service will be used to bridge the public LoadBalancer IP to the new deployment pods using the label `name: nginx-ingress-microk8s-controller-opt`.

## 3. Implementation Plan
1. Delete the ghost `DaemonSet` from the `ingress` namespace.
2. Apply the refactored `nginx-ingress-controller-opt.yaml` manifest.
3. Apply the Sovereign Service and RBAC layers.
4. Verify the IP assigned to the `nginx-ingress-sovereign` service.

## 4. Trustworthy Audit
A successful adaptation is confirmed only when:
- `kubectl get pods -n ingress` shows 100% readiness.
- The LoadBalancer IP is retrieved and reported successfully in the ignition log.
