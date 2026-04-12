# SOP: TFS BASELINE CORE

## STAGE 0: Recovery Checkpoint (Mandatory)
1. **Verify Vault:** Ensure `SUCCESSION_LOG.md` confirms `SOP-VAULT COMPLETE`.
2. **Verify Keycloak:** Ensure Keycloak internal endpoints are responsive.
3. **Verify Registry:** Confirm all core images are present in GCP Artifact Registry.

## I. Microservice Deployment (The Baseline)
1. **Execute official `tfs.sh`:** Use the `deploy` flag with the **mandated architectural whitelist** of components.
2. **Fidelity Check:** Ensure no manual overrides to the ETSI manifests are applied (The Baseline Fidelity Lock).
3. **Internal Verification:** Verify that all microservices transition to `Running` state within GKE.

## II. Service Handshaking
1. **Check Logs:** Verify gRPC handshakes between Context, Device, and Service modules.
2. **Backoff Check:** Ensure mandatory cooldowns were respected during deployment (The Backoff Law).

## III. Persistence Checkpoint (Sovereign Save)
1. **Commit:** `git commit -m "CHECKPOINT: SOP-CORE COMPLETE"`.
2. **Push:** Push to GitHub.
