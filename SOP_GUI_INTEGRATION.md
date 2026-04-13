# SOP: GUI INTEGRATION (Sovereign Control Plane)

This document specifies the architectural standard for integrating a custom GUI (e.g., AI Studio) with the Sovereign TFS Control Plane.

## 1. Authentication Strategy: Keycloak Bypass
Based on the architectural audit (LOG-029), the TFS backend microservices in this baseline do not enforce OIDC at the service layer.
- **Decision**: Keycloak is deprecated as a mandatory Identity Provider (IdP) for the backend APIs.
- **Infrastructure**: Keycloak results in unnecessary resource consumption and 'Identity Deadlocks' during bootstrap.

## 2. API Exposure & Port Mapping
The following gRPC services are defined as the 'Sovereign Integration Points':
- **Context Service**: Port 1010 (Inventory, Topology, and Contextual State)
- **Service Service**: Port 1020 (Path Computation and Service Provisioning)
- **NBI (Northbound Interface)**: Port 1080 (High-level Service Abstraction)

## 3. Connectivity Standards (The Secure Bridge)
- **Development Environment**: Access is granted via `kubectl port-forward` through the secure agent channel.
- **Cloud Integration (AI Studio)**: Access is granted via GKE LoadBalancer, restricted exclusively to authorized AI Studio IP ranges via the `loadBalancerSourceRanges` manifest field.
