# Project Resume Guide: cogctl-gke-v01

## 1. Environment State
- **Namespace:** default (Confirmed via kubectl get svc -A)
- **TFS Services:** context, device, service, slice (All Active)
- **Data Status:** Hardware/Topology loaded. E2E Slices PENDING.

## 2. Recovery Tunnels (Run first)
```bash
killall kubectl 2>/dev/null
kubectl port-forward svc/contextservice 1010:1010 &
kubectl port-forward svc/deviceservice 2020:2020 &
kubectl port-forward svc/serviceservice 3030:3030 &
kubectl port-forward svc/sliceservice 4040:4040 &
```

## 3. Resume Commands
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/baseline/tfs-controller/src
export CONTEXTSERVICE_SERVICE_HOST=127.0.0.1
export CONTEXTSERVICE_SERVICE_PORT_GRPC=1010
export DEVICESERVICE_SERVICE_HOST=127.0.0.1
export DEVICESERVICE_SERVICE_PORT_GRPC=2020
export SERVICESERVICE_SERVICE_HOST=127.0.0.1
export SERVICESERVICE_SERVICE_PORT_GRPC=3030
export SLICESERVICE_SERVICE_HOST=127.0.0.1
export SLICESERVICE_SERVICE_PORT_GRPC=4040

# Fire the E2E Slice Load
python3 -m tests.tools.load_scenario ./baseline/tfs-controller/src/tests/ofc25/descriptors/topology_e2e-local-vm.json
```
