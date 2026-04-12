# INTEGRATION STANDARDS: TFS CONTROLLER DASHBOARD

## 1. Service Exposure (Networking)
- **nb-service:** Exposed on **Port 443** via GKE Ingress.
- **Protocols:** HTTPS and WSS (WebSocket Secure).
- **CORS Preflight:** Must support **OPTIONS** requests.
- **WebSockets:** Support for long-lived TCP connections and WSS upgrades.

## 2. CORS Configuration
- **Allowed Origins:** `https://<DASHBOARD_URL>`
- **Methods:** GET, POST, PUT, DELETE, OPTIONS.
- **Headers:** Content-Type, Authorization, X-Requested-With.
- **Credentials:** `true`.

## 3. Identity (Keycloak)
- **Realm:** `tfs`
- **Client ID:** `tfs-dashboard`
- **Access Type:** `public` (PKCE Flow).
- **Redirect URIs:** `https://<DASHBOARD_URL>/*`

## 4. Required Output Environment Variables
- `VITE_TFS_API_URL`
- `VITE_TFS_WS_URL`
- `VITE_KEYCLOAK_URL`
- `VITE_KEYCLOAK_REALM`
- `VITE_KEYCLOAK_CLIENT_ID`

## 5. Security
- Mandatory TLS encryption.
- No self-signed certificates in production.
