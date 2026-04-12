#!/bin/bash
# GitHub Succession Synchronization Engine (Batch 2)

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

# --- MISSING LOG SERIES (001-015) ---
create_issue "LOG-005: Architecture - Minimalism & In-Cluster Hosting" "Issue: Manual manifest hacking and upstream flux risk. Decision: Adopted Minimalism Lock (Config over Modification) and Snapshot Strategy (Host binaries in-cluster)." "architecture"
create_issue "LOG-006: Sovereignty - Recovery Law & Context Persistence" "Issue: Risk of building on a 'Dirty' environment state. Decision: Mandated Ground Truth verification at start of every session." "governance"
create_issue "LOG-008: Operations - Persistence Checkpoint (Sovereign Save)" "Issue: Risk of mission-state loss. Decision: Mandated Git Push after every successful SOP transition." "governance"
create_issue "LOG-010: Quality - Baseline Fidelity Lock" "Issue: AI Agent deviation from official scripts. Decision: Prohibited manual overrides of ETSI TFS scripts (tfs.sh) unless approved." "quality"
create_issue "LOG-015: Infrastructure - Binary Sync Hardening" "Issue: IAM permission denials during Cloud Build sync. Fix: Explicitly delegated IAM to Default Compute Service Account." "infrastructure"
