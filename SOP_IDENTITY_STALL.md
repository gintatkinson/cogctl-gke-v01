# SOP: Identity Mirroring Stall (Secret Key Realignment)

## 1. Problem Definition
*   **The Problem**: A microservice (e.g., `monitoringservice`) references a Kubernetes secret (e.g., `qdb-data`) via `envFrom`, but crashes or fails to populate service endpoints despite the pod being `Running`.
*   **The Symptom**: `kubectl get endpoints` returns `EMPTY` for the service. Logs show application-level connection failures (e.g., "QuestDB not found") or `CrashLoopBackOff`.
*   **The Root Cause**: The Secret exists but uses generic keys (`username`, `password`), while the application code expects specific environment variables (e.g., `METRICSDB_USER`, `METRICSDB_PASS`). Since `envFrom` maps keys directly to variable names, the application "sees" only the generic variables and ignores them.

## 2. Verification Protocol
1.  **Check Service Endpoints**:
    ```bash
    kubectl get endpoints <service_name>
    ```
    If empty, the pod is not marked as `Ready`.
2.  **Audit Secret Keys**:
    ```bash
    kubectl get secret <secret_name> -o jsonpath='{.data}'
    ```
3.  **Audit Source Code**:
    Search the service source for `os.environ.get` to identify the expected variable names.

## 3. Resolution Protocol
1.  **Nuclear Mapping**: Re-create the secret with BOTH generic and specific keys to ensure total coverage.
    ```bash
    kubectl create secret generic qdb-data \
      --from-literal=username=admin \
      --from-literal=password=quest \
      --from-literal=METRICSDB_USER=admin \
      --from-literal=METRICSDB_PASS=quest
    ```
2.  **Maturation Trigger**: Force a rollout of the affected microservices.
    ```bash
    kubectl delete pods -l app=<service_name>
    ```

## 4. Governance
*   All infrastructure secrets MUST be birthed in the `default` namespace.
*   Secret names MUST match the `envFrom` references in the official ETSI manifests.
