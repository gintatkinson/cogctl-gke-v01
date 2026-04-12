#!/bin/bash
# GitHub Succession Synchronization Engine v1.0

PROJECT_ID="cogctl-gke-v01"
REPO_OWNER="gintatkinson"
REPO_NAME="cogctl-gke-v01"

# 1. Retrieve the Sovereign Token
PAT=$(/home/parallels/google-cloud-sdk/bin/gcloud secrets versions access latest --secret="GITHUB_SOVEREIGN_PAT" --project="$PROJECT_ID")

create_issue() {
    local title=$1
    local body=$2
    local label=$3
    
    echo "Creating Issue: $title..."
    curl -s -X POST \
        -H "Accept: application/vnd.github+json" \
        -H "Authorization: Bearer $PAT" \
        https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/issues \
        -d "$(jq -n --arg t "$title" --arg b "$body" --arg l "$label" '{title: $t, body: $b, labels: [$l]}')"
}

# --- LOG SERIES (Architectural) ---
create_issue "LOG-001: Cost Stewardship - GKE Autopilot Choice" "Decision: Use GKE Autopilot for 'Pay-per-Pod' billing to satisfy cost optimization requirements." "architecture"
create_issue "LOG-002: Security - Secret Migration (Credential Sovereignty)" "Issue: Plaintext PAT in markdown files violates Sovereignty. Fix: Migrated all secrets to GCP Secret Manager." "security"
create_issue "LOG-003: Portability - Relative Repository Links" "Issue: Absolute file URIs are non-portable. Fix: Use relative links for documentation integrity." "documentation"
create_issue "LOG-004: Standards - Meta-Cognitive Integration" "Issue: Lack of formal recovery standards. Decision: Integrated Ground Truth, Audit-First, and Succession laws into the Sovereign Bible." "governance"
create_issue "LOG-007: Guardrails - Explicit Authorization Lock" "Issue: Risk of autonomous AI actions based on ambiguity. Fix: Established the Authorization Lock as the master gate for infrastructure changes." "governance"
create_issue "LOG-009: Purity - SBOM Integrity Law" "Issue: Risk of external dependency flux. Decision: Established No External Garbage law to limit stack to sanctioned components." "architecture"
create_issue "LOG-024: Resilience - High-Entropy Identity (Vacuum Shift)" "Issue: Metadata deadlocks from orphaned infrastructure. Fix: Mandated unique identifiers for all resources to enable non-blocking recovery." "resilience"

# --- BB SERIES (Tactical) ---
create_issue "BB-012: Failure - Orphaned Infrastructure State (Ghost Cluster)" "Discovery: GKE PROVISIONING stalls caused by overlapping requests and poisoned network ranges. Recovery: Abandon default subnet; transition to isolated VPC." "bug"
create_issue "BB-002: Performance - Service Handshake Storms" "Discovery: Rapid-fire microservice deployment causes gRPC-web timeouts. Fix: Implemented mandatory Backoff Law." "performance"

# --- META ---
create_issue "SYSTEM: Succession Migration Complete" "Summary: All legacy markdown discovery items from SUCCESSION_LOG.md and BLACKBOX.md have been synchronized to GitHub Issues." "meta"
