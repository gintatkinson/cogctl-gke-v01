# SOP: KNOWLEDGE ANCHORING (Issue & Resolution Mapping)

This protocol ensures that architectural shifts and infrastructure failures are documented with 100% fidelity across the repository and the tracking system.

## 1. The GitHub Issue Pattern (The Tracking)
Every critical blocker or architectural decision must have a GitHub Issue structured as follows:
- **Problem Statement**: Clear, high-level description of the failure or blocker.
- **Symptoms & Diagnostics**: Exact CLI output (`kubectl`, `gcloud`), error codes, and symptoms.
- **Root Cause**: The underlying technical reason (e.g., missing NAT, redundant IdP).
- **Strategic Pivot**: The technical rationale for the chosen solution.
- **Solution Link**: A direct GitHub URL to a standalone Solution Specification (SOP).

## 2. The Solution Specification (The Record)
Log entries in the Succession Log are insufficient for complex solutions. A standalone Solution Specification document (SOP) must be created/updated to define:
- **Architecture**: The new 'How' (The hardened standard).
- **Specifications**: Explicit ports, IPs, and logic definitions.
- **Verification**: The explicit steps required to prove the fix works correctly.

## 3. The Synchronization Law
The GitHub Issue and the Solution Specification must be updated, pushed, and verified BEFORE the execution of the fix commences.
