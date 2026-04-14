# ContainerLab

The setup consists of a management network for configuring and managing nodes.
srl1 and srl2 are interconnected.
client1 is connected to srl1 and client2 to srl2.
Routing between client1 and client2 is set up via the Nokia SR Linux nodes.

## Management Network
Name: mgmt-net
Subnet: 172.100.100.0/24

## Node Kinds
Nokia SR Linux: Image ghcr.io/nokia/srlinux:23.10.3
Linux: Image ghcr.io/hellt/network-multitool

## Nodes

### Nokia SR Linux
- Type: ixr6
- CPU: 0.5
- Memory: 2GB
- Management IP: 172.100.100.101

The provided SR Linux CLI commands in the _srl.cli_ enables system management and configures the GNMI server with OpenConfig models.

### Linux

Assigns IP 172.16.1.10/24 to eth1 and adds route to 172.16.2.0/24 via 172.16.1.1

In this topology file, the clients are pre-configured with the respectivly IP addresses in their interfaces and routes in their IP tables.

### Links
- Connect srl1:e1-1 to srl2:e1-1
- Connect client1:eth1 to srl1:e1-2
- Connect client2:eth1 to srl2:e1-2