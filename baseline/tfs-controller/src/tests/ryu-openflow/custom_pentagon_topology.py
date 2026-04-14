# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink

class PentagonTopo(Topo):
    def build(self):
        sw1 = self.addSwitch('s1')
        sw2 = self.addSwitch('s2')
        sw3 = self.addSwitch('s3')
        sw4 = self.addSwitch('s4')
        sw5 = self.addSwitch('s5')

        h1 = self.addHost('h1', ip='10.0.0.1', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', ip='10.0.0.2', mac='00:00:00:00:00:02')
        h3 = self.addHost('h3', ip='10.0.0.3', mac='00:00:00:00:00:03')
        h4 = self.addHost('h4', ip='10.0.0.4', mac='00:00:00:00:00:04')

        self.addLink(sw1, sw2)
        self.addLink(sw2, sw3)
        self.addLink(sw3, sw4)
        self.addLink(sw4, sw5)
        self.addLink(sw5, sw1)

        self.addLink(h1, sw2)
        self.addLink(h2, sw2)
        self.addLink(h3, sw5)
        self.addLink(h4, sw5)

if __name__ == '__main__':
    topo = PentagonTopo()
    net = Mininet(topo=topo, controller=lambda name: RemoteController(name, ip='127.0.0.1'), link=TCLink)
    
    net.start()
    net.staticArp()

    print('Custom Pentagon Topology is up with static ARP.')
    CLI(net)  
    net.stop()
