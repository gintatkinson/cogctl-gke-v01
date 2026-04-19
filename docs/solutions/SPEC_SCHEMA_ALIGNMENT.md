# SPEC: Protobuf Schema Alignment & Load Scenario Transition

## 1. The Problem
**Symptom:** `TypeError: bad argument type for built-in operation`
**Root Cause:** Hardcoded test scripts (`hackfest3/LoadDescriptors.py`) used `**device` unpacking, which is incompatible with modern Protobuf 4.x/5.x schemas in the TFS Controller.

## 2. The Resolution
Abandon fragile test-specific loaders in favor of the centralized **Scenario Loader Tool**.

## 3. Implementation
1. **Coordinates:** Use `127.0.0.1` via kubectl port-forward.
2. **Command:**
   ```bash
   python3 -m tests.tools.load_scenario ./baseline/tfs-controller/src/load_generator/tests/descriptors.json
   ```

## 4. Verification
Confirmed Context "admin" and Devices appear in WebUI via the tooling parser.
