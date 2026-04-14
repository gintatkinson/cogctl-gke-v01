# TeraFlowSDN - ETSI F5G PoC CAMARA Guide

This guide describes how to:
1. Configure and Deploy TeraFlowSDN for the ETSI F5G PoC CAMARA
2. Start Mock IETF ACTN SDN Controller (for testing and debugging)
3. Onboard the network topology descriptor
4. Expose the topology through the RESTConf IETF Network endpoint
5. Create Services through RESTConf IETF L3VPN endpoint
6. Get State of Services through RESTConf IETF L3VPN endpoint
7. Check configurations done in the Mock IETF ACTN SDN Controller (for testing and debugging)
8. Destroy Services through RESTConf IETF L3VPN endpoint


## 1. Configure and Deploy TeraFlowSDN for the ETSI F5G PoC CAMARA

This guide assumes the user pre-configured a physical/virtual machine based on the steps described in
the official
[ETSI TeraFlowSDN - Deployment Guide](https://labs.etsi.org/rep/tfs/controller/-/wikis/1.-Deployment-Guide).

__NOTE__: When you perform step _1.3. Deploy TeraFlowSDN_, configure the `my_deploy.sh` script modifying
the following settings:
```bash
# ...
export TFS_COMPONENTS="context device pathcomp service slice nbi webui"
# ...
export CRDB_DROP_DATABASE_IF_EXISTS="YES"
# ...
export QDB_DROP_TABLES_IF_EXIST="YES"
# ...
```

After modifying the file, deploy the TeraFlowSDN using the regular script `./deploy/all.sh`.
The script might take a while to run, especially the first time, since it needs to build the TeraFlowSDN
microservices.


## 2. Start Mock IETF ACTN SDN Controller (for testing and debugging)

__NOTE__: This step is not needed when using the real NCE-T controller.

Start the Mock IETF ACTN SDN Controller. This controller is a simple Python script that accepts requests
based on agreed F5G PoC CAMARA and stores it in memory, mimicking the NCE-T controller.

Run the Mock IETF ACTN SDN Controller as follows:
```bash
python src/tests/tools/mock_ietf_actn_sdn_ctrl/MockIetfActnSdnCtrl.py
```


## 3. Onboard the network topology descriptor

The network topology descriptor is a TeraFlowSDN configuration file describing the different elements to be
managed by the SDN controller, such as devices, links, networks, etc. A preliminary descriptor has been
prepared for the PoC CAMARA. The file is named as `topology-real.json`.

**NOTE**: Before onboarding file `topology-real.json`, update settings of device `nce-t` to match the IP
address, port, username, password, HTTP scheme, etc. of the real NCE-T.

To onboard the descriptor file, navigate to the [TeraFlowSDN WebUI](http://127.0.0.1/webui) > Home.
Browse the file through the _Descriptors_ field, and click the _Submit_ button that is next to the field.
The onboarding should take few seconds and the WebUI should report that 1 context, 1 topology, 1 controller,
10 devices, and 24 links were added. Also, it should report that 1 topology was updated.

Next, select in the field _Ctx/Topo_ the entry named as `Context(admin):Topology(admin)`, and click the
_Submit_ button that is next to the field. The topology should be displayed just below.

Then, navigate to the WebUI > Devices and WebUI > Links sections to familiarize with the details provided
for each entity. You can check the details of each entity by clicking the eye-shaped icon on the right
side of each row.

The underlying devices are configured as EMULATED entities while the NCE-T controller is configured as an
IP SDN controller. Auto-discovery of devices is not implemented as this will fall in PoC phase two.


## 4. Expose the topology through the RESTConf IETF Network endpoint

The TeraFlowSDN controller features an NBI component that exposes RESTConf-based endpoints. To retrieve the
topology following the IETF Network data model, use the following `curl` (or similar) command:

```bash
curl -u admin:admin http://127.0.0.1/restconf/data/ietf-network:networks/
```

__NOTE__: The command requires to interrogate the complete database and might take few seconds to complete.


## 5. Create Services through RESTConf IETF L3VPN endpoint

The TeraFlowSDN controller's NBI component also exposes the IETF L3VPN endpoints to
create/check_status/delete services. To try them, use the following `curl` (or similar) commands:

```bash
curl -u admin:admin -X POST -H "Content-Type: application/json" -d @src/nbi/tests/data/ietf_l3vpn_req_svc1.json http://127.0.0.1/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services
curl -u admin:admin -X POST -H "Content-Type: application/json" -d @src/nbi/tests/data/ietf_l3vpn_req_svc2.json http://127.0.0.1/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services
```

__NOTE 1__: This command uses the provided descriptors for creating the VPN services with some adaptations
to adjust to the official data model.

__NOTE 2__: This command retrieves no data if everything succeeds, in case of error, it will be reported.

This step will create the services in TeraFlowSDN and create the appropriate configuration rules in the
NCE-T controller through the appropriate service handlers and SBI drivers.

When the services are created, navigate to the WebUI > Services section to familiarize with the details
provided for each service. You can check the details of the service by clicking the eye-shaped icon on
the right side of each row.

Note that two services are created per requested VPN. The reason for that is because those services named
as "vpnX" (the name provided in the request) correspond to end-to-end services, while the others with a UUID
as a name are generated by TeraFlowSDN to represent the transport segment managed through the NCE-T.
TeraFlowSDN gathers the settings from the upper-layer end-to-end service and contructs the NCE-T-bound
services.

Also, you can navigate to the WebUI > Devices section, click on the eye-shaped icon next to the `nce-t`
device and check the configuration rules (defined using an internal data model, not IETF ACTN) that are
later converted into the IETF ACTN configuration instructions sent to the NCE-T.

You should see in configuration rules of the `nce-t` device rules with a resource key formatted as
`/osu_tunnels/osu_tunnel[{osu-tunnel-name}]` for each OSU tunnel, and others with resource key like
`/etht_services/etht_service[{etht-service-name}]` for each EthT service.


## 6. Get State of Services through RESTConf IETF L3VPN endpoint

To get the status of the services, use the following `curl` (or similar) commands:

```bash
curl -u admin:admin http://127.0.0.1/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services/vpn-service=vpn1
curl -u admin:admin http://127.0.0.1/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services/vpn-service=vpn2
```

__NOTE__: This command retrieves an empty dictionary with no error if the service is ready and ACTIVE.


## 7. Check configurations done in the Mock IETF ACTN SDN Controller (for testing and debugging)

__NOTE__: This step is not needed when using the real NCE-T controller.

While running the Mock IETF ACTN SDN Controller, you can interrogate the OSU tunnels and EthT Services
created using the following commands:

```bash
curl --insecure https://127.0.0.1:8443/restconf/v2/data/ietf-te:te/tunnels
curl --insecure https://127.0.0.1:8443/restconf/v2/data/ietf-eth-tran-service:etht-svc
```


## 8. Destroy Services through RESTConf IETF L3VPN endpoint

To destroy the services, use the following `curl` (or similar) commands:

```bash
curl -u admin:admin -X DELETE http://127.0.0.1/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services/vpn-service=vpn1
curl -u admin:admin -X DELETE http://127.0.0.1/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services/vpn-service=vpn2
```

__NOTE__: This command retrieves no data when it succeeds.

When the services are deleted, navigate to the WebUI > Services section verify that no service is present.
Besides, navigate to the WebUI > Devices section, and inspect the NCE-T device to verify that the OSU
tunnel and ETHT service configuration rules disapeared.
