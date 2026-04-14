# Mock IETF L3VPN SDN Controller

This REST server implements very basic support for the following YANG data models:
- YANG Data Model for L3VPN Service Delivery
  - Ref: https://datatracker.ietf.org/doc/html/rfc8049

The aim of this server is to enable testing ietf netowrk slice service handler, ietf l3vpn service handler, and ietf l3vpn driver


## 1. Install requirements for the Mock IETF Network Slice SDN controller
__NOTE__: if you run the Mock IETF L3VPN SDN controller from the PyEnv used for developing on the TeraFlowSDN
framework and you followed the official steps in
[Development Guide > Configure Environment > Python](https://labs.etsi.org/rep/tfs/controller/-/wikis/2.-Development-Guide/2.1.-Configure-Environment/2.1.1.-Python),
all the requirements are already in place. Install them only if you execute it in a separate/standalone environment.

Install the required dependencies as follows:
```bash
pip install -r src/tests/tools/mock_ietf_l3vpn_sdn_ctrl/requirements.in
```

Run the Mock IETF L3VPN SDN Controller as follows:
```bash
python src/tests/tools/mock_ietf_l3vpn_sdn_ctrl/MockIetfL3VPNSdnCtrl.py
```


## 2. Run the Mock IETF L3VPN SDN controller
Run the Mock IETF L3VPN SDN Controller as follows:
```bash
python src/tests/tools/mock_ietf_l3vpn_sdn_ctrl/MockIetfL3VPNSdnCtrl.py
```
