# How to Locally Run and Test Analytic Frontend Service

### Pre-requisets 
The following requirements should be fulfilled before the execuation of Analytics service.

1. A virtual enviornment exist with all the required packages listed in [requirements.in](https://labs.etsi.org/rep/tfs/controller/-/blob/develop/src/analytics/frontend/requirements.in) sucessfully  installed.
2. The Analytics backend service should be running.
3. All required Kafka topics must exist. Call `create_all_topics` from the [Kafka class](https://labs.etsi.org/rep/tfs/controller/-/blob/develop/src/common/tools/kafka/Variables.py) to create any topics that do not already exist.
```
from common.tools.kafka.Variables import KafkaTopic
KafkaTopic.create_all_topics()
```

4. There will be an input stream on the Kafka topic that the Streamer class will consume and apply a defined thresholds.
- A JSON encoded string should be generated in the following format:
```
'{"time_stamp": "2024-09-03T12:36:26Z", "kpi_id": "6e22f180-ba28-4641-b190-2287bf448888", "kpi_value": 44.22}'
```
- The Kafka producer key should be the UUID of the Analyzer used when creating it.
- Generate the stream on the following Kafka topic: `KafkaTopic.ANALYTICS_RESPONSE.value`.

## Steps to create and start Analyzer
The analyzer can be declared as below but there are many other ways to declare:

The given object creation process for `_create_analyzer` involves defining an instance of the `Analyzer` message from the [gRPC definition](https://labs.etsi.org/rep/tfs/controller/-/blob/develop/proto/analytics_frontend.proto) and populating its fields.

```
from common.proto.analytics_frontend_pb2 import AnalyzerId
_create_analyzer_id = AnalyzerId()
```

Here is a breakdown of how each field is populated:

### 1. **Analyzer ID**
   - `analyzer_id`: This field uses a unique ID to identify the analyzer. In this case, the ID is a UUID.
     ```python
     _create_analyzer.analyzer_id.analyzer_id.uuid = "efef4d95-1cf1-43c4-9742-95c283ddd7a6"
     ```
   - The commented-out code shows how the UUID can be generated dynamically using Python's `uuid.uuid4()`. However, for now, a static UUID is used.

### 2. **Algorithm Name**
   - `algorithm_name`: Specifies the name of the algorithm to be executed by the analyzer.
     ```python
     _create_analyzer.algorithm_name = "Test_Aggergate_and_Threshold"
     ```

### 3. **Operation Mode**
   - `operation_mode`: Sets the mode in which the analyzer operates, in this case, it's set to `ANALYZEROPERATIONMODE_STREAMING`.
     ```python
     _create_analyzer.operation_mode = AnalyzerOperationMode.ANALYZEROPERATIONMODE_STREAMING
     ```

### 4. **Input KPI IDs**
   - `input_kpi_ids`: This is a list of KPI IDs that will be used as input for the analysis. KPI IDs are represented using `KpiId`, and UUIDs are assigned to each input. The Spark streamer assume that the provided KPIs exists in the KPI Descriptor database.
     ```python
     _kpi_id = KpiId()
     _kpi_id.kpi_id.uuid = "6e22f180-ba28-4641-b190-2287bf448888"
     _create_analyzer.input_kpi_ids.append(_kpi_id)
     
     _kpi_id.kpi_id.uuid = "1e22f180-ba28-4641-b190-2287bf446666"
     _create_analyzer.input_kpi_ids.append(_kpi_id)
     ```

### 5. **Output KPI IDs**
   - `output_kpi_ids`: A list of KPI IDs that are produced as output after analysis. Each one is generated and appended to the list.
     ```python
     _kpi_id = KpiId()
     _create_analyzer.output_kpi_ids.append(_kpi_id)
     ```

### 6. **Parameters**
   - `parameters`: This is a dictionary containing key-value pairs of various parameters used by the analyzer. These values are often algorithm-specific.
     - **Thresholds**: A dictionary containing threshold possible values (min, max, avg, first, last, stdev)_<any_name>. For example: "min_latency", "max_bandwidth", "avg_datarate" etc. 
       ```python
       _threshold_dict = {
           'min_latency' : (00, 10), 
           'max_bandwidth': (40, 50), 
           'avg_datarate': (00, 10)
       }
       _create_analyzer.parameters['thresholds'] = json.dumps(_threshold_dict)
       ```
     - **Window Size**: Specifies the size of the time window (e.g., `60 seconds`).
       ```python
       _create_analyzer.parameters['window_size'] = "60 seconds"
       ```
     - **Window Slider**: Defines the sliding window interval (e.g., `30 seconds`).
       ```python
       _create_analyzer.parameters['window_slider'] = "30 seconds"
       ```

###  **Calling `StartAnalyzer` with an Analyzer Frontend Object**
   - The following code demonstrates how to call `StartAnalyzer()` with an Analyzer object:
```python
from analytics.frontend.client.AnalyticsFrontendClient import AnalyticsFrontendClient

analytics_client_object = AnalyticsFrontendClient()
analytics_client_object.StartAnalyzer(_create_analyzer_id)
```

### **How to Receive Analyzer Response**
   - `GetAlarms(<kpi_id>) -> KpiAlarms` is a method in the `KPI Value Api` that retrieves alarms for a given KPI ID. This method returns a stream of alarms associated with the specified KPI.
