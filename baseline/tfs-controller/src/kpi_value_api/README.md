# How to locally run and test KPI Value API

### Pre-requisets 
Ensure the following requirements are met before executing the KPI Value API service.

1. The KPI Manger service is running and Apache Kafka is running.

2. A virtual enviornment exist with all the required packages listed in ["requirements.in"](https://labs.etsi.org/rep/tfs/controller/-/blob/develop/src/kpi_value_api/requirements.in) file sucessfully installed.


### Messages format templates
The ["messages"](https://labs.etsi.org/rep/tfs/controller/-/blob/develop/src/kpi_value_api/tests/messages.py) python file contains templates for creating gRPC messages.

### Unit test file
The ["KPI Value API test"](https://labs.etsi.org/rep/tfs/controller/-/blob/develop/src/kpi_value_api/tests/test_kpi_value_api.py) python file enlist various tests conducted to validate functionality.

### Flow of execution (Kpi Value Api Service functions)
1. Call `StoreKpiValues(KpiValueList)` to produce `Kpi Value` on a Kafka Topic. (The `KpiValueWriter` microservice will consume and process this `Kpi Value`)

2. Call `SelectKpiValues(KpiValueFilter) -> KpiValueList` to read metric from the Prometheus DB.

3. Call `GetKpiAlarms(KpiId) -> KpiAlarms` to read alrams from the Kafka.
