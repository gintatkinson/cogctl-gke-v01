# Tool: Load Scenario:

Simple tool to populate ETSI TeraFlowSDN controller with same descriptors that can be loaded through the WebUI.

## Example:

Deploy TeraFlowSDN controller with your specific settings:
```(bash)
cd ~/tfs-ctrl
source my_deploy.sh 
./deploy.sh 
```

Populate TeraFlowSDN controller with your descriptor file:
```(bash)
./src/tests/tools/load_scenario/run.sh src/tests/tools/load_scenario/example_descriptors.json
```
