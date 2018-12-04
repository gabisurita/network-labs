Static IP Routing
=================

Activity 1
==========

Using Miniedit Tool
-------------------

<img src="../img/4_miniedit_topology.png " alt="Miniedit described topology" width="500">


ARP Auto-discovery
------------------

```
mininet> h1 ip neighbour show
mininet> h2 ip neighbour show
mininet> h3 ip neighbour show
mininet> h4 ip neighbour show
```

```
ininet> h1 ping -c 1 h2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=0.626 ms
--- 10.0.0.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 999ms
rtt min/avg/max/mdev = 0.072/0.349/0.626/0.277 ms
```

```
mininet> h1 ip neighbour show
10.0.0.2 dev h1-eth0 lladdr 36:a0:fa:07:aa:f6 REACHABLE
mininet> h2 ip neighbour show
10.0.0.1 dev h2-eth0 lladdr da:8e:41:d3:7e:d2 REACHABLE
```


```
mininet> pingall
*** Ping: testing ping reachability
r2 -> r1 r4 r3 r6 r5 X X X X X
r1 -> r2 r4 r3 r6 r5 X X X X X
r4 -> r2 r1 r3 r6 r5 X X X X X
r3 -> r2 r1 r4 r6 r5 X X X X X
r6 -> r2 r1 r4 r3 r5 X X X X X
r5 -> r2 r1 r4 r3 r6 X X X X X
h2 -> r2 r1 r4 r3 r6 r5 h4 h1 h3 h5
h4 -> r2 r1 r4 r3 r6 r5 h2 h1 h3 h5
h1 -> r2 r1 r4 r3 r6 r5 h2 h4 h3 h5
h3 -> r2 r1 r4 r3 r6 r5 h2 h4 h1 h5
h5 -> r2 r1 r4 r3 r6 r5 h2 h4 h1 h3
*** Results: 27% dropped (80/110 received)
```

```
mininet> h1 ip neighbour show
10.0.0.2 dev h1-eth0 lladdr c2:11:95:e9:54:e3 REACHABLE
10.0.0.3 dev h1-eth0 lladdr 9e:fe:b0:2a:7b:e7 REACHABLE
10.0.0.4 dev h1-eth0 lladdr 0a:7d:10:ea:7b:c9 REACHABLE
10.0.0.5 dev h1-eth0 lladdr 0a:57:01:d3:a4:8b REACHABLE
mininet> h2 ip neighbour show
10.0.0.1 dev h2-eth0 lladdr 86:b1:45:3d:d3:65 REACHABLE
10.0.0.3 dev h2-eth0 lladdr 9e:fe:b0:2a:7b:e7 REACHABLE
10.0.0.5 dev h2-eth0 lladdr 0a:57:01:d3:a4:8b REACHABLE
10.0.0.4 dev h2-eth0 lladdr 0a:7d:10:ea:7b:c9 REACHABLE
mininet> h3 ip neighbour show
10.0.0.1 dev h3-eth0 lladdr 86:b1:45:3d:d3:65 STALE
10.0.0.4 dev h3-eth0 lladdr 0a:7d:10:ea:7b:c9 STALE
10.0.0.5 dev h3-eth0 lladdr 0a:57:01:d3:a4:8b STALE
10.0.0.2 dev h3-eth0 lladdr c2:11:95:e9:54:e3 STALE
mininet> h4 ip neighbour show
10.0.0.3 dev h4-eth0 lladdr 9e:fe:b0:2a:7b:e7 STALE
10.0.0.2 dev h4-eth0 lladdr c2:11:95:e9:54:e3 STALE
10.0.0.5 dev h4-eth0 lladdr 0a:57:01:d3:a4:8b STALE
10.0.0.1 dev h4-eth0 lladdr 86:b1:45:3d:d3:65 STALE
```

Default IP routing
------------------

On the last step, we noticed that there's no connectivity from routes r{2-6} to the hosts. We can check the ho


```
mininet> h1 ip route show
10.0.0.0/8 dev h1-eth0  proto kernel  scope link  src 10.0.0.1
mininet> h2 ip route show
10.0.0.0/8 dev h2-eth0  proto kernel  scope link  src 10.0.0.2
mininet> h3 ip route show
10.0.0.0/8 dev h3-eth0  proto kernel  scope link  src 10.0.0.3
mininet> h4 ip route show
10.0.0.0/8 dev h4-eth0  proto kernel  scope link  src 10.0.0.4
```

Olhando para a declaração do roteador no script, vemos que de fato o IP das máquinas ainda não foi configurado. Observamos ainda que o roteador nada mais é do que um host como um outro host Linux qualquer, com exceção que o kernel foi configurado para fazer redirecionamento de pacotes ao invés de descartar pacotes IP que não são para o próprio host.

```python
r1 = net.addHost('r1', cls=Node, ip='0.0.0.0')
r1.cmd('sysctl -w net.ipv4.ip_forward=1')
```

Os roteadores, no entanto, ainda não estão configurados. Não foram configurados endereços de IP, subredes, nem entradas de roteamento.


Activity 2
==========

Two subnetworks `10.0.0.0/23` (broadcast `10.0.1.255`) and `10.0.2.0/23` (broadcast `10.0.3.255`).

We can add the second subnetwork to the existing typology:

```diff
git diff
diff --git a/example_3_2.py b/example_3_2.py
index 2113f67..293eb28 100644
--- a/example_3_2.py
+++ b/example_3_2.py
@@ -47,16 +47,25 @@ def build_topo(net):
+
+    R1 = net.get("r1")
+    HOST_101 = net.addHost(
+        "h101", ip="10.0.2.101/23", defaultRoute="via 10.0.2.21"
+    )
+
+    net.addLink(HOST_101, R1, intfName2="r1-eth4")
+    R1.setIP("10.0.2.21", intf="r1-eth4")
+

```

We can check connectivity between hosts and as expected two hosts from different subnetworks can't ping each other.

```
mininet> pingall
*** Ping: testing ping reachability
r1 -> r2 r3 r4 r5 r6 h1 h2 h3 h4 h5 h101
r2 -> r1 r3 r4 r5 r6 h1 h2 h3 h4 h5 X
r3 -> r1 r2 r4 r5 r6 h1 h2 h3 h4 h5 X
r4 -> r1 r2 r3 r5 r6 h1 h2 h3 h4 h5 X
r5 -> r1 r2 r3 r4 r6 h1 h2 h3 h4 h5 X
r6 -> r1 r2 r3 r4 r5 h1 h2 h3 h4 h5 X
h1 -> r1 r2 r3 r4 r5 r6 h2 h3 h4 h5 X
h2 -> r1 r2 r3 r4 r5 r6 h1 h3 h4 h5 X
h3 -> r1 r2 r3 r4 r5 r6 h1 h2 h4 h5 X
h4 -> r1 r2 r3 r4 r5 r6 h1 h2 h3 h5 X
h5 -> r1 r2 r3 r4 r5 r6 h1 h2 h3 h4 X
h101 -> r1 X X X X X X X X X X
*** Results: 15% dropped (112/132 received)
```

This can be solved by adding manual IP routes to all the hosts.

```
mininet> h1 ip route add 10.0.2.0/23 via 10.0.1.21
mininet> h2 ip route add 10.0.2.0/23 via 10.0.1.21
mininet> h3 ip route add 10.0.2.0/23 via 10.0.1.21
mininet> h4 ip route add 10.0.2.0/23 via 10.0.1.21
mininet> h5 ip route add 10.0.2.0/23 via 10.0.1.21
mininet> r1 ip route add 10.0.2.0/23 via 10.0.1.21
mininet> r2 ip route add 10.0.2.0/23 via 10.0.1.21
mininet> r3 ip route add 10.0.2.0/23 via 10.0.1.21
mininet> r4 ip route add 10.0.2.0/23 via 10.0.1.21
mininet> r5 ip route add 10.0.2.0/23 via 10.0.1.21
mininet> r6 ip route add 10.0.2.0/23 via 10.0.1.21
```

Checking connectivity again, we can see that now all hosts can ping each other.

```
mininet> pingall
*** Ping: testing ping reachability
r1 -> r2 r3 r4 r5 r6 h1 h2 h3 h4 h5 h101
r2 -> r1 r3 r4 r5 r6 h1 h2 h3 h4 h5 h101
r3 -> r1 r2 r4 r5 r6 h1 h2 h3 h4 h5 h101
r4 -> r1 r2 r3 r5 r6 h1 h2 h3 h4 h5 h101
r5 -> r1 r2 r3 r4 r6 h1 h2 h3 h4 h5 h101
r6 -> r1 r2 r3 r4 r5 h1 h2 h3 h4 h5 h101
h1 -> r1 r2 r3 r4 r5 r6 h2 h3 h4 h5 h101
h2 -> r1 r2 r3 r4 r5 r6 h1 h3 h4 h5 h101
h3 -> r1 r2 r3 r4 r5 r6 h1 h2 h4 h5 h101
h4 -> r1 r2 r3 r4 r5 r6 h1 h2 h3 h5 h101
h5 -> r1 r2 r3 r4 r5 r6 h1 h2 h3 h4 h101
h101 -> r1 r2 r3 r4 r5 r6 h1 h2 h3 h4 h5
*** Results: 0% dropped (132/132 received)
```

It's worth noticing the difference in the TTL of the ICMP `ping` packages. If we ping between two hosts between the same subnetwork the TTL is equals to 64. When using `ping` through different subnetworks, the TTL is decreased by one in every hop.

```
mininet> h1 ping -c1 h2
PING 10.0.0.102 (10.0.0.102) 56(84) bytes of data.
64 bytes from 10.0.0.102: icmp_seq=1 ttl=64 time=0.377 ms

--- 10.0.0.102 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.377/0.377/0.377/0.000 ms
mininet> h1 ping -c1 h101
PING 10.0.2.101 (10.0.2.101) 56(84) bytes of data.
64 bytes from 10.0.2.101: icmp_seq=1 ttl=63 time=0.347 ms

--- 10.0.2.101 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.347/0.347/0.347/0.000 ms
```

Activity 3
==========


```
mininet> pingall
*** Ping: testing ping reachability
r1 -> r2 r3 r4 r5 r6 h1 h101 h110
r2 -> r1 r3 r4 r5 r6 h1 h101 h110
r3 -> r1 r2 r4 r5 r6 h1 h101 h110
r4 -> r1 r2 r3 r5 r6 h1 h101 h110
r5 -> r1 r2 r3 r4 r6 h1 h101 h110
r6 -> r1 r2 r3 r4 r5 h1 h101 h110
h1 -> r1 r2 r3 r4 r5 r6 h101 h110
h101 -> r1 r2 r3 r4 r5 r6 h1 h110
h110 -> r1 r2 r3 r4 r5 r6 h1 h101
*** Results: 0% dropped (72/72 received)
```

```
mininet> h1 tracepath h101
 1?: [LOCALHOST]                                         pmtu 1500
 1:  10.0.1.25                                             0.202ms
 1:  10.0.1.25                                             0.014ms
 2:  10.0.11.21                                            0.015ms
 3:  10.0.2.101                                            0.039ms reached
     Resume: pmtu 1500 hops 3 back 3

mininet> h1 tracepath h110
 1?: [LOCALHOST]                                         pmtu 1500
 1:  10.0.1.24                                             0.191ms
 1:  10.0.1.24                                             0.014ms
 2:  10.0.12.110                                           0.014ms reached
     Resume: pmtu 1500 hops 2 back 2

mininet> h110 tracepath h1
 1?: [LOCALHOST]                                         pmtu 1500
 1:  10.0.13.24                                            0.027ms
 1:  10.0.13.24                                            0.010ms
 2:  10.0.0.101                                            0.142ms reached
     Resume: pmtu 1500 hops 2 back 2
mininet>
```


```
mininet> h1 ping -c 3 h101
PING 10.0.2.101 (10.0.2.101) 56(84) bytes of data.
64 bytes from 10.0.2.101: icmp_seq=1 ttl=62 time=0.033 ms
64 bytes from 10.0.2.101: icmp_seq=2 ttl=62 time=0.047 ms
64 bytes from 10.0.2.101: icmp_seq=3 ttl=62 time=0.077 ms

--- 10.0.2.101 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1998ms
rtt min/avg/max/mdev = 0.033/0.052/0.077/0.019 ms

mininet> h1 ping -c 3 h110
PING 10.0.12.110 (10.0.12.110) 56(84) bytes of data.
From 10.0.1.25: icmp_seq=1 Redirect Host(New nexthop: 10.0.1.24)
64 bytes from 10.0.12.110: icmp_seq=1 ttl=63 time=0.357 ms
64 bytes from 10.0.12.110: icmp_seq=2 ttl=63 time=0.232 ms
64 bytes from 10.0.12.110: icmp_seq=3 ttl=63 time=0.083 ms

--- 10.0.12.110 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1998ms
rtt min/avg/max/mdev = 0.083/0.224/0.357/0.112 ms

mininet> h101 ping -c 3 h110
PING 10.0.12.110 (10.0.12.110) 56(84) bytes of data.
64 bytes from 10.0.12.110: icmp_seq=1 ttl=61 time=0.305 ms
64 bytes from 10.0.12.110: icmp_seq=2 ttl=61 time=0.056 ms
64 bytes from 10.0.12.110: icmp_seq=3 ttl=61 time=0.065 ms

--- 10.0.12.110 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1998ms
rtt min/avg/max/mdev = 0.056/0.142/0.305/0.115 ms
```

```
mininet> r1 ip route
10.0.0.0/23 via 10.0.11.25 dev eth3
10.0.2.0/23 dev eth4  proto kernel  scope link  src 10.0.3.21
10.0.4.0/23 dev eth1  proto kernel  scope link  src 10.0.5.21
10.0.6.0/23 via 10.0.5.22 dev eth1
10.0.8.0/23 via 10.0.5.22 dev eth1
10.0.10.0/23 dev eth3  proto kernel  scope link  src 10.0.11.21
10.0.12.0/23 via 10.0.11.25 dev eth3

mininet> r2 ip route
10.0.0.0/23 via 10.0.5.21 dev eth2
10.0.2.0/23 via 10.0.5.21 dev eth2
10.0.4.0/23 dev eth2  proto kernel  scope link  src 10.0.5.22
10.0.6.0/23 dev eth1  proto kernel  scope link  src 10.0.7.22
10.0.8.0/23 via 10.0.7.23 dev eth1
10.0.10.0/23 via 10.0.5.21 dev eth2
10.0.12.0/23 via 10.0.7.23 dev eth1

mininet> r3 ip route
10.0.0.0/23 via 10.0.9.24 dev eth1
10.0.2.0/23 via 10.0.7.22 dev eth2
10.0.4.0/23 via 10.0.7.22 dev eth2
10.0.6.0/23 dev eth2  proto kernel  scope link  src 10.0.7.23
10.0.8.0/23 dev eth1  proto kernel  scope link  src 10.0.9.23
10.0.10.0/23 via 10.0.7.22 dev eth2
10.0.12.0/23 via 10.0.9.24 dev eth1

mininet> r4 ip route
10.0.0.0/23 dev eth5  proto kernel  scope link  src 10.0.1.24
10.0.2.0/23 via 10.0.1.25 dev eth5
10.0.4.0/23 via 10.0.9.23 dev eth2
10.0.6.0/23 via 10.0.9.23 dev eth2
10.0.8.0/23 dev eth2  proto kernel  scope link  src 10.0.9.24
10.0.10.0/23 via 10.0.1.25 dev eth5
10.0.12.0/23 dev eth4  proto kernel  scope link  src 10.0.13.24

mininet> r5 ip route
10.0.0.0/23 dev eth5  proto kernel  scope link  src 10.0.1.25
10.0.2.0/23 via 10.0.11.21 dev eth1
10.0.4.0/23 via 10.0.11.21 dev eth1
10.0.6.0/23 via 10.0.1.24 dev eth5
10.0.8.0/23 via 10.0.1.24 dev eth5
10.0.10.0/23 dev eth1  proto kernel  scope link  src 10.0.11.25
10.0.12.0/23 via 10.0.1.24 dev eth5

mininet> r6 ip route
10.0.0.0/23 dev eth2  proto kernel  scope link  src 10.0.1.26
10.0.2.0/23 via 10.0.1.25 dev eth2
10.0.4.0/23 via 10.0.1.25 dev eth2
10.0.6.0/23 via 10.0.1.25 dev eth2
10.0.8.0/23 via 10.0.1.24 dev eth2
10.0.10.0/23 via 10.0.1.25 dev eth2
10.0.12.0/23 via 10.0.1.24 dev eth2
```


```python
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
```

```python
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
```

```python
def setup_routes(net):
    routers = [net.get(name) for name in ROUTER_NAMES]
    R1, R2, R3, R4, R5, R6 = routers

    # R1 Routes
    R1.add_route("10.0.6.0/23", "10.0.5.22")
    R1.add_route("10.0.8.0/23", "10.0.5.22")

    R1.add_route("10.0.0.0/23", "10.0.11.25")
    R1.add_route("10.0.12.0/23", "10.0.11.25")

    # R2 Routes
    R2.add_route("10.0.0.0/23", "10.0.5.21")
    R2.add_route("10.0.2.0/23", "10.0.5.21")
    R2.add_route("10.0.10.0/23", "10.0.5.21")

    R2.add_route("10.0.8.0/23", "10.0.7.23")
    R2.add_route("10.0.12.0/23", "10.0.7.23")

    # R3 Routes
    R3.add_route("10.0.2.0/23", "10.0.7.22")
    R3.add_route("10.0.4.0/23", "10.0.7.22")
    R3.add_route("10.0.10.0/23", "10.0.7.22")

    R3.add_route("10.0.0.0/23", "10.0.9.24")
    R3.add_route("10.0.12.0/23", "10.0.9.24")

    # R4 Routes
    R4.add_route("10.0.2.0/23", "10.0.1.25")
    R4.add_route("10.0.10.0/23", "10.0.1.25")

    R4.add_route("10.0.4.0/23", "10.0.9.23")
    R4.add_route("10.0.6.0/23", "10.0.9.23")

    # R5 Routes
    R5.add_route("10.0.2.0/23", "10.0.11.21")
    R5.add_route("10.0.4.0/23", "10.0.11.21")

    R5.add_route("10.0.6.0/23", "10.0.1.24")
    R5.add_route("10.0.8.0/23", "10.0.1.24")
    R5.add_route("10.0.12.0/23", "10.0.1.24")

    # R6 Routes
    R6.add_route("10.0.2.0/23", "10.0.1.25")
    R6.add_route("10.0.4.0/23", "10.0.1.25")
    R6.add_route("10.0.6.0/23", "10.0.1.25")
    R6.add_route("10.0.10.0/23", "10.0.1.25")

    R6.add_route("10.0.8.0/23", "10.0.1.24")
    R6.add_route("10.0.12.0/23", "10.0.1.24")
```

Adding a NAT
============


```diff
$ git diff
diff --git a/example_3_3.py b/example_3_3.py
index de3d31f..d9a2760 100644
--- a/example_3_3.py
+++ b/example_3_3.py
@@ -6,6 +6,7 @@ from mininet.cli import CLI
 from mininet.log import setLogLevel
 from mininet.link import TCLink
 from mininet.node import Node, OVSKernelSwitch
+from mininet.nodelib import NAT


 HOST_NAMES = ["h1", "h101", "h110"]
@@ -63,6 +64,17 @@ def build_topo(topo):
         "h110", ip="10.0.12.110/23", defaultRoute="via 10.0.13.24"
     )

+    # Create NAT node
+    nat = topo.addHost(
+        "nat1",
+        cls=NAT,
+        ip="10.0.14.1",
+        subnet='10.0.0.0/16',
+        inetIntf="eth0",
+        localIp='10.1.2.2/24',
+        inNamespace=False,
+    )
+
     topo.addLink(HOST_1, S1)
     topo.addLink(HOST_101, R1, intfName2="eth4")
     topo.addLink(HOST_110, R4, intfName2="eth4")
@@ -74,6 +86,7 @@ def build_topo(topo):
     topo.addLink(R5, S1, intfName1="eth5")
     topo.addLink(R6, S1, intfName1="eth2")
     topo.addLink(R5, R1, intfName1="eth1", intfName2="eth3")
+    topo.addLink(nat, R6, intfName2="eth1")

     # Subnet 10.0.0.0/23
     R4.setIP("10.0.1.24/23", intf="eth5")
@@ -102,10 +115,14 @@ def build_topo(topo):
     # Subnet 10.0.12.0/23
     R4.setIP("10.0.13.24/23", intf="eth4")

+    # Subnet 10.0.14.0/23
+    R6.setIP("10.0.15.26/23", intf="eth1")
+

 def setup_routes(net):
     routers = [net.get(name) for name in ROUTER_NAMES]
     R1, R2, R3, R4, R5, R6 = routers
+    nat = net.get("nat1")

     # R1 Routes
     R1.add_route("10.0.6.0/23", "10.0.5.22")
@@ -114,6 +131,8 @@ def setup_routes(net):
     R1.add_route("10.0.0.0/23", "10.0.11.25")
     R1.add_route("10.0.12.0/23", "10.0.11.25")

+    R1.setDefaultRoute("via 10.0.11.25")
+
     # R2 Routes
     R2.add_route("10.0.0.0/23", "10.0.5.21")
     R2.add_route("10.0.2.0/23", "10.0.5.21")
@@ -122,6 +141,8 @@ def setup_routes(net):
     R2.add_route("10.0.8.0/23", "10.0.7.23")
     R2.add_route("10.0.12.0/23", "10.0.7.23")

+    R2.setDefaultRoute("via 10.0.5.21")
+
     # R3 Routes
     R3.add_route("10.0.2.0/23", "10.0.7.22")
     R3.add_route("10.0.4.0/23", "10.0.7.22")
@@ -130,6 +151,8 @@ def setup_routes(net):
     R3.add_route("10.0.0.0/23", "10.0.9.24")
     R3.add_route("10.0.12.0/23", "10.0.9.24")

+    R3.setDefaultRoute("via 10.0.9.24")
+
     # R4 Routes
     R4.add_route("10.0.2.0/23", "10.0.1.25")
     R4.add_route("10.0.10.0/23", "10.0.1.25")
@@ -137,6 +160,8 @@ def setup_routes(net):
     R4.add_route("10.0.4.0/23", "10.0.9.23")
     R4.add_route("10.0.6.0/23", "10.0.9.23")

+    R4.setDefaultRoute("via 10.0.1.26")
+
     # R5 Routes
     R5.add_route("10.0.2.0/23", "10.0.11.21")
     R5.add_route("10.0.4.0/23", "10.0.11.21")
@@ -145,6 +170,8 @@ def setup_routes(net):
     R5.add_route("10.0.8.0/23", "10.0.1.24")
     R5.add_route("10.0.12.0/23", "10.0.1.24")

+    R5.setDefaultRoute("via 10.0.1.26")
+
     # R6 Routes
     R6.add_route("10.0.2.0/23", "10.0.1.25")
     R6.add_route("10.0.4.0/23", "10.0.1.25")
@@ -154,6 +181,11 @@ def setup_routes(net):
     R6.add_route("10.0.8.0/23", "10.0.1.24")
     R6.add_route("10.0.12.0/23", "10.0.1.24")

+    R6.setDefaultRoute("via 10.0.14.1")
+
+    # NAT Routes
+    nat.cmd("ip route add 10.0.0.0/16 via 10.0.15.26")
+

```



```
mininet> h101 ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
^C
--- 8.8.8.8 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1000ms

mininet> h1 ping -c 1 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=59 time=17.1 ms

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 17.104/17.104/17.104/0.000 ms
mininet> h110 ping -c 1 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=57 time=16.6 ms

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 16.647/16.647/16.647/0.000 ms
```



Appendix 1 - Mininet Issue
==========================

```python
#!/usr/bin/python

import atexit
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.node import OVSKernelSwitch


HOST_NAMES = ["h1", "h101", "h110"]
ROUTER_NAMES = ["r{}".format(id + 1) for id in range(6)]


def enable_routing(router):
    router.cmd("sysctl -w net.ipv4.ip_forward=1")


def add_route(host, address, route):
    host.cmd("echo hi")
    cmd = "ip route add {address} via {route}".format(
        address=address, route=route, host=host
    )
    host.cmd(cmd)


def build_topo(topo):
    # Create routers
    routers = [topo.addHost(name, ip=None) for name in ROUTER_NAMES]

    R1, R2, R3, R4, R5, R6 = routers

    for router in routers:
        enable_routing(router)

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

    # Subnet 10.0.0.0/23
    topo.addLink(HOST_1, S1)
    topo.addLink(R4, S1, intfName1="r4-eth5")
    topo.addLink(R5, S1, intfName1="r5-eth5")
    topo.addLink(R6, S1, intfName1="r6-eth2")

    R4.setIP("10.0.1.24/23", intf="r4-eth5")
    R5.setIP("10.0.1.25/23", intf="r5-eth5")
    R6.setIP("10.0.1.26/23", intf="r6-eth2")

    # Subnet 10.0.2.0/23
    topo.addLink(HOST_101, R1, intfName2="r1-eth4")

    R1.setIP("10.0.3.21/23", intf="r1-eth4")

    # Subnet 10.0.4.0/23
    topo.addLink(R1, R2, intfName1="r1-eth1", intfName2="r2-eth2")

    R1.setIP("10.0.5.21/23", intf="r1-eth1")
    R2.setIP("10.0.5.22/23", intf="r2-eth2")

    # Subnet 10.0.6.0/23
    topo.addLink(R2, R3, intfName1="r2-eth1", intfName2="r3-eth2")

    R2.setIP("10.0.7.22/23", intf="r2-eth1")
    R3.setIP("10.0.7.23/23", intf="r3-eth2")

    # Subnet 10.0.8.0/23
    topo.addLink(R3, R4, intfName1="r3-eth1", intfName2="r4-eth2")

    R3.setIP("10.0.9.23/23", intf="r3-eth1")
    R4.setIP("10.0.9.24/23", intf="r4-eth2")

    # Subnet 10.0.10.0/23
    topo.addLink(R1, R5, intfName1="r1-eth3", intfName2="r5-eth1")

    R5.setIP("10.0.11.25/23", intf="r5-eth1")
    R1.setIP("10.0.11.21/23", intf="r1-eth3")

    # Subnet 10.0.12.0/23
    topo.addLink(HOST_110, R4, intfName1="h110-eth0", intfName2="r4-eth4")

    R4.setIP("10.0.13.24/23", intf="r4-eth4")

    # R1 Routes
    add_route(R1, "10.0.4.0/23", "10.0.5.22")
    add_route(R1, "10.0.6.0/23", "10.0.5.22")

    add_route(R1, "10.0.0.0/23", "10.0.11.25")
    add_route(R1, "10.0.8.0/23", "10.0.11.25")
    add_route(R1, "10.0.12.0/23", "10.0.11.25")

    # R2 Routes
    add_route(R2, "10.0.0.0/23", "10.0.5.21")
    add_route(R2, "10.0.2.0/23", "10.0.5.21")
    add_route(R2, "10.0.10.0/23", "10.0.5.21")

    add_route(R2, "10.0.8.0/23", "10.0.7.23")
    add_route(R2, "10.0.12.0/23", "10.0.7.23")

    # R3 Routes
    add_route(R3, "10.0.2.0/23", "10.0.7.22")
    add_route(R3, "10.0.4.0/23", "10.0.7.22")
    add_route(R3, "10.0.10.0/23", "10.0.7.22")

    add_route(R3, "10.0.0.0/23", "10.0.9.24")
    add_route(R3, "10.0.12.0/23", "10.0.9.24")

    # R4 Routes
    add_route(R4, "10.0.2.0/23", "10.0.1.25")
    add_route(R4, "10.0.4.0/23", "10.0.1.25")
    add_route(R4, "10.0.10.0/23", "10.0.1.25")

    add_route(R4, "10.0.6.0/23", "10.0.9.24")

    # R5 Routes
    add_route(R5, "10.0.2.0/23", "10.0.11.21")
    add_route(R5, "10.0.4.0/23", "10.0.11.21")

    add_route(R5, "10.0.6.0/23", "10.0.1.25")
    add_route(R5, "10.0.8.0/23", "10.0.1.25")
    add_route(R5, "10.0.12.0/23", "10.0.1.25")

    # R6 Routes
    add_route(R6, "10.0.2.0/23", "10.0.1.25")
    add_route(R6, "10.0.4.0/23", "10.0.1.25")
    add_route(R6, "10.0.6.0/23", "10.0.1.25")
    add_route(R6, "10.0.10.0/23", "10.0.1.25")

    add_route(R6, "10.0.8.0/23", "10.0.1.24")
    add_route(R6, "10.0.12.0/23", "10.0.1.24")


def start_network(net):
    net = Mininet(build=False, autoSetMacs=True, link=TCLink)
    build_topo(net)
    net.build()
    net.start()
    CLI(net)


def stop_network(net):
    if net is not None:
        net.stop()


if __name__ == "__main__":
    net = None
    atexit.register(lambda: stop_network(net))
    setLogLevel("info")
    start_network(net)

```

```
wifi@wifi-VirtualBox:~$ sudo python shared/example_3_3.py
*** Configuring hosts
r1 r2 r3 r4 r5 r6 h1 h101 h110
*** Starting controller

*** Starting 1 switches
s1 ...
*** Starting CLI:
mininet> r6 ip route
10.0.0.0/23 dev r6-eth2  proto kernel  scope link  src 10.0.1.26
```
