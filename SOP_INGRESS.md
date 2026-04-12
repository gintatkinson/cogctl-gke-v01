# SOP: CONNECTIVITY & INGRESS

## STAGE 0: Recovery Checkpoint (Mandatory)
1. **Verify Core:** Ensure `SUCCESSION_LOG.md` confirms `SOP-CORE COMPLETE`.
2. **Verify Services:** Confirm all core microservices are `Running` and stable.

## I. GKE Ingress Configuration
1. **TLS Provisioning:** Configure ManagedCertificates or Secret-based TLS for Ingress.
2. **BackendConfig:**
   - Configure **WSS (WebSocket Security)** support.
   - Set connection timeouts and draining for long-lived streams.
3. **Frontend Expiry:** Ensure **Port 443** is open and routing to `nb-service`.

## II. CORS & Security
1. **CORS Policy:** Configure `nb-service` to allow origins from the Cloud Run Dashboard.
2. **WebSocket Pre-flight:** Verify **OPTIONS** requests for ORS pre-flight are handled.

## III. Persistence Checkpoint (Sovereign Save)
1. **Commit:** `git commit -m "CHECKPOINT: SOP-INGRESS COMPLETE"`.
2. **Push:** Push to GitHub.
