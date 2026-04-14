# How to locally run and test KPI manager micro-service

### Pre-requisets 
Ensure the following requirements are met before executing the KPI management service:

1. A virtual enviornment exist with all the required packages listed in ["requirements.in"](https://labs.etsi.org/rep/tfs/controller/-/blob/develop/src/kpi_manager/requirements.in) sucessfully  installed.
2. Verify the creation of required database and table. The 
[KPI DB test](https://labs.etsi.org/rep/tfs/controller/-/blob/develop/src/kpi_manager/tests/test_kpi_db.py) python file lists the functions to create tables and the database.

### Messages format templates
The ["messages"](https://labs.etsi.org/rep/tfs/controller/-/blob/develop/src/kpi_manager/tests/test_messages.py) python file contains templates for creating gRPC messages.

### Flow of execution (Kpi Manager Service functions)
1. Call the gRPC method `SetKpiDescriptor(KpiDescriptor)->KpiId` to add the KpiDescriptor to the `Kpi` DB. `KpiDescriptor` and `KpiId` are both pre-defined gRPC message types.

2. Call `GetKpiDescriptor(KpiId)->KpiDescriptor` to read the `KpiDescriptor` from the DB and `DeleteKpiDescriptor(KpiId)` to delete the `KpiDescriptor` from the DB.

3. Call `SelectKpiDescriptor(KpiDescriptorFilter)->KpiDescriptorList` to get all `KpiDescriptor` objects that matches filter criteria. `KpiDescriptorFilter` and `KpiDescriptorList` are pre-defined gRPC message types.
