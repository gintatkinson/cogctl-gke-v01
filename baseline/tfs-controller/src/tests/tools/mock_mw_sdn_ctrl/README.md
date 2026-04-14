# Mock MicroWave SDN Controller

This REST server implements very basic support for the following YANG data models:
- IETF YANG data model for Network Topology
  - Ref: https://www.rfc-editor.org/rfc/rfc8345.html
- IETF YANG data model for Transport Network Client Signals
  - Ref: https://www.ietf.org/archive/id/draft-ietf-ccamp-client-signal-yang-07.html

The aim of this server is to enable testing the MicroWaveDeviceDriver and the MicroWaveServiceHandler.
Follow the steps below to perform the test:

## 1. Deploy TeraFlowSDN controller and the scenario
Deploy the test scenario "microwave_deploy.sh":
```bash
source src/tests/tools/mock_mw_sdn_ctrl/scenario/microwave_deploy.sh
./deploy/all.sh
```

## 2. Install requirements and run the Mock MicroWave SDN controller
__NOTE__: if you run the Mock MicroWave SDN controller from the PyEnv used for developping on the TeraFlowSDN framework,
all the requirements are already in place. Install them only if you execute it in a separate/standalone environment.

Install the required dependencies as follows:
```bash
pip install Flask==2.1.3 Flask-RESTful==0.3.9
```

Run the Mock MicroWave SDN Controller as follows:
```bash
python src/tests/tools/mock_mw_sdn_ctrl/MockMWSdnCtrl.py
```

## 3. Deploy the test descriptors
Edit the descriptors to meet your environment specifications.
Edit "network_descriptors.json" and change IP address and port of the MicroWave SDN controller of the "MW" device.
- Set value of config rule "_connect/address" to the address of the host where the Mock MicroWave SDN controller is
  running (default="192.168.1.1").
- Set value of config rule "_connect/port" to the port where your Mock MicroWave SDN controller is listening on
  (default="8443").

Upload the "network_descriptors.json" through the TeraFlowSDN WebUI.
- If not already selected, select context "admin".
- Check that a network topology with 4 routers + 1 microwave radio system are loaded. They should form 2 rings.

Upload the "service_descriptor.json" through the TeraFlowSDN WebUI.
- Check that 2 services have been created.
- The "mw-svc" should have a connection and be supported by a sub-service.
- The sub-service should also have a connection.
- The R1, R3, and MW devices should have configuration rules established.

# 4. Delete the microwave service
Find the "mw-svc" on the WebUI, navigate to its details, and delete the service pressing the "Delete Service" button.
The service, sub-service, and device configuration rules should be removed.
