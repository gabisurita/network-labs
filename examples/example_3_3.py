#!/usr/bin/python

import atexit
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.node import Node, OVSKernelSwitch
from mininet.nodelib import NAT


HOST_NAMES = ["h1", "h101", "h110"]
ROUTER_NAMES = ["r{}".format(id + 1) for id in range(6)]


class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd("sysctl net.ipv4.ip_forward=1")

    def terminate(self):
        self.cmd("sysctl net.ipv4.ip_forward=0")
        super(LinuxRouter, self).terminate()

    def add_route(self, address, route):
        """
        Add manual IP route to the router

        Args:
            address: Route address (address/mask format).
            route: IP to adress to route packets.
        """

        self.cmd("ip route add {address} via {route}".format(
            address=address, route=route
        ))


def build_topo(topo):
    # Create routers
    routers = [
        topo.addHost(name, cls=LinuxRouter, ip=None) for name in ROUTER_NAMES
    ]

    R1, R2, R3, R4, R5, R6 = routers

    # Create 10.0.0.0/23 subnet switch
    S1 = topo.addSwitch("s1", cls=OVSKernelSwitch, failMode="standalone")
    S1.start([])

    # Create hosts with default gateways
    HOST_1 = topo.addHost(
        "h1", ip="10.0.0.101/23", defaultRoute="via 10.0.1.25"
    )

    HOST_101 = topo.addHost(
        "h101", ip="10.0.2.101/23", defaultRoute="via 10.0.3.21"
    )

    HOST_110 = topo.addHost(
        "h110", ip="10.0.12.110/23", defaultRoute="via 10.0.13.24"
    )

    # Create NAT node
    nat = topo.addHost(
        "nat1",
        cls=NAT,
        ip="10.0.14.1",
        subnet='10.0.0.0/16',
        inetIntf="eth0",
        localIp='10.1.2.2/24',
        inNamespace=False,
    )

    topo.addLink(HOST_1, S1)
    topo.addLink(HOST_101, R1, intfName2="eth4")
    topo.addLink(HOST_110, R4, intfName2="eth4")

    topo.addLink(R1, R2, intfName1="eth1", intfName2="eth2")
    topo.addLink(R2, R3, intfName1="eth1", intfName2="eth2")
    topo.addLink(R3, R4, intfName1="eth1", intfName2="eth2")
    topo.addLink(R4, S1, intfName1="eth5")
    topo.addLink(R5, S1, intfName1="eth5")
    topo.addLink(R6, S1, intfName1="eth2")
    topo.addLink(R5, R1, intfName1="eth1", intfName2="eth3")
    topo.addLink(nat, R6, intfName2="eth1")

    # Subnet 10.0.0.0/23
    R4.setIP("10.0.1.24/23", intf="eth5")
    R5.setIP("10.0.1.25/23", intf="eth5")
    R6.setIP("10.0.1.26/23", intf="eth2")

    # Subnet 10.0.2.0/23
    R1.setIP("10.0.3.21/23", intf="eth4")

    # Subnet 10.0.4.0/23
    R1.setIP("10.0.5.21/23", intf="eth1")
    R2.setIP("10.0.5.22/23", intf="eth2")

    # Subnet 10.0.6.0/23
    R2.setIP("10.0.7.22/23", intf="eth1")
    R3.setIP("10.0.7.23/23", intf="eth2")

    # Subnet 10.0.8.0/23
    R3.setIP("10.0.9.23/23", intf="eth1")
    R4.setIP("10.0.9.24/23", intf="eth2")

    # Subnet 10.0.10.0/23
    R5.setIP("10.0.11.25/23", intf="eth1")
    R1.setIP("10.0.11.21/23", intf="eth3")

    # Subnet 10.0.12.0/23
    R4.setIP("10.0.13.24/23", intf="eth4")

    # Subnet 10.0.14.0/23
    R6.setIP("10.0.15.26/23", intf="eth1")


def setup_routes(net):
    routers = [net.get(name) for name in ROUTER_NAMES]
    R1, R2, R3, R4, R5, R6 = routers
    nat = net.get("nat1")

    # R1 Routes
    R1.add_route("10.0.6.0/23", "10.0.5.22")
    R1.add_route("10.0.8.0/23", "10.0.5.22")

    R1.add_route("10.0.0.0/23", "10.0.11.25")
    R1.add_route("10.0.12.0/23", "10.0.11.25")

    R1.setDefaultRoute("via 10.0.11.25")

    # R2 Routes
    R2.add_route("10.0.0.0/23", "10.0.5.21")
    R2.add_route("10.0.2.0/23", "10.0.5.21")
    R2.add_route("10.0.10.0/23", "10.0.5.21")

    R2.add_route("10.0.8.0/23", "10.0.7.23")
    R2.add_route("10.0.12.0/23", "10.0.7.23")

    R2.setDefaultRoute("via 10.0.5.21")

    # R3 Routes
    R3.add_route("10.0.2.0/23", "10.0.7.22")
    R3.add_route("10.0.4.0/23", "10.0.7.22")
    R3.add_route("10.0.10.0/23", "10.0.7.22")

    R3.add_route("10.0.0.0/23", "10.0.9.24")
    R3.add_route("10.0.12.0/23", "10.0.9.24")

    R3.setDefaultRoute("via 10.0.9.24")

    # R4 Routes
    R4.add_route("10.0.2.0/23", "10.0.1.25")
    R4.add_route("10.0.10.0/23", "10.0.1.25")

    R4.add_route("10.0.4.0/23", "10.0.9.23")
    R4.add_route("10.0.6.0/23", "10.0.9.23")

    R4.setDefaultRoute("via 10.0.1.26")

    # R5 Routes
    R5.add_route("10.0.2.0/23", "10.0.11.21")
    R5.add_route("10.0.4.0/23", "10.0.11.21")

    R5.add_route("10.0.6.0/23", "10.0.1.24")
    R5.add_route("10.0.8.0/23", "10.0.1.24")
    R5.add_route("10.0.12.0/23", "10.0.1.24")

    R5.setDefaultRoute("via 10.0.1.26")

    # R6 Routes
    R6.add_route("10.0.2.0/23", "10.0.1.25")
    R6.add_route("10.0.4.0/23", "10.0.1.25")
    R6.add_route("10.0.6.0/23", "10.0.1.25")
    R6.add_route("10.0.10.0/23", "10.0.1.25")

    R6.add_route("10.0.8.0/23", "10.0.1.24")
    R6.add_route("10.0.12.0/23", "10.0.1.24")

    R6.setDefaultRoute("via 10.0.14.1")

    # NAT Routes
    nat.cmd("ip route add 10.0.0.0/16 via 10.0.15.26")


def start_network(net):
    net = Mininet(build=False, autoSetMacs=True, link=TCLink)
    build_topo(net)
    net.build()
    net.start()
    setup_routes(net)
    CLI(net)


def stop_network(net):
    if net is not None:
        net.stop()


if __name__ == "__main__":
    net = None
    atexit.register(lambda: stop_network(net))
    setLogLevel("info")
    start_network(net)
