Static IP Routing
=================

Activity 1
==========


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

