# Computer Networks (BSDCBZC481)
# Session 10: Network Layer Addressing — IPv4/IPv6, Subnetting Math, NAT & DHCP
### Exhaustive Slide-by-Slide Academic Exam Revision Manual & Problem Solving Guide

---

## 1. Session Context & Pedagogical Scope
- **Course Code & Title**: BSDCBZC481 — Computer Networks
- **Instructor**: Dr. K. Kalaiselvi (BITS Pilani)
- **Primary Textbooks**:
  - J.F. Kurose & K.W. Ross, *Computer Networking: A Top-Down Approach*, 5th/6th Edition, Chapter 4 (T1)
  - B.A. Forouzan, *Data Communications and Networking*, 4th Edition, Chapters 19 & 20 (T2)
- **Lecture Slide Mapping**: CS10: Network Layer — Slides 1 to 55 (Complete Coverage)
- **Core Syllabus Covered**:
  1. IPv4 Datagram Format: Dissection of all 14 Header Fields & The 4-Byte Word Boundary
  2. IP Fragmentation & Reassembly: MTU Constraints, Fragment Offset 8-Byte Scaling & Flag Logic
  3. Classful IP Addressing History (Classes A, B, C, D, E) & Structural Inefficiencies
  4. Classless Inter-Domain Routing (CIDR, RFC 4632): Prefix Notation (`/x`) & Subnet Masks
  5. Rigorous Subnetting Mathematics: Total IPs, Usable Hosts ($2^{32-x} - 2$), Network IDs & Directed Broadcasts
  6. Variable Length Subnet Masking (VLSM) Hierarchical Network Design
  7. Dynamic Host Configuration Protocol (DHCP, RFC 2131): The Four-Step DORA Protocol Exchange
  8. Network Address Translation (NAT, RFC 3022): 16-Bit Port Translation Tables & Inbound Traversal
  9. IPv6 Protocol Suite: Fixed 40-Byte Base Header, Extension Headers & Flow Labeling
  10. Migration from IPv4 to IPv6: Dual-Stack Infrastructure vs. 6to4 Encapsulation Tunneling
  11. High-Yield Open-Book Exam Traps, Rigorous Numerical Problems & Fast Revision Checklist

---

## 2. IPv4 Datagram Architecture & Header Dissection (Slides 4–10)

The IPv4 datagram consists of a mandatory $20\text{-byte}$ base header, optional extension fields (up to $40\text{ bytes}$), and the payload data.

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          TOTAL LENGTH (16)    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         IDENTIFICATION (16)   |Flags|   FRAGMENT OFFSET (13)  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| TIME TO LIVE  |  PROTOCOL (8) |       HEADER CHECKSUM (16)    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    SOURCE IP ADDRESS (32 bits)                |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 DESTINATION IP ADDRESS (32 bits)              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    OPTIONS (0 to 40 bytes, if any)            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            PAYLOAD DATA                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### 2.1 Complete Field-by-Field Breakdown
1. **Version (4 bits)**: Defines IP version (`4` for IPv4: `0100_2`).
2. **Internet Header Length (IHL, 4 bits)**: Header length measured in **32-bit (4-byte) words**. Minimum value is $5$ ($5 \times 4 = 20\,\text{bytes}$); maximum is $15$ ($15 \times 4 = 60\,\text{bytes}$).
3. **Type of Service (ToS / DiffServ, 8 bits)**: Used for packet classification and Quality of Service (QoS). Includes 6 bits of Differentiated Services Code Point (DSCP) and 2 bits of Explicit Congestion Notification (ECN).
4. **Total Length (16 bits)**: Total length of datagram in bytes (**Header + Data**). Maximum theoretical size is $2^{16} - 1 = 65,535\,\text{bytes}$.
5. **Identification (16 bits)**: Unique sequence ID assigned by source host; shared across all fragments of the same original datagram.
6. **Flags (3 bits)**:
   - Bit 0: Reserved (must be 0).
   - Bit 1: **DF (Don't Fragment)**: If set to 1, routers are forbidden from fragmenting the datagram. If packet exceeds link MTU, router drops it and returns an ICMP "Fragmentation Needed" error.
   - Bit 2: **MF (More Fragments)**: 1 indicates more fragments follow; 0 indicates this is the final fragment.
7. **Fragment Offset (13 bits)**: Specifies the position of this fragment's payload relative to the original unfragmented payload, **measured in 8-byte (64-bit) blocks**.
8. **Time to Live (TTL, 8 bits)**: Hop limit counter decremented by 1 at every router. Prevents undeliverable packets from looping infinitely. If $TTL$ reaches 0, router drops packet and sends **ICMP Time Exceeded (Type 11, Code 0)**.
9. **Protocol (8 bits)**: Identifies the upper-layer transport protocol: `6` for TCP, `17` for UDP, `1` for ICMP, `89` for OSPF.
10. **Header Checksum (16 bits)**: 1's complement checksum protecting **only the IP header** (not data). Must be recalculated at every router because TTL changes!

---

## 3. IP Fragmentation & Reassembly (Slides 11–16)

### 3.1 Link Maximum Transmission Unit (MTU)
Different physical link-layer technologies enforce different frame payload limits (**MTU**). For example, standard Ethernet has an MTU of $1,500\,\text{bytes}$.

```
[ Big Datagram (4,000 Bytes) ] ===> [ Router R1 ] === (MTU = 1500 B) ===>
                                          |
        +---------------------------------+---------------------------------+
        |                                 |                                 |
        v                                 v                                 v
[ Frag 1: 1500 B ]               [ Frag 2: 1500 B ]               [ Frag 3: 1040 B ]
(Offset=0, MF=1)                 (Offset=185, MF=1)               (Offset=370, MF=0)
```

### 3.2 The Golden Rules of IP Fragmentation
1. **Fragmentation can occur at the source or any intermediate router**.
2. **Reassembly occurs strictly at the final destination host**, NEVER at intermediate routers! (Because fragments can take completely different paths across the network core).
3. **The 8-Byte Offset Divisibility Rule**: Every non-terminal fragment's data payload length **must be a strict multiple of 8 bytes**.
4. **Offset Formulation**:
   $$\text{Fragment Offset} = \frac{\text{Byte Position of First Data Byte in Fragment}}{8}$$

---

## 4. IPv4 Addressing: Classful Architecture vs. CIDR (Slides 17–28)

An IPv4 address is a 32-bit binary identifier assigned to every network interface card (NIC).

### 4.1 Historical Classful Addressing (Slide 19)

```
Class A:  0 [  Network ID: 7 bits  ] [       Host ID: 24 bits (16.7M hosts)       ]  0.0.0.0/8
Class B: 10 [    Network ID: 14 bits    ] [    Host ID: 16 bits (65,534 hosts)    ]  128.0.0.0/16
Class C: 110 [     Network ID: 21 bits         ] [ Host ID: 8 bits (254 hosts) ]     192.0.0.0/24
Class D: 1110 [                Multicast Group ID (28 bits)                    ]     224.0.0.0/4
Class E: 1111 [                Reserved for Experimental Use                   ]     240.0.0.0/4
```

- **The Classful Failure**: Extreme rigidity caused catastrophic address space waste. A company needing 500 IP addresses was forced to request a Class B block ($65,534$ addresses), leaving $> 65,000$ addresses permanently wasted (**internal fragmentation**).

### 4.2 Classless Inter-Domain Routing (CIDR, RFC 4632)
CIDR completely abolishes address classes. An IP address is written as:
$$\mathbf{a.b.c.d / x}$$
where $x$ denotes the **prefix length** (the number of leading bits defining the subnet/network portion). The remaining $(32 - x)$ bits identify hosts within that subnet.

---

## 5. Rigorous Subnetting Mathematics & VLSM Formulations (Slides 29–36)

### 5.1 Universal Subnetting Formulas

```
Given an IPv4 block: a.b.c.d / x

1. Number of Host Bits (h):            h = 32 - x
2. Total IP Addresses in Block:        N_total = 2^h = 2^(32 - x)
3. Total Usable Host IP Addresses:     N_usable = 2^h - 2 = 2^(32 - x) - 2
4. Subnet Mask:                        x consecutive 1s followed by (32 - x) 0s
5. Network ID (Subnet Address):        IP (bitwise AND) Subnet Mask
6. Directed Broadcast Address:         Network ID (bitwise OR) (NOT Subnet Mask)
7. First Usable Host Address:          Network ID + 1
8. Last Usable Host Address:           Broadcast Address - 1
```

> [!IMPORTANT]
> **Why Subtract 2 from Usable Host IPs?**:
> 1. **Host bits all 0s**: Reserved to identify the **Network Subnet itself** (Network ID).
> 2. **Host bits all 1s**: Reserved as the **Directed Broadcast Address** (targets all hosts in that specific subnet).

### 5.2 Private IP Address Blocks (RFC 1918)
Non-routable over the public Internet; reserved exclusively for private local networks:
- `10.0.0.0/8` ($10.0.0.0 - 10.255.255.255$): $16,777,216$ addresses.
- `172.16.0.0/12` ($172.16.0.0 - 172.31.255.255$): $1,048,576$ addresses.
- `192.168.0.0/16` ($192.168.0.0 - 192.168.255.255$): $65,536$ addresses.

---

## 6. Dynamic Host Configuration Protocol (DHCP, RFC 2131) (Slides 37–42)

DHCP is a client-server protocol enabling "plug-and-play" automated IP configuration.
- Operates over **UDP port 67 (Server)** and **UDP port 68 (Client)**.
- Allocates: IP address, Subnet Mask, Default Gateway router IP, and Local DNS server IP.

### 6.1 The Four-Step DORA Protocol Exchange (Slide 39)

```
DHCP CLIENT (New host: 0.0.0.0)                               DHCP SERVER (223.1.2.5)
       |                                                               |
       |--- (1) DHCP DISCOVER ---------------------------------------->|
       |    src: 0.0.0.0:68, dst: 255.255.255.255:67                   |
       |    yiaddr: 0.0.0.0, Transaction ID: 654                       |
       |                                                               |
       |<-- (2) DHCP OFFER --------------------------------------------|
       |    src: 223.1.2.5:67, dst: 255.255.255.255:68                 |
       |    yiaddr: 223.1.2.4 (Offered IP), Lease: 3600s, Trans ID: 654 |
       |                                                               |
       |--- (3) DHCP REQUEST ----------------------------------------->|
       |    src: 0.0.0.0:68, dst: 255.255.255.255:67                   |
       |    Accepts: 223.1.2.4, Server ID: 223.1.2.5                   |
       |                                                               |
       |<-- (4) DHCP ACK ----------------------------------------------|
       |    src: 223.1.2.5:67, dst: 255.255.255.255:68                 |
       |    Confirms lease, Mask, Default Gateway, DNS                 |
       v                                                               v
```

- **Why Broadcast `255.255.255.255` on Step 3?**:
  In networks with multiple DHCP servers, multiple servers may return DHCP Offers. When the client selects one offer, broadcasting the DHCP Request informs the other servers that their offers were rejected, allowing them to release their reserved IPs back into the available pool!

---

## 7. Network Address Translation (NAT, RFC 3022) (Slides 43–47)

NAT allows an entire local subnet with thousands of private devices (`10.0.0.0/8` or `192.168.0.0/16`) to access the public Internet using a **single public IPv4 address**.

```
PRIVATE HOME NETWORK (10.0.0.0/24)             NAT ROUTER                PUBLIC INTERNET
Host 10.0.0.1:3345                                WAN IP: 138.76.29.7
      |                                                |
      |--- Datagram: Src: 10.0.0.1:3345 -------------> | Rewrites header:
      |              Dst: 128.119.40.186:80            | Src: 138.76.29.7:5001 ---> [ Web Server ]
      |                                                | Dst: 128.119.40.186:80     128.119.40.186:80
      |                                                |
      |                                                | <--- Reply datagram:
      | <--- Restores original destination:            |      Src: 128.119.40.186:80
      |      Dst: 10.0.0.1:3345                        |      Dst: 138.76.29.7:5001
```

### 7.1 The NAT Translation Table
NAT maps private socket pairs to temporary external port numbers:

| WAN Side (Public IP & Port) | LAN Side (Private Internal IP & Port) |
| :---: | :---: |
| `138.76.29.7:5001` | `10.0.0.1:3345` |
| `138.76.29.7:5002` | `10.0.0.2:3345` |
| `138.76.29.7:5003` | `10.0.0.3:4210` |

- A single public IP has $2^{16} = 65,535$ available 16-bit port numbers, theoretically supporting up to $60,000+$ concurrent sessions.

### 7.2 The NAT Traversal Dilemma
- If an external client attempts to initiate contact with an internal server (`10.0.0.1:80`), the NAT router receives an unsolicited packet on public port 80. Since no active translation table entry exists, the NAT router drops the packet.
- **Solutions**:
  1. **Static Port Forwarding**: Hardcode a rule mapping WAN port 80 to `10.0.0.1:80`.
  2. **UPnP (Universal Plug and Play)**: Host automatically configures NAT port mappings via IGD protocol.
  3. **STUN / Relay (TURN)**: Intermediate cloud relay server bridges connections.

---

## 8. IPv6 Architecture & Migration Mechanisms (Slides 48–55)

IPv6 expands address length from 32 bits to **128 bits** ($2^{128} \approx 3.4 \times 10^{38}$ addresses).

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version| Traffic Class |           FLOW LABEL (20 bits)        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         PAYLOAD LENGTH (16)   |  NEXT HEADER  |   HOP LIMIT   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                  SOURCE IP ADDRESS (128 bits)                 |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|               DESTINATION IP ADDRESS (128 bits)               |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### 8.1 Key Architectural Improvements in IPv6
- **Fixed 40-Byte Base Header**: Streamlines processing in router hardware ASICs.
- **Flow Labeling (20 bits)**: Identifies packets belonging to specific real-time QoS flows without deep packet inspection.
- **Next Header**: Eliminates rigid options; chains variable **Extension Headers** (Hop-by-Hop, Routing, Fragment, ESP, AH).
- **No Header Checksum**: Checksum completely eliminated from IP header to maximize packet forwarding speed.
- **No Router Fragmentation**: Routers **never fragment** IPv6 packets; Path MTU Discovery (PMTUD) forces the sending host to size packets appropriately.

### 8.2 Transition Strategies: Dual-Stack vs. Tunneling (Slides 53–54)
1. **Dual Stack**: Routers and hosts run both IPv4 and IPv6 protocol stacks simultaneously.
2. **Tunneling**: IPv6 datagrams are encapsulated as the payload inside standard IPv4 datagrams to traverse legacy IPv4 networks:
   `[ IPv4 Header (Protocol=41) ] [ Original IPv6 Datagram ]`

---

## 9. Master Protocol Comparison: IPv4 vs. IPv6

| Technical Dimension | IPv4 | IPv6 |
| :--- | :--- | :--- |
| **Address Size** | $32\text{ bits}$ ($4\text{ bytes}$) | **$128\text{ bits}$** ($16\text{ bytes}$) |
| **Address Space** | $2^{32} \approx 4.29 \times 10^9$ | $2^{128} \approx 3.4 \times 10^{38}$ |
| **Header Format** | Variable ($20-60\text{ bytes}$) | **Strictly Fixed ($40\text{ bytes}$)** |
| **Header Checksum** | Present (recalculated at every hop) | **Eliminated completely** |
| **Fragmentation** | Performed by routers and sender | **Performed strictly by sender** (PMTUD) |
| **Configuration** | Manual or DHCP | **Stateless Auto-configuration (SLAAC)** or DHCPv6 |
| **Security** | IPsec optional | IPsec natively architected |

---

## 10. High-Yield Open-Book Exam Traps & Examiner Tricks

1. **The Fragment Offset 8-Byte Scaling Trap**:
   - *Trap*: Writing the byte offset directly into the Fragment Offset field.
   - *Fact*: The Fragment Offset field stores the offset **divided by 8**! If the byte offset is 1,480, the field value is $1,480 / 8 = \mathbf{185}$.
2. **The IPv4 Total Length vs. Data Length Trap**:
   - *Trap*: Confusing Total Length with payload data length.
   - *Fact*: Total Length = **Header Length + Payload Length**. To find payload, you must subtract $\text{IHL} \times 4$.
3. **The Subnet Broadcast Address Usability Trap**:
   - *Trap*: Assigning the last address in a subnet block to a host NIC.
   - *Fact*: The last address in any block has all host bits set to 1 and is strictly reserved as the **Directed Broadcast Address**.

---

## 11. Solved High-Yield Numerical Exam Problems

### Problem 1: Step-by-Step IP Fragmentation & Header Reconstruction
**Problem Statement**:
A host generates an IPv4 datagram with a 20-byte IP header and $3,800\,\text{bytes}$ of TCP data (Total Length $= 3,820\,\text{bytes}$, Identification $= 4200$, $\text{DF} = 0$, $\text{MF} = 0$, $\text{Offset} = 0$).
This datagram encounters an outgoing link with an $\text{MTU} = 1,420\,\text{bytes}$.
1. Determine how many fragments are created.
2. For each fragment, specify: Total Length, Data Length, Identification, More Fragments (MF) flag, and Fragment Offset.

**Step-by-Step Solution**:

1. **Determine Maximum Data Payload per Fragment**:
   - Link MTU $= 1,420\,\text{bytes}$.
   - IP Header size $= 20\,\text{bytes}$.
   - Available payload capacity $= 1,420 - 20 = 1,400\,\text{bytes}$.
   - Check 8-byte divisibility:
     $$1,400 / 8 = 175 \quad (\text{Exact integer! Fully divisible by 8})$$
   - Total data to transmit $= 3,800\,\text{bytes}$.

2. **Decompose into Fragments**:
   - **Fragment 1**:
     - Data Payload: $1,400\,\text{bytes}$ (Bytes $0$ to $1,399$).
     - Total Length $= 1,400 + 20 = \mathbf{1,420\,\text{bytes}}$.
     - Identification $= \mathbf{4200}$.
     - MF Flag $= \mathbf{1}$ (More fragments follow).
     - Fragment Offset $= \frac{0}{8} = \mathbf{0}$.
   - **Fragment 2**:
     - Data Payload: $1,400\,\text{bytes}$ (Bytes $1,400$ to $2,799$).
     - Total Length $= 1,400 + 20 = \mathbf{1,420\,\text{bytes}}$.
     - Identification $= \mathbf{4200}$.
     - MF Flag $= \mathbf{1}$.
     - Fragment Offset $= \frac{1,400}{8} = \mathbf{175}$.
   - **Fragment 3 (Final Fragment)**:
     - Remaining Data: $3,800 - 2,800 = 1,000\,\text{bytes}$ (Bytes $2,800$ to $3,799$).
     - Total Length $= 1,000 + 20 = \mathbf{1,020\,\text{bytes}}$.
     - Identification $= \mathbf{4200}$.
     - MF Flag $= \mathbf{0}$ (Terminal fragment).
     - Fragment Offset $= \frac{2,800}{8} = \mathbf{350}$.

---

### Problem 2: Variable Length Subnet Masking (VLSM) Network Design
**Problem Statement**:
An enterprise is allocated the CIDR block `192.168.10.0/24`. The network engineer must design four distinct subnets:
- Subnet A: 60 host addresses
- Subnet B: 28 host addresses
- Subnet C: 12 host addresses
- Subnet D: 12 host addresses
Design the VLSM subnets. For each subnet, compute the Subnet Mask, Network Address, Directed Broadcast Address, and Usable Host IP Range.

**Step-by-Step Solution**:

*Rule: Always allocate from largest subnet to smallest subnet to preserve contiguous address blocks!*

1. **Subnet A (60 hosts)**:
   - Need $60$ hosts $\implies 2^h - 2 \ge 60 \implies 2^h \ge 62 \implies h = 6$ bits ($2^6 = 64$).
   - Prefix length: $x = 32 - 6 = \mathbf{/26}$.
   - Subnet Mask: `255.255.255.192`.
   - **Network Address**: `192.168.10.0/26`.
   - Host range: `192.168.10.1` to `192.168.10.62`.
   - **Broadcast Address**: `192.168.10.63`.

2. **Subnet B (28 hosts)**:
   - Next available IP: `192.168.10.64`.
   - Need $28$ hosts $\implies 2^h - 2 \ge 28 \implies 2^h \ge 30 \implies h = 5$ bits ($2^5 = 32$).
   - Prefix length: $x = 32 - 5 = \mathbf{/27}$.
   - Subnet Mask: `255.255.255.224`.
   - **Network Address**: `192.168.10.64/27`.
   - Host range: `192.168.10.65` to `192.168.10.94`.
   - **Broadcast Address**: `192.168.10.95`.

3. **Subnet C (12 hosts)**:
   - Next available IP: `192.168.10.96`.
   - Need $12$ hosts $\implies 2^h - 2 \ge 12 \implies 2^h \ge 14 \implies h = 4$ bits ($2^4 = 16$).
   - Prefix length: $x = 32 - 4 = \mathbf{/28}$.
   - Subnet Mask: `255.255.255.240`.
   - **Network Address**: `192.168.10.96/28`.
   - Host range: `192.168.10.97` to `192.168.10.110`.
   - **Broadcast Address**: `192.168.10.111`.

4. **Subnet D (12 hosts)**:
   - Next available IP: `192.168.10.112`.
   - Need $12$ hosts $\implies h = 4$ bits ($2^4 = 16$).
   - Prefix length: $x = 32 - 4 = \mathbf{/28}$.
   - Subnet Mask: `255.255.255.240`.
   - **Network Address**: `192.168.10.112/28`.
   - Host range: `192.168.10.113` to `192.168.10.126`.
   - **Broadcast Address**: `192.168.10.127`.

---

## 12. Ultra-Fast Exam Revision Checklist
- [ ] IPv4 Base Header is 20 bytes; IHL is in 4-byte words; Total Length includes header and data.
- [ ] Fragmentation: Done by routers/hosts, reassembly only at destination; Fragment Offset $= \text{byte offset} / 8$.
- [ ] CIDR Notation `a.b.c.d/x`: $x$ network bits, $32 - x$ host bits.
- [ ] Usable Hosts: $2^{32 - x} - 2$ (subtract Network Address where host bits=0, and Broadcast Address where host bits=1).
- [ ] Private IP ranges (RFC 1918): `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`.
- [ ] DHCP: 4-step DORA exchange (Discover, Offer, Request, ACK) over UDP ports 67/68 using broadcast.
- [ ] NAT: Maps private `(IP, Port)` to public `(IP, Port)`; solves IPv4 address exhaustion at boundary.
- [ ] IPv6 Header: Fixed 40 bytes; 128-bit addresses; eliminates checksum, router fragmentation, and rigid options.
- [ ] IPv6 Transition: Dual-stack (runs both protocols) and Tunneling (IPv6 inside IPv4).
