# Demonstration of a Scalable and Efficient Pipeline for ML-based Optical Network Monitoring

__Authors__: [Carlos Natalino](https://www.chalmers.se/en/persons/carda/), Lluis Gifre Renom, Raul Muñoz, Ricard Vilalta, Marija Furdek and Paolo Monti

## Executing

All the commands here assume you are in the TFS home folder.

First, we need to load the TFS deploy specifications:

```bash
source src/tests/scenario3/optical/deploy_specs.sh
```

Then, we load the environment variables that identify the TFS deployment:

```bash
source tfs_runtime_env_vars.sh
```

Then, we are able to execute the load generator:

```bash
python src/tests/scenario3/optical/ofc23/run_experiment_demo.py
```