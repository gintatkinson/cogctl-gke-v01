# How to run locally the monitoring service (tested in Ubuntu 20.04)


## Download the grpc health probe

`
GRPC_HEALTH_PROBE_VERSION=v0.2.0 
`

`
wget -qO/bin/grpc_health_probe https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-linux-amd64
`

`
chmod +x /bin/grpc_health_probe
`

## Get packages

`
python3 -m pip install pip-tools
`

`
python3 -m pip install -r requirements.txt
`

## Install prometheus client

`
pip3 install prometheus_client
`

## Execute server
`
cd monitoring
`

`
python3 monitoring/monitoring_server.py
`

## Execute client
`
python3 monitoring_client.py
`

# How to create and execute the monitoring server in a docker container

## Install docker
`
curl -fsSL https://get.docker.com -o get-docker.sh
`
sudo sh get-docker.sh
`
## Build service
`
cd src
`

`
./build.sh
`

## Run service
`
./start.sh
`
