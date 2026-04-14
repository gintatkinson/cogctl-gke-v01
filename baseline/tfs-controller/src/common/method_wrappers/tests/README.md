# Performance Evaluation Method Wrapper

## Description:

- enable prometheus addon:
```
tfs@tfs-vm:~/tfs-ctrl$ microk8s.enable prometheus
```

- wait till prometheus becomes enabled (when enabled, press Ctrl+C):
```
tfs@tfs-vm:~/tfs-ctrl$ watch -n 1 microk8s.status --wait-ready
```

- wait till all pods in the monitoring namespace have STATE=Running and READY=X/X (when done, press Ctrl+C):
```
tfs@tfs-vm:~/tfs-ctrl$ watch -n 1 kubectl get pods --all-namespaces
```

- deploy as:
```
tfs@tfs-vm:~/tfs-ctrl$ source src/common/method_wrappers/tests/deploy_specs.sh
tfs@tfs-vm:~/tfs-ctrl$ ./deploy.sh
```

- expose prometheus and grafana
  - (required) terminal 1 (grafana UI): `kubectl port-forward -n monitoring service/grafana --address 0.0.0.0 3001:3000`
  - (optional) terminal 2 (prometheus UI): `kubectl port-forward -n monitoring service/prometheus-k8s --address 0.0.0.0 9090:9090`
  - (optional) terminal 3 (alertmanager UI): `kubectl port-forward -n monitoring service/alertmanager-main --address 0.0.0.0 9093:9093`

- if using remote server/VM for running MicroK8s and VSCode, forward ports 3001, 9090, 9093

- (only used for internal framework debugging) run manual tests over the performance evaluation framework
  - terminal 4:
  ```
  export PYTHONPATH=/home/tfs/tfs-ctrl/src
  python -m common.method_wrappers.tests
  ```

- log into grafana:
  - browse: http://127.0.0.1:3000
  - user/pass: admin/admin
  - upload dashboards through "left menu > Dashboards > Manage > Import"
    - upload grafana_prometheus_component_rpc.json
    - upload grafana_prometheus_device_driver.json
    - upload grafana_prometheus_service_handler.json
  - watch in real time the dashboard

- upload topology through WebUI and navigate
  - should see histogram changing in Grafana

## References:
- [Prometheus - Tutorials - Getting Started](https://prometheus.io/docs/tutorials/getting_started/)
- [Prometheus - Tutorials - Understanding metric types](https://prometheus.io/docs/tutorials/understanding_metric_types/)
- [Prometheus - Tutorials - Instrumenting HTTP server in Go](https://prometheus.io/docs/tutorials/instrumenting_http_server_in_go/)
- [Prometheus - Tutorials - Visualizing metrics using Grafana](https://prometheus.io/docs/tutorials/visualizing_metrics_using_grafana/)
- [Prometheus - Tutorials - Alerting based on metrics](https://prometheus.io/docs/tutorials/alerting_based_on_metrics/)
- [Prometheus Operator - Guide](https://www.infracloud.io/blogs/prometheus-operator-helm-guide/)
- [Prometheus Operator - ServiceMonitor definition](https://prometheus-operator.dev/docs/operator/api/#monitoring.coreos.com/v1.ServiceMonitor)
- [Prometheus Operator - ServiceMonitor example 1](https://stackoverflow.com/questions/45613660/how-do-you-add-scrape-targets-to-a-prometheus-server-that-was-installed-with-kub)
- [Prometheus Operator - ServiceMonitor example 2](https://stackoverflow.com/questions/52991038/how-to-create-a-servicemonitor-for-prometheus-operator)
- [How to visualize Prometheus histograms in Grafana](https://grafana.com/blog/2020/06/23/how-to-visualize-prometheus-histograms-in-grafana/)
- [Prometheus Histograms with Grafana Heatmaps](https://towardsdatascience.com/prometheus-histograms-with-grafana-heatmaps-d556c28612c7)
