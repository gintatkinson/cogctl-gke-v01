# How to locally run and test Telemetry service

### Pre-requisets 
The following requirements should be fulfilled before the execuation of Analytics service.

1. A virtual enviornment exist with all the required packages listed in [requirements.in](https://labs.etsi.org/rep/tfs/controller/-/blob/develop/src/telemetry/requirements.in) sucessfully  installed.
2. The Telemetry backend service should be running.
3. All required Kafka topics must exist. Call `create_all_topics` from the [Kafka class](https://labs.etsi.org/rep/tfs/controller/-/blob/develop/src/common/tools/kafka/Variables.py) to create any topics that do not already exist.
```
from common.tools.kafka.Variables import KafkaTopic
KafkaTopic.create_all_topics()
```

## Steps to create telemetry collector
The collector can be declared as below but there are many other ways to declare:

```
_create_collector_request                                  = telemetry_frontend_pb2.Collector()
_create_collector_request.collector_id.collector_id.uuid   = str(uuid.uuid4()) 
_create_collector_request.kpi_id.kpi_id.uuid               = str(uuid.uuid4())
_create_collector_request.duration_s                       = 100  # in seconds
_create_collector_request.interval_s                       = 10   # in seconds
```
