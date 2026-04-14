# Generic Mock RESTCONF Server

This server implements a basic RESTCONF Server that can load, potentially, any YANG data model.
Just copy this file structure, drop in fodler `./yang` your YANG data models.
Hierarchical folder structures are also supported.
YangModelDiscoverer will parse the models, identify imports and dependencies, and sort the models before loading.

The server can be configured using the following environment variables:
- `RESTCONF_PREFIX`, defaults to `"/restconf"`
- `YANG_SEARCH_PATH`, defaults to `"./yang"`
- `STARTUP_FILE`, defaults to `"./startup.json"`
- `SECRET_KEY`, defaults to `secrets.token_hex(64)`


See a simple working example in folder `src/tests/tools/simap_server`


## Build the RESTCONF Server Docker image
```bash
./build.sh
```

## Deploy the RESTCONF Server
```bash
./deploy.sh
```

## Destroy the RESTCONF Server
```bash
./destroy.sh
```
