# P4 Sources

We employ the P4 sources from the [fabric-tna](https://github.com/stratum/fabric-tna/tree/main) project.

To compile a relevant P4 target binary and P4 info file, do:

```shell
git clone https://github.com/stratum/fabric-tna.git

cd ./fabric-tna

make fabric-int-v1model
```

At this point, a relevant `build.sh` script is being run and a P4 program is being compiled.

After a successful compilation, some artifacts (p4info.txt, bmv2.json) will be generated and placed into `build` sub-folder.

```shell
ls build/fabric-int/bmv2 
_pp.p4     bmv2.json  p4info.txt
```

These artefacts are now moved into this repository.
