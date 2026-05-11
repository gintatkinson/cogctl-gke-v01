# Graduation Implementation Plan (v2.0)
**Directive**: [DIR-2026-05-01-002] & [PROTOCOL-RESET-030]
**Status**: AWAITING EXECUTIVE REVIEW

## 1. Indentation & Structural Integrity Fix
The `harden_manifest.py` logic has been redesigned for syntactic rigidity. The failure in previous builds was caused by whitespace normalization errors during heredoc injection.

### Verified 4-Space Logic
```python
import sys, yaml

def harden():
    """Atomic Manifest Hardener (Verified 4-space logic)"""
    if len(sys.argv) < 5:
        sys.exit(1)
    file_path, service_name, tag, registry = sys.argv[1:]
    try:
        with open(file_path, 'r') as f:
            data = list(yaml.load_all(f, Loader=yaml.FullLoader))
        for doc in data:
            if not doc or 'kind' not in doc:
                continue
            if doc['kind'] in ['Deployment', 'StatefulSet']:
                for container in doc['spec']['template']['spec']['containers']:
                    container['image'] = f"{registry}/{service_name}:{tag}"
                    container['imagePullPolicy'] = 'Always'
        with open(file_path, 'w') as f:
            yaml.dump_all(data, f)
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    harden()
```

## 2. Service Induction Sequence
Services will be induced in batches to ensure dependencies are resolved before dependent logic starts.

1.  **Batch A (The Backbone)**: `context`, `device`, `service`
2.  **Batch B (Orchestration)**: `slice`, `pathcomp`, `nbi`
3.  **Batch C (Intelligence)**: `automation`, `monitoring`, `webui`
4.  **Batch D (Analysis)**: `analytics`, `telemetry`

## 3. GitHub Graduation Issues Mapping
The following issues are staged for creation upon induction success:
- `GRAD-001`: Verify Context Service binding to CockroachDB (NS: default).
- `GRAD-002`: Verify Device Driver inventory via gRPC.
- `GRAD-011`: Verify Telemetry data stream from NATS to InfluxDB.

## 4. Post-Induction Verification (Step #14 ➔ #15)
Success of Step #14 is defined by:
- All 11 pods in `Running` state (1/1 READY).
- `kubectl get services` showing correct exposure (LoadBalancer for NBI, NodePort for WebUI).

---
**Agent Recommendation**: Proceed with the authorized induction once the logic is visually inspected by the Executive.
