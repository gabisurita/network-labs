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


#
CORE_BW = 10e3  # 10 Gbps
CORE_DELAY = 1  # 1 ms
DISTRIBUTION_BW = 1e3  # 1 Gbps
DISTRIBUTION_DELAY = 3  # 3ms
ACCESS_BW = 100  # 100 Mbps
ACCESS_DELAY = 5  # 5ms


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
        topo.addLink(
            host, ACCESS_SWITCHES[idx / 2], bw=ACCESS_BW, delay=ACCESS_DELAY
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
