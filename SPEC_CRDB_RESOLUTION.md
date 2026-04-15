# SOLUTION SPECIFICATION: CRDB_NAMESPACE Resolution
**Date:** 2026-04-15
**Component:** `contextservice`
**Domain:** Database Topology / Foundation

## 1. Problem Statement
The ETSI TFS `contextservice` (Version 3.0.0+) implements a hard database connection check in `service/database/Engine.py`. One of the mandatory environment variables for this check is `CRDB_NAMESPACE`. If this variable is null or missing, the service raises a fatal exception during startup, causing a `CrashLoopBackOff`.

## 2. Technical Evidence
### Crash Trace (Forensic Audit):
```python
File "/var/teraflow/context/service/database/Engine.py", line 29, in get_engine
  CRDB_NAMESPACE = get_setting('CRDB_NAMESPACE')
File "/var/teraflow/common/Settings.py", line 70, in get_setting
  raise Exception('Setting({:s}) not specified in environment or configuration'.format(str(name)))
Exception: Setting(CRDB_NAMESPACE) not specified in environment or configuration
```

## 3. Resolution Logic
The variable `CRDB_NAMESPACE` must be set to the namespace where the CockroachDB service endpoint is hosted. In the GKE Genesis architecture, this is defaults to `"default"`.

### Implementation Requirement:
- **Baseline Hardening**: The variable MUST be defined directly in the `Deployment` manifest or the core `ConfigMap` to ensure persistence across "Core Refreshes".
- **Value**: `"default"`
- **Protocol**: Always verify `kubectl get secret crdb-data` contains the matching database credentials.

## 4. Immutable Safeguard
Any agent or script performing a "total reset" or "re-ignition" MUST verify the presence of this variable before marking Phase 5 as success.

---
**Status:** IMPLEMENTED (Phase 6 Restoration)
**Issue Reference:** # (To be populated)
