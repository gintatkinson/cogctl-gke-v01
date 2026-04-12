#!/bin/bash
# GitHub Succession Synchronization Engine (Black Box Batch)

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

# --- MISSING BB SERIES (001-012) ---
create_issue "BB-001: Risk - Antigravity Context Persistence" "Discovery: In the event of a hard crash, agent internal memory is lost. Lock: Verification of Succession Log (GitHub) and Black Box are the only survival mechanisms." "governance"
create_issue "BB-003: Failure - Viewport Violation (Local Docker)" "Discovery: Attempting to use local Docker for Artifact Sync failed due to missing toolchains. Lock: All binary movements must occur in GCP Data Plane (Cloud Build)." "bug"
create_issue "BB-004: Blocker - GitHub Authentication Failure" "Discovery: Git push and API access failed due to missing credentials. Lock: Shifted to SSH and GCP Secret Manager authorized PAT." "security"
create_issue "BB-005: Security - Identity Secured" "Discovery: Received GitHub PAT. Stored securely in Secret Manager (v1). Enable sovereign push." "security"
create_issue "BB-009: Recovery - Git Ref Mismatch" "Discovery: fatal: cannot lock ref HEAD. Caused by IDE watcher vs Agent URL reset conflict. Fix: git reset performed to satisfy state." "bug"
create_issue "BB-010: Failure - Image Path Corruption" "Discovery: Cloud Build failed due to unresolved PROJECT_ID variable. Fix: Hardcoded IDs in sync YAMLs to ensure stability." "bug"
create_issue "BB-011: Failure - Bootstrap Path Failure" "Discovery: infra/bootstrap.sh failed because gcloud was missing from PATH. Fix: Injected absolute SDK paths." "bug"
