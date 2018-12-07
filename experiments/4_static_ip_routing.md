Static IP Routing
=================

On this activity, we'll explore network routing with manually described IP routing tables.
Although setting manual routes is usually hard to maintain in large networks, being replaced for
autonomous protocols such as RIP or OSPF, it's still widely used in small networks or when system
administrators want to have full control of the network.

Using Miniedit Tool
===================

First, we'll explore a Mininet tool that is useful for describing and presenting complex interfaces
called Miniedit. Miniedit is a Python based graphical interface for describing most common network devices
such as routers, hosts and switches. You can start it with the command below:

```
python mininet/examples/miniedit.py
```

It's also able to generate a Mininet Python script using the export command. On the next steps we'll be using
the Mininet topology below described with Miniedit. It's generated source is available at
[examples/example_3_1.py](examples/example_3_1.py)

<img src="../img/4_miniedit_topology.png " alt="Miniedit described topology" width="500">


ARP Auto-discovery
==================

Before going straightforward to IP routing, we can also explore the OSI Layer 2/3 interface performed by
the ARP protocol. The ARP protocol is responsible for finding the IP address of a host using layer 2
broadcasting. ARP is used to build the neighborhood of a device so it can ping other devices within
the same network.

By checking the ARP tables during the topology initialization, we can see that all ARP tables are empty.

```
mininet> h1 ip neighbour show
mininet> h2 ip neighbour show
mininet> h3 ip neighbour show
mininet> h4 ip neighbour show
```

By trying to communicate two hosts, we can see that their entries were added to both host ARP tables.

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

If we ask ping all hosts in the topology, we can than see the resulting ARP tables now contain all
the other hosts.

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

Switching loops (or layer 2 loops)
----------------------------------

Notice that the topology above doesn't have loops. Layer two, or switching loops happen when there's at least
two layer 2 devices between two devices. That can lead to broadcast messages, such as "Who has?" ARP messages
to be retransmitted infinitely, causing a flood of packages on the network.

Solutions to prevent switching loops can address the network topology, by preventing physical loops between
devices or with software solutions such as the [spanning tree protocol](https://en.wikipedia.org/wiki/Spanning_Tree_Protocol).


Default IP routing
------------------

On the last step, we noticed that there's no connectivity from routes r{2-6} to the hosts.
We can check the hosts IP routing tables.

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

By looking at the router statement in the script, we can see that it's in fact defined as a simple Linux
host with an additional kernel command to enable IP Forwarding between network interfaces. We can also see
that the router IP has not been configured yet.

```python
r1 = net.addHost('r1', cls=Node, ip='0.0.0.0')
r1.cmd('sysctl -w net.ipv4.ip_forward=1')
```

Configuring IP routes
=====================

On this example, we'll use the script [examples/example_3_2.py](examples/example_3_2.py). We basically
adapted the script used on the last session to include the routers IP addresses. We will try to reproduce
the topology described on the figure below. We can see that it has two subnetworks ranging from
`10.0.0.0/23` (broadcast `10.0.1.255`) and `10.0.2.0/23` (broadcast `10.0.3.255`).

<img src="../img/4_two_subnetworks_topology.png " alt="Topology with two subnetworks." width="500">

We can add the second subnetwork to the existing typology by applying the following diff:

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

We can check connectivity between hosts and as expected two hosts from different subnetworks
can't ping each other. That happens because there's no known routes between the two subnetworks
in the routers.

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

It's worth noticing the difference in the TTL of the ICMP `ping` packages. If we ping between two hosts between the same subnetwork the TTL is equals to 64.
When using `ping` through different subnetworks, the TTL is decreased by one in every hop.
This avoids IP packages being trapped in routing loops and staying a long time in the network.
Packages that don't reach their destination before TTL reaches zero are dropped.

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

Building complex topologies with static routes
==============================================

On this example, our challenge is to create a more complex topology with static IP routes
between subnetworks using Mininet. The expected topology is in the figure below.

<img src="img/4_multiple_subnetworks_topology.png" alt="Topology with multiple subnetworks." width="500">

The script describing the topology is available at [examples/example_3_3.py](examples/example_3_3.py).
We will go through the steps used to describe it.

First, we created a class representing a Router. It basically runs the kernel command to enable IP
forwarding during the startup described on the last session and a python method that gives us a
friendly programming interface to the `ip route add` command.

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

Next, we create the topology itself by describing the hosts, routers, the switch for the subnetwork 10.0.0.0
and their links. We also set the IP for every interface of the routers and hosts.


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

Finally, we reach the routing table setup. We manually add a route to all the routers so than can ping
each other. The strategy used was to manually assign the shortest path for every subnetwork.

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

We can check for connectivity using the `pingall` command.

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

The `tracepath` command between hosts are also an interesting way to confirm that the hosts have
the defined path between each other. A `ping` command will also tell us the TTL for each path.

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

Finally, we can also check that all routers routing tables have routes to all the defined IP ranges.

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


Adding a NAT
============

Network address translation, or NAT, is a network interface capable of mapping one IP range into another
by modifying each packet IP header. It's specially useful for mapping local or virtualized networks into
physical or publicly exposed addresses. They can be found in network access points or in virtualization
softwares such as [Docker](https://docs.docker.com/v17.09/engine/userguide/networking/#an-overlay-network-without-swarm-mode).

Mininet already provides an easy way to define a NAT for the virtualized network into the host network.
We can add it with the following diff. Notice that we are setting all router default routes to the NAT,
so it behaves such as the internet on our topology.

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

We can check that the NAT is working by trying to Ping a publicly available IP, such
as [Google Public DNS](https://developers.google.com/speed/public-dns/) at IP `8.8.8.8`.


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
