# Incident Report: TelemetryService CrashLoopBackOff

**Date:** 2026-04-29
**Component:** `telemetryservice` (Sovereign GKE Genesis v3.1)

## Problem Description
The `telemetryservice-c687bd966-wzgn7` pod entered a `CrashLoopBackOff` state. A diagnostic analysis revealed that the `backend` container was healthy, while the `frontend` container crashed continuously on startup.

The container logs for `frontend` reported the following fatal error:
```
Exception: Setting(CRDB_SSLMODE) not specified in environment or configuration
```
This indicated a configuration drift. While the local manifest source-of-truth (`./baseline/tfs-controller/manifests/telemetryservice.yaml`) accurately contained the required `CRDB_SSLMODE: disable` environment variable, the active deployment in the cluster was missing this critical value.

## Resolution
To safely reconcile the environment without impacting the other 10 microservices, the baseline manifest was forcefully reapplied to the cluster:

```bash
kubectl apply -f ./baseline/tfs-controller/manifests/telemetryservice.yaml
```

Because Kubernetes handles differential updates and the deployment specifies `strategy: type: Recreate`, this cleanly terminated the defective pod and spawned a healthy instance with the corrected environment, restoring 2/2 Ready status. No other services were impacted.
