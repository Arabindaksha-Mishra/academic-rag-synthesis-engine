# Computer Networks (BSDCBZC481)
<div class="subheading">Master Fast-Lookup Index & Quick Reference Cheat Sheet</div>

## 1. Lecture Roadmap & Physical Booklet Navigation
| Session & Code | Topic / Core Domain | Slide Range | 30-Sheet Printable Booklet Part |
| :--- | :--- | :---: | :--- |
| **Session 01** | OSI 7-Layer, TCP/IP 5-Layer, Delays | 1 – 62 | **Part 01 of 06** (Sheets 001–030) |
| **Session 02** | Network Core, Packet vs Circuit Switching | 63 – 108 | **Part 01 & Part 02** |
| **Session 04** | Application Layer: HTTP/1.1, HTTP/2, DNS | 109 – 149 | **Part 02 of 06** (Sheets 031–060) |
| **Session 05** | P2P BitTorrent, Socket Programming | 150 – 180 | **Part 02 & Part 03** |
| **Session 06** | Transport Layer, Multiplexing, UDP | 181 – 220 | **Part 03 of 06** (Sheets 061–090) |
| **Session 07** | RDT Principles, Go-Back-N, Selective Repeat | 221 – 263 | **Part 03 & Part 04** |
| **Session 08** | TCP Congestion Control (AIMD), Flow Control | 264 – 312 | **Part 04 of 06** (Sheets 091–120) |
| **Session 09** | Network Data Plane, Router Architectures | 313 – 356 | **Part 04 & Part 05** |
| **Session 10** | IPv4 Addressing, Subnetting Math, NAT | 357 – 411 | **Part 05 of 06** (Sheets 121–150) |
| **Session 11** | Routing Algorithms: Dijkstra, Bellman-Ford | 412 – 476 | **Part 05 & Part 06** |
| **Session 12** | Link Layer: Framing, CRC, Ethernet, CSMA/CD | 477 – 525 | **Part 06 of 06** (Sheets 151–168) |
| **Session 13** | Wireless LANs (802.11 Wi-Fi, CSMA/CA) | 526 – 566 | **Part 06 of 06** |
| **Session 14** | Network Security, SSL/TLS, IPsec, Firewalls | 567 – 627 | **Part 06 of 06** |
| **Session 15** | Multimedia Networking, Video Streaming (DASH) | 628 – 672 | **Part 06 of 06** |

## 2. Essential Mathematical Formulas & Metrics
<table width="100%" border="0" cellspacing="0" cellpadding="6" style="background-color: #f0fdf4; border-left: 4px solid #16a34a; margin: 5px 0;">
<tr><td>
<b>Total Nodal Delay:</b> $d_{nodal} = d_{proc} + d_{queue} + d_{trans} + d_{prop}$<br>
- <b>Transmission Delay:</b> $d_{trans} = \frac{L}{R}$ &nbsp; (L = packet length in bits, R = link rate in bps)<br>
- <b>Propagation Delay:</b> $d_{prop} = \frac{d}{s}$ &nbsp; (d = link distance in meters, s = propagation speed $\approx 2 \times 10^8 \text{ m/s}$)<br>
- <b>Traffic Intensity:</b> $I = \frac{L \cdot a}{R}$ &nbsp; ($I \approx 0 \implies$ small delay, $I \to 1 \implies$ asymptotic queue delay, $I > 1 \implies$ packet loss)
</td></tr>
</table>

<table width="100%" border="0" cellspacing="0" cellpadding="6" style="background-color: #f0fdf4; border-left: 4px solid #16a34a; margin: 5px 0;">
<tr><td>
<b>Bandwidth-Delay Product (BDP):</b> $\text{BDP} = R \times \text{RTT}$ (Maximum in-flight bits required to fully saturate pipe)<br>
<b>Utilization (Stop-and-Wait):</b> $U_{sender} = \frac{L/R}{\text{RTT} + L/R}$ | <b>Pipelined:</b> $U = \frac{N \times (L/R)}{\text{RTT} + L/R}$
</td></tr>
</table>

<table width="100%" border="0" cellspacing="0" cellpadding="6" style="background-color: #f0fdf4; border-left: 4px solid #16a34a; margin: 5px 0;">
<tr><td>
<b>IPv4 Subnetting Calculations:</b><br>
- Given prefix $/n$: Subnet Mask has $n$ ones. Host bits $h = 32 - n$.<br>
- Total Addresses $= 2^h$. <b>Usable Host Addresses:</b> $2^h - 2$ (subtract Network and Broadcast IDs).
</td></tr>
</table>

<table width="100%" border="0" cellspacing="0" cellpadding="6" style="background-color: #f0fdf4; border-left: 4px solid #16a34a; margin: 5px 0;">
<tr><td>
<b>Routing Algorithms:</b><br>
- <b>Dijkstra (Link State - OSPF):</b> $D(v) = \min(D(v), D(w) + c(w, v))$ &nbsp; [Time Complexity: $O(N^2)$ or $O(N \log N)$]<br>
- <b>Bellman-Ford (Distance Vector - RIP/BGP):</b> $d_x(y) = \min_v \{c(x, v) + d_v(y)\}$
</td></tr>
</table>

## 3. Core Protocols & Layer Cheat Sheet
| Protocol | Network Layer | Transport | Port | Key Features |
| :--- | :--- | :--- | :---: | :--- |
| **DNS** | Application | UDP / TCP | 53 | Hierarchical, Root $\to$ TLD $\to$ Auth, A/AAAA/CNAME/MX records |
| **HTTP/1.1** | Application | TCP | 80 | Persistent TCP, pipelining, Head-of-Line blocking |
| **HTTP/2** | Application | TCP | 443 | Binary framing, multiplexed streams, HPACK header compression |
| **HTTP/3** | Application | UDP (QUIC) | 443 | Zero-RTT reconnect, stream-level multiplexing, no HoL blocking |
| **TCP** | Transport | IP | - | Connection-oriented, 20B header, 3-way handshake, reliable, AIMD |
| **UDP** | Transport | IP | - | Connectionless, 8B header (Src, Dst, Len, Checksum), low latency |
| **OSPF** | Network | IP (proto 89) | - | Link-State, Dijkstra, intra-AS hierarchical areas |
| **BGP** | Network | TCP | 179 | Path-Vector, inter-AS policy routing, AS-PATH attribute prevents loops |
