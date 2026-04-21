# TECHNICAL IMPLEMENTATION LOG: THE BLACK BOX

## 1. System Recovery Records

### REC-001: Toolchain Path Hardening (Succession Regression Audit)
- **Discovery**: SDK binaries (`gcloud`, `gh`) failed to load in non-interactive shells and orchestration scripts due to legacy absolute paths (`/home/parallels/...`).
- **Remediation**: Expanded logic to mandate **Mandatory Script-Level Path Sanitization**. Replaced all absolute calls with relative calls anchored by a reconciled, Homebrew-aware `PATH`.

### REC-002: Service Endpoint Deadlocks
- **Discovery**: GKE Autopilot probes failed for 2nd-container sidecars (NGINX/Envoy), preventing pod readiness.
- **Remediation**: Implemented a Surgical Probe Relaxation Patch (Removing readiness/liveness probes from sidecars).

### REC-003: Core Configuration Gap (CRDB_NAMESPACE)
- **Discovery**: `contextservice` crashed due to missing `CRDB_NAMESPACE` setting.
- **Remediation**: Permanently injected variable into the deployment manifest. Logged in Solution Spec.

### REC-004: Ingress Perimeter Alignment
- **Discovery**: Ingress resource birthed with the wrong selector for the NGINX controller.
- **Remediation**: Corrected deployment labels and updated ingress mapping.

### REC-005: NBI Broker Synchronization OOM Deadlock
- **Discovery**: GKE Autopilot executed an OOM-kill on `nbiservice` during its initial Kafka topic synchronization due to a massive memory spike upon successful broker connection.
- **Remediation**: Surgically elevated the deployment resource limits to `memory=2Gi` to bridge the initialization spike. Logged in Solution Spec.

### REC-006: Readiness Dependency & Manifest Hardening
- **Discovery**: WebUI service failed ignition due to a `ModuleNotFoundError` for `flask-healthz` (missing from unified requirements) and a `Werkzeug 3.0` regression.
- **Remediation**: Anchored exact pins (`flask-healthz==1.0.1`, `Werkzeug==2.3.7`) in the Gold Master foundation.

### REC-007: Perimeter IP Drift & Firewall Deadlock
- **Discovery**: LoadBalancer identity shifted during the v3.0 GKE re-birth, causing 404 deadlocks. VPC firewall rules also isolated external traffic from the NGINX controller.
- **Remediation**: Anchored static IP `34.31.116.202` in persistence metadata and injected public ingress rules (TCP 80/443) into the genesis fabric.

### REC-008: CRD Propagation & Sequential Hardening
- **Discovery**: Build #14 failed due to a race condition where `CrdbCluster` was applied before the CockroachDB Operator was birthed, causing a 'resource mapping not found' error.
- **Remediation**: Implemented deterministic sequencing in `cloudbuild_final.yaml`. Mandatory `kubectl wait` for CRD stability followed by `kubectl rollout status` for the operator manager before applying the database cluster manifest.

### REC-010: Database Manifest Validation & Restoration
- **Discovery**: Build #17 failed with `apiVersion not set` because `nats/cluster.yaml` was a Helm values file misidentified as a K8s resource by wildcard matching.
- **Remediation**: Surgically purged the toxic configuration file and hardened `cloudbuild_final.yaml` to explicitly target verified manifests: `nats_fidelity.yaml` and `kafka/single-node.yaml`.

### REC-011: WebUI Internal Linkage & VNT-Manager Sync
- **Discovery**: Build #18 failed with `ModuleNotFoundError: No module named 'vnt_manager'` in the WebUI service.
- **Remediation**: Expanded the WebUI Docker context to include internal dependencies (`common`, `vnt_manager`, and service descriptors).

### REC-012: Deterministic Path Resolution & Source-Floor Alignment
- **Discovery**: Build #19 failed with persistent `ModuleNotFoundError` despite context expansion due to package nesting mismatches.
- **Remediation**: Implemented a "Source-Floor" architecture in the WebUI Dockerfile, copying the entire `src/` tree and explicitly anchoring `PYTHONPATH=/var/teraflow` to ensure absolute parity with the developer resolution environment.

### REC-013: Unified Proto-Dependency Restoration
- **Discovery**: Build #20 failed with `ModuleNotFoundError` in the WebUI orchestrator because the `common/proto` symlink was dangling (the `proto/` tree was outside the build context).
- **Remediation**: Transitioned to a "Unified Context" model, ingesting both the `src/` and `proto/` trees into the container and surgically reconciling the symlink bridge at `/var/teraflow/common/proto`.

### REC-014: Deployment-vs-Synthesis Alignment (The Final Loop)
- **Discovery**: Build #21 failed with persistent `ModuleNotFoundError` despite the structural fix because the GKE deployment manifest points to a tagged image (`webui:2026-04-20`). The deployment pipeline was simply re-birthing the *old* unhardened binary from the registry.
- **Remediation**: Re-triggered the surgical "Gold Master" synthesis build to physically bake the Source-Floor architecture and Symlink Reconciliation into the Artifact Registry before triggering the final production rollout.

### REC-016: Dependency Floor Harmonization
- **Discovery**: Build #22 failed with `ResolutionImpossible` due to a structural conflict between the modern Protobuf 5.x runtime and the ancient gRPC 1.47 floor.
- **Remediation**: Attempted to modernize the gRPC floor to 1.62.x, which was subsequently overridden by the Lead Architect in favor of a strict baseline restoration.

### REC-017: Strict Baseline Restoration & Protobuf Downgrade
- **Discovery**: The "Modernization" path (Phase 7.13) presented excessive risk to the enclave's foundational stability given the scope of the ETSI TFS codebase.
- **Remediation**: Reverted the dependency floor to a strictly pinned state: `protobuf==3.20.3` and `grpcio==1.47.5`. Mutated the synthesis tag to `2026-04-21-rc2` to ensure a clean, cacheless birth of the orchestrator.

### REC-018: Build-Time Gencode Synthesis & Alignment
- **Discovery**: Phase 7.14 failed with `ImportError` due to a collision between the historical library (3.20.3) and the modern gencode (v6.31.0).
- **Remediation**: Re-engineered the Docker build process to autonomously synthesize the gRPC gencode *at build-time* using the container's own library environment. Applied the 'Readiness Relaxation Patch' (60s delay) to ensure sidecar stability during the final graduation rollout.

### REC-019: Manifest Variable Hardening
- **Discovery**: Build #27 failed due to an expansion deadlock where shell-level variables were lost during the Cloud Build execution phase.
- **Remediation**: Transitioned the Gold Master manifest to declarative substitutions (_SERVICES, _TAG, REGISTRY). This ensures cryptographic continuity and variable stability for the final rc3 birth.

### REC-020: Environmental Variable Hardening
- **Discovery**: Build #29 failed due to a shadowing deadlock where declarative substitutions were lost within the nested shell context of the building container.
- **Remediation**: Transitioned to explicit environmental injection, passing manifest constants directly into the container's environment space. This is the terminal structural fix for the Sovereign Genesis graduation.

### REC-021: Total Variable Isolation
- **Discovery**: Build #31 failed during the pre-parsing phase because Cloud Build attempted to expand shell-internal tokens (e.g., $${ADDR}) as built-in substitutions.
- **Remediation**: Implemented 'Double-Dollar' escaping ($$SERVICES, $$TAG, $${ADDR}) to isolate all shell-internal variables relative to the Cloud Build executor, ensuring absolute manifest stability for the final rc3 birth.

### REC-022: Gencode Resolution Alignment
- **Discovery**: Phase 7.21 `rc3` synthesis (Build #36/37) failed with a compiler deadlock because `grpc_tools.protoc` could not resolve internal imports (e.g., `import "context.proto"`) due to a misaligned include path.
- **Remediation**: Hardened the orchestrator synthesis by shifting the include root to `-I=proto`, aligning the compiler viewport with the internal schema logic and ensuring successful birth of the graduation stubs.

### REC-031: Manifest Expansion Hardening
- **Discovery**: RC4 artifacts were birthed as 'Untagged' due to a Cloud Build variable expansion collision ($$TAG expansion failure).
- **Remediation**: Hardened the Gold Master manifest to utilize direct substitution injection ($_TAG, $_REGISTRY), ensuring 100% cryptographic tag parity during synthesis.

---

## 2. Immutable Operational Constraints
- **Constraint 01**: All infrastructure changes MUST be executed via Cloud Build.
- **Constraint 02**: No manual `kubectl` patches are allowed without manifest back-porting.
- **Constraint 03**: Every session must begin with a Technical Health Audit (SOP-01).

---
**Status**: ACTIVE
**Source of Truth**: Aligned with the 1-6 SOP Framework.
docs/incidents/13_SCREEN_AUDIT.md
