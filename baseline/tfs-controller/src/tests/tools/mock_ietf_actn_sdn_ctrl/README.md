# Mock IETF ACTN SDN Controller

This REST server implements very basic support for the following YANG data models:
- IETF YANG Data Model for Transport Network Client Signals (draft-ietf-ccamp-client-signal-yang-10)
  - Ref: https://datatracker.ietf.org/doc/draft-ietf-ccamp-client-signal-yang/
- IETF YANG Data Model for Traffic Engineering Tunnels, Label Switched Paths and Interfaces (draft-ietf-teas-yang-te-34)
  - Ref: https://datatracker.ietf.org/doc/draft-ietf-teas-yang-te/

The aim of this server is to enable testing the IetfActnDeviceDriver and the IetfActnServiceHandler.


## 1. Install requirements for the Mock IETF ACTN SDN controller
__NOTE__: if you run the Mock IETF ACTN SDN controller from the PyEnv used for developing on the TeraFlowSDN
framework and you followed the official steps in
[Development Guide > Configure Environment > Python](https://labs.etsi.org/rep/tfs/controller/-/wikis/2.-Development-Guide/2.1.-Configure-Environment/2.1.1.-Python),
all the requirements are already in place. Install them only if you execute it in a separate/standalone environment.

Install the required dependencies as follows:
```bash
pip install -r src/tests/tools/mock_ietf_actn_sdn_ctrl/requirements.in
```

Run the Mock IETF ACTN SDN Controller as follows:
```bash
python src/tests/tools/mock_ietf_actn_sdn_ctrl/MockIetfActnSdnCtrl.py
```


## 2. Run the Mock IETF ACTN SDN controller
Run the Mock IETF ACTN SDN Controller as follows:
```bash
python src/tests/tools/mock_ietf_actn_sdn_ctrl/MockIetfActnSdnCtrl.py
```
