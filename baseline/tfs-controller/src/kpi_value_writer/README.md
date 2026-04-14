# How to locally run and test the KPI Value Writer

### Pre-requisets 
Ensure the following requirements are meet before executing the KPI Value Writer service.

1. The KPI Manger and KPI Value API services are running.

2. A Virtual enviornment exist with all the required packages listed in the ["requirements.in"](https://labs.etsi.org/rep/tfs/controller/-/blob/develop/src/kpi_value_writer/requirements.in) file installed sucessfully.

### Messages format templates
The ["messages"](https://labs.etsi.org/rep/tfs/controller/-/blob/develop/src/kpi_value_writer/tests/test_messages.py) python file contains the templates to create gRPC messages.


### Flow of execution
1. The service will be running, consuming KPI values from the Kafka topic, and pushing KPI metrics to Prometheus.
