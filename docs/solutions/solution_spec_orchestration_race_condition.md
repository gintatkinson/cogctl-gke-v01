# TECHNICAL SOLUTION SPEC: Orchestration Eventual Consistency Race Condition

**Issue:** Topology Injection Failure via `ForeignKeyViolation`
**Date:** 2026-04-20
**Status:** IMPLEMENTED (Tactical) / PENDING UPSTREAM FIX (Strategic)
**Component:** `tests.tools.load_scenario` / Orchestration Layer

## 1. Problem Statement
During automated deployment of infrastructure scenarios, the sequential injection of physical topologies followed immediately by orchestration configurations results in a fatal crash:
`psycopg2.errors.ForeignKeyViolation: insert or update on table "service_endpoint" violates foreign key constraint...`

## 2. Architectural Root Cause
The ETSI TFS automated testing tools (`load_scenario`) assume instantaneous global consistency. In a distributed cloud environment (GKE Autopilot), there is a propagation delay. The Context and Device services ingest the initial topology and emit events to Kafka, but the Python loader instantly executes the Orchestration payload before the Kafka consumers have fully reconciled and committed the `endpoint` records to the database. 

## 3. Tactical Resolution (Local Workaround)
A strict `sleep 30` propagation delay must be enforced between the physical infrastructure injection and the orchestration injection.

## 4. Strategic Resolution (Upstream ETSI TFS Recommendation)
Implicit temporal coupling must be replaced with deterministic state verification (Loader-Side Polling) or an Orchestrator-Side exponential backoff retry loop for the `import_topology` routine.
