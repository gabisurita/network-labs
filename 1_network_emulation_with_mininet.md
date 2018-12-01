
Network Emulation With Mininet
==============================


Goals
=====

1. Understand how the Mininet network emulator works
2. Practice creating and analyzing network topologies


Warming Up
==========

Run `sudo mn --help`. This will give some basic instructions of running Mininet.

```
Usage: mn [options]
(type mn -h for details)

The mn utility creates Mininet network from the command line. It can create
parametrized topologies, invoke the Mininet CLI, and run tests.
```


Lets start Mininet with the default topology using `--mac` parameter, that will tell Mininet to automatically set host MAC Addresses.


```
wifi@wifi-VirtualBox:~$ sudo -E mn --mac
```

This will start the Mininet network emulator and the Mininet terminal.

Let's explore some basic commands:

1. `pingall`: test the connectivity between all hosts
2. `intfs`: show all network interfaces
3. `net`: show a list of network elements and their connections


Sample executions:

```
mininet-wifi> pingall
*** Ping: testing ping reachability
h1 -> h2
h2 -> h1
*** Results: 0% dropped (2/2 received)
```

```
mininet-wifi> intfs
h1: h1-eth0
h2: h2-eth0
s1: lo,s1-eth1,s1-eth2
c0:
```

```
mininet-wifi> net
h1 h1-eth0:s1-eth1
h2 h2-eth0:s1-eth2
s1 lo:  s1-eth1:h1-eth0 s1-eth2:h2-eth0
c0
```

Mininet terminal also supports the `{host} {command}` syntax in order to run any command on a given topology host. It will also substitute the topology host name for the host IP. For example:

```
h1 ping -c 1 h2
```

Is equivalent to running the following command on host h1.

```
ping -c 1 10.0.0.2
```

For more complex operations, you may also open a separate shell session for a host and run commands directly. You may try

```
h1 xterm
```

And on the `xterm` window on H1, try:

```
ping -c 1 10.0.0.2

```

Sample executions:

```
mininet-wifi> h1 ping -c 1 h2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=4.21 ms

--- 10.0.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 4.217/4.217/4.217/0.000 ms
```

```
t@mininet-vm:~# ping -c 1 10.0.0.2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=4.15 ms

--- 10.0.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 4.154/4.154/4.154/0.000 ms
```


Using iproute2 package
----------------------


Note this package also deprecates other network commands (all still available of course) such as ifconfig, arp, ifup, ifdown, netstat, route and others.

```
ip [options] object command [parameters]

```

1. `ip address show`: display all IP addresses and related interfaces and MAC addresses.
2. `ip route show`: display all routes in all routing tables.
3. `ip neighbour show`: display all arp table entries.


Examples:

```
mininet-wifi> h1 ip address show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: h1-eth0@if388: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 00:00:00:00:00:01 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.0.0.1/8 brd 10.255.255.255 scope global h1-eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::200:ff:fe00:1/64 scope link
       valid_lft forever preferred_lft forever
```

```
mininet-wifi> h2 ip address show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: h2-eth0@if389: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 00:00:00:00:00:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.0.0.2/8 brd 10.255.255.255 scope global h2-eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::200:ff:fe00:2/64 scope link
       valid_lft forever preferred_lft forever
```

```
mininet-wifi> h1 ip route show
10.0.0.0/8 dev h1-eth0  proto kernel  scope link  src 10.0.0.1
```

```
mininet-wifi> h2 ip route show
10.0.0.0/8 dev h2-eth0  proto kernel  scope link  src 10.0.0.2
```

```
mininet-wifi> h1 ip neighbour show
10.0.0.2 dev h1-eth0 lladdr 00:00:00:00:00:02 STALE
```

```
mininet-wifi> h2 ip neighbour show
10.0.0.1 dev h2-eth0 lladdr 00:00:00:00:00:01 STALE
```


Creating network topologies
===========================

Mininet includes a Python framework from describing network topologies.

TODO

```
git clone https://github.com/glaucogoncalves/sdnufrpe
cd sdnufrpe
```

Let's execute a simple topology named `pratica-1-II`.

```
sudo python pratica-1-II.py
```

We can also see how the contents of the script look like:


```python
#Simple practice of the course Advanced Topics in Computer Networks at UFRPE/Brazil
#Author: Kleber Leal and Glauco Goncalves, PhD

import atexit
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import info,setLogLevel

net = None

def createTopo():
        topo=Topo()

        #Create Nodes
        topo.addHost("h1")
        topo.addHost("h2")
        topo.addHost("h3")
        topo.addHost("h4")
        topo.addSwitch('s1')
        topo.addSwitch('s2')
        topo.addSwitch('s3')

        #Create links
        topo.addLink('s1','s2')
        topo.addLink('s1','s3')
        topo.addLink('h1','s2')
        topo.addLink('h2','s2')
        topo.addLink('h3','s3')
        topo.addLink('h4','h3')
        return topo

def startNetwork():
        topo = createTopo()
        global net
        net = Mininet(topo=topo, autoSetMacs=True)
        net.start()
        CLI(net)

def stopNetwork():
        if net is not None:
                net.stop()

if __name__ == '__main__':
        atexit.register(stopNetwork)
        setLogLevel('info')
        startNetwork()
```

If we check this topology for conectivity, we can see that hosts h1, h2 and h3 can ping each other, by h4 has no connectivity.


```
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2 h3 X
h2 -> h1 h3 X
h3 -> h1 h2 X
h4 -> X X X
*** Results: 50% dropped (6/12 received)
```

By analyzing the script source code, we can see that hosts h1 to h3 are connected in the same network through switches s2 or s3 and s2 and s3 are connected through s1. The host h4 is the only exception and it's connected directly to h3 instead. We can try to add h4 to the switch tree so it will be in the same network as the other hosts.

W can edit `pratica-1-II.py` with the following diff:

```
wifi@wifi-VirtualBox:~/sdnufrpe$ git diff
diff --git a/pratica-1-II.py b/pratica-1-II.py
index 6e53746..3194886 100644
--- a/pratica-1-II.py
+++ b/pratica-1-II.py
-        topo.addLink('h4','h3')
+        topo.addLink('h4','s3')
```

We can now restart the topology and check for connectivity again. We can see that the applied patch works.


```
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2 h3 h4
h2 -> h1 h3 h4
h3 -> h1 h2 h4
h4 -> h1 h2 h3
*** Results: 0% dropped (12/12 received)
```

Defining bandwidth, delay, and loss rate of packets of network links
====================================================================

TODO


```python
#Exercise practice of the course Advanced Topics in Computer Networks at UFRPE/Brazil
#Author: Kleber Leal and Glauco Goncalves, PhD

import atexit
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import info,setLogLevel
from mininet.link import TCLink

net = None

def createTopo():
        topo=Topo()

        #Create Nodes
        topo.addHost("h1")
        topo.addHost("h2")
        topo.addHost("h3")
        topo.addHost("h4")
        topo.addSwitch('s1')
        topo.addSwitch('s2')
        topo.addSwitch('s3')

        #Create links
        topo.addLink('s1','s2',bw=100,delay='100ms',loss=10)
        topo.addLink('s1','s3')
        topo.addLink('h1','s2')
        topo.addLink('h2','s2')
        topo.addLink('h3','s3')
        topo.addLink('h4','s3')
        return topo

def startNetwork():
        topo = createTopo()
        global net
        net = Mininet(topo=topo, autoSetMacs=True, link=TCLink)
        net.start()
        CLI(net)

def stopNetwork():
        if net is not None:
                net.stop()

if __name__ == '__main__':
        atexit.register(stopNetwork)
        setLogLevel('info')
        startNetwork()
```

TODO

```

mininet> h1 ping -c 20 h2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=7.83 ms
64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.326 ms
64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=0.043 ms
64 bytes from 10.0.0.2: icmp_seq=4 ttl=64 time=0.059 ms
64 bytes from 10.0.0.2: icmp_seq=5 ttl=64 time=0.042 ms
64 bytes from 10.0.0.2: icmp_seq=6 ttl=64 time=0.036 ms
64 bytes from 10.0.0.2: icmp_seq=7 ttl=64 time=0.056 ms
64 bytes from 10.0.0.2: icmp_seq=8 ttl=64 time=0.042 ms
64 bytes from 10.0.0.2: icmp_seq=9 ttl=64 time=0.061 ms
64 bytes from 10.0.0.2: icmp_seq=10 ttl=64 time=0.184 ms
64 bytes from 10.0.0.2: icmp_seq=11 ttl=64 time=0.059 ms
64 bytes from 10.0.0.2: icmp_seq=12 ttl=64 time=0.091 ms
64 bytes from 10.0.0.2: icmp_seq=13 ttl=64 time=0.048 ms
64 bytes from 10.0.0.2: icmp_seq=14 ttl=64 time=0.038 ms
64 bytes from 10.0.0.2: icmp_seq=15 ttl=64 time=0.041 ms
64 bytes from 10.0.0.2: icmp_seq=16 ttl=64 time=0.060 ms
64 bytes from 10.0.0.2: icmp_seq=17 ttl=64 time=0.043 ms
64 bytes from 10.0.0.2: icmp_seq=18 ttl=64 time=0.061 ms
64 bytes from 10.0.0.2: icmp_seq=19 ttl=64 time=0.047 ms
64 bytes from 10.0.0.2: icmp_seq=20 ttl=64 time=0.042 ms

--- 10.0.0.2 ping statistics ---
20 packets transmitted, 20 received, 0% packet loss, time 19013ms
rtt min/avg/max/mdev = 0.036/0.460/7.830/1.692 ms
```

```
mininet> h1 ping -c 20 h4
PING 10.0.0.4 (10.0.0.4) 56(84) bytes of data.
64 bytes from 10.0.0.4: icmp_seq=1 ttl=64 time=210 ms
64 bytes from 10.0.0.4: icmp_seq=2 ttl=64 time=203 ms
64 bytes from 10.0.0.4: icmp_seq=3 ttl=64 time=202 ms
64 bytes from 10.0.0.4: icmp_seq=4 ttl=64 time=211 ms
64 bytes from 10.0.0.4: icmp_seq=5 ttl=64 time=200 ms
64 bytes from 10.0.0.4: icmp_seq=6 ttl=64 time=200 ms
64 bytes from 10.0.0.4: icmp_seq=7 ttl=64 time=208 ms
64 bytes from 10.0.0.4: icmp_seq=8 ttl=64 time=201 ms
64 bytes from 10.0.0.4: icmp_seq=9 ttl=64 time=200 ms
64 bytes from 10.0.0.4: icmp_seq=10 ttl=64 time=204 ms
64 bytes from 10.0.0.4: icmp_seq=11 ttl=64 time=201 ms
64 bytes from 10.0.0.4: icmp_seq=12 ttl=64 time=201 ms
64 bytes from 10.0.0.4: icmp_seq=13 ttl=64 time=201 ms
64 bytes from 10.0.0.4: icmp_seq=15 ttl=64 time=208 ms
64 bytes from 10.0.0.4: icmp_seq=17 ttl=64 time=201 ms
64 bytes from 10.0.0.4: icmp_seq=18 ttl=64 time=211 ms
64 bytes from 10.0.0.4: icmp_seq=20 ttl=64 time=201 ms

--- 10.0.0.4 ping statistics ---
20 packets transmitted, 17 received, 15% packet loss, time 19079ms
rtt min/avg/max/mdev = 200.379/204.203/211.469/3.943 ms
```


```
mininet> iperf h1 h2
*** Iperf: testing TCP bandwidth between h1 and h2
*** Results: ['57.4 Gbits/sec', '57.4 Gbits/sec']
```

```
mininet> iperf h1 h4
*** Iperf: testing TCP bandwidth between h1 and h4
*** Results: ['203 Kbits/sec', '229 Kbits/sec']
```

**Curiosity**: You can also check the UDP bandwidth using `iperfudp`. We can see that if we don't care about packet loss that much we can achieve a much higher bandwidth, but that's usually a challenge for most web applications.

```
mininet> iperfudp 20M h1 h4
*** Iperf: testing UDP bandwidth between h1 and h4
*** Results: ['20M', '18.0 Mbits/sec', '18.0 Mbits/sec']
```


Experimenting with a more complex topology
==========================================

Topology:

```
Core:
  Distribution 1:
    Access 1:
      Host 1
      Host 2

    Access 2:
      Host 3
      Host 4

  Distribution 2:
    Access 3:
      Host 5
      Host 6

    Access 4:
      Host 7
      Host 8
```

Link Parameters:

* Core to Distribution (d1,d2): 10Gbps, 1ms
* Distribution to Access (a1,a2,a3,a4): 1Gbps, 3ms
* Access to Hosts: 100Mbps, 5ms


```
wifi@wifi-VirtualBox:~$ sudo python shared/mininet-tutorial/example_1_4.py
```

```
mininet> net
h1 h1-eth0:s1-eth2
h2 h2-eth0:s1-eth3
h3 h3-eth0:s2-eth2
h4 h4-eth0:s2-eth3
h5 h5-eth0:s3-eth2
h6 h6-eth0:s3-eth3
h7 h7-eth0:s4-eth2
h8 h8-eth0:s4-eth3
a1 lo:  a1-eth1:c1-eth1 a1-eth2:s1-eth1 a1-eth3:s2-eth1
a2 lo:  a2-eth1:c1-eth2 a2-eth2:s3-eth1 a2-eth3:s4-eth1
c1 lo:  c1-eth1:a1-eth1 c1-eth2:a2-eth1
s1 lo:  s1-eth1:a1-eth2 s1-eth2:h1-eth0 s1-eth3:h2-eth0
s2 lo:  s2-eth1:a1-eth3 s2-eth2:h3-eth0 s2-eth3:h4-eth0
s3 lo:  s3-eth1:a2-eth2 s3-eth2:h5-eth0 s3-eth3:h6-eth0
s4 lo:  s4-eth1:a2-eth3 s4-eth2:h7-eth0 s4-eth3:h8-eth0
c0
```

```
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2 h3 h4 h5 h6 h7 h8
h2 -> h1 h3 h4 h5 h6 h7 h8
h3 -> h1 h2 h4 h5 h6 h7 h8
h4 -> h1 h2 h3 h5 h6 h7 h8
h5 -> h1 h2 h3 h4 h6 h7 h8
h6 -> h1 h2 h3 h4 h5 h7 h8
h7 -> h1 h2 h3 h4 h5 h6 h8
h8 -> h1 h2 h3 h4 h5 h6 h7
*** Results: 0% dropped (56/56 received)
```

```
mininet> iperf h1 h2
*** Iperf: testing TCP bandwidth between h1 and h2
*** Results: ['67.5 Mbits/sec', '79.5 Mbits/sec']
mininet> iperf h1 h3
*** Iperf: testing TCP bandwidth between h1 and h3
*** Results: ['74.3 Mbits/sec', '88.0 Mbits/sec']
mininet> iperf h1 h5
*** Iperf: testing TCP bandwidth between h1 and h5
*** Results: ['79.4 Mbits/sec', '94.7 Mbits/sec']
```



Curiosity: Why the first ping takes longer?
===========================================

TODO

Hip: ARP

Set manual -> Nope

Explain


References
==========

Packet Pushers. The Linux ip Command – An Ostensive Overview. https://packetpushers.net/linux-ip-command-ostensive-definition/
