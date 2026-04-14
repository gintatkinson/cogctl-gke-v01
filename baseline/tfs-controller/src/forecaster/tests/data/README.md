# Manual Forecaster test:

- Move to root folder:
```bash
cd ~/tfs-ctrl
```

- Edit `my_deploy.sh` and enable the `monitoring` and the `forecaster` components:
```bash
export TFS_COMPONENTS="context device monitoring forecaster pathcomp service slice compute webui load_generator"
```

- Edit `deploy/tfs.sh` and disable linkerd injection to capture unencrypted traffic.
```bash
cp ./manifests/"${COMPONENT}"service.yaml "$MANIFEST"
#cat ./manifests/"${COMPONENT}"service.yaml | linkerd inject - --proxy-cpu-request "10m" --proxy-cpu-limit "1" --proxy-memory-request "64Mi" --proxy-memory-limit "256Mi" > "$MANIFEST"
```

- Deploy TeraFlowSDN controller:
```bash
source my_deploy.sh
./deploy/all.sh
```

- Onboard the topology descriptor `topology.json` through the WebUI.

- Source the runtime environment variables and inject the link utilization KPI values into the Monitoring database:
```bash
source tfs_runtime_env_vars.sh
python src/forecaster/tests/data/inject_samples.py
```

- Onboard the service descriptor `service.json` through the WebUI.
