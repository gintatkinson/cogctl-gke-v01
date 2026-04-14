# Mock NCE Controller

This REST server implements very basic support for the NCE access controller.

The aim of this server is to enable testing IETF Network Slice NBI, NCE driver and NCE service handler.


## 1. Install requirements for the Mock NCE controller
__NOTE__: if you run the Mock NCE controller from the PyEnv used for developing on the TeraFlowSDN
framework and you followed the official steps in
[Development Guide > Configure Environment > Python](https://labs.etsi.org/rep/tfs/controller/-/wikis/2.-Development-Guide/2.1.-Configure-Environment/2.1.1.-Python),
all the requirements are already in place. Install them only if you execute it in a separate/standalone environment.

Install the required dependencies as follows:
```bash
pip install -r src/tests/tools/mock_nce_ctrl/requirements.in
```

Run the Mock NCE Controller as follows:
```bash
python src/tests/tools/mock_nce_ctrl/MockNCECtrl.py
```


## 2. Run the Mock NCE controller
Run the Mock NCE Controller as follows:
```bash
python src/tests/tools/mock_nce_ctrl/MockNCECtrl.py
```
