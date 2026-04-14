#!/usr/bin/python

#  Copyright 2019-present Open Networking Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import argparse

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import Host
from mininet.topo import Topo
from stratum import StratumBmv2Switch

CPU_PORT = 255

class IPv4Host(Host):
    """Host that can be configured with an IPv4 gateway (default route).
    """

    def config(self, mac=None, ip=None, defaultRoute=None, lo='up', gw=None,
               **_params):
        super(IPv4Host, self).config(mac, ip, defaultRoute, lo, **_params)
        self.cmd('ip -4 addr flush dev %s' % self.defaultIntf())
        self.cmd('ip -6 addr flush dev %s' % self.defaultIntf())
        self.cmd('ip -4 link set up %s' % self.defaultIntf())
        self.cmd('ip -4 addr add %s dev %s' % (ip, self.defaultIntf()))
        if gw:
            self.cmd('ip -4 route add default via %s' % gw)
        # Disable offload
        for attr in ["rx", "tx", "sg"]:
            cmd = "/sbin/ethtool --offload %s %s off" % (
                self.defaultIntf(), attr)
            self.cmd(cmd)

        def updateIP():
            return ip.split('/')[0]

        self.defaultIntf().updateIP = updateIP

class TutorialTopo(Topo):
    """Basic Server-Client topology with IPv4 hosts"""

    def __init__(self, *args, **kwargs):
        Topo.__init__(self, *args, **kwargs)

        # Spines
        # gRPC port 50001
        switch1 = self.addSwitch('switch1', cls=StratumBmv2Switch, cpuport=CPU_PORT)
        # gRPC port 50002
        switch2 = self.addSwitch('switch2', cls=StratumBmv2Switch, cpuport=CPU_PORT)

        # IPv4 hosts attached to switch 1
        client = self.addHost('client', cls=IPv4Host, mac="aa:bb:cc:dd:ee:11",
                           ip='10.0.0.1/24', gw='10.0.0.100')
        server = self.addHost('server', cls=IPv4Host, mac="aa:bb:cc:dd:ee:22",
                           ip='10.0.0.2/24', gw='10.0.0.100')
        self.addLink(client, switch1)  # switch1: port 1
        self.addLink(switch1, switch2)  # switch1: port 2 == switch2: port 1
        self.addLink(switch2, server)  # switch2: port 2

def main():
    net = Mininet(topo=TutorialTopo(), controller=None)
    net.start()

    client = net.hosts[0]
    client.setARP('10.0.0.2', 'aa:bb:cc:dd:ee:22')
    server = net.hosts[1]
    server.setARP('10.0.0.1', 'aa:bb:cc:dd:ee:11')

    CLI(net)
    net.stop()
    print '#' * 80
    print 'ATTENTION: Mininet was stopped! Perhaps accidentally?'
    print 'No worries, it will restart automatically in a few seconds...'
    print 'To access again the Mininet CLI, use `make mn-cli`'
    print 'To detach from the CLI (without stopping), press Ctrl-D'
    print 'To permanently quit Mininet, use `make stop`'
    print '#' * 80


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Mininet topology script for 2x2 fabric with stratum_bmv2 and IPv4 hosts')
    args = parser.parse_args()
    setLogLevel('info')

    main()
