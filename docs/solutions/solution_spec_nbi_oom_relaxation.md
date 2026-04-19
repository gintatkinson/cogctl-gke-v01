# TECHNICAL SOLUTION SPEC: NBI OOM Relaxation

**Issue:** NBI Service OOMKilled via Kafka Sync Spike
**Date:** 2026-04-19
**Status:** IMPLEMENTED (Tactical) / PENDING BACK-PORT
**Reference:** Directive 5.1, Directive 4.2

## 1. Problem Statement
After correcting the Kafka DNS routing, the `nbiservice` successfully connected to the Kafka broker. However, the service immediately experienced a massive memory spike during the Gunicorn worker boot and initial Kafka topic synchronization phase, causing it to crash repeatedly.

## 2. Environment Constraint
The Sovereign GKE Autopilot environment enforces strict node-level memory constraints. The default container allocation (1Gi or less) was breached by the initialization spike, resulting in the kernel executing an immediate `OOMKilled` termination to protect the node.

## 3. Tactical Resolution
A runtime patch was applied to surgically elevate the container resource ceiling to bridge the initialization spike.

**Command Executed:**
`kubectl set resources deployment nbiservice -c=server --limits=cpu=1000m,memory=2Gi --requests=cpu=500m,memory=1Gi -n default`

## 4. Baseline Back-port Requirement
**Mandate (Directive 4.2):** This tactical resource elevation must be ported into the baseline `nbiservice` manifest (`baseline/tfs-controller/manifests/nbi/`) during the next repository synchronization to ensure immutable configuration compliance.
