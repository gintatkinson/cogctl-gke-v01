# Infinera Readme

There are some instructions at https://labs.etsi.org/rep/tfs/controller/-/tree/develop/tutorial . They are not completely up to date and don't 100% work.

Note that many of the scripts expect this and that K8s namespace being used, they are not consistent, so use manual kubectl commands where necessary.

Infinera repo (cloned from upstream) is https://bitbucket.infinera.com/projects/XRCA/repos/teraflow/browse . The main development branch for us is xr-development (branched of origin/develop).

## Preliminaries

Kubernetes must be installed and configured.

Note that if runninc MicroK8s (I would highly recommend it), then install also regular kubectl so that scripts work. That is, download the kubectl, and also export credidentials to standard location.

```bash
# As a root
su -
cd /usr/local/bin
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod 755 kubectl
exit

# As your local user
cd ~/.kube
microk8s config > config
```

Helm 3 is mandatory as of February 2023. Enable it with microk8s command. Then create wrapper shell script to expose it with standard name:

```
sudo su -
cat > /usr/bin/helm3
#!/bin/sh
microk8s.helm3 "$@"
^D
chmod 755 /usr/bin/helm3
```

Using symbolic link does not work, because snap wraps the real binary and won't work if name is different.

Local Docker registry is needed for build results. Use the following command to start local registry (docker will pull necessary images from Internet)

```bash
docker run -d -p 32000:5000 --restart=always --name registry registry:2
```

Setup mydeploy script outside the git repo. E.g. following will do. SOURCE IT ON ALL SHELLS.
Use https://labs.etsi.org/rep/tfs/controller/-/blob/develop/my_deploy.sh as example.
Script requires more variables than before as of February 2023.

```bash
# See https://labs.etsi.org/rep/tfs/controller/-/blob/develop/my_deploy.sh
# Use  docker run -d -p 32000:5000 --restart=always --name registry registry:2 
export TFS_REGISTRY_IMAGE="http://localhost:32000/tfs/"
export TFS_COMPONENTS="context device ztp monitoring pathcomp service slice nbi webui load_generator"
export TFS_IMAGE_TAG="dev"
export TFS_K8S_NAMESPACE="tfs"
export TFS_EXTRA_MANIFESTS="manifests/nginx_ingress_http.yaml"
export TFS_GRAFANA_PASSWORD="admin123+"
#export TFS_SKIP_BUILD=""
export CRDB_NAMESPACE="crdb"
export CRDB_USERNAME="tfs"
export CRDB_PASSWORD="tfs123"
export CRDB_DEPLOY_MODE="single"
export CRDB_DROP_DATABASE_IF_EXISTS=""
export CRDB_REDEPLOY=""
export NATS_NAMESPACE="nats"
export NATS_REDEPLOY=""
export QDB_NAMESPACE="qdb"
export QDB_USERNAME="admin"
export QDB_PASSWORD="quest"
export QDB_TABLE="tfs_monitoring"
export QDB_REDEPLOY=""
```

Build is containerized, pytest used for setup is not. Teraflow has some third party venv suggestion in docs. However standard venv works. Create:

```bash
python -m venv .venv
source .venv/bin/activate
./install_requirements.sh
```

SOURCE VENV ACTIVATE ON ANY SHELL USED FOR PYTHON RELATED WORK (e.g. pytest).

Use apt-get to install any missing tools (e.g. jq is required).

For host based Python development (e.g. VS Code) and test script execution, generate protobuf stubs:

```bash
cd proto
./generate_code_python.sh 
cd ../src/context
ln -s ../../proto/src/python proto
```

For VS Code python extension imports it is convenient to set file .env to top level with content:

```
PYTHONPATH=src
```
This will make imports to work properly in all cases.

## Building

Run deploy script to build in docker containers and then instantiate to configured K8s cluster. Deploy script must be sources for this to work!

```bash
./deploy/all.sh
```

If protobuf definitions have changed, regenerate version controlled Java files manually
(it is a horrifying bug in build system that this is not automated!).
```
cd ztp
# In case Java is not already installed
sudo apt-get install openjdk-11-jdk -y
export MAVEN_OPTS='--add-exports=java.base/jdk.internal.module=ALL-UNNAMED --add-exports jdk.compiler/com.sun.tools.javac.file=ALL-UNNAMED   --add-exports jdk.compiler/com.sun.tools.javac.parser=ALL-UNNAMED   --add-exports jdk.compiler/com.sun.tools.javac.tree=ALL-UNNAMED   --add-exports jdk.compiler/com.sun.tools.javac.util=ALL-UNNAMED --add-exports jdk.compiler/com.sun.tools.javac.tree=ALL-UNNAMED   --add-exports jdk.compiler/com.sun.tools.javac.api=ALL-UNNAMED'
cd src/policy
./mvnw compile
cd -
cd src/ztp
./mvnw compile
```

Compilation fails but does update the protobuf generated files.

## Testing

Upload descriptors_emulatex_xr.json via WEB UI to setup fake topology.

Setup service by following commands in src directory. Kubernetes endpoins change on every build, so setup script is mandatory.

```bash
    source  device/service/drivers/xr/setup_test_env.sh
    python -m pytest --verbose tests/ofc22/tests/test_functional_create_service_xr.py 
```

For topology different than used by the test_functional_create/delete_service_xr.py, one can also
use service-cli.py tool in the xr module directory. It allows creation of ELINE services between
arbitrary endpoints in the topology (with consequent underlying XR service instantiation). Run in
*xr module directory*.  Representative examples:
```
    PYTHONPATH=../../../../ ./service-cli.py create 1 R1-EMU 13/1/2 500 2 R3-EMU 13/1/2 500
    PYTHONPATH=../../../../ ./service-cli.py list
    PYTHONPATH=../../../../ ./service-cli.py delete 43a8046a-5dec-463d-82f7-7cc3442dbf4f
```

It is also possible to create direct XR services without multi-layer services. E.g.:
```
    PYTHONPATH=../../../../  ./service-cli.py create-xr FooService X1-XR-CONSTELLATION  "XR HUB 1|XR-T1" "XR LEAF 2|XR-T1"
```

Additionally it is possible to list services and endpoints:
```
    PYTHONPATH=../../../../  ./service-cli.py list-endpoints
    PYTHONPATH=../../../../  ./service-cli.py delete 43a8046a-5dec-463d-82f7-7cc3442dbf4f
```

The PYTHONPATH is mandatory. Suitable topology JSON must have been loaded before. With the
CocroachDB persistence, it is sufficient to load the topology once and it will persist.

Good logs to check are:

* kubectl logs   service/deviceservice     --namespace tfs
* kubectl logs   service/webuiservice     --namespace tfs

New 2.0 version of Teraflow has persistent database. To clean up any failed state
(e.g. from debugging session), set before deploy:

```
export CRDB_DROP_DATABASE_IF_EXISTS=YES 
```

In normal test runs it is not necessary to clear the database. However DO NOT RE-UPLOAD THE TOPOLOGY JSON FILE if DB has not been cleared.

## Unit Tests
Run in src directory (src under repo top level) with command:

```bash
PYTHONPATH=. pytest device/service/drivers/xr/cm
```

The PYTHONPATH is vital for imports to work properly.

## cm-cli

The tool cm-cli in the xr driver directory can be use to connect to CM and test the connectivity. For example:

```bash
./cm-cli.py 172.19.219.44  443 xr-user-1 xr-user-1 --show-constellation-by-hub-name="XR HUB 1"
./cm-cli.py 172.19.219.44  443 xr-user-1 xr-user-1 --list-constellations
./cm-cli.py 172.19.219.44  443 xr-user-1 xr-user-1 --create-connection="FOO;XR HUB 1|XR-T4;XR LEAF 1|XR-T1"
./cm-cli.py 172.19.219.44  443 xr-user-1 xr-user-1 --show-connection-by-name="FooBar123"
./cm-cli.py 172.19.219.44  443 xr-user-1 xr-user-1 --list-connections
# Modify argumens: href;uuid;ifname;ifname
# uuid translates to name TF:uuid
./cm-cli.py 172.19.219.44  443 xr-user-1 xr-user-1 --modify-connection="/network-connections/0637da3b-3b20-4b44-a513-035e6ef897a3;MyCon1;XR HUB 1|XR-T1;XR LEAF 1|XR-T2;25"
./cm-cli.py 172.19.219.44  443 xr-user-1 xr-user-1 --delete-connection=/network-connections/138f0cc0-3dc6-4195-97c0-2cbed5fd59ba
 ./cm-cli.py 172.19.219.44  443 xr-user-1 xr-user-1 --create-transport-capacity="FOO;XR HUB 1|XR-T4;XR LEAF 1|XR-T1;12"
 ./cm-cli.py 172.19.219.44  443 xr-user-1 xr-user-1 --list-transport-capacities
# Exercise almost full path of SetConfig. Can also be used for changing bandwidth (e.g. in demos) of an service
./cm-cli.py 172.19.219.44  443 xr-user-1 xr-user-1 --emulate-tf-set-config-service="XR HUB 1;teraflow_service_uuid;XR HUB 1|XR-T4;XR LEAF 1|XR-T1;125"
```
