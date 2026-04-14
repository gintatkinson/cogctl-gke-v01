# Tool: Perf Plots Generator:

Simple tool to gather performance data from Prometheus and produce histogram plots.

## Example:

- Ensure your MicroK8s includes the monitoring addon and your deployment specs the service monitors.

- Deploy TeraFlowSDN controller with your specific settings:
```(bash)
cd ~/tfs-ctrl
source my_deploy.sh 
./deploy.sh 
```

- Execute the test you want to meter.

- Select the appropriate script:
    - Device_Driver_Methods   : To report Device Driver Methods
    - Device_Driver_Details   : To report Device Add/Configure Details
    - Service_Handler_Methods : To report Service Handler Methods
    - Component_RPC_Methods   : To report Component RPC Methods

- Tune the experiment settings

- Execute the report script:
```(bash)
PYTHONPATH=./src python -m tests.tools.perf_plots.<script>
```
