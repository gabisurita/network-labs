Network Forensics
=================

Network forensics is the branch of forensic science (and more specifically of digital forensics) responsible of analyzing and studying network traffic for legal purposes such as illegal activity over the internet or digital crimes such as network invasion.

In the experiment, we will analyze some packets captured in a network and try to reconstruct the scenario that created this traffic.

For visualizing the captured data, we'll be using Wireshark and it's command line alternative `tshark` you can install it on debian based systems using:

```
sudo apt-get install tshark
```

All captures mentioned on this activity are available at `captures/example_7` directory. To visualize a capture, run:

```
wifi@wifi-VirtualBox:~$ tshark -r captures/example_7/1-2.pcap
```

By passing the option `-V`, you'll also get the frame data.


Discovering Devices
===================

Capture 1-2
===========


On capture 1-2, we can see device A getting its IP `10.0.0.12` from the DNS server running at `10.0.0.1`, performs and ARP discovery to what appears to a router, performs a DNS request to a name server at `172.31.255.2` and than send HTTP requests over TCP to a server running on `172.16.143.2` under the name `server.test`.

We can trust Host A MAC Address (`00:00:00_00:00:02`) to be their on because it's on the border of the network. Currently the only think we can be sure about device B is that it's interface is mapped to the MAC `f6:b8:e1:de:f7:38`.


DHCP Handshake
--------------

```
    1   0.000000      0.0.0.0 → 255.255.255.255 DHCP 342 DHCP Discover - Transaction ID 0x9e3a9a1e
    2   0.002148     10.0.0.1 → 255.255.255.255 DHCP 323 DHCP Offer    - Transaction ID 0x9e3a9a1e
    3   0.002703      0.0.0.0 → 255.255.255.255 DHCP 342 DHCP Request  - Transaction ID 0x9e3a9a1e
    4   0.004093     10.0.0.1 → 255.255.255.255 DHCP 323 DHCP ACK      - Transaction ID 0x9e3a9a1e
```

ARP Request
-----------

```
    9   7.139811 00:00:00_00:00:02 → Broadcast    ARP 42 Who has 10.0.0.1? Tell 10.0.0.12
   10   7.142488 f6:b8:e1:de:f7:38 → 00:00:00_00:00:02 ARP 42 10.0.0.1 is at f6:b8:e1:de:f7:38
```

DNS Request
-----------

```
   11   7.142501    10.0.0.12 → 172.31.255.2 DNS 74 Standard query 0x0176 A webserver.test
   12   7.144997    10.0.0.12 → 172.31.255.2 DNS 74 Standard query 0x44ff AAAA webserver.test
   13   7.149826 172.31.255.2 → 10.0.0.12    DNS 90 Standard query response 0x0176 A webserver.test A 172.16.143.2
   14   7.152335 172.31.255.2 → 10.0.0.12    DNS 90 Standard query response 0x44ff AAAA webserver.test A 172.16.143.2
```


HTTP Request (over TCP)
-----------------------

```
   18   7.159449    10.0.0.12 → 172.16.143.2 HTTP 188 GET /index.html HTTP/1.1
   (...)
   38   7.162307 172.16.143.2 → 10.0.0.12    HTTP 3460 HTTP/1.0 200 OK  (text/html)
```


Mapped Interfaces
-----------------


| Device | Interface |    Mac Address        |      IP      |           Roles           |
|:------:|:---------:|:---------------------:|:------------:|:-------------------------:|
|    A   |     1     |   00:00:00_00:00:02   |   10.0.0.12  | DHCP Client / HTTP Client |
|    B   |     2     | f6:b8:e1:de:f7:38 (?) |       ?      |             ?             |
|    ?   |     ?     |            ?          |   10.0.0.1   | DHCP Server / Router (?)  |
|    ?   |     ?     |            ?          | 172.31.255.2 |        DNS Server         |
|    ?   |     ?     |            ?          | 172.16.143.2 |        HTTP Server        |



Capture 3-4
===========

On capture 3-4, we can see device C also performing a DHCP Handshake to get the IP `10.0.0.13`. It than doesn't do much, just receives an ARP request that doesn't matches it's MAC.

From this capture we can't infer much about device C, it's probably an idle host, but this gives information about device B since it did let an ARP request go through, and thus seems to be a Level 2 switch.

DHCP Handshake
--------------

```
    1   0.000000      0.0.0.0 → 255.255.255.255 DHCP 342 DHCP Discover - Transaction ID 0x9e3a9a1e
    2   0.001061     10.0.0.1 → 255.255.255.255 DHCP 323 DHCP Offer    - Transaction ID 0x9e3a9a1e
    3   0.002315      0.0.0.0 → 255.255.255.255 DHCP 342 DHCP Request  - Transaction ID 0x9e3a9a1e
    4   0.003006     10.0.0.1 → 255.255.255.255 DHCP 323 DHCP ACK      - Transaction ID 0x9e3a9a1e
    5   1.123440      0.0.0.0 → 255.255.255.255 DHCP 342 DHCP Discover - Transaction ID 0xfa0b0f5b
    6   1.125826     10.0.0.1 → 255.255.255.255 DHCP 323 DHCP Offer    - Transaction ID 0xfa0b0f5b
    7   1.126265      0.0.0.0 → 255.255.255.255 DHCP 342 DHCP Request  - Transaction ID 0xfa0b0f5b
    8   1.128055     10.0.0.1 → 255.255.255.255 DHCP 323 DHCP ACK      - Transaction ID 0xfa0b0f5b
```

ARP Request
-----------

```
    9   7.140100 00:00:00_00:00:02 → Broadcast    ARP 42 Who has 10.0.0.1? Tell 10.0.0.12
```

DHCP Handshake ACK
------------------

```
Frame 8: 323 bytes on wire (2584 bits), 323 bytes captured (2584 bits)
Bootstrap Protocol (ACK)
    Message type: Boot Reply (2)
    Hardware type: Ethernet (0x01)
    Hardware address length: 6
    Hops: 0
    Transaction ID: 0xfa0b0f5b
    Seconds elapsed: 0
    Bootp flags: 0x0000 (Unicast)
        0... .... .... .... = Broadcast flag: Unicast
        .000 0000 0000 0000 = Reserved flags: 0x0000
    Client IP address: 0.0.0.0
    Your (client) IP address: 10.0.0.13
    Next server IP address: 0.0.0.0
    Relay agent IP address: 0.0.0.0
    Client MAC address: 00:00:00_00:00:03 (00:00:00:00:00:03)
    Client hardware address padding: 00000000000000000000
    Server host name not given
    Boot file name not given
    Magic cookie: DHCP
    Option: (53) DHCP Message Type (ACK)
        Length: 1
        DHCP: ACK (5)
    Option: (54) DHCP Server Identifier
        Length: 4
        DHCP Server Identifier: 10.0.0.1
    Option: (51) IP Address Lease Time
        Length: 4
        IP Address Lease Time: (30s) 30 seconds
    Option: (1) Subnet Mask
        Length: 4
        Subnet Mask: 255.255.255.0
    Option: (3) Router
        Length: 4
        Router: 10.0.0.1
    Option: (6) Domain Name Server
        Length: 4
        Domain Name Server: 172.31.255.2
    Option: (15) Domain Name
        Length: 5
        Domain Name: local
    Option: (255) End
        Option End: 255
```

Mapped Interfaces
-----------------

| Device | Interface |    Mac Address    |      IP      |           Roles           |
|:------:|:---------:|:-----------------:|:------------:|:-------------------------:|
|    A   |     1     | 00:00:00_00:00:02 |   10.0.0.12  | DHCP Client / HTTP Client |
|    B   |     2     |         NA        |      NA      |         L2 Switch         |
|    B   |     3     |         NA        |      NA      |         L2 Switch         |
|    C   |     4     | 00:00:00_00:00:03 |   10.0.0.13  |        DHCP Client        |
|    ?   |     ?     | f6:b8:e1_de:f7:38 |       ?      |             ?             |
|    ?   |     ?     |         ?         |   10.0.0.1   | DHCP Server / Router (?)  |
|    ?   |     ?     |         ?         | 172.31.255.2 |        DNS Server         |
|    ?   |     ?     |         ?         | 172.16.143.2 |        HTTP Server        |



Capture 5-6
===========

On capture 5-6 we can see all the outbound traffic than we've seem on 1-2 and 3-4, which makes us infer that it's probably a router or a switch. By looking at the ARP request we've seem on 1-2, we can see the response message on this host, and that it matches the device D address. This information confirms that device D is a router, as well as the DHCP server.

ARP Request
-----------

```
    9   7.140099 00:00:00_00:00:02 → Broadcast    ARP 42 Who has 10.0.0.1? Tell 10.0.0.12
   10   7.140137 f6:b8:e1:de:f7:38 → 00:00:00_00:00:02 ARP 42 10.0.0.1 is at f6:b8:e1:de:f7:38
```

Mapped Interfaces
-----------------


| Device | Interface |    Mac Address    |      IP      |           Roles           |
|:------:|:---------:|:-----------------:|:------------:|:-------------------------:|
|    A   |     1     | 00:00:00_00:00:02 |   10.0.0.12  | DHCP Client / HTTP Client |
|    B   |     2     |         NA        |      NA      |         L2 Switch         |
|    B   |     3     |         NA        |      NA      |         L2 Switch         |
|    C   |     4     | 00:00:00_00:00:03 |   10.0.0.13  |        DHCP Client        |
|    B   |     5     |         NA        |      NA      |         L2 Switch         |
|    D   |     6     | f6:b8:e1_de:f7:38 |   10.0.0.1   |    DHCP Server / Router   |
|    ?   |     ?     |         ?         | 172.31.255.2 |         DNS Server        |
|    ?   |     ?     |         ?         | 172.16.143.2 |        HTTP Server        |


Capture 7-8
===========

At capture 7-8, we can see the DNS destination arriving being resolved. This let's us know that the DNS server is running on device E.

ARP Request
-----------

```
    1   0.000000 00:00:00_00:00:04 → Broadcast    ARP 42 Who has 172.31.255.2? Tell 172.31.255.1
    2   0.000018 00:00:00_00:00:01 → 00:00:00_00:00:04 ARP 42 172.31.255.2 is at 00:00:00:00:00:01

```

DNS Request
-----------

```
    3   0.000022    10.0.0.12 → 172.31.255.2 DNS 74 Standard query 0x0176 A webserver.test
    4   0.001229    10.0.0.12 → 172.31.255.2 DNS 74 Standard query 0x44ff AAAA webserver.test
    5   0.004400 172.31.255.2 → 10.0.0.12    DNS 90 Standard query response 0x0176 A webserver.test A 172.16.143.2
    6   0.008189 172.31.255.2 → 10.0.0.12    DNS 90 Standard query response 0x44ff AAAA webserver.test A 172.16.143.2
```

Mapped Interfaces
-----------------

| Device | Interface |    Mac Address    |      IP      |           Roles           |
|:------:|:---------:|:-----------------:|:------------:|:-------------------------:|
|    A   |     1     | 00:00:00_00:00:02 |   10.0.0.12  | DHCP Client / HTTP Client |
|    B   |     2     |         NA        |      NA      |         L2 Switch         |
|    B   |     3     |         NA        |      NA      |         L2 Switch         |
|    C   |     4     | 00:00:00_00:00:03 |   10.0.0.13  |        DHCP Client        |
|    B   |     5     |         NA        |      NA      |         L2 Switch         |
|    D   |     6     | f6:b8:e1_de:f7:38 |   10.0.0.1   |    DHCP Server / Router   |
|    D   |     7     | 00:00:00_00:00:04 |   10.0.0.1   |    DHCP Server / Router   |
|    E   |     8     | 00:00:00_00:00:01 | 172.31.255.2 |         DNS Server        |
|    ?   |     ?     |         ?         | 172.16.143.2 |        HTTP Server        |


Capture 9-10
============

At capture 9-10, we can see BGP packages between IPs `192.168.1.1` and `192.168.1.2`, which clearly gives us information that these both devices are BGP routers. We can also see the HTTP/TCP requests that started on Device A addressed from `192.168.1.1`, which let us know that it's associated with device D (and `192.168.1.2` is from device F). Finally, we can use that information to retrieve the MAC Addresses from the ARP request.

ARP Request
-----------

```
    1   0.000000 32:06:37:2d:43:a6 → Broadcast    ARP 42 Who has 192.168.1.2? Tell 192.168.1.1
    2   0.000042 00:00:00_00:00:05 → 32:06:37:2d:43:a6 ARP 42 192.168.1.2 is at 00:00:00:00:00:05
```

BGP Exchange
------------

```
   12   0.043629  192.168.1.2 → 192.168.1.1  BGP 119 OPEN Message
   13   0.043651  192.168.1.1 → 192.168.1.2  TCP 66 179 → 39958 [ACK] Seq=1 Ack=54 Win=29184 Len=0 TSval=415175 TSecr=415175
   14   0.044539  192.168.1.1 → 192.168.1.2  BGP 138 OPEN Message, KEEPALIVE Message
   15   0.044567  192.168.1.2 → 192.168.1.1  TCP 66 39958 → 179 [ACK] Seq=54 Ack=73 Win=29696 Len=0 TSval=415175 TSecr=415175
```

HTTP Request
------------

```
   25   1.316440  192.168.1.1 → 172.16.143.2 HTTP 188 GET /index.html HTTP/1.1
   (...)
   45   1.319227 172.16.143.2 → 192.168.1.1  HTTP 3460 HTTP/1.0 200 OK  (text/html)
```

Mapped Interfaces
-----------------


| Device | Interface |    Mac Address    |      IP      |           Roles           |
|:------:|:---------:|:-----------------:|:------------:|:-------------------------:|
|    A   |     1     | 00:00:00_00:00:02 |   10.0.0.12  | DHCP Client / HTTP Client |
|    B   |     2     |         NA        |      NA      |         L2 Switch         |
|    B   |     3     |         NA        |      NA      |         L2 Switch         |
|    C   |     4     | 00:00:00_00:00:03 |   10.0.0.13  |        DHCP Client        |
|    B   |     5     |         NA        |      NA      |         L2 Switch         |
|    D   |     6     | f6:b8:e1_de:f7:38 |   10.0.0.1   |    DHCP Server / Router   |
|    D   |     7     | 00:00:00_00:00:04 |   10.0.0.1   |    DHCP Server / Router   |
|    E   |     8     | 00:00:00_00:00:01 | 172.31.255.2 |         DNS Server        |
|    D   |     9     | 32:06:37_2d:43:a6 |  192.168.1.1 |         BGP Router        |
|    F   |     10    | 00:00:00_00:00:05 |  192.168.1.2 |         BGP Router        |
|    ?   |     ?     |         ?         | 172.16.143.2 |        HTTP Server        |


Capture 11-12
=============

Capture 11-12 simply shows the HTTP/TCP communication originated in device B that reached device F. We can tell that device F is using the IP `172.16.143.1` through the ARP request and related to MAC `be:61:96:2b:2d:5f`, but we can't get much information about device G yet.

ARP Request
-----------

```
    1   0.000000 be:61:96:2b:2d:5f → Broadcast    ARP 42 Who has 172.16.143.2? Tell 172.16.143.1
    2   0.000023 00:00:00_00:00:06 → be:61:96:2b:2d:5f ARP 42 172.16.143.2 is at 00:00:00:00:00:06
```


Mapped Interfaces
-----------------


| Device | Interface |    Mac Address    |      IP      |           Roles           |
|:------:|:---------:|:-----------------:|:------------:|:-------------------------:|
|    A   |     1     | 00:00:00_00:00:02 |   10.0.0.12  | DHCP Client / HTTP Client |
|    B   |     2     |         NA        |      NA      |         L2 Switch         |
|    B   |     3     |         NA        |      NA      |         L2 Switch         |
|    C   |     4     | 00:00:00_00:00:03 |   10.0.0.13  |        DHCP Client        |
|    B   |     5     |         NA        |      NA      |         L2 Switch         |
|    D   |     6     | f6:b8:e1_de:f7:38 |   10.0.0.1   |    DHCP Server / Router   |
|    D   |     7     | 00:00:00_00:00:04 |   10.0.0.1   |    DHCP Server / Router   |
|    E   |     8     | 00:00:00_00:00:01 | 172.31.255.2 |         DNS Server        |
|    D   |     9     | 32:06:37_2d:43:a6 |  192.168.1.1 |         BGP Router        |
|    F   |     10    | 00:00:00_00:00:05 |  192.168.1.2 |         BGP Router        |
|    F   |     11    | be:61:96:2b:2d:5f | 172.16.143.1 |           Router          |
|    G   |     12    |         ?         |       ?      |             ?             |
|    ?   |     ?     |         ?         | 172.16.143.2 |        HTTP Server        |


Capture 13-14
=============

Finally, at capture 13-14, we found exactly the same data we saw on capture 13-14, which tells us that device G is an L2 Switch, and that our HTTP server is device H and that it's MAC address is `00:00:00:00:00:06`.

Mapped Interfaces
-----------------


| Device | Interface |    Mac Address    |      IP      |           Roles           |
|:------:|:---------:|:-----------------:|:------------:|:-------------------------:|
|    A   |     1     | 00:00:00_00:00:02 |   10.0.0.12  | DHCP Client / HTTP Client |
|    B   |     2     |         NA        |      NA      |         L2 Switch         |
|    B   |     3     |         NA        |      NA      |         L2 Switch         |
|    C   |     4     | 00:00:00_00:00:03 |   10.0.0.13  |        DHCP Client        |
|    B   |     5     |         NA        |      NA      |         L2 Switch         |
|    D   |     6     | f6:b8:e1_de:f7:38 |   10.0.0.1   |    DHCP Server / Router   |
|    D   |     7     | 00:00:00_00:00:04 |   10.0.0.1   |    DHCP Server / Router   |
|    E   |     8     | 00:00:00_00:00:01 | 172.31.255.2 |         DNS Server        |
|    D   |     9     | 32:06:37_2d:43:a6 |  192.168.1.1 |         BGP Router        |
|    F   |     10    | 00:00:00_00:00:05 |  192.168.1.2 |         BGP Router        |
|    F   |     11    |  be:61:96_2b:2d:5 | 172.16.143.1 |           Router          |
|    G   |     12    |         NA        |      NA      |         L2 Switch         |
|    G   |     13    |         NA        |      NA      |         L2 Switch         |
|    H   |     14    | 00:00:00_00:00:06 | 172.16.143.2 |        HTTP Server        |


OSI Application Layer (7) Communications
========================================

DHCP Handshake
--------------

The main purpose of DHCP, or Dynamic Host Configuration Protocol, is to assign IP addresses and other networking parameters (such as DNS servers) automatically on a local network. Preventing assigning IPs manually which are usually hard to maintain.

* Works over TCP.
* Is composed of four steps, known as Discover, Offer, Request and ACK.
* Happened between:
  - A (Client) / D (Server)
  - B (Client) / D (Server)


<img src="https://en.wikipedia.org/wiki/File:DHCP_session.svg" alt="BGP Handshake" width="500">

DNS Resolution
--------------

Stains for Domain Name System and is responsible for assign an IP address for what's called a domain name. Domain names are a human friendly way to remember IP addresses. Some examples are `unicamp.br`, `google.com` or `www.wikipedia.org`.

* Works over UDP.
* Is composed of a simple request/response pair.
* Happened between A (Client) / E (Server).

HTTP Request
------------

HTTP or Hypertext Transfer Protocol is one of the most common protocols for communicating with content servers when using WEB browsers or APIs. It's known as the standard for presenting structured information int the Web.

* Works over TCP.
* Is composed of a simple request/response pair.
* Happened between A (Client) / H (Server).


OSI Transport Layer (4) Communications
======================================

TCP
---

TCP, or Transmission Control Protocol, delivers streamed data over the IP protocol and it's guaranteed to be reliable, ordered, and error-checked.

* Happened between
  - A / D (DHCP Handshake)
  - A / H (HTTP Request)
  - B / D (DHCP Handshake)
* Are composed of
  - A three way handshake (Packets SYN, SYN + ACK, and ACK).
  - Any number of packets containing data and ACKs.
  - A 4 way shutdown (FIN, ACK, FIN, ACK)


<img src="https://notes.shichao.io/unp/figure_2.5.png" alt="BGP Handshake" width="500">


UDP
---

UDP, or User Datagram Protocol, delivers data as a stream of packets that have no error checking or delivery guarantees.

* Happened between
  - A / E (DNS Resolution)
* Are simple one way streamed packets.


Replicating the scenario
========================

TODO
