# Computer Networks (BSDCBZC481)
# Master Exam Preparation & Comprehensive Study Guide

---

## Quick Navigation Index

- [Session 01: Networking Fundamentals & Delays](#session-01-networking-fundamentals--delays)
- [Session 02: Network Core, Edge & Switching](#session-02-network-core-edge--switching)
- [Session 04 & 05: Application Layer, HTTP & DNS](#session-04--05-application-layer-http--dns)
- [Session 06: Transport Layer Fundamentals & UDP](#session-06-transport-layer-fundamentals--udp)
- [Session 07: Reliable Data Transfer (RDT) & TCP Architecture](#session-07-reliable-data-transfer-rdt--tcp-architecture)
- [Session 08: TCP Congestion Control & Flow Control](#session-08-tcp-congestion-control--flow-control)
- [Session 09: Network Layer Data Plane & Routers](#session-09-network-layer-data-plane--routers)
- [Session 10: IPv4, Subnetting Math & NAT](#session-10-ipv4-subnetting-math--nat)
- [Session 11: Routing Algorithms (Dijkstra & Bellman-Ford)](#session-11-routing-algorithms-dijkstra--bellman-ford)
- [Session 12: Link Layer, Error Detection & CSMA/CD](#session-12-link-layer-error-detection--csmacd)
- [Session 13: Wireless & Mobile Networks (802.11)](#session-13-wireless--mobile-networks-80211)
- [Session 14: Network Security & Cryptography](#session-14-network-security--cryptography)
- [Session 15: Multimedia Networking & Course Review](#session-15-multimedia-networking--course-review)

---

### Session 01: Networking Fundamentals & Delays
- **OSI 7-Layer Model vs. TCP/IP 5-Layer Stack**:
  | Layer # | OSI Layer | TCP/IP Layer | PDU (Protocol Data Unit) | Core Protocols / Devices |
  | :---: | :--- | :--- | :--- | :--- |
  | 7 | Application | Application | Data / Message | HTTP, DNS, SMTP, FTP, SSH |
  | 6 | Presentation | Application | Data | TLS/SSL, ASCII, JPEG |
  | 5 | Session | Application | Data | RPC, NetBIOS |
  | 4 | Transport | Transport | Segment (TCP) / Datagram (UDP) | TCP, UDP, SCTP |
  | 3 | Network | Network / Internet | Datagram / Packet | IPv4, IPv6, ICMP, OSPF, BGP, Routers |
  | 2 | Data Link | Data Link | Frame | Ethernet (802.3), Wi-Fi (802.11), Switches |
  | 1 | Physical | Physical | Bit stream | Cables (Cat6, Fiber), Hubs, Modems |

- **Total Nodal Delay Formula**:
  $$d_{\text{nodal}} = d_{\text{proc}} + d_{\text{queue}} + d_{\text{trans}} + d_{\text{prop}}$$
  1. **Processing Delay ($d_{\text{proc}}$)**: Time to check bit errors and read routing table. Typically $< 10\,\mu\text{s}$.
  2. **Queuing Delay ($d_{\text{queue}}$)**: Time spent waiting in queue before transmission. Depends on traffic intensity:
     $$I = \frac{L \times a}{R}$$
     *(Where $L$ = packet length in bits, $a$ = average arrival rate in packets/sec, $R$ = transmission link bandwidth in bps)*
     - $I \approx 0$: negligible queueing delay.
     - $I \to 1$: delay grows asymptotically large.
     - $I > 1$: queue grows infinitely, packet loss occurs.
  3. **Transmission Delay ($d_{\text{trans}}$)**: Time needed to push all bits into the link:
     $$d_{\text{trans}} = \frac{L}{R}$$
  4. **Propagation Delay ($d_{\text{prop}}$)**: Time for 1 bit to travel across the physical medium:
     $$d_{\text{prop}} = \frac{d}{s}$$
     *(Where $d$ = physical distance, $s$ = propagation speed, $\approx 2 \times 10^8\,\text{m/s}$ in copper/fiber)*

---

### Session 02: Network Core, Edge & Switching
- **Circuit Switching vs. Packet Switching**:
  - *Circuit Switching*: Dedicated end-to-end circuit reserved for duration of call (e.g. traditional telephone). FDM (Frequency Division) or TDM (Time Division). No queuing delay, guaranteed throughput, but wastes capacity when idle.
  - *Packet Switching*: Data divided into packets; packets share network resources on demand (*Statistical Multiplexing*). Store-and-forward at each router. Higher efficiency, supports more concurrent users, but subject to queuing and packet loss.

---

### Session 04 & 05: Application Layer, HTTP & DNS
- **HTTP Generations Comparison**:
  - **HTTP/1.0**: Non-persistent. Each object (image, CSS) requires a separate TCP 3-way handshake. Total delay per object $= 2 \times RTT + \text{transmission time}$.
  - **HTTP/1.1**: Persistent connections. Multiple objects downloaded over same TCP connection. Pipelining supported. Still suffers from *Head-of-Line (HoL) blocking* at application layer.
  - **HTTP/2**: Binary framing layer. Multiplexes concurrent bidirectional streams over a single TCP connection. Header compression (HPACK), server push.
  - **HTTP/3**: Runs over **QUIC** (UDP). Eliminates TCP-level Head-of-Line blocking; 0-RTT connection establishment on re-connect.

- **DNS (Domain Name System)**:
  - *Hierarchy*: Root DNS servers $\to$ TLD servers (.com, .org) $\to$ Authoritative DNS servers.
  - *Resolution Modes*:
    - **Iterative**: Local DNS server contacts root, root replies with TLD referral; local server contacts TLD, etc.
    - **Recursive**: Queried server takes burden of contacting others and returns final IP.
  - *DNS Record Types*:
    - **A**: Hostname $\to$ IPv4 address.
    - **AAAA**: Hostname $\to$ IPv6 address.
    - **NS**: Domain $\to$ Authoritative Name Server hostname.
    - **CNAME**: Alias hostname $\to$ Canonical canonical hostname.
    - **MX**: Domain $\to$ Mail server hostname.

---

### Session 06: Transport Layer Fundamentals & UDP
- **Transport vs. Network Layer**:
  - Network layer provides logical communication between *hosts*.
  - Transport layer provides logical communication between *processes* (using Port numbers: 16-bit, $0 - 65535$).
- **UDP (User Datagram Protocol - RFC 768)**:
  - Connectionless, lightweight, unreliable, unthrottled transmission.
  - Header Size: **8 bytes total** (4 fields $\times$ 2 bytes):
    `[Source Port (16b)] | [Destination Port (16b)] | [Length (16b)] | [Checksum (16b)]`
  - **Internet Checksum Calculation**:
    1. Divide segment into 16-bit words.
    2. Sum words using 1's complement arithmetic (wrap around end carry).
    3. Take bitwise NOT of final sum $\to$ written to Checksum field.

---

### Session 07: Reliable Data Transfer (RDT) & TCP Architecture
- **Pipelined Protocol Comparison**:
  | Feature | Stop-and-Wait | Go-Back-N (GBN) | Selective Repeat (SR) |
  | :--- | :--- | :--- | :--- |
  | **Window Size ($N$)** | $1$ | $N > 1$ (Sender window $N$, Receiver window $= 1$) | $N > 1$ (Sender window $N$, Receiver window $= N$) |
  | **ACK Mechanism** | Individual ACK | **Cumulative ACK** (ACK $n$ confirms all packets up to $n$) | **Individual ACK** (ACK $n$ confirms only packet $n$) |
  | **Timers** | 1 timer | **Single timer** for oldest unacknowledged packet | **Individual timer** for every unacknowledged packet |
  | **On Timeout** | Retransmit packet | Retransmit **ALL $N$ packets** in the window | Retransmit **ONLY the timed-out packet** |
  | **Max Window Constraint**| - | $N \le 2^k - 1$ ($k$ = sequence bits) | $N \le 2^{k-1}$ (prevents sequence overlap) |

- **TCP Segment Header (20 Bytes minimum)**:
  - Sequence Number (32-bit): Byte-stream index of first data byte in segment.
  - Acknowledgment Number (32-bit): Next expected byte from peer (cumulative).
  - Header Length (4 bits / Data Offset), Flags (URG, ACK, PSH, RST, SYN, FIN).
  - Receive Window (16-bit): Advertised flow control capacity.

- **TCP 3-Way Handshake & Connection Teardown**:
  - *Connection Establishment*:
    1. Client $\to$ Server: `SYN=1, seq=x`
    2. Server $\to$ Client: `SYN=1, ACK=1, seq=y, ack=x+1`
    3. Client $\to$ Server: `ACK=1, seq=x+1, ack=y+1`
  - *Connection Teardown*:
    1. Initiator $\to$ Receiver: `FIN=1, seq=u`
    2. Receiver $\to$ Initiator: `ACK=1, ack=u+1`
    3. Receiver $\to$ Initiator: `FIN=1, seq=v`
    4. Initiator $\to$ Receiver: `ACK=1, ack=v+1` $\to$ Enters `TIME_WAIT` ($2 \times \text{MSL}$).

---

### Session 08: TCP Congestion Control & Flow Control
- **Flow Control vs. Congestion Control**:
  - *Flow Control*: Prevents sender from overflowing the **receiver's buffer** (`rwnd` in header).
  - *Congestion Control*: Prevents senders from overloading the **network fabric** (`cwnd`).
  - Effective Sending Window: $W = \min(cwnd, rwnd)$.

- **TCP Congestion Control States (AIMD)**:
  1. **Slow Start**:
     - Begins with $cwnd = 1 \text{ MSS}$.
     - Doubles $cwnd$ every RTT ($cwnd \leftarrow cwnd \times 2$) $\to$ Exponential growth.
     - Transitions to Congestion Avoidance when $cwnd \ge ssthresh$.
  2. **Congestion Avoidance**:
     - Increases $cwnd$ by $1 \text{ MSS}$ per RTT ($cwnd \leftarrow cwnd + 1/\text{cwnd}$) $\to$ Linear growth.
  3. **Loss Event Reactions**:
     - *Timeout (Severe Congestion)*:
       - $ssthresh = cwnd / 2$
       - $cwnd = 1 \text{ MSS}$ (Restarts Slow Start)
     - *Triple Duplicate ACKs (Mild Congestion)*:
       - **TCP Tahoe**: Treats 3 dup ACKs same as timeout ($cwnd = 1$).
       - **TCP Reno (Fast Recovery)**: $ssthresh = cwnd / 2$, sets $cwnd = ssthresh + 3 \text{ MSS}$, continues linear growth.

---

### Session 09: Network Layer Data Plane & Routers
- **Router Internal Architecture**:
  1. *Input Ports*: Physical termination, data link decapsulation, lookup table match, queuing.
  2. *Switching Fabric*: Moves packets from input port to output port:
     - **Via Memory**: CPU manages copy to system RAM (slowest).
     - **Via Bus**: Shared bus contention limits bandwidth.
     - **Via Interconnection Network (Crossbar)**: Non-blocking parallel crossbar switches ($2N$ buses).
  3. *Output Ports*: Buffers packets; scheduling (FIFO, Priority, Round Robin, Weighted Fair Queuing).

---

### Session 10: IPv4, Subnetting Math & NAT
- **IPv4 Address Formats & CIDR**:
  - 32 bits, expressed as 4 dotted-decimal octets: `a.b.c.d/x` (where $x$ is prefix length).
  - **Subnet Formulas**:
    - Number of total addresses $= 2^{(32 - x)}$.
    - Number of usable host addresses $= 2^{(32 - x)} - 2$ *(Subtract 2 for Network ID and Directed Broadcast)*.
    - Subnet Mask: $x$ consecutive `1`s followed by $(32 - x)$ `0`s.
  - **Private Address Ranges (RFC 1918)**:
    - `10.0.0.0/8` ($10.0.0.0 - 10.255.255.255$)
    - `172.16.0.0/12` ($172.16.0.0 - 172.31.255.255$)
    - `192.168.0.0/16` ($192.168.0.0 - 192.168.255.255$)

- **Worked Subnetting Example**:
  - Given: `192.168.10.0/26`:
    - Prefix $= 26 \to 32 - 26 = 6$ host bits.
    - Subnet Mask: $255.255.255.192$ (Binary: `11000000` in last octet).
    - Total IP addresses $= 2^6 = 64$.
    - Usable host IPs $= 64 - 2 = 62$.
    - Block range: `192.168.10.0` to `192.168.10.63`.
    - Network Address: `192.168.10.0`, Broadcast Address: `192.168.10.63`.

- **Network Address Translation (NAT)**:
  - Maps multiple private internal IPs (`192.168.x.x`) to a single public IP using port numbers:
  - *NAT Translation Table*: `(Private IP, Private Port) <---> (Public IP, Assigned Port)`.

---

### Session 11: Routing Algorithms (Dijkstra & Bellman-Ford)
- **Link-State Routing (Dijkstra’s Shortest Path Algorithm)**:
  - Global knowledge: all routers possess complete topology map via Link State Advertisements (LSAs).
  - **Algorithm**:
    - Let $D(v)$ be current cost of least-cost path from source to $v$.
    - Let $N'$ be set of nodes whose least-cost paths are definitively known.
    - Loop: Find $w \notin N'$ with minimum $D(w)$; add $w$ to $N'$; update:
      $$D(v) = \min(D(v), D(w) + c(w, v)) \quad \forall v \notin N'$$
  - Complexity: $O(V^2)$ or $O(E + V \log V)$ with min-heap. Used in **OSPF**.

- **Distance-Vector Routing (Bellman-Ford Equation)**:
  - Decentralized: routers exchange distance vectors only with direct physical neighbors.
  - **Bellman-Ford Equation**:
    $$d_x(y) = \min_v \left\{c(x, v) + d_v(y)\right\}$$
    *(Where $c(x, v)$ is cost to neighbor $v$, and $d_v(y)$ is $v$'s advertised distance to destination $y$)*
  - **Count-to-Infinity Problem**: Routing loops when a link fails; solved via *Poisoned Reverse* (if $Z$ routes through $Y$ to $X$, $Z$ advertises $d_Z(X) = \infty$ to $Y$) and *Split Horizon*. Used in **RIP**.

---

### Session 12: Link Layer, Error Detection & CSMA/CD
- **Cyclic Redundancy Check (CRC)**:
  - Sender and receiver agree on a $(r + 1)$-bit generator polynomial $G$.
  - To send $d$-bit data $D$, append $r$ zero bits $\to D \cdot 2^r$.
  - Divide $D \cdot 2^r$ by $G$ using modulo-2 arithmetic (XOR without carries).
  - Remainder $R$ ($r$ bits) is appended to data $\to$ Transmitted frame $= \langle D, R \rangle$.
  - Receiver divides $\langle D, R \rangle$ by $G$; if remainder $\neq 0$, error detected!

- **CSMA/CD (Carrier Sense Multiple Access with Collision Detection)**:
  1. *Carrier Sense*: Listen before transmitting. If channel idle, transmit; if busy, wait.
  2. *Collision Detection*: Listen while transmitting.
  3. If collision detected, abort immediately and transmit a 48-bit **Jam Signal**.
  4. *Binary Exponential Backoff*: After $m^{\text{th}}$ consecutive collision, pick random $K \in \{0, 1, 2, \dots, 2^m - 1\}$ (capped at $m=10$); wait $K \times 512$ bit times before retrying.

---

### Session 13: Wireless & Mobile Networks (802.11)
- **Hidden Terminal Problem**: Node A and Node C can both reach Node B (AP), but cannot hear each other due to distance/obstacles. Simultaneous transmission causes collision at B.
- **RTS/CTS Solution (CSMA/CA)**:
  - Sender sends **RTS** (Request to Send) frame.
  - AP broadcasts **CTS** (Clear to Send) giving exclusive reservation. All nodes hearing CTS back off.
- **Mobile IP**:
  - *Home Agent (HA)*: Router in home network maintaining permanent Home Address.
  - *Foreign Agent (FA)*: Assigns temporary Care-of-Address (CoA) to mobile node.
  - *Tunneling*: Home agent encapsulates packets in new IP header directed to CoA.

---

### Session 14: Network Security & Cryptography
- **CIA Triad**: Confidentiality, Integrity, Availability.
- **Symmetric vs. Asymmetric Cryptography**:
  | Feature | Symmetric Encryption | Asymmetric Encryption |
  | :--- | :--- | :--- |
  | **Keys** | Single shared secret key for encryption & decryption | Public key (encrypt) + Private key (decrypt) |
  | **Speed** | 1000× faster (Hardware accelerated) | Slower, mathematically intensive |
  | **Key Distribution** | Problematic (must securely share secret key) | Easy (Public key distributed openly) |
  | **Algorithms** | AES (128/192/256 bit), 3DES, ChaCha20 | RSA, ECC (Elliptic Curve), Diffie-Hellman |

- **Security Protocols across Network Stack**:
  - *Application Layer*: HTTPS, PGP, SSH, S/MIME.
  - *Transport Layer*: SSL / TLS (Handshake protocol negotiates ciphers and keys; Record protocol provides encryption and integrity via HMAC).
  - *Network Layer (IPsec)*:
    - **AH (Authentication Header)**: Provides integrity and authentication, NO encryption.
    - **ESP (Encapsulating Security Payload)**: Provides encryption AND authentication.
    - **Modes**: Transport mode (encrypts payload only) vs. Tunnel mode (encrypts entire original IP packet and adds new IP header).

---

### Session 15: Multimedia Networking & Course Review
- **Streaming Stored Video (DASH)**: Dynamic Adaptive Streaming over HTTP. Server divides video into chunks encoded at multiple bitrates. Client dynamically requests chunk bitrate matching current measured throughput.
- **RTP / RTCP**: Real-time Transport Protocol running over UDP providing sequence numbers and timestamps for jitter compensation.
