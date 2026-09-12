# BITS WILP Computer Networks (BSDCBZC481 / BITS ZC481)
# Master Session-by-Session & Topic-Wise YouTube Video Playlist
### Ranked Strictly in Priority Order (Highest Exam Weightage First, Starting with Session 10)

> [!TIP]
> **HOW TO USE THIS PLAYLIST FOR LAST-MINUTE EXAM PREP**:
> - Watch videos at **1.5× or 1.75× playback speed**.
> - Prioritize **Tiers 1 & 2 (Sessions 10, 11, 08, 12, 07, 06, 02)** where 80%+ of the quantitative exam marks are concentrated.
> - Focus on the **numerical steps** demonstrated on the whiteboard (how they write the equations and construct the tables).

---

## Quick Priority Navigation
1. [Priority 1: Session 10 — IP Addressing, Subnetting/VLSM, NAT, DHCP, Fragmentation](#priority-1-session-10--ip-addressing-subnetting-nat-dhcp--fragmentation) *(18% – 22% Weightage)*
2. [Priority 2: Session 11 — Routing Algorithms: Dijkstra, Bellman-Ford, OSPF, BGP](#priority-2-session-11--routing-algorithms-dijkstra-bellman-ford-ospf-bgp) *(15% – 20% Weightage)*
3. [Priority 3: Session 08 — TCP Congestion Control (AIMD, Tahoe vs Reno)](#priority-3-session-08--tcp-congestion-control-aimd-tahoe-vs-reno) *(12% – 15% Weightage)*
4. [Priority 4: Session 12 — Link Layer, CRC Division, Ethernet, Switch Learning](#priority-4-session-12--link-layer-crc-division-ethernet--switch-learning) *(12% – 15% Weightage)*
5. [Priority 5: Session 07 — TCP Header, 3-Way Handshake & Flow Control](#priority-5-session-07--tcp-header-3-way-handshake--flow-control) *(10% – 12% Weightage)*
6. [Priority 6: Session 06 — UDP & Reliable Data Transfer (Stop-and-Wait, GBN, SR)](#priority-6-session-06--udp--reliable-data-transfer-stop-and-wait-gbn-sr) *(8% – 10% Weightage)*
7. [Priority 7: Session 02 — Network Core, Nodal Delays & Packet Switching](#priority-7-session-02--network-core-nodal-delays--packet-switching) *(8% – 10% Weightage)*
8. [Priority 8: Session 13 — Wireless Networks, 802.11 CSMA/CA, Mobile IP](#priority-8-session-13--wireless-networks-80211-csmaca-mobile-ip) *(8% – 10% Weightage)*
9. [Priority 9: Session 14 — Network Security, RSA Algorithm, Cryptography](#priority-9-session-14--network-security-rsa-algorithm-cryptography) *(8% – 10% Weightage)*
10. [Priority 10: Session 09 — Router Architecture & Switching Fabrics](#priority-10-session-09--router-architecture--switching-fabrics) *(5% – 8% Weightage)*
11. [Priority 11: Session 15 — Multimedia Networks & QoS (Leaky / Token Bucket)](#priority-11-session-15--multimedia-networks--qos-leaky--token-bucket) *(5% – 8% Weightage)*
12. [Priority 12: Session 04 — Application Layer: HTTP Evolution & DNS](#priority-12-session-04--application-layer-http-evolution--dns) *(5% – 8% Weightage)*
13. [Priority 13: Session 05 — Application Layer: P2P & Socket Programming](#priority-13-session-05--application-layer-p2p--socket-programming) *(3% – 5% Weightage)*
14. [Priority 14: Session 01 — Introduction & Network Models (OSI vs TCP/IP)](#priority-14-session-01--introduction--network-models-osi-vs-tcpip) *(3% – 5% Weightage)*

---

### Priority 1: Session 10 — IP Addressing, Subnetting, NAT, DHCP & Fragmentation
* **Slide Deck**: [`Session_10_Network_Layer_IP_Addressing_NAT.pdf`](file:///usr/local/google/home/arabindaksha/Modify-pdf/exam_ready_pdf_modules/2_Computer_Networks_BSDCBZC481/sessionwise_lectures/Session_10_Network_Layer_IP_Addressing_NAT.pdf)
* **Exam Weightage**: **18% – 22%** (Compulsory Numericals)

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **Subnetting & VLSM Shortcuts** | [Gate Smashers – Subnetting in Computer Networks](https://www.youtube.com/watch?v=1Zx2nI03n-Q) | Gate Smashers (~12m) | $2^h - 2 \ge N$, prefix $/x$, and subnet mask conversion |
| **VLSM Step-by-Step Allocation** | [NetworkChuck – Subnetting Mastery (VLSM)](https://www.youtube.com/results?search_query=NetworkChuck+VLSM+subnetting) | NetworkChuck (~15m) | Descending order allocation for multi-department topologies |
| **IPv4 Packet Fragmentation** | [Gate Smashers – IPv4 Datagram Fragmentation](https://www.youtube.com/watch?v=R9j7P7Gj434) | Gate Smashers (~11m) | 8-byte offset rule ($\text{Data Start}/8$), DF/MF flags |
| **IPv4 Header Fields** | [Gate Smashers – IPv4 Header Format](https://www.youtube.com/results?search_query=Gate+Smashers+IPv4+Header+Format) | Gate Smashers (~10m) | IHL (4-byte words), Total Length vs Payload, TTL, Checksum |
| **DHCP 4-Step DORA Protocol** | [Gate Smashers – DHCP Protocol Working](https://www.youtube.com/watch?v=kYyO1d5e3oE) | Gate Smashers (~9m) | Ports 67/68, Discover-Offer-Request-ACK broadcast reason |
| **NAT & Port Translation (NAPT)** | [Gate Smashers – Network Address Translation (NAT)](https://www.youtube.com/watch?v=rd57p8u8w6U) | Gate Smashers (~10m) | WAN/LAN mapping table, private RFC 1918 address preservation |
| **IPv6 Header & Transition** | [Gate Smashers – IPv6 Header Format & Migration](https://www.youtube.com/results?search_query=Gate+Smashers+IPv6+Header+Format) | Gate Smashers (~12m) | Fixed 40-byte header, no checksum, Dual-Stack vs Tunneling |

---

### Priority 2: Session 11 — Routing Algorithms: Dijkstra, Bellman-Ford, OSPF, BGP
* **Slide Deck**: [`Session_11_Network_Layer_Routing_Algorithms.pdf`](file:///usr/local/google/home/arabindaksha/Modify-pdf/exam_ready_pdf_modules/2_Computer_Networks_BSDCBZC481/sessionwise_lectures/Session_11_Network_Layer_Routing_Algorithms.pdf)
* **Exam Weightage**: **15% – 20%** (Guaranteed Graph / Algorithmic Problem)

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **Dijkstra's Algorithm (Link-State)** | [Abdul Bari – Dijkstra's Algorithm Step-by-Step](https://www.youtube.com/watch?v=XB4MIexqxYo) | Abdul Bari (~16m) | Constructing iteration table: $N', D(v), p(v)$, tie-breaking |
| **Bellman-Ford (Distance Vector)** | [Abdul Bari – Bellman-Ford Algorithm](https://www.youtube.com/watch?v=lyw4FaxrwHg) | Abdul Bari (~18m) | Dynamic programming formula: $d_x(y) = \min_v [c(x,v) + d_v(y)]$ |
| **Count-to-Infinity & Poisoned Reverse** | [Gate Smashers – Distance Vector & Count to Infinity](https://www.youtube.com/results?search_query=Gate+Smashers+Distance+Vector+Count+to+Infinity) | Gate Smashers (~11m) | Routing loops, Split Horizon, why Poison Reverse fails for $\ge 3$ nodes |
| **OSPF vs RIP (Intra-AS)** | [Gate Smashers – OSPF Protocol in Computer Networks](https://www.youtube.com/results?search_query=Gate+Smashers+OSPF+Protocol) | Gate Smashers (~12m) | Link-State vs Distance-Vector, Area 0 Backbone, hop count limits |
| **BGP-4 (Inter-AS Path Vector)** | [Gate Smashers – BGP Protocol (Border Gateway)](https://www.youtube.com/results?search_query=Gate+Smashers+BGP+Protocol) | Gate Smashers (~13m) | AS-PATH loop prevention, eBGP vs iBGP, NEXT-HOP attribute |

---

### Priority 3: Session 08 — TCP Congestion Control (AIMD, Tahoe vs Reno)
* **Slide Deck**: [`Session_08_Transport_Layer_TCP_Congestion.pdf`](file:///usr/local/google/home/arabindaksha/Modify-pdf/exam_ready_pdf_modules/2_Computer_Networks_BSDCBZC481/sessionwise_lectures/Session_08_Transport_Layer_TCP_Congestion.pdf)
* **Exam Weightage**: **12% – 15%** (High Probability Numerical/Graph)

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **TCP Congestion Control (Tahoe vs Reno)** | [Gate Smashers – TCP Congestion Control (AIMD, Tahoe & Reno)](https://www.youtube.com/watch?v=kYv-Fj82P5w) | Gate Smashers (~13m) | Slow Start, Congestion Avoidance, ssthresh, Timeout vs 3 Dup ACKs |
| **AIMD & Fast Recovery Mechanics** | [Neso Academy – TCP Congestion Control](https://www.youtube.com/results?search_query=Neso+Academy+TCP+Congestion+Control) | Neso Academy (~14m) | Sawtooth curve, multiplicative decrease, additive linear increase |
| **Textbook Author Deep-Dive** | [Jim Kurose – TCP Congestion Control Lecture](https://www.youtube.com/results?search_query=Jim+Kurose+TCP+Congestion+Control) | Jim Kurose (~15m) | Author explanation of Reno Fast Recovery and TCP fairness |

---

### Priority 4: Session 12 — Link Layer, CRC Division, Ethernet & Switch Learning
* **Slide Deck**: [`Session_12_Link_Layer_LANs_and_Ethernet.pdf`](file:///usr/local/google/home/arabindaksha/Modify-pdf/exam_ready_pdf_modules/2_Computer_Networks_BSDCBZC481/sessionwise_lectures/Session_12_Link_Layer_LANs_and_Ethernet.pdf)
* **Exam Weightage**: **12% – 15%** (Guaranteed Problem)

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **CRC Generation & Check (Modulo-2)** | [Gate Smashers – CRC (Cyclic Redundancy Check)](https://www.youtube.com/watch?v=kU8Y1L2f7nQ) | Gate Smashers (~12m) | Modulo-2 binary XOR long division, polynomial degree $k$, FCS |
| **CSMA/CD & Collision Detection** | [Gate Smashers – CSMA/CD Protocol](https://www.youtube.com/watch?v=k6e492rPqJk) | Gate Smashers (~11m) | Min frame size condition: $L_{min} \ge 2 \cdot t_{prop} \cdot R$, Exponential backoff |
| **Switch Self-Learning Table** | [Gate Smashers – Switches in Computer Networks](https://www.youtube.com/results?search_query=Gate+Smashers+Switches+Self+Learning) | Gate Smashers (~10m) | Table entries `[MAC, Port, TTL]`, Forwarding vs Filtering vs Flooding |

---

### Priority 5: Session 07 — TCP Header, 3-Way Handshake & Flow Control
* **Slide Deck**: [`Session_07_Transport_Layer_TCP_Structure.pdf`](file:///usr/local/google/home/arabindaksha/Modify-pdf/exam_ready_pdf_modules/2_Computer_Networks_BSDCBZC481/sessionwise_lectures/Session_07_Transport_Layer_TCP_Structure.pdf)
* **Exam Weightage**: **10% – 12%**

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **TCP 3-Way Handshake & Teardown** | [Gate Smashers – TCP 3-Way Handshake](https://www.youtube.com/watch?v=s1R1Yp42V6Q) | Gate Smashers (~10m) | SYN, SYN-ACK, ACK sequence tracking (SYN consumes 1 sequence number!) |
| **TCP Header Format Dissection** | [Gate Smashers – TCP Header Format](https://www.youtube.com/watch?v=R9K2S2W1-sQ) | Gate Smashers (~12m) | 20-byte base header, Flags (URG, ACK, PSH, RST, SYN, FIN), rwnd |
| **TCP Flow Control (Sliding Window)** | [Gate Smashers – Flow Control in TCP](https://www.youtube.com/results?search_query=Gate+Smashers+Flow+Control+in+TCP) | Gate Smashers (~9m) | Receiver window (`rwnd`) feedback, Silly Window Syndrome prevention |

---

### Priority 6: Session 06 — UDP & Reliable Data Transfer (Stop-and-Wait, GBN, SR)
* **Slide Deck**: [`Session_06_Transport_Layer_UDP_and_RDT.pdf`](file:///usr/local/google/home/arabindaksha/Modify-pdf/exam_ready_pdf_modules/2_Computer_Networks_BSDCBZC481/sessionwise_lectures/Session_06_Transport_Layer_UDP_and_RDT.pdf)
* **Exam Weightage**: **8% – 10%**

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **Go-Back-N (GBN) Protocol** | [Gate Smashers – Go-Back-N Sliding Window](https://www.youtube.com/watch?v=A-tV4-3V7cE) | Gate Smashers (~14m) | Sender window $W \le 2^k - 1$, receiver buffer $= 1$, cumulative ACKs |
| **Selective Repeat (SR) Protocol** | [Gate Smashers – Selective Repeat Protocol](https://www.youtube.com/results?search_query=Gate+Smashers+Selective+Repeat+Protocol) | Gate Smashers (~12m) | Sender & receiver window $W \le 2^{k-1}$, independent timers, individual ACKs |
| **UDP Checksum Calculation** | [Gate Smashers – UDP Checksum Calculation](https://www.youtube.com/results?search_query=Gate+Smashers+UDP+Checksum+Calculation) | Gate Smashers (~10m) | 16-bit 1's complement addition, wrap-around carry, pseudo-header |

---

### Priority 7: Session 02 — Network Core, Nodal Delays & Packet Switching
* **Slide Deck**: [`Session_02_Network_Edge_Core_and_Switching.pdf`](file:///usr/local/google/home/arabindaksha/Modify-pdf/exam_ready_pdf_modules/2_Computer_Networks_BSDCBZC481/sessionwise_lectures/Session_02_Network_Edge_Core_and_Switching.pdf)
* **Exam Weightage**: **8% – 10%**

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **4 Nodal Delays (Formula & Math)** | [Gate Smashers – Delays in Computer Networks](https://www.youtube.com/results?search_query=Gate+Smashers+Delays+in+Computer+Networks) | Gate Smashers (~11m) | $d_{trans} = L/R$, $d_{prop} = d/s$, $d_{nodal} = d_{proc} + d_{queue} + d_{trans} + d_{prop}$ |
| **Packet Switching vs Circuit Switching** | [Gate Smashers – Packet Switching vs Circuit Switching](https://www.youtube.com/results?search_query=Gate+Smashers+Packet+Switching+vs+Circuit+Switching) | Gate Smashers (~9m) | Statistical multiplexing vs dedicated bandwidth (FDM/TDM) |

---

### Priority 8: Session 13 — Wireless Networks, 802.11 CSMA/CA & Mobile IP
* **Slide Deck**: [`Session_13_Wireless_and_Mobile_Networks.pdf`](file:///usr/local/google/home/arabindaksha/Modify-pdf/exam_ready_pdf_modules/2_Computer_Networks_BSDCBZC481/sessionwise_lectures/Session_13_Wireless_and_Mobile_Networks.pdf)
* **Exam Weightage**: **8% – 10%**

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **CSMA/CA & RTS/CTS Exchange** | [Gate Smashers – CSMA/CA Protocol](https://www.youtube.com/results?search_query=Gate+Smashers+CSMA+CA+Protocol) | Gate Smashers (~10m) | Collision avoidance, NAV (Network Allocation Vector), SIFS/DIFS |
| **Hidden & Exposed Terminal Problem** | [Gate Smashers – Hidden and Exposed Station Problem](https://www.youtube.com/results?search_query=Gate+Smashers+Hidden+and+Exposed+Station+Problem) | Gate Smashers (~10m) | Why CSMA/CD fails in wireless; RTS/CTS virtual sensing fix |
| **Mobile IP Architecture** | [Gate Smashers – Mobile IP Architecture](https://www.youtube.com/results?search_query=Gate+Smashers+Mobile+IP) | Gate Smashers (~11m) | Home Agent, Foreign Agent, Care-of-Address (CoA), Triangular Routing |

---

### Priority 9: Session 14 — Network Security, RSA Algorithm & Cryptography
* **Slide Deck**: [`Session_14_Network_Security_Cryptography.pdf`](file:///usr/local/google/home/arabindaksha/Modify-pdf/exam_ready_pdf_modules/2_Computer_Networks_BSDCBZC481/sessionwise_lectures/Session_14_Network_Security_Cryptography.pdf)
* **Exam Weightage**: **8% – 10%**

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **RSA Algorithm (Numerical Trace)** | [Abdul Bari – RSA Algorithm Step-by-Step](https://www.youtube.com/watch?v=4zahvcJ9glg) | Abdul Bari (~15m) | Prime selection ($p, q$), $n = p \cdot q$, $\phi(n) = (p-1)(q-1)$, $e \cdot d \equiv 1 \pmod{\phi(n)}$ |
| **Symmetric vs Asymmetric Crypto** | [Gate Smashers – Cryptography & Network Security](https://www.youtube.com/results?search_query=Gate+Smashers+Symmetric+vs+Asymmetric+Cryptography) | Gate Smashers (~10m) | DES/AES secret key vs RSA public key, key exchange problem |
| **Firewalls & IPsec Architecture** | [Gate Smashers – Firewalls in Network Security](https://www.youtube.com/results?search_query=Gate+Smashers+Firewall+Types) | Gate Smashers (~10m) | Packet filtering vs stateful inspection; AH (Integrity) vs ESP (Encryption) |

---

### Priority 10: Session 09 — Router Architecture & Switching Fabrics
* **Slide Deck**: [`Session_09_Network_Layer_Data_Plane_Routers.pdf`](file:///usr/local/google/home/arabindaksha/Modify-pdf/exam_ready_pdf_modules/2_Computer_Networks_BSDCBZC481/sessionwise_lectures/Session_09_Network_Layer_Data_Plane_Routers.pdf)
* **Exam Weightage**: **5% – 8%**

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **Router Building Blocks & Input Ports** | [Jim Kurose – What's Inside a Router?](https://www.youtube.com/results?search_query=Jim+Kurose+Inside+a+Router) | Jim Kurose (~12m) | Input port processing, lookup, line termination, forwarding engine |
| **Switching Fabrics & HOL Blocking** | [Gate Smashers – Router Architecture & Switching Fabrics](https://www.youtube.com/results?search_query=Gate+Smashers+Switching+Fabrics) | Gate Smashers (~10m) | Memory vs Bus vs Crossbar interconnects; Head-of-Line (HOL) blocking |

---

### Priority 11: Session 15 — Multimedia Networks & QoS (Leaky / Token Bucket)
* **Slide Deck**: [`Session_15_Multimedia_Networks_and_Review.pdf`](file:///usr/local/google/home/arabindaksha/Modify-pdf/exam_ready_pdf_modules/2_Computer_Networks_BSDCBZC481/sessionwise_lectures/Session_15_Multimedia_Networks_and_Review.pdf)
* **Exam Weightage**: **5% – 8%**

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **Leaky Bucket Algorithm (Shaping)** | [Gate Smashers – Leaky Bucket Algorithm](https://www.youtube.com/watch?v=k6hFq94b9f0) | Gate Smashers (~9m) | Enforces strictly constant output rate; drops packets when queue overflows |
| **Token Bucket Algorithm (Policing)** | [Gate Smashers – Token Bucket Algorithm](https://www.youtube.com/watch?v=R9Z-v-nU-1w) | Gate Smashers (~10m) | Accumulates tokens at rate $r$; permits controlled burst transmission up to capacity $b$ |
| **Packet Scheduling (FIFO, RR, WFQ)** | [Gate Smashers – Quality of Service & Scheduling](https://www.youtube.com/results?search_query=Gate+Smashers+Packet+Scheduling+QoS) | Gate Smashers (~11m) | Strict Priority vs Round Robin vs Weighted Fair Queuing (WFQ) |

---

### Priority 12: Session 04 — Application Layer: HTTP Evolution & DNS
* **Slide Deck**: [`Session_04_App_Layer_Web_HTTP_DNS.pdf`](file:///usr/local/google/home/arabindaksha/Modify-pdf/exam_ready_pdf_modules/2_Computer_Networks_BSDCBZC481/sessionwise_lectures/Session_04_App_Layer_Web_HTTP_DNS.pdf)
* **Exam Weightage**: **5% – 8%**

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **DNS Hierarchy & Resolution** | [Gate Smashers – Domain Name System (DNS)](https://www.youtube.com/watch?v=XnS9W_gZ170) | Gate Smashers (~11m) | Root, TLD, Authoritative; Iterative vs Recursive query latency |
| **HTTP/1.0 vs 1.1 vs 2.0 vs 3.0** | [Gate Smashers – HTTP Protocol & Evolution](https://www.youtube.com/results?search_query=Gate+Smashers+HTTP+Protocol) | Gate Smashers (~12m) | Non-persistent ($2\text{ RTT}\times N$) vs Persistent ($2\text{ RTT} + N\times\text{RTT}$), HOL blocking, QUIC |

---

### Priority 13: Session 05 — Application Layer: P2P & Socket Programming
* **Slide Deck**: [`Session_05_App_Layer_P2P_and_Sockets.pdf`](file:///usr/local/google/home/arabindaksha/Modify-pdf/exam_ready_pdf_modules/2_Computer_Networks_BSDCBZC481/sessionwise_lectures/Session_05_App_Layer_P2P_and_Sockets.pdf)
* **Exam Weightage**: **3% – 5%**

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **P2P File Distribution vs Client-Server** | [Jim Kurose – P2P File Distribution](https://www.youtube.com/results?search_query=Jim+Kurose+P2P+File+Distribution) | Jim Kurose (~12m) | Scalability analysis: distribution time $D_{CS} \ge \max\{NF/u_s, F/d_{min}\}$ vs $D_{P2P}$ |
| **Socket Programming (TCP vs UDP)** | [Gate Smashers – Socket Programming Basics](https://www.youtube.com/results?search_query=Gate+Smashers+Socket+Programming) | Gate Smashers (~10m) | System calls: `socket()`, `bind()`, `listen()`, `accept()`, `connect()` |

---

### Priority 14: Session 01 — Introduction & Network Models (OSI vs TCP/IP)
* **Slide Deck**: [`Session_01_Intro_and_Network_Models.pdf`](file:///usr/local/google/home/arabindaksha/Modify-pdf/exam_ready_pdf_modules/2_Computer_Networks_BSDCBZC481/sessionwise_lectures/Session_01_Intro_and_Network_Models.pdf)
* **Exam Weightage**: **3% – 5%**

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **OSI 7-Layer vs TCP/IP 5-Layer** | [Gate Smashers – OSI Model vs TCP/IP Model](https://www.youtube.com/results?search_query=Gate+Smashers+OSI+vs+TCP+IP) | Gate Smashers (~12m) | Layer duties, data unit names (Message, Segment, Datagram, Frame, Bits) |
| **Encapsulation & Decapsulation** | [PowerCert – TCP/IP & Data Encapsulation](https://www.youtube.com/results?search_query=PowerCert+Data+Encapsulation) | PowerCert (~8m) | Visual header appending and stripping across network boundaries |
