# encoding: utf-8

import atexit
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink


# Entity Names

CORE_SwITCH = "c1"
DISTRIBUTION_SWICHES = ["a{}".format(id + 1) for id in range(2)]
ACCESS_SWITCHES = ["s{}".format(id + 1) for id in range(4)]
HOSTS = ["h{}".format(id + 1) for id in range(8)]


# Link Parameters
CORE_BW = 1e3  # 1 Gbps
CORE_DELAY = 2  # 2 ms
DISTRIBUTION_BW = 100  # 100 Mbps
DISTRIBUTION_DELAY = 2  # 2ms
ACCESS_BW = 10  # 10 Mbps
ACCESS_DELAY = 2  # 2ms


# Bad Link hosts
BAD_LINK_HOSTS = ["h8"]
BAD_LINK_LOSS = 15


def createTopo():
    topo = Topo()

    # Create switches
    for switch in ACCESS_SWITCHES + DISTRIBUTION_SWICHES + [CORE_SwITCH]:
        topo.addSwitch(switch)

    # Create hosts
    for host in HOSTS:
        topo.addHost(host)

    # Create core to distribution links
    for idx, distribution in enumerate(DISTRIBUTION_SWICHES):
        topo.addLink(distribution, CORE_SwITCH, bw=CORE_BW, delay=CORE_DELAY)

    # Create distribution to access links
    for idx, access in enumerate(ACCESS_SWITCHES):
        topo.addLink(
            access,
            DISTRIBUTION_SWICHES[idx / 2],
            bw=DISTRIBUTION_BW,
            delay=DISTRIBUTION_DELAY,
        )

    # Create access to host links
    for idx, host in enumerate(HOSTS):
        loss = BAD_LINK_LOSS if host in BAD_LINK_HOSTS else 0

        topo.addLink(
            host,
            ACCESS_SWITCHES[idx / 2],
            bw=ACCESS_BW,
            delay=ACCESS_DELAY,
            loss=loss,
        )

    return topo


def startNetwork(net):
    topo = createTopo()
    net = Mininet(topo=topo, autoSetMacs=True, link=TCLink)
    net.start()
    CLI(net)


def stopNetwork(net):
    if net is not None:
        net.stop()


if __name__ == "__main__":
    net = None
    atexit.register(lambda: stopNetwork(net))
    setLogLevel("info")
    startNetwork(net)
