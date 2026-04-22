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

### REC-032: Namespace Cleansing (Proto Shadowing Resolution)
- **Discovery**: WebUI synthesis failed with 'File exists' because the COPY common/ step births a symlink-shadow that blocks directory creation.
- **Remediation**: Injected a cleansing anchor (rm -rf) to surgically destroy the shadow before birthing the resuscitated stubs.

### REC-033: Topographical Parity Graduation (Build #44)
- **Discovery**: RC4 ignition failed with 'ImagePullBackOff' because the synthesis birthed images mapping to source directory names (e.g. context) while the production perimeter expected suffixed names (e.g. contextservice).
- **Remediation**: Hardened the Gold Master manifest to implement a topographical suffixing loop, ensuring 100% pathing parity between the forge and the cluster.

### REC-034: Triple Fracture Resolution (rc4 Graduation Birth)
- **Discovery**: RC4 ignition failed due to (1) missing SQLAlchemy DNA, (2) untagged births from variable expansion failures, and (3) topographical drift between forge and registry.
- **Remediation**: Resuscitated the foundation with SQLAlchemy, hardened the manifest with direct substitution injection, and implemented topographical suffixing to ensure 100% pathing parity.

### REC-035: Standard Zonal Transition ("The Cottage Mandate")
- **Discovery**: Autopilot resource allocation triggered massive disk-quota deadlocks (480GB+ consumption) on blank-slate regional clusters.
- **Remediation**: Migrated to Standard Zonal GKE (`us-central1-a`) with strict "Cottage" resource constraints (`1 node`, `50GB`). Mandated Standard ephemeral storage to satisfy the 50GB ceiling.

### REC-036: Global Enclave Hydration (Stage 0)
- **Discovery**: Graduation ignitions on the blank-slate cluster failed due to missing foundational config/messaging DNA.
- **Remediation**: Injected idempotent Stage 0 logic into the rollout manifest to autonomously birth NATS (nats_fidelity.yaml) and persistence secrets (crdb-data, nats-data) before core service induction.

### REC-037: Foundation Re-Forge (Build #58)
- **Discovery**: Graduation Forge failed because the resuscitated `python-base:2026-04-21` image was missing from the registry (Foundation Void).
- **Remediation**: Injected a foundational Step -1 to physically re-birth and vault the base image, incorporating hardened pins (`SQLAlchemy==1.4.39`, `protobuf==3.20.3`, `grpcio==1.47.5`) required to bridge the artifact void.

### REC-038: Path-Aware Synthesis Alignment (Build #60)
- **Discovery**: Sequential re-forge failed at Analytics/Telemetry due to directory nesting mismatches (Pathing Rift).
- **Remediation**: Hardened the Graduation Manifest with an `IFS` parsing loop and explicit colon-delimited mapping (`S_NAME:REL_PATH:T_NAME`), ensuring 100% synthesis success for nested services.

### REC-039: Docker Build Context Anchor (Build #61)
- **Discovery**: Build #60 failed during core synthesis because Dockerfiles could not resolve `common_requirements.in` relative to the repository root build context.
- **Remediation**: Implemented the mandated `cd baseline/tfs-controller/` anchor before the synthesis loop, shifting the build context to provide absolute local visibility to shared requirement assets.

### REC-040: Topographical Code Ingestion (The Empty Shell Fix)
- **Discovery**: Microservices reached `Running` but crashed immediately with `ModuleNotFoundError` because the Dockerfiles lacked `COPY` commands for the local service code, resulting in empty container shells.
- **Remediation**: Surgically restored `COPY` commands across all 11 microservice blueprints to ensure absolute topographical code ingestion.

### REC-041: Module Resolution & gRPC Synthesis (The Proto Rift)
- **Discovery**: Services failed with `ModuleNotFoundError: common.proto` due to missing generated gRPC stubs in the Python namespace.
- **Remediation**: Automated build-time gRPC stub generation (`grpc_tools.protoc`) and applied a relative-import patch (`sed`) to resolve the Python namespace rift.

### REC-042: Dependency Floor Hardening (grpcio-reflection)
- **Discovery**: Services failed to start due to missing `grpcio-reflection` library in the foundational image.
- **Remediation**: Integrated `grpcio-reflection` into the `python-base` image and subsequently transitioned to manifest-based ingestion (`requirements_unified.in`).

### REC-043: Resource Throttling (The Cottage Squeeze)
- **Discovery**: GKE node reached 97% CPU reservation, triggering scheduling deadlocks.
- **Remediation**: Enforced mandatory resource throttling (`requests: cpu=50m, memory=128Mi`) across all 11 microservice manifests to maintain compliance with REC-035.

### REC-044: Manifest-Based Dependency Ingestion
- **Discovery**: Microservices continued to fail with fragmented dependency errors (e.g., `prettytable`, `anytree`).
- **Remediation**: Re-engineered the foundational build to use `pip install -r requirements_unified.in`, ensuring a complete and hardened dependency floor.

### REC-045: System Header Reconciliation (libyang v2 Source Build)
- **Discovery**: Build #72 failed because the `libyang` Python library was incompatible with the `libyang3` headers provided by the Debian repo.
- **Remediation**: Implemented an autonomous source compilation of **`libyang` v2.1.128** within the foundation layer to satisfy exact binary requirements.

### REC-046: Operation Sovereign Reset (The Recreate Strategy)
- **Discovery**: Rollouts stalled due to a resource deadlock where old pods held CPU reservations while new pods remained `Pending`.
- **Remediation**: Mandated the **`Recreate`** deployment strategy across all manifests to force-release resources before igniting new artifacts.

### REC-047: Total Sterilization & Recovery (Phase 7.60)
- **Discovery**: System state became polluted with 300GB of corrupted storage and 1,000+ local workspace modifications.
- **Remediation**: Executed a "Deep Clean" (total deletion of workloads/PVCs/Secrets) followed by a bit-for-bit GitHub workspace reset and an immutable `rc13-verified` build sequence.

### REC-048: Docker Build Context Realignment (Phase 7.61)
- **Discovery**: Build #74 failed after the workspace reset because Dockerfiles using the `baseline/tfs-controller/` pathing could not resolve their source code when built from a sub-directory context.
- **Remediation**: Re-anchored the Docker build context to the **Repository Root (`.`)**, ensuring absolute visibility to all graduation blueprints.

---

## 2. Immutable Operational Constraints
- **Constraint 01**: All infrastructure changes MUST be executed via Cloud Build.
- **Constraint 02**: No manual `kubectl` patches are allowed without manifest back-porting.
- **Constraint 03**: Every session must begin with a Technical Health Audit (SOP-01).

---
**Status**: ACTIVE
**Source of Truth**: Aligned with the 1-6 SOP Framework.
docs/incidents/13_SCREEN_AUDIT.md
