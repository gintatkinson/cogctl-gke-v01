# OFC'24 - Test scenario

## Start Topology
Topology is composed of 2 transponders managed through OpenConfig and 2 Multi-granular ROAMDS
Strat the topology executing the following command:
```bash
sudo ./start_topo.sh
```

## Populate the TFS context and topology
Pushing the JSON files following the file indexes, i.e, 1, 2, 3, ...
The last JSON file with ID 7 is the service.
To check the service is onboarded successfully go into the TFS WebUI and check the `Service` tab.

## Check configuration in devices
Check if the devices are configured properly.
To check that, run, for each device (X={1, 2, 3, 4}):
```bash
screen -r tX
```
To release the terminal, press `Ctrl + A + D`
