<table width="100%" border="0" cellspacing="0" cellpadding="12" style="background-color: #1e3a8a; border-left: 6px solid #38bdf8; margin-bottom: 12px; border-radius: 4px;">
<tr>
<td style="color: #ffffff;">
<div style="font-size: 14pt; font-weight: bold; color: #ffffff; margin-bottom: 4px;">BITS PILANI WILP — OPEN-BOOK EXAM HIGH-YIELD MASTER COMPANION</div>
<div style="font-size: 8.8pt; color: #dbeafe; font-weight: 500;"><b>COURSE:</b> Computer Networks (BSDC BZC481) &nbsp;|&nbsp; <b>TARGET SCORE:</b> 90% – 95% Marks &nbsp;|&nbsp; <b>MODE:</b> Open-Book Permitted</div>
</td>
</tr>
</table>

# SECTION 1: BITS WILP OPEN-BOOK EXAM STRATEGY & SCORING PROTOCOL

> [!IMPORTANT]
> **THE 90-95% COMPUTER NETWORKS SCORING FORMULA:**
> In BITS WILP Computer Networks exams, open-book questions test **mathematical protocol modeling, packet header bit-level dissection, state machine transitions, and architectural trade-off justification**.
> 
> Follow the **Full-Marks Protocol Answer Structure**:
> 1. **Mathematical Derivation & Variable Definition:** Always write the governing formula with exact units ($bps, \text{ bytes}, \mu s, ms$). Show every algebraic step.
> 2. **Packet Header / State Transition Diagram:** For transport and network layer questions, specify header field offsets, flags ($SYN, ACK, FIN$), and sequence number progression.
> 3. **Scenario Justification:** When asked to select or design a protocol (e.g., TCP vs UDP, GBN vs SR, LS vs DV), provide a multi-column comparison table citing delay, overhead, packet loss tolerance, and buffering constraints.

---

# SECTION 2: MASTER RAPID LOOK-UP & EXAM HALL TRIAGE MATRIX

| Exam Keyword / Scenario Cue | Target Session | Key Protocols / Theorems to Cite | Primary Formulas / Equations to Apply | Top Examiner Trap to Avoid |
| :--- | :--- | :--- | :--- | :--- |
| **"Transmission vs Propagation Delay"** | **Session 01** | Packet switching, Nodal delay | $d_{trans} = L/R$, $d_{prop} = d/s$, $d_{nodal} = \sum d_i$ | Confusing transmission speed ($R$) with propagation speed ($s \approx 2 \times 10^8 \text{ m/s}$) |
| **"HTTP Latency / Persistent vs Non-Persistent"** | **Session 02** | HTTP/1.0, HTTP/1.1, HTTP/2, Caching | Non-Persistent: $2 RTT \times N$; Persistent: $2 RTT + N \times RTT$ | Forgetting the initial $1 RTT$ TCP handshake overhead |
| **"UDP Checksum Calculation"** | **Session 04** | UDP 8-byte header, Pseudo-header | 16-bit 1s Complement Addition & Inversion | Forgetting to add back the carry bit before bitwise inversion |
| **"Pipelining: Go-Back-N vs Selective Repeat"** | **Session 04** | Cumulative ACK vs Individual ACK | Window constraint: $W_S + W_R \le 2^k$ ($W \le 2^{k-1}$ for SR) | Exceeding maximum window size, causing sequence number ambiguity |
| **"TCP Handshake & Sequence Number Tracking"** | **Session 05** | 3-Way Handshake, 4-Way Teardown | $Seq_{next} = Seq_{curr} + \text{Payload Bytes}$; $ACK = Seq_{rcvd} + 1$ | SYN/FIN consume 1 sequence number; pure ACK consumes 0! |
| **"TCP Congestion Control & Window Progression"** | **Session 06** | AIMD, Slow Start, Fast Retransmit | Reno: $ssthresh = cwnd/2, cwnd = ssthresh + 3$; Tahoe: $cwnd=1$ | Confusing Tahoe (resets to 1 MSS on 3 dup ACKs) with Reno (Fast Recovery) |
| **"IPv4 Header & Packet Fragmentation"** | **Session 07** | MTU, Fragment Offset, Flags (DF, MF) | $\text{Offset} = \text{Data Bytes} / 8$; $\text{Fragment Data} \le MTU - 20$ | Offset is in units of 8-byte blocks, NOT individual bytes! |
| **"CIDR Subnetting & VLSM Design"** | **Session 08** | Subnet Mask, Network ID, Broadcast ID | Host IPs $= 2^H - 2$; Subnets $= 2^S$; Prefix $= 32 - H$ | Forgetting to subtract 2 (Network address and Broadcast address) |
| **"Dijkstra Link-State Routing Algorithm"** | **Session 09** | Global shortest path, Forwarding table | $D(v) = \min(D(v), D(w) + c(w,v))$ | Skipping intermediate node updates or misidentifying tie-breakers |
| **"Distance Vector & Count-to-Infinity"** | **Session 09** | Bellman-Ford, Split Horizon, Poisoned Reverse | $d_x(y) = \min_v \{ c(x,v) + d_v(y) \}$ | Assuming Poison Reverse solves routing loops with $\ge 3$ nodes |
| **"BGP Inter-AS & OSPF Intra-AS Routing"** | **Session 10** | Path Vector, Autonomous Systems, Areas | BGP Attributes: AS-PATH, NEXT-HOP, Local Pref | Confusing intra-AS performance metrics with inter-AS policy rules |
| **"SDN Architecture & OpenFlow"** | **Session 11** | Control/Data plane separation | Flow Table matching: Match + Counters + Actions | Assuming OpenFlow controller modifies hardware ASICs directly |
| **"CRC Polynomial Division"** | **Session 12** | Frame Check Sequence (FCS), XOR division | Remainder $R = (D \times 2^r) \bmod G$ via modulo-2 | Using standard arithmetic division instead of bitwise XOR |
| **"CSMA/CD Minimum Frame Size & Efficiency"** | **Session 12** | Carrier sense, Exponential Backoff | $L_{min} \ge 2 \cdot t_{prop} \cdot R$; Backoff: choose $K \in [0, 2^m-1]$ | Calculating frame transmission time less than round-trip propagation |
| **"Ethernet Switch Self-Learning & Spanning Tree"** | **Session 13** | Filtering, Forwarding, Flooding, STP | Forwarding Table: [MAC, Port, TTL] | Flooding unicast frames when the destination MAC is already in table |
| **"Wi-Fi Hidden Terminal & RTS/CTS"** | **Session 14** | 802.11 CSMA/CA, NAV (Virtual Carrier Sense) | RTS/CTS duration field sets Network Allocation Vector | Claiming CSMA/CD can be used in wireless (physical impossibility) |

---

# SECTION 3: SESSION-BY-SESSION HIGH-YIELD OPEN-BOOK MASTERY

## Session 01: Networking Core, Edge & Delay Performance Metrics
* **Network Core Mechanisms:** Packet Switching vs Circuit Switching.
  * *Circuit Switching:* Dedicated end-to-end connection, reserved bandwidth, guaranteed performance, call setup overhead, idle waste (FDM/TDM).
  * *Packet Switching:* Statistical multiplexing, on-demand resource sharing, store-and-forward latency, buffer queuing/loss, higher user capacity.
* **4 Fundamental Nodal Delays:**
  $$d_{\text{nodal}} = d_{\text{proc}} + d_{\text{queue}} + d_{\text{trans}} + d_{\text{prop}}$$
  * *Processing Delay ($d_{\text{proc}}$):* Time to inspect packet header and determine output link (typically microseconds).
  * *Queuing Delay ($d_{\text{queue}}$):* Time waiting at output link buffer for transmission. Depends on congestion / traffic intensity $I = La/R$. If $I > 1$, queue grows indefinitely!
  * *Transmission Delay ($d_{\text{trans}}$):* Time required to push all packet bits onto the link: $d_{\text{trans}} = L / R$ ($L$ = packet size in bits, $R$ = link bandwidth in bps).
  * *Propagation Delay ($d_{\text{prop}}$):* Time for a bit to travel physical medium: $d_{\text{prop}} = d / s$ ($d$ = distance in meters, $s$ = propagation speed $\approx 2 \times 10^8 \text{ m/s}$ in copper/fiber).

## Session 02: Application Layer, HTTP Evolution & DNS Hierarchy
* **HTTP Versions Comparison:**
  * *HTTP/1.0:* Non-persistent (new TCP connection per object $\to 2 RTT + \text{transfer}$ per object).
  * *HTTP/1.1:* Persistent connection default ($1 RTT$ for TCP handshake, then multiple objects requested over same connection; optional pipelining). Head-of-Line (HOL) blocking at application layer.
  * *HTTP/2:* Binary framing layer, multiplexed streams over a single TCP connection, header compression (HPACK), server push. Resolves HTTP HOL blocking, but suffers from TCP-level HOL blocking on packet drop!
  * *HTTP/3:* Runs over **QUIC (UDP-based)**. Eliminates TCP HOL blocking; zero-RTT connection resumption ($0-RTT$); connection migration across IP changes (mobile handover).
* **DNS Architecture:** Hierarchical distributed database: Root DNS $\to$ Top-Level Domain (TLD) DNS (.com, .org, .edu) $\to$ Authoritative DNS servers. Iterative queries (client queries each level) vs Recursive queries (server queries on client's behalf).

## Session 04: Transport Layer Services, UDP & Reliable Data Transfer (RDT)
* **Multiplexing & Demultiplexing:** Transport layer delivers data to correct socket using port numbers.
  * *UDP Demux:* 2-tuple (Destination IP, Destination Port).
  * *TCP Demux:* 4-tuple (Source IP, Source Port, Destination IP, Destination Port).
* **UDP Header (8 Bytes total):** Source Port (16b), Destination Port (16b), Length (16b), Checksum (16b).
* **Pipelined Protocols: Go-Back-N (GBN) vs Selective Repeat (SR):**
  * *Go-Back-N:* Sender window $N$; Receiver window = 1. Cumulative ACKs ($ACK(n)$ acknowledges all packets up to $n$). Discards out-of-order packets. Single timer for oldest unacknowledged packet. On timeout, retransmits all $N$ unacknowledged packets!
  * *Selective Repeat:* Sender window $N$; Receiver window $N$. Individual ACKs. Buffers out-of-order packets. Individual timer per packet. On timeout, retransmits only the specific missing packet.
  * *Window Size Rule:* To prevent sequence number ambiguity:
    $$W_{\text{sender}} + W_{\text{receiver}} \le 2^k \implies W \le 2^{k-1} \quad (\text{for Selective Repeat, where } k \text{ is seq bit length})$$

## Session 05: TCP Connection Management, Flow Control & Silly Window
* **TCP 3-Way Handshake:**
  1. *Client $\to$ Server:* $SYN = 1, Seq = x$ (No data payload; consumes 1 sequence number).
  2. *Server $\to$ Client:* $SYN = 1, ACK = 1, Seq = y, Ack = x + 1$ (Consumes 1 sequence number).
  3. *Client $\to$ Server:* $ACK = 1, Seq = x + 1, Ack = y + 1$ (May contain data; if no data, consumes 0 seq numbers).
* **TCP 4-Way Connection Teardown:**
  1. $A \to B: FIN = 1, Seq = u$.
  2. $B \to A: ACK = 1, Ack = u + 1$. ($B$ enters CLOSE_WAIT; $A$ enters FIN_WAIT_2).
  3. $B \to A: FIN = 1, Seq = v, Ack = u + 1$. ($B$ enters LAST_ACK).
  4. $A \to B: ACK = 1, Ack = v + 1$. ($A$ enters TIME_WAIT for $2 \times MSL \approx 120\text{s}$ before closed).
* **TCP Flow Control:** Prevents sender from overflowing receiver buffer.
  $$\text{Receive Window } rwnd = \text{RcvBuffer} - (\text{LastByteRcvd} - \text{LastByteRead})$$
  Sender ensures: $\text{LastByteSent} - \text{LastByteAcked} \le rwnd$.
* **Silly Window Syndrome:** Occurs when receiver advertises tiny window sizes (e.g. 1 byte) or sender transmits tiny segments.
  * *Sender Solution (Nagle's Algorithm):* If application produces data in small chunks, send first chunk immediately; buffer subsequent data until previous ACK arrives OR buffer reaches Maximum Segment Size (MSS).
  * *Receiver Solution (Clark's Algorithm):* Prevent advertising a non-zero $rwnd$ until buffer has space for $\min(\text{MSS}, \text{RcvBuffer} / 2)$.

## Session 06: TCP Congestion Control (AIMD, Tahoe & Reno)
* **Additive Increase Multiplicative Decrease (AIMD):**
  * Increase $cwnd$ by $1 \text{ MSS}$ every RTT in absence of loss.
  * Cut $cwnd$ in half upon detecting loss via 3 duplicate ACKs.
* **4 Congestion Control Phases:**
  1. *Slow Start:* $cwnd$ starts at $1 \text{ MSS}$; doubles every RTT ($cwnd = cwnd \times 2$) until $cwnd \ge ssthresh$.
  2. *Congestion Avoidance:* Linear growth ($cwnd = cwnd + 1 \text{ MSS}$ per RTT).
  3. *Fast Retransmit:* 3 duplicate ACKs trigger immediate retransmission of missing segment before retransmit timer expires.
  4. *Fast Recovery (TCP Reno):*
     * $ssthresh = cwnd / 2$
     * $cwnd = ssthresh + 3 \text{ MSS}$ (accounts for segments buffered by receiver)
     * Resumes linear congestion avoidance without dropping back to slow start!
* **TCP Tahoe vs TCP Reno Rule:**
  * *Tahoe:* On ANY loss (Timeout OR 3 Dup ACKs), sets $ssthresh = cwnd / 2$ and drops $cwnd = 1 \text{ MSS}$ (Slow Start).
  * *Reno:* On Timeout $\to$ drops $cwnd = 1 \text{ MSS}$. On 3 Dup ACKs $\to$ enters Fast Recovery ($cwnd = ssthresh + 3 \text{ MSS}$).

## Session 07: Network Layer Data Plane & IPv4 Fragmentation
* **IPv4 Header Fields (20 Bytes Minimum):**
  * Version (4b), IHL (4b - header length in 32-bit words, min 5 = 20B), Type of Service / DiffServ (8b), Total Length (16b - bytes).
  * Identification (16b), Flags (3b: Reserved, DF = Don't Fragment, MF = More Fragments), Fragment Offset (13b - **units of 8-byte blocks!**).
  * TTL (8b - decremented by 1 at each router; dropped if 0), Protocol (8b: 6 for TCP, 17 for UDP, 1 for ICMP), Header Checksum (16b), Source IP (32b), Dest IP (32b).
* **Fragmentation Algorithm:**
  * When packet length $> MTU$, packet is fragmented.
  * Maximum data payload per fragment $= \lfloor (MTU - 20) / 8 \rfloor \times 8$.
  * For all fragments except the last, $MF = 1$. For the last fragment, $MF = 0$.
  * $\text{Fragment Offset} = \text{Cumulative Data Bytes Preceding this Fragment} / 8$.

## Session 08: IPv4 Addressing, CIDR, VLSM & NAT
* **CIDR Notation ($a.b.c.d / x$):**
  * $x$ is prefix length (network bits); $32 - x = H$ (host bits).
  * Number of addresses in block $= 2^H$.
  * Number of assignable host interfaces $= 2^H - 2$ (subtract Network Address and Broadcast Address).
* **Network Address Translation (NAT):**
  * Private IP ranges (RFC 1918): `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`.
  * NAT Translation Table maps: $(\text{Private IP}, \text{Private Port}) \longleftrightarrow (\text{NAT Public IP}, \text{Assigned Public Port})$.
  * Enables thousands of LAN devices to share a single public IPv4 address.
  * *Limitations:* Violates end-to-end principle; breaks incoming peer-to-peer connections (requires STUN, TURN, or UPnP).

## Session 09: Network Layer Control Plane: Routing Algorithms
* **Link-State (LS) Routing — Dijkstra's Algorithm:**
  * Global algorithm: Every router receives full link-state broadcast (LSP) and knows complete network topology.
  * Computes least-cost paths from source node $u$ to all other nodes.
  * Time complexity: $O(N^2)$ or $O(E \log N)$ with min-heap.
* **Distance Vector (DV) Routing — Bellman-Ford Algorithm:**
  * Decentralized, iterative, asynchronous algorithm.
  * Routers only know costs to immediate neighbors and exchange distance vectors with neighbors.
  * Bellman-Ford Equation:
    $$d_x(y) = \min_v \{ c(x,v) + d_v(y) \}$$
  * *Count-to-Infinity Problem:* Good news travels fast; bad news travels slow. When a link breaks, neighboring nodes create routing loops bouncing increments until reaching infinity (e.g. 16 in RIP).
  * *Mitigation:* Split Horizon (do not advertise route back to the neighbor from whom it was learned) and Poisoned Reverse (advertise cost as $\infty$ back to that neighbor). Note: Poisoned reverse fails for loops involving 3 or more nodes!

## Session 10: Intra-AS (OSPF, RIP) & Inter-AS (BGP-4) Routing
* **Intra-AS (Interior Gateway Protocols):**
  * *RIP (Routing Information Protocol):* Distance-vector; hop count metric (max 15 hops; 16 = $\infty$); periodic updates every 30s.
  * *OSPF (Open Shortest Path First):* Link-state; uses Dijkstra; supports hierarchical areas (Area 0 = Backbone); fast convergence; authenticated packets; equal-cost multi-path (ECMP).
* **Inter-AS (Exterior Gateway Protocols):**
  * *BGP-4 (Border Gateway Protocol):* Path-Vector protocol. Glues the global Internet.
  * Autonomous Systems (AS): eBGP (between border routers of different ASes) and iBGP (propagates reachability within the AS).
  * Key BGP Attributes: `AS-PATH` (list of ASes traversed; prevents routing loops), `NEXT-HOP` (IP address of the border router starting the path).
  * Policy-based routing: Commercial relationships (Customer-Provider, Peer-Peer) dictate route advertisement, overriding pure performance metrics.

## Session 11: Software-Defined Networking (SDN)
* **Architectural Paradigm:** Decouples Control Plane (logically centralized software controller) from Data Plane (fast hardware packet switches).
* **OpenFlow Protocol:** Standard interface between SDN controller and switches.
  * Flow Table Entries: **Match Fields** (Headers from Layers 2, 3, 4) $+$ **Counters** (Packets, bytes) $+$ **Actions** (Forward to port, Drop, Modify header fields, Send to controller).

## Session 12: Link Layer, Error Control (CRC) & MAC Protocols
* **Error Detection:**
  * *Parity:* Single bit (detects odd-number bit errors); 2D parity (can detect and correct single-bit errors).
  * *Cyclic Redundancy Check (CRC):* Polynomial arithmetic modulo-2 (bitwise XOR). Hardware-efficient and detects all burst errors of length $\le r$.
* **Multiple Access Protocols:**
  * *Channel Partitioning:* TDMA (time slots), FDMA (frequency bands), CDMA (code division).
  * *Random Access:*
    * Pure ALOHA: Max efficiency $= 1 / (2e) \approx 18.4\%$.
    * Slotted ALOHA: Max efficiency $= 1 / e \approx 36.8\%$.
    * CSMA (Carrier Sense Multiple Access): "Listen before talk".
    * CSMA/CD (Collision Detection - Ethernet): Listen before transmit; abort immediately upon collision.
      * Exponential Backoff: After $m$-th collision, choose $K \in \{0, 1, \dots, 2^m - 1\}$ (capped at $m=10$). Wait $K \times 512$ bit times.
      * Collision Detection Condition: Frame transmission time must be at least twice the maximum one-way propagation delay:
        $$t_{\text{trans}} \ge 2 \cdot t_{\text{prop}} \implies \frac{L_{\text{min}}}{R} \ge 2 \cdot \frac{d}{s} \implies L_{\text{min}} \ge 2 \cdot t_{\text{prop}} \cdot R$$

## Session 13: Link Layer Addressing, Ethernet & Switches
* **MAC Address vs IP Address:** MAC is flat, permanent 48-bit hex address (e.g. `00:1A:2B:3C:4D:5E`) burned into NIC ROM. IP is hierarchical 32-bit address reflecting current topological location.
* **ARP (Address Resolution Protocol):** Resolves IP address to MAC address within a local broadcast domain. ARP Request is broadcast (`FF:FF:FF:FF:FF:FF`); ARP Reply is unicast. ARP cache entries timeout after 15-20 minutes.
* **Ethernet Switches:** Plug-and-play, transparent self-learning devices.
  * Maintains a Switch Table: `[MAC Address, Interface Port, Timestamp]`.
  * When frame arrives on interface $x$ with destination MAC $D$:
    1. Record $(SrcMAC, x)$ in table.
    2. If $D$ is in table for port $y$: if $y = x$, drop frame (filtering); else forward frame onto port $y$.
    3. If $D$ is NOT in table, **flood** frame onto all interfaces except $x$.
  * **Spanning Tree Protocol (STP):** Eliminates bridge loops by disabling redundant switch links dynamically.

## Session 14: Wireless Networks, 802.11 Wi-Fi & Mobility
* **Wireless Challenges:** Attenuation, multipath propagation, interference.
* **Hidden Terminal Problem:** Node A and Node C can both transmit to B, but cannot hear each other; simultaneous transmissions collide at B.
* **Exposed Terminal Problem:** Node B transmits to A; Node C mistakenly refrains from transmitting to D because it hears B, even though transmissions wouldn't interfere.
* **802.11 CSMA/CA (Collision Avoidance):**
  * Cannot detect collisions while transmitting (radio transmits at high power, drowning incoming signals).
  * Uses RTS/CTS handshake: Sender transmits short Request to Send (RTS); Receiver responds with Clear to Send (CTS); surrounding nodes update their Network Allocation Vector (NAV) and defer transmission.
* **Mobile IP:** Mobile node has permanent **Home Address** at Home Network and temporary **Care-of-Address (CoA)** at Foreign Network. Home Agent intercepts packets and tunnels them to Foreign Agent via IP-in-IP encapsulation.

## Session 15: Network Security & Cryptographic Protocols
* **SSL/TLS Handshake:**
  1. *Client Hello:* Supported cipher suites, client random $R_C$.
  2. *Server Hello:* Selected cipher suite, server random $R_S$, digital certificate containing Server Public Key.
  3. *Key Exchange:* Client verifies certificate with CA; encrypts **Pre-Master Secret** using Server Public Key and sends to server.
  4. *Session Key Derivation:* Both compute symmetric session keys from $R_C, R_S$, and Pre-Master Secret.
  5. *Finished:* Encrypted MAC verification.
* **IPsec Architecture:** Operates at Layer 3.
  * *Authentication Header (AH):* Provides data integrity and origin authentication, but NO confidentiality (payload unencrypted).
  * *Encapsulating Security Payload (ESP):* Provides confidentiality (encryption), data integrity, and authentication.
  * *Transport Mode:* Encrypts only IP payload (header preserved; host-to-host).
  * *Tunnel Mode:* Encrypts entire inner IP packet and prepends a new outer IP header (gateway-to-gateway VPN).

## Session 16: Multimedia Streaming & Network Management
* **DASH (Dynamic Adaptive Streaming over HTTP):** Video encoded at multiple bitrates and divided into 2-10s chunks. Client requests chunk bitrates dynamically based on available bandwidth.
* **Content Distribution Networks (CDN):** Geographically distributed proxy servers. DNS redirects user requests to the closest edge server ("Enter Deep" vs "Bring Home").
* **SNMP (Simple Network Management Protocol):** Manager-Agent model. Uses SMI (Structure of Management Information) and MIB (Management Information Base). UDP port 161 (Get/Set) and 162 (Traps).

---

# SECTION 4: MASTER NUMERICAL & ALGORITHMIC SOLVING BLUEPRINTS

## BLUEPRINT 1: Variable Length Subnet Masking (VLSM) Template

> [!IMPORTANT]
> **SYSTEMATIC VLSM 4-STEP ALLOCATION METHOD:**
> 1. **Sort Subnet Requirements in Descending Order:** Always allocate the largest subnet first!
> 2. **Determine Host Bits Required ($H$):**
>    $$2^H - 2 \ge \text{Hosts Required} \implies H = \lceil \log_2(\text{Hosts} + 2) \rceil$$
> 3. **Determine Subnet Prefix Length:** $\text{Prefix} = 32 - H$.
> 4. **Calculate Block Size (Step Size):** $\text{Block Size} = 2^H$. Next subnet starts at $\text{Current Network Address} + 2^H$.

### Fully Worked Exam Problem:
**Problem:** Allocate subnets from `192.168.10.0/24` for 4 departments: Dept A (60 hosts), Dept B (28 hosts), Dept C (12 hosts), and Point-to-Point WAN Link (2 hosts).

**Step-by-Step Solution Table:**

| Dept / Link | Hosts Needed | Formula: $2^H - 2 \ge N$ | Host Bits ($H$) | Prefix ($32-H$) | Subnet Mask | Subnet Network ID | Usable Host IP Range | Broadcast Address |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Dept A** | 60 | $2^6 - 2 = 62 \ge 60$ | 6 | `/26` | `255.255.255.192` | `192.168.10.0/26` | `192.168.10.1` – `192.168.10.62` | `192.168.10.63` |
| **Dept B** | 28 | $2^5 - 2 = 30 \ge 28$ | 5 | `/27` | `255.255.255.224` | `192.168.10.64/27` | `192.168.10.65` – `192.168.10.94` | `192.168.10.95` |
| **Dept C** | 12 | $2^4 - 2 = 14 \ge 12$ | 4 | `/28` | `255.255.255.240` | `192.168.10.96/28` | `192.168.10.97` – `192.168.10.110` | `192.168.10.111` |
| **WAN Link** | 2 | $2^2 - 2 = 2 \ge 2$ | 2 | `/30` | `255.255.255.252` | `192.168.10.112/30` | `192.168.10.113` – `192.168.10.114` | `192.168.10.115` |

---

## BLUEPRINT 2: Cyclic Redundancy Check (CRC) Calculation Template

> [!IMPORTANT]
> **CRC GENERATION & VERIFICATION RULES:**
> 1. Let data frame $D$ have $k$ bits, generator polynomial $G$ have degree $r$ ($r+1$ bits).
> 2. Append $r$ zero bits to $D$: $D \times 2^r$.
> 3. Divide $(D \times 2^r)$ by $G$ using **Modulo-2 Binary Division (Bitwise XOR)**.
> 4. The $r$-bit remainder is the Frame Check Sequence (FCS) $R$.
> 5. Transmitted frame $T = (D \times 2^r) \oplus R$. Receiver divides $T$ by $G$; if remainder is $0$, no error detected!

### Fully Worked Exam Problem:
**Problem:** Compute the CRC FCS for data bits $D = 1010001101$ using generator polynomial $G(x) = x^5 + x^4 + x^2 + 1$.
* $G(x)$ in binary: $1 \cdot x^5 + 1 \cdot x^4 + 0 \cdot x^3 + 1 \cdot x^2 + 0 \cdot x^1 + 1 \cdot x^0 = \mathbf{110101}$ (Degree $r = 5$).
* Append $5$ zeros to $D$: $1010001101 \mathbf{00000}$.
* Perform Modulo-2 division of $101000110100000$ by $110101$:
  * $101000 \oplus 110101 = 011101 \to$ bring down next bit $\dots$
  * Final 5-bit remainder $R = \mathbf{01110}$.
  * Transmitted Frame $= \mathbf{101000110101110}$.

---

## BLUEPRINT 3: Dijkstra's Shortest Path Table Construction Template

> [!IMPORTANT]
> **DIJKSTRA STEP-BY-STEP TABLE PROTOCOL:**
> * Set $N' = \{u\}$ (source node). For all $v \notin N'$, $D(v) = c(u,v)$; if no direct link, $D(v) = \infty$.
> * At each step, find $w \notin N'$ such that $D(w)$ is minimum. Add $w$ to $N'$.
> * Update $D(v)$ for all neighbors of $w$: $D(v) = \min(D(v), D(w) + c(w,v))$.
> * Record predecessor pointer $p(v)$ to trace reverse path.

---

# SECTION 5: UNIVERSAL OPEN-BOOK COMPARISON & PROTOCOL MATRICES

### Transport Layer: TCP vs UDP Deep Comparative Matrix
| Dimension | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) |
| :--- | :--- | :--- |
| **Connection State** | Connection-oriented (3-way handshake required) | Connectionless (no setup latency) |
| **Reliability** | Guaranteed delivery (In-order, no loss, no duplicates) | Best-effort (packets may drop, duplicate, or arrive out of order) |
| **Header Overhead** | 20 Bytes minimum (up to 60 Bytes with options) | Exactly 8 Bytes |
| **Flow Control** | Yes (Sliding window via $rwnd$) | None |
| **Congestion Control** | Yes (AIMD, Slow Start, Fast Recovery via $cwnd$) | None (sends at arbitrary rate) |
| **Transmission Model** | Byte stream (no message boundaries) | Datagram / Message-oriented (preserves boundaries) |
| **Ideal Application Profiles** | Web (HTTP), Email (SMTP), File Transfer (FTP), SSH | Real-time gaming, VoIP, DNS queries, Video streaming (RTP) |

### Routing Protocols: Link-State vs Distance-Vector Comparative Matrix
| Dimension | Link-State (OSPF, IS-IS) | Distance-Vector (RIP, IGRP) |
| :--- | :--- | :--- |
| **Topology Knowledge** | Global: Each router knows complete network topology | Local: Each router only knows costs to direct neighbors |
| **Algorithm** | Dijkstra's Shortest Path Algorithm | Bellman-Ford Distributed Equation |
| **Message Complexity** | $O(N \cdot E)$ messages via link-state broadcast | Exchanges only with immediate neighbors |
| **Convergence Speed** | Fast ($O(N^2)$ local computation; no loops) | Slow (suffers from Count-to-Infinity & routing loops) |
| **Loop Mitigation** | Inherent (complete topology view prevents loops) | Split Horizon, Poisoned Reverse, Holddown Timers |
| **Memory & CPU Load** | High (stores entire network graph and link states) | Low (stores only direct distance vectors) |

---

# SECTION 6: 7-DAY MASTER STUDY & PRINTOUT TABBING BATTLE PLAN

* [ ] **Day 1: Delays, Application Layer & HTTP/DNS (Sessions 01, 02)**
  * Place physical sticky tabs on: *Delay Formulas ($d_{trans}, d_{prop}$)* and *HTTP 1.0 vs 1.1 vs 2 vs 3 Comparison*.
  * Solve 2 problems computing total nodal delay and persistent HTTP object download times.
* [ ] **Day 2: Transport Layer, UDP & Pipelining (Session 04)**
  * Tab: *UDP Checksum Calculation Template* and *Go-Back-N vs Selective Repeat Window Rules*.
  * Practice the 1s complement checksum verification on a 16-bit word sequence.
* [ ] **Day 3: TCP Handshake, Flow & Congestion Control (Sessions 05, 06)**
  * Tab: *TCP Sequence Tracking*, *3-Way Handshake / 4-Way Teardown*, and *AIMD / Fast Recovery Graph*.
  * Solve 1 TCP window size progression trace under Slow Start, Timeout, and 3-Dup-ACK events.
* [ ] **Day 4: Network Layer Data Plane, IPv4 & VLSM Subnetting (Sessions 07, 08)**
  * Tab: *IPv4 Fragmentation Offset Formula* and *VLSM 4-Step Allocation Table*.
  * Design a complete VLSM subnetting plan for a 5-subnet enterprise topology.
* [ ] **Day 5: Routing Algorithms & SDN (Sessions 09, 10, 11)**
  * Tab: *Dijkstra Table Construction*, *Bellman-Ford Equation*, and *BGP Attributes*.
  * Solve a 6-node network graph using Dijkstra's algorithm showing every iteration of $N'$ and $D(v)$.
* [ ] **Day 6: Link Layer, CRC, CSMA/CD & LAN Switching (Sessions 12, 13)**
  * Tab: *CRC Modulo-2 Division Blueprint* and *Switch Self-Learning Table Rules*.
  * Solve 2 CRC generator polynomial division problems and compute minimum frame size for CSMA/CD.
* [ ] **Day 7: Wireless, Security & Exam Simulation (Sessions 14, 15, 16 & Tabbing Rehearsal)**
  * Tab: *RTS/CTS Handshake*, *SSL/TLS Handshake*, and *IPsec AH vs ESP comparison*.
  * Review all sticky tabs and confirm all formulas and blueprints can be opened in under 10 seconds!