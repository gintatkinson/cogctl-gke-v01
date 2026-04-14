# Probe for P4 mininet devices

Step 1:
To copy the necessary files, run:

```
probe-tfs/deploy.sh
```

Step 2:
To connect to the mininet docker, run:

```
probe-tfs/connect-to-mininet.sh
```

Step 3:
From inside the mininet docker, run:

```
./tfsagent
```

Step 4 (on another terminal):
Establish the service:
```
src/tests/p4/run_test_02_create_service.sh
```

Step 5:
From inside mininet (make mn-cli):
```
client ./tfsping
```

Step 6 (on another terminal):
To check the latest monitoring samples, run
```
python src/tests/p4/probe/monitoring_kpis.py
```
