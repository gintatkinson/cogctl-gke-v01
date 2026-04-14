# Mock TFS NBI Dependencies

This gRPC Mock TFS NBI Dependencies server implements very basic support for the testing of the NBI component.


## 1. Install requirements for the Mock TFS NBI Dependencies
__NOTE__: if you run the Mock TFS NBI Dependencies from the PyEnv used for developing on the TeraFlowSDN
framework and you followed the official steps in
[Development Guide > Configure Environment > Python](https://tfs.etsi.org/documentation/latest/development_guide/#211-python),
all the requirements are already in place. Install them only if you execute it in a separate/standalone environment.

Install the required dependencies as follows:
```bash
pip install -r src/tests/tools/mock_tfs_nbi_dependencies/requirements.in
```

## 2. Run the Mock TFS NBI Dependencies
Run the Mock TFS NBI Dependencies as follows:
```bash
PYTHONPATH=./src python -m tests.tools.mock_tfs_nbi_dependencies
```
