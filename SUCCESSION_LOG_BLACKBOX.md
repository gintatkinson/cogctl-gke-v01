# SUCCESSION LOG: THE BLACK BOX (FLIGHT RECORDER)

## Purpose
Knowledge acquired during failure is the most critical asset for recovery. This high-frequency log records tactical discoveries, dependency conflicts, and failed attempts *immediately* during SOP execution to survive system crashes.

---

## I. Genesis Recovery Stream

### BB-001: Antigravity Context Persistence
- **Discovery:** In the event of a hard crash, the agent's internal thought history is lost.
- **Lock:** The **Succession Log** (GitHub) and this **Black Box** (Local/Sync) are the only survival mechanisms.
- **Protocol:** Manual sync/push is required regularly even mid-SOP until agent authentication is established.

### BB-002: Service Timeout (Handshake Storms)
- **Discovery:** Rapid-fire deployment of microservices causes GRP-web timeouts.
- **Lock:** Implemented **The Backoff Law** (mandatory sleep) in `infra/bootstrap.sh`.

### BB-003: Viewport Violation (RECOVERY)
- **Discovery:** Attempting to use local Docker for Artifact Sync violated the **Viewport Principle** (Rule 2) and failed due to missing toolchains on the host.
- **Lock:** All binary movements MUST occur within the GCP Data Plane (Cloud Build).
- **Protocol:** Use `gcloud builds submit` with `infra/cloudbuild_sync.yaml`.
