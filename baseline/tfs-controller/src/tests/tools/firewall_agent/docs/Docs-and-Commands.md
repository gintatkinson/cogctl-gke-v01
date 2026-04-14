# Docs and Commands

- Ref: https://ral-arturo.org/2020/11/22/python-nftables-tutorial.html
- Ref: https://www.netfilter.org/projects/nftables/manpage.html
- Ref: https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes

- Note: table and chain can have comment as well.

## Example Commands:

```bash
sudo nft --interactive --handle

# WORKS to block traffic, but weird as external facing port is 30435, not 85
insert rule ip filter FORWARD iifname "enp0s3" tcp dport 85 drop

# WORKS to block/allow traffic by external facing port 30435
add table ip filter
add chain ip filter PREROUTING { type filter hook prerouting priority raw; policy accept; }
add rule ip filter PREROUTING tcp dport 30435 reject
insert rule ip filter PREROUTING ip saddr 10.0.2.2/32 tcp dport 30435 accept
insert rule ip filter PREROUTING ip saddr 10.0.2.10/32 tcp dport 30435 accept

list chain ip filter PREROUTING
table ip filter {
        chain PREROUTING { # handle 30
                type filter hook prerouting priority raw; policy accept;
                ip saddr 10.0.2.10 tcp dport 30435 accept # handle 34
                ip saddr 10.0.2.2 tcp dport 30435 accept # handle 33
                tcp dport 30435 reject # handle 31
        }
}

delete rule ip filter PREROUTING handle 34
delete rule ip filter PREROUTING handle 33
delete rule ip filter PREROUTING handle 31


# =============================

sudo nft add table ip filter
sudo nft add chain ip filter input  {type filter hook input priority filter ; policy accept; }
sudo nft add chain ip filter output {type filter hook output priority filter; policy accept; }

# Example options
#sudo nft add rule ip filter input
#    iifname lo
#    oifname lo
#    ip saddr 0.0.0.0/0
#    ip daddr 192.168.0.10/32
#    tcp sport 12345
#    tcp dport 80
#    accept/drop/reject
#    comment "my-rule-name"

sudo nft add rule ip filter input iifname enp0s3 ip saddr 0.0.0.0/0 ip daddr 192.168.0.10/32 tcp sport 12345 tcp dport 80 accept comment "my-rule-in-test"
sudo nft add rule ip filter output oifname enp0s3 ip daddr 0.0.0.0/0 ip saddr 192.168.0.10/32 tcp dport 80 tcp sport 12345 drop comment "my-rule-out-test"
```


## Running code:

```python
import json
import nftables

nft = nftables.Nftables()
nft.set_json_output(True)
rc, output, error = nft.cmd("list ruleset")
print(json.loads(output))
```

Retrieves in `output`:

```json
{
    "nftables": [
        {
            "metainfo": {
                "version": "1.1.3",
                "release_name": "Commodore Bullmoose #4",
                "json_schema_version": 1
            }
        },
        {
            "table": {
                "family": "ip",
                "name": "nat",
                "handle": 1
            }
        },
        {
            "chain": {
                "family": "ip",
                "table": "nat",
                "name": "DOCKER",
                "handle": 1
            }
        },
        {
            "chain": {
                "family": "ip",
                "table": "nat",
                "name": "PREROUTING",
                "handle": 6,
                "type": "nat",
                "hook": "prerouting",
                "prio": -100,
                "policy": "accept"
            }
        },
        {
            "chain": {
                "family": "ip",
                "table": "nat",
                "name": "OUTPUT",
                "handle": 8,
                "type": "nat",
                "hook": "output",
                "prio": -100,
                "policy": "accept"
            }
        },
        {
            "chain": {
                "family": "ip",
                "table": "nat",
                "name": "POSTROUTING",
                "handle": 10,
                "type": "nat",
                "hook": "postrouting",
                "prio": 100,
                "policy": "accept"
            }
        },
        {
            "rule": {
                "family": "ip",
                "table": "nat",
                "chain": "DOCKER",
                "handle": 14,
                "expr": [
                    {
                        "match": {
                            "op": "==",
                            "left": {
                                "meta": {
                                    "key": "iifname"
                                }
                            },
                            "right": "docker0"
                        }
                    },
                    {
                        "counter": {
                            "packets": 0,
                            "bytes": 0
                        }
                    },
                    {
                        "return": null
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip",
                "table": "nat",
                "chain": "PREROUTING",
                "handle": 7,
                "expr": [
                    {
                        "xt": {
                            "type": "match",
                            "name": "addrtype"
                        }
                    },
                    {
                        "counter": {
                            "packets": 2,
                            "bytes": 88
                        }
                    },
                    {
                        "jump": {
                            "target": "DOCKER"
                        }
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip",
                "table": "nat",
                "chain": "OUTPUT",
                "handle": 9,
                "expr": [
                    {
                        "match": {
                            "op": "!=",
                            "left": {
                                "payload": {
                                    "protocol": "ip",
                                    "field": "daddr"
                                }
                            },
                            "right": {
                                "prefix": {
                                    "addr": "127.0.0.0",
                                    "len": 8
                                }
                            }
                        }
                    },
                    {
                        "xt": {
                            "type": "match",
                            "name": "addrtype"
                        }
                    },
                    {
                        "counter": {
                            "packets": 12,
                            "bytes": 720
                        }
                    },
                    {
                        "jump": {
                            "target": "DOCKER"
                        }
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip",
                "table": "nat",
                "chain": "POSTROUTING",
                "handle": 13,
                "expr": [
                    {
                        "match": {
                            "op": "!=",
                            "left": {
                                "meta": {
                                    "key": "oifname"
                                }
                            },
                            "right": "docker0"
                        }
                    },
                    {
                        "match": {
                            "op": "==",
                            "left": {
                                "payload": {
                                    "protocol": "ip",
                                    "field": "saddr"
                                }
                            },
                            "right": {
                                "prefix": {
                                    "addr": "172.17.0.0",
                                    "len": 16
                                }
                            }
                        }
                    },
                    {
                        "counter": {
                            "packets": 74,
                            "bytes": 4651
                        }
                    },
                    {
                        "xt": {
                            "type": "target",
                            "name": "MASQUERADE"
                        }
                    }
                ]
            }
        },
        {
            "table": {
                "family": "ip",
                "name": "filter",
                "handle": 2
            }
        },
        {
            "chain": {
                "family": "ip",
                "table": "filter",
                "name": "DOCKER",
                "handle": 1
            }
        },
        {
            "chain": {
                "family": "ip",
                "table": "filter",
                "name": "DOCKER-FORWARD",
                "handle": 2
            }
        },
        {
            "chain": {
                "family": "ip",
                "table": "filter",
                "name": "DOCKER-BRIDGE",
                "handle": 3
            }
        },
        {
            "chain": {
                "family": "ip",
                "table": "filter",
                "name": "DOCKER-CT",
                "handle": 4
            }
        },
        {
            "chain": {
                "family": "ip",
                "table": "filter",
                "name": "DOCKER-ISOLATION-STAGE-1",
                "handle": 5
            }
        },
        {
            "chain": {
                "family": "ip",
                "table": "filter",
                "name": "DOCKER-ISOLATION-STAGE-2",
                "handle": 6
            }
        },
        {
            "chain": {
                "family": "ip",
                "table": "filter",
                "name": "FORWARD",
                "handle": 7,
                "type": "filter",
                "hook": "forward",
                "prio": 0,
                "policy": "accept"
            }
        },
        {
            "chain": {
                "family": "ip",
                "table": "filter",
                "name": "DOCKER-USER",
                "handle": 18
            }
        },
        {
            "chain": {
                "family": "ip",
                "table": "filter",
                "name": "INPUT",
                "handle": 26,
                "type": "filter",
                "hook": "input",
                "prio": 0,
                "policy": "accept"
            }
        },
        {
            "rule": {
                "family": "ip",
                "table": "filter",
                "chain": "DOCKER",
                "handle": 21,
                "expr": [
                    {
                        "match": {
                            "op": "!=",
                            "left": {
                                "meta": {
                                    "key": "iifname"
                                }
                            },
                            "right": "docker0"
                        }
                    },
                    {
                        "match": {
                            "op": "==",
                            "left": {
                                "meta": {
                                    "key": "oifname"
                                }
                            },
                            "right": "docker0"
                        }
                    },
                    {
                        "counter": {
                            "packets": 0,
                            "bytes": 0
                        }
                    },
                    {
                        "drop": null
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip",
                "table": "filter",
                "chain": "DOCKER-FORWARD",
                "handle": 11,
                "expr": [
                    {
                        "counter": {
                            "packets": 188597,
                            "bytes": 246896440
                        }
                    },
                    {
                        "jump": {
                            "target": "DOCKER-CT"
                        }
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip",
                "table": "filter",
                "chain": "DOCKER-FORWARD",
                "handle": 10,
                "expr": [
                    {
                        "counter": {
                            "packets": 68171,
                            "bytes": 3005971
                        }
                    },
                    {
                        "jump": {
                            "target": "DOCKER-ISOLATION-STAGE-1"
                        }
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip",
                "table": "filter",
                "chain": "DOCKER-FORWARD",
                "handle": 9,
                "expr": [
                    {
                        "counter": {
                            "packets": 68171,
                            "bytes": 3005971
                        }
                    },
                    {
                        "jump": {
                            "target": "DOCKER-BRIDGE"
                        }
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip",
                "table": "filter",
                "chain": "DOCKER-FORWARD",
                "handle": 20,
                "expr": [
                    {
                        "match": {
                            "op": "==",
                            "left": {
                                "meta": {
                                    "key": "iifname"
                                }
                            },
                            "right": "docker0"
                        }
                    },
                    {
                        "counter": {
                            "packets": 68171,
                            "bytes": 3005971
                        }
                    },
                    {
                        "accept": null
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip",
                "table": "filter",
                "chain": "DOCKER-BRIDGE",
                "handle": 23,
                "expr": [
                    {
                        "match": {
                            "op": "==",
                            "left": {
                                "meta": {
                                    "key": "oifname"
                                }
                            },
                            "right": "docker0"
                        }
                    },
                    {
                        "counter": {
                            "packets": 0,
                            "bytes": 0
                        }
                    },
                    {
                        "jump": {
                            "target": "DOCKER"
                        }
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip",
                "table": "filter",
                "chain": "DOCKER-CT",
                "handle": 22,
                "expr": [
                    {
                        "match": {
                            "op": "==",
                            "left": {
                                "meta": {
                                    "key": "oifname"
                                }
                            },
                            "right": "docker0"
                        }
                    },
                    {
                        "xt": {
                            "type": "match",
                            "name": "conntrack"
                        }
                    },
                    {
                        "counter": {
                            "packets": 120426,
                            "bytes": 243890469
                        }
                    },
                    {
                        "accept": null
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip",
                "table": "filter",
                "chain": "DOCKER-ISOLATION-STAGE-1",
                "handle": 24,
                "expr": [
                    {
                        "match": {
                            "op": "==",
                            "left": {
                                "meta": {
                                    "key": "iifname"
                                }
                            },
                            "right": "docker0"
                        }
                    },
                    {
                        "match": {
                            "op": "!=",
                            "left": {
                                "meta": {
                                    "key": "oifname"
                                }
                            },
                            "right": "docker0"
                        }
                    },
                    {
                        "counter": {
                            "packets": 68171,
                            "bytes": 3005971
                        }
                    },
                    {
                        "jump": {
                            "target": "DOCKER-ISOLATION-STAGE-2"
                        }
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip",
                "table": "filter",
                "chain": "DOCKER-ISOLATION-STAGE-2",
                "handle": 25,
                "expr": [
                    {
                        "match": {
                            "op": "==",
                            "left": {
                                "meta": {
                                    "key": "oifname"
                                }
                            },
                            "right": "docker0"
                        }
                    },
                    {
                        "counter": {
                            "packets": 0,
                            "bytes": 0
                        }
                    },
                    {
                        "drop": null
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip",
                "table": "filter",
                "chain": "FORWARD",
                "handle": 19,
                "expr": [
                    {
                        "counter": {
                            "packets": 188597,
                            "bytes": 246896440
                        }
                    },
                    {
                        "jump": {
                            "target": "DOCKER-USER"
                        }
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip",
                "table": "filter",
                "chain": "FORWARD",
                "handle": 8,
                "expr": [
                    {
                        "counter": {
                            "packets": 188597,
                            "bytes": 246896440
                        }
                    },
                    {
                        "jump": {
                            "target": "DOCKER-FORWARD"
                        }
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip",
                "table": "filter",
                "chain": "INPUT",
                "handle": 27,
                "expr": [
                    {
                        "match": {
                            "op": "==",
                            "left": {
                                "payload": {
                                    "protocol": "ip",
                                    "field": "saddr"
                                }
                            },
                            "right": "9.9.9.9"
                        }
                    },
                    {
                        "counter": {
                            "packets": 0,
                            "bytes": 0
                        }
                    },
                    {
                        "drop": null
                    }
                ]
            }
        },
        {
            "table": {
                "family": "ip6",
                "name": "nat",
                "handle": 3
            }
        },
        {
            "chain": {
                "family": "ip6",
                "table": "nat",
                "name": "DOCKER",
                "handle": 1
            }
        },
        {
            "chain": {
                "family": "ip6",
                "table": "nat",
                "name": "PREROUTING",
                "handle": 2,
                "type": "nat",
                "hook": "prerouting",
                "prio": -100,
                "policy": "accept"
            }
        },
        {
            "chain": {
                "family": "ip6",
                "table": "nat",
                "name": "OUTPUT",
                "handle": 4,
                "type": "nat",
                "hook": "output",
                "prio": -100,
                "policy": "accept"
            }
        },
        {
            "rule": {
                "family": "ip6",
                "table": "nat",
                "chain": "PREROUTING",
                "handle": 3,
                "expr": [
                    {
                        "xt": {
                            "type": "match",
                            "name": "addrtype"
                        }
                    },
                    {
                        "counter": {
                            "packets": 0,
                            "bytes": 0
                        }
                    },
                    {
                        "jump": {
                            "target": "DOCKER"
                        }
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip6",
                "table": "nat",
                "chain": "OUTPUT",
                "handle": 5,
                "expr": [
                    {
                        "match": {
                            "op": "!=",
                            "left": {
                                "payload": {
                                    "protocol": "ip6",
                                    "field": "daddr"
                                }
                            },
                            "right": "::1"
                        }
                    },
                    {
                        "xt": {
                            "type": "match",
                            "name": "addrtype"
                        }
                    },
                    {
                        "counter": {
                            "packets": 0,
                            "bytes": 0
                        }
                    },
                    {
                        "jump": {
                            "target": "DOCKER"
                        }
                    }
                ]
            }
        },
        {
            "table": {
                "family": "ip6",
                "name": "filter",
                "handle": 4
            }
        },
        {
            "chain": {
                "family": "ip6",
                "table": "filter",
                "name": "DOCKER",
                "handle": 1
            }
        },
        {
            "chain": {
                "family": "ip6",
                "table": "filter",
                "name": "DOCKER-FORWARD",
                "handle": 2
            }
        },
        {
            "chain": {
                "family": "ip6",
                "table": "filter",
                "name": "DOCKER-BRIDGE",
                "handle": 3
            }
        },
        {
            "chain": {
                "family": "ip6",
                "table": "filter",
                "name": "DOCKER-CT",
                "handle": 4
            }
        },
        {
            "chain": {
                "family": "ip6",
                "table": "filter",
                "name": "DOCKER-ISOLATION-STAGE-1",
                "handle": 5
            }
        },
        {
            "chain": {
                "family": "ip6",
                "table": "filter",
                "name": "DOCKER-ISOLATION-STAGE-2",
                "handle": 6
            }
        },
        {
            "chain": {
                "family": "ip6",
                "table": "filter",
                "name": "FORWARD",
                "handle": 7,
                "type": "filter",
                "hook": "forward",
                "prio": 0,
                "policy": "accept"
            }
        },
        {
            "chain": {
                "family": "ip6",
                "table": "filter",
                "name": "DOCKER-USER",
                "handle": 12
            }
        },
        {
            "rule": {
                "family": "ip6",
                "table": "filter",
                "chain": "DOCKER-FORWARD",
                "handle": 11,
                "expr": [
                    {
                        "counter": {
                            "packets": 0,
                            "bytes": 0
                        }
                    },
                    {
                        "jump": {
                            "target": "DOCKER-CT"
                        }
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip6",
                "table": "filter",
                "chain": "DOCKER-FORWARD",
                "handle": 10,
                "expr": [
                    {
                        "counter": {
                            "packets": 0,
                            "bytes": 0
                        }
                    },
                    {
                        "jump": {
                            "target": "DOCKER-ISOLATION-STAGE-1"
                        }
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip6",
                "table": "filter",
                "chain": "DOCKER-FORWARD",
                "handle": 9,
                "expr": [
                    {
                        "counter": {
                            "packets": 0,
                            "bytes": 0
                        }
                    },
                    {
                        "jump": {
                            "target": "DOCKER-BRIDGE"
                        }
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip6",
                "table": "filter",
                "chain": "FORWARD",
                "handle": 13,
                "expr": [
                    {
                        "counter": {
                            "packets": 0,
                            "bytes": 0
                        }
                    },
                    {
                        "jump": {
                            "target": "DOCKER-USER"
                        }
                    }
                ]
            }
        },
        {
            "rule": {
                "family": "ip6",
                "table": "filter",
                "chain": "FORWARD",
                "handle": 8,
                "expr": [
                    {
                        "counter": {
                            "packets": 0,
                            "bytes": 0
                        }
                    },
                    {
                        "jump": {
                            "target": "DOCKER-FORWARD"
                        }
                    }
                ]
            }
        }
    ]
}
```
