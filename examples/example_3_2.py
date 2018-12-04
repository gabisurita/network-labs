#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info


SWITCH_NAMES = ["sw2_{}".format(id + 1) for id in range(5)] + ["sw3_1"]
HOST_NAMES = ["h{}".format(id + 1) for id in range(5)]
ROUTER_NAMES = ["r{}".format(id + 1) for id in range(6)]


def enable_routing(router):
    router.cmd("sysctl -w net.ipv4.ip_forward=1")


def build_topo(net):
    switches = [
        net.addSwitch(switch, cls=OVSKernelSwitch, failMode="standalone")
        for switch in SWITCH_NAMES
    ]

    routers = [
        net.addHost(
            name, ip="10.0.1.{}/23".format(idx + 21), defaultRoute=None
        )
        for idx, name in enumerate(ROUTER_NAMES)
    ]

    hosts = [
        net.addHost(
            name, ip="10.0.0.{}/23".format(idx + 101), defaultRoute=None
        )
        for idx, name in enumerate(HOST_NAMES)
    ]

    for router in routers:
        enable_routing(router)

    for idx, host in enumerate(hosts):
        net.addLink(host, switches[idx])

    SW2_5 = net.get("sw2_5")
    SW3_1 = net.get("sw3_1")

    for switch in switches[:4]:
        net.addLink(switch, SW2_5)

    for router in routers:
        net.addLink(router, SW3_1)

    net.addLink(SW2_5, SW3_1)

    R1 = net.get("r1")
    HOST_101 = net.addHost(
        "h101", ip="10.0.2.101/23", defaultRoute="via 10.0.2.21"
    )

    net.addLink(HOST_101, R1, intfName2="r1-eth4")
    R1.setIP("10.0.2.21/23", intf="r1-eth4")


def start_topo():
    net = Mininet(topo=None, build=False, ipBase="10.0.0.100/23")

    info("*** Starting network\n")
    build_topo(net)
    net.build()

    info("*** Starting controllers\n")
    for controller in net.controllers:
        controller.start()

    info("*** Starting switches\n")
    for name in SWITCH_NAMES:
        net.get(name).start([])

    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    start_topo()
