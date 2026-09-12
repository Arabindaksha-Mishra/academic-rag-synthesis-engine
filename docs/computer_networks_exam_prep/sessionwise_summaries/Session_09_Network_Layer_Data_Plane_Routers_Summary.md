# Computer Networks (BSDCBZC481)
# Session 09: Network Layer Data Plane — Router Architecture & Packet Scheduling
### Exhaustive Slide-by-Slide Academic Exam Revision Manual & Problem Solving Guide

---

## 1. Session Context & Pedagogical Scope
- **Course Code & Title**: BSDCBZC481 — Computer Networks
- **Instructor**: Dr. K. Kalaiselvi (BITS Pilani)
- **Primary Textbooks**:
  - J.F. Kurose & K.W. Ross, *Computer Networking: A Top-Down Approach*, 5th/6th Edition, Chapter 4 (T1)
  - B.A. Forouzan, *Data Communications and Networking*, 4th Edition, Chapter 19 (T2)
- **Lecture Slide Mapping**: CS9: Network Layer — Slides 1 to 44 (Complete Coverage)
- **Core Syllabus Covered**:
  1. Network Layer Architectural Paradigm: Data Plane vs. Control Plane
  2. Network Service Models: Internet Best-Effort vs. ATM Guaranteed QoS
  3. Anatomy of a High-Performance Router: Input Ports, Switching Fabric, Output Ports & Routing Processor
  4. Input Port Processing: Physical Line Termination, Link-Layer Decapsulation & Decentralized Lookup
  5. The Longest Prefix Matching (LPM) Algorithm & Hardware TCAM Lookups
  6. The Three Switching Fabric Paradigms: Memory, Bus, and Crossbar Interconnection Networks
  7. Head-of-Line (HoL) Blocking: Mathematical Phenomenon, Proof & Virtual Output Queuing (VOQ)
  8. Output Port Queuing, Buffer Sizing Rules (Stanford Formula: $B = \text{RTT} \cdot C / \sqrt{N}$) & RED
  9. Packet Scheduling Disciplines: FIFO, Non-Preemptive Priority Queuing, Round Robin & Weighted Fair Queuing (WFQ)
  10. High-Yield Open-Book Exam Traps, Rigorous Numerical Problems & Fast Revision Checklist

---

## 2. Data Plane vs. Control Plane Paradigm (Slides 3–6)

The network layer provides end-to-end host-to-host communication. Modern network architecture explicitly decouples the network layer into two functional planes:

```
+-------------------------------------------------------------------------+
|                      CONTROL PLANE (Software / Global)                  |
|    - Routing algorithms (OSPF, BGP) or Software-Defined Network (SDN)   |
|      remote controller.                                                 |
|    - Operates on milliseconds-to-seconds timescale in software CPU.     |
|    - Computes global end-to-end paths; populates Forwarding Tables.     |
+-------------------------------------------------------------------------+
                                     |
              Installs Forwarding    | Tables
                                     v
+-------------------------------------------------------------------------+
|                       DATA PLANE (Hardware / Local)                     |
|    - Local, per-router functions.                                       |
|    - Inspects arriving IP packet header; looks up entry in forwarding   |
|      table; switches packet from input port to output port.             |
|    - Operates on nanoseconds timescale directly in ASIC hardware.       |
+-------------------------------------------------------------------------+
```

### 2.1 Network Service Models (Slide 6)
- **Internet "Best-Effort" Service Model**:
  - Delivers packets with **zero guarantees** regarding throughput, packet loss, end-to-end delay, or packet ordering.
  - *Philosophical Rationale*: Simplicity at the core enables minimal router complexity, rapid hardware scaling, and moves sophisticated intelligence (reliability, congestion control) to the end systems (End-to-End Principle).
- **Alternative Telecommunication Models (ATM / IntServ)**:
  - Constant Bit Rate (CBR) / Variable Bit Rate (VBR): Provide strict deterministic timing and bandwidth guarantees, but require complex per-flow state inside every core switch.

---

## 3. Anatomy of a High-Performance Router (Slides 7–14)

A router consists of four primary hardware components:

```
+-------------------------------------------------------------------------+
|                            ROUTING PROCESSOR                            |
|             (Software CPU: executes routing protocols, OSPF/BGP)         |
+-------------------------------------------------------------------------+
       |                                                           ^
       | Installs Forwarding Tables                                | Routing Control Packets
       v                                                           |
+--------------+          +-----------------------+         +--------------+
|  INPUT PORT  | =======> |                       | ======> |  OUTPUT PORT |
|  (Lookup &   |          |   SWITCHING FABRIC    |         |  (Queuing &  |
|   Forwarding)|          |  (Memory, Bus, or     |         |   Scheduling)|
+--------------+          |   Crossbar)           |         +--------------+
|  INPUT PORT  | =======> |                       | ======> |  OUTPUT PORT |
+--------------+          +-----------------------+         +--------------+
```

1. **Input Ports**:
   - *Physical Layer*: Terminates physical wire/fiber, converts electromagnetic signals to bits.
   - *Link Layer*: Decapsulates link-layer frames (e.g., extracts IP packet from Ethernet frame), verifies CRC.
   - *Decentralized Forwarding*: Inspects destination IP address and queries a local copy of the forwarding table to determine the target output port.
2. **Switching Fabric**: High-speed internal bus or crossbar network transferring packets from input ports to output ports.
3. **Output Ports**: Stores packets received from the switching fabric in buffer memory and schedules them for physical transmission onto the outgoing link.
4. **Routing Processor**: Executes control-plane routing algorithms, handles ICMP errors, manages the master routing table, and compiles forwarding tables for distribution to input port hardware.

---

## 4. Input Port Processing & Longest Prefix Matching (Slides 15–20)

### 4.1 Decentralized Lookup
To eliminate central CPU bottlenecks, high-performance routers maintain a shadow copy of the forwarding table on every single input port interface card (**decentralized switching**).

### 4.2 The Longest Prefix Matching (LPM) Algorithm
When an IP datagram arrives with a 32-bit destination address, the router compares the destination address against all prefix entries in its forwarding table.
> [!IMPORTANT]
> **Longest Prefix Matching Rule**:
> When a destination address matches multiple prefixes in the forwarding table, the router **must forward the packet to the link interface corresponding to the longest (most specific) matching prefix**.

#### Worked Example:
Suppose a router has the following forwarding table:

| Prefix Entry (Binary) | CIDR Notation | Outgoing Link Interface |
| :--- | :--- | :---: |
| `11001000 00010111 00010*** ********` | `200.23.16.0/20` | **Interface 0** |
| `11001000 00010111 00011000 ********` | `200.23.24.0/21` | **Interface 1** |
| `11001000 00010111 00011*** ********` | `200.23.24.0/20` | **Interface 2** |
| Otherwise | Default Route (`0.0.0.0/0`) | **Interface 3** |

- **Destination 1**: `200.23.16.12` $\to$ `11001000 00010111 00010000 00001100`
  - Matches Prefix 0 (20-bit match: `11001000 00010111 00010`).
  - **Forwarded to Interface 0**.
- **Destination 2**: `200.23.24.50` $\to$ `11001000 00010111 00011000 00110010`
  - Matches Prefix 1 (21-bit match: `11001000 00010111 00011000`).
  - Matches Prefix 2 (20-bit match: `11001000 00010111 00011`).
  - Longest prefix is 21 bits $\implies$ **Forwarded to Interface 1**!

### 4.3 Ternary Content-Addressable Memory (TCAM)
Software binary search trees (trie structures) require $O(\log W)$ lookups. Modern multi-terabit core routers use **TCAM** hardware, which searches millions of prefix rules in parallel in a single clock cycle ($O(1)$ lookup), returning the longest matching mask in nanoseconds!

---

## 5. Switching Fabrics Deep Dive (Slides 21–25)

The switching fabric is the physical backplane moving packets from input ports to output ports.

```
1. SWITCHING VIA MEMORY:         2. SWITCHING VIA BUS:            3. CROSSBAR NETWORK:
   [ Input ]      [ Output ]        [ Input 1 ]     [ Input 2 ]        Out 1  Out 2  Out 3
       \              ^                 |               |               |      |      |
        \            /                  +-------+-------+       In 1 --[x]----[ ]----[ ]--
         v          /                           |                      |      |      |
      [ System Memory ]                   Shared Bus            In 2 --[ ]----[x]----[ ]--
      (CPU copies packet)                       |                      |      |      |
                                        +-------+-------+       In 3 --[ ]----[ ]----[x]--
                                        |               |              (Non-blocking parallel)
                                    [ Output 1 ]    [ Output 2 ]
```

### 5.1 The Three Switching Architectures

| Switching Type | Internal Mechanism | Maximum Switching Speed | Primary Architectural Bottleneck |
| :--- | :--- | :--- | :--- |
| **Via Memory (1st Gen)** | Input port signals CPU via interrupt; packet is copied across system bus into shared RAM, then copied to output port. | Limited by system memory bandwidth; packet traverses bus **twice** ($B_{\text{mem}} / 2$). | Memory bus contention; cannot forward two packets concurrently. |
| **Via Bus (2nd Gen)** | Input port transfers packet directly across a shared internal backplane bus without CPU intervention. | Limited by backplane bus bandwidth ($B_{\text{bus}}$). Typical rates: $1-10\,\text{Gbps}$. | **Bus Contention**: Only one packet can traverse the bus at any instant. Other input ports must wait. |
| **Crossbar Network (3rd Gen)**| An $N \times N$ matrix of horizontal and vertical buses intersecting at fabric crosspoint switches. | **Non-blocking parallel switching**: Can transfer up to $N$ packets simultaneously! Aggregate throughput $= N \times R$. | **Output Contention**: Multiple input ports attempting to send to the *same* output port simultaneously. |

---

## 6. Head-of-Line (HoL) Blocking & Virtual Output Queuing (Slides 26–29)

### 6.1 The HoL Blocking Phenomenon
HoL blocking occurs at **input-queued routers** with a crossbar switching fabric:
- Suppose two packets at the front of Input Queue 1 and Input Queue 2 both compete for **Output Port 1**.
- The crossbar fabric can only connect one input to Output Port 1 at a time; suppose Input 1 wins contention.
- Input Queue 2 is forced to wait.
- **The Catastrophe**: A second packet sitting behind the head of Input Queue 2 is destined for an entirely **idle Output Port 3**. Even though Output Port 3 is completely free, this second packet is trapped and blocked because the packet in front of it is stalled!

```
Input Port 1:  [ For Out 2 ] [ For Out 1 ] ===> (Fabric serves Out 1) ===> [ Out 1 (Busy) ]
                                    ^
                                    | (Contention!)
Input Port 2:  [ For Out 3 ] [ For Out 1 ] ===> (BLOCKED!)
                     ^
                     | (TRAPPED: Blocked from reaching free Out 3!)
```

### 6.2 Mathematical Throughput Limit Under HoL Blocking
In a classic theoretical derivation by Karol, Hluchyj, and Morgan (1987):
Under uniform random traffic and infinite queues, an input-queued switch without Virtual Output Queuing suffers an asymptotic saturation throughput limit of:
$$\text{Maximum Throughput} = 2 - \sqrt{2} \approx \mathbf{0.586} \quad (\mathbf{58.6\%})$$
More than $41\%$ of the switch's theoretical switching bandwidth is completely lost to HoL blocking!

### 6.3 Solution: Virtual Output Queuing (VOQ)
Instead of maintaining a single FIFO queue, each input port maintains **$N$ distinct independent sub-queues**, one dedicated for each output port. A packet for Output 3 is placed in Queue 3 and transmitted immediately, completely bypassing any packet waiting for Output 1!

---

## 7. Output Port Queuing & Buffer Sizing Rules (Slides 30–35)

### 7.1 When Does Output Queuing Occur?
Output queuing occurs when the arrival rate from the high-speed switching fabric exceeds the transmission rate of the outgoing physical link. If the buffer fills completely, arriving packets are dropped (**Buffer Overflow / Packet Loss**).

### 7.2 Router Buffer Sizing Rules of Thumb

1. **Traditional Rule of Thumb (Slide 33)**:
   Historically, network engineers sized router buffers to the Bandwidth-Delay Product:
   $$B = \text{RTT} \times C$$
   - $\text{RTT}$: Typical end-to-end round trip time ($\approx 250\,\text{ms}$).
   - $C$: Transmission link capacity.
   - *Example*: For a $10\,\text{Gbps}$ link, $B = 0.250\,\text{s} \times 10\,\text{Gbps} = 2.5\,\text{Gbits} = \mathbf{312.5\,\text{MB}}$ of high-speed SRAM per port!

2. **The Modern Stanford Buffer Sizing Rule (Appenzeller et al., 2004)**:
   When a link carries a large number of independent TCP flows ($N$), their packet drops are desynchronized:
   $$B = \frac{\text{RTT} \times C}{\sqrt{N}}$$
   - *Impact*: For $N = 10,000$ TCP flows on a $10\,\text{Gbps}$ link, $\sqrt{N} = 100$. The required buffer drops from $312.5\,\text{MB}$ to just **$3.125\,\text{MB}$**! This allows buffers to be integrated directly onto the router ASIC chip, slashing router cost and power.

### 7.3 Random Early Detection (RED)
- Traditional **Drop-Tail** drops packets only when the buffer is $100\%$ full. This causes **Global Synchronization**: hundreds of TCP flows simultaneously suffer packet loss, halve their windows at the same time, and collapse link utilization.
- **RED (Active Queue Management)** maintains an exponentially smoothed average queue length ($\text{AvgQueue}$).
  - If $\text{AvgQueue} < \text{MinThreshold}$: Admit all packets.
  - If $\text{MinThreshold} \le \text{AvgQueue} \le \text{MaxThreshold}$: Drop or mark incoming packets with a probability that increases linearly with queue depth.
  - If $\text{AvgQueue} > \text{MaxThreshold}$: Drop all incoming packets.
- *Advantage*: Drops packets early, signaling individual TCP senders to throttle before full buffer collapse occurs.

---

## 8. Packet Scheduling Disciplines (Slides 36–42)

Packet scheduling decides which packet in the buffer queue is transmitted next onto the outbound link.

```
1. FIFO (First-In-First-Out):
   [ Pkt 4 ] [ Pkt 3 ] [ Pkt 2 ] [ Pkt 1 ] ===> Transmitted strictly in order of arrival

2. NON-PREEMPTIVE PRIORITY QUEUING:
   High Priority Queue: [ Pkt H2 ] [ Pkt H1 ] ===> Always served first!
   Low Priority Queue:  [ Pkt L2 ] [ Pkt L1 ] ===> Served ONLY when High Queue is empty!

3. ROUND ROBIN:
   Class 1 Queue: [ C1-2 ] [ C1-1 ] --\
   Class 2 Queue: [ C2-2 ] [ C2-1 ] ----> Cycles: C1-1 -> C2-1 -> C1-2 -> C2-2
```

### 8.1 Detailed Scheduling Mechanisms

1. **FIFO with Drop-Tail (Slide 37)**:
   Packets are transmitted strictly in the order they arrived. Zero prioritization.
2. **Priority Queuing (Slide 38–39)**:
   - Packets are sorted into priority classes (e.g., VoIP = High, File Transfer = Low).
   - High-priority queue is always served first.
   - **Non-Preemptive**: If transmission of a low-priority packet has already begun, it is allowed to complete even if a high-priority packet arrives.
   - *Risk*: **Starvation** of low-priority queues if high-priority traffic is sustained.
3. **Round Robin Queuing (Slide 40)**:
   - Packets are classified into multiple service classes.
   - The scheduler cycles through the classes in order: Class 1 $\to$ Class 2 $\to$ Class 3, transmitting one packet from each non-empty queue per round. Prevents starvation.
4. **Weighted Fair Queuing (WFQ - Slide 41–42)**:
   - Generalized Round Robin where each class $i$ is assigned a mathematical weight $w_i$.
   - In any interval where all classes have packets, Class $i$ is guaranteed to receive a fraction of the link bandwidth equal to:
     $$\text{Guaranteed Bandwidth Fraction} = \frac{w_i}{\sum_{j} w_j}$$
   - **Ideal QoS Isolation**: Provides bandwidth fairness while preventing abusive flows from starving other classes!

---

## 9. High-Yield Open-Book Exam Traps & Examiner Tricks

1. **The HoL Blocking Architecture Trap**:
   - *Question*: *"Does Head-of-Line (HoL) blocking occur at router output ports?"*
   - *Fact*: **NO!** HoL blocking occurs strictly at **input ports** when packets destined for different output ports are queued behind a blocked packet. Output ports suffer from queuing delay, but not HoL blocking.
2. **The Non-Preemptive Priority Misconception**:
   - *Question*: *"A high-priority packet arrives while a 1,500-byte low-priority packet is 10% into transmission on a 1 Gbps link. Does the router interrupt the low-priority packet?"*
   - *Fact*: **No**. Non-preemptive scheduling allows the current packet to finish transmission completely before switching to the high-priority queue.
3. **The Buffer Sizing $\sqrt{N}$ Scaling Trap**:
   - *Trap*: Applying the traditional $B = \text{RTT} \cdot C$ formula to an Internet core router carrying tens of thousands of flows.
   - *Fact*: Modern core routers carrying large $N$ flows must be sized using the Stanford formula $B = \text{RTT} \cdot C / \sqrt{N}$ to avoid over-buffering and bufferbloat!

---

## 10. Solved High-Yield Numerical Exam Problems

### Problem 1: Longest Prefix Matching Forwarding Lookup
**Problem Statement**:
A router has the following CIDR forwarding table:

| Prefix | Next Hop Link Interface |
| :--- | :---: |
| `128.96.34.0/23` | Interface 0 |
| `128.96.34.128/25` | Interface 1 |
| `128.96.35.0/24` | Interface 2 |
| `128.96.32.0/20` | Interface 3 |
| `0.0.0.0/0` (Default) | Interface 4 |

Determine the forwarding interface for packets with the following destination addresses:
1. Destination A: `128.96.34.135`
2. Destination B: `128.96.34.60`
3. Destination C: `128.96.35.40`
4. Destination D: `128.96.40.1`

**Step-by-Step Solution**:

Convert prefixes and addresses to binary for the critical 3rd and 4th octets ($128.96$ matches all):
- `/23`: `00100010 0*******` (covers `34.0` to `35.255` with 0 in bit 24) $\to$ `34.0 - 35.255` (first 23 bits: `34.0 - 35.255`? Wait: `34 = 00100010_2`, `35 = 00100011_2`. First 23 bits fix `00100010` and `00100011`? Binary `34` is `00100010`. In /23, the 23rd bit is bit 7 of the 3rd octet, which is `0` for 34 and `1` for 35! So `128.96.34.0/23` covers `128.96.34.0` through `128.96.35.255`).
- `/25`: `34.128/25` $\to$ `128.96.34.128` through `128.96.34.255`.
- `/24`: `35.0/24` $\to$ `128.96.35.0` through `128.96.35.255`.
- `/20`: `32.0/20` $\to$ `128.96.32.0` through `128.96.47.255`.

1. **Destination A: `128.96.34.135`**:
   - Matches `/20` (Interface 3).
   - Matches `/23` (Interface 0).
   - Matches `/25` (Interface 1: $135 \ge 128$).
   - Longest matching prefix is **/25** $\implies$ **Interface 1**.

2. **Destination B: `128.96.34.60`**:
   - Matches `/20` (Interface 3).
   - Matches `/23` (Interface 0: $60 < 128$, falls inside `34.0/23`).
   - Does NOT match `/25` ($60 < 128$).
   - Longest matching prefix is **/23** $\implies$ **Interface 0**.

3. **Destination C: `128.96.35.40`**:
   - Matches `/20` (Interface 3).
   - Matches `/23` (Interface 0).
   - Matches `/24` (Interface 2: 3rd octet is exactly 35).
   - Longest matching prefix is **/24** $\implies$ **Interface 2**.

4. **Destination D: `128.96.40.1`**:
   - 3rd octet is 40. Matches `/20` (range 32 to 47).
   - Does NOT match `/23`, `/25`, or `/24`.
   - Longest matching prefix is **/20** $\implies$ **Interface 3**.

---

### Problem 2: Weighted Fair Queuing (WFQ) Bandwidth Allocation
**Problem Statement**:
A router output link has a transmission capacity of $R = 100\,\text{Mbps}$.
The router implements Weighted Fair Queuing (WFQ) with three active traffic classes:
- Class 1 (Video Conferencing): Weight $w_1 = 4$
- Class 2 (Web Traffic): Weight $w_2 = 3$
- Class 3 (Background FTP): Weight $w_3 = 1$
1. If all three classes have a large backlog of queued packets, calculate the guaranteed transmission rate allocated to each class.
2. If Class 1 is idle (no packets queued), how is the $100\,\text{Mbps}$ link bandwidth dynamically shared between Class 2 and Class 3?

**Step-by-Step Solution**:

1. **All Three Classes Backlogged**:
   - Total weight: $\sum w_j = w_1 + w_2 + w_3 = 4 + 3 + 1 = 8$.
   - Bandwidth allocated to Class 1:
     $$R_1 = \frac{w_1}{\sum w_j} \times R = \frac{4}{8} \times 100\,\text{Mbps} = \mathbf{50\,\text{Mbps}}$$
   - Bandwidth allocated to Class 2:
     $$R_2 = \frac{w_2}{\sum w_j} \times R = \frac{3}{8} \times 100\,\text{Mbps} = \mathbf{37.5\,\text{Mbps}}$$
   - Bandwidth allocated to Class 3:
     $$R_3 = \frac{w_3}{\sum w_j} \times R = \frac{1}{8} \times 100\,\text{Mbps} = \mathbf{12.5\,\text{Mbps}}$$

2. **Class 1 is Idle**:
   - Active weight sum: $w_2 + w_3 = 3 + 1 = 4$.
   - New rate for Class 2:
     $$R'_2 = \frac{3}{4} \times 100\,\text{Mbps} = \mathbf{75\,\text{Mbps}}$$
   - New rate for Class 3:
     $$R'_3 = \frac{1}{4} \times 100\,\text{Mbps} = \mathbf{25\,\text{Mbps}}$$
   - *Takeaway*: WFQ provides **work-conserving fairness**; unused bandwidth from idle classes is distributed proportionally among active classes!

---

## 11. Ultra-Fast Exam Revision Checklist
- [ ] Data Plane: Local hardware forwarding in ASICs/TCAM ($O(1)$ nanoseconds).
- [ ] Control Plane: Global software path computation (OSPF, BGP, SDN) in milliseconds.
- [ ] Longest Prefix Matching (LPM): Router forwards packet to interface matching longest binary prefix.
- [ ] Switching Fabrics: Memory (CPU double bus copy), Bus (shared backplane contention), Crossbar ($N \times N$ non-blocking parallel).
- [ ] Head-of-Line (HoL) Blocking: Occurs at input ports; limits throughput to $58.6\%$ unless Virtual Output Queuing (VOQ) is used.
- [ ] Buffer Sizing: Traditional $B = \text{RTT} \cdot C$; Stanford rule for $N$ flows is $B = \text{RTT} \cdot C / \sqrt{N}$.
- [ ] RED (Random Early Detection): Probabilistic early packet dropping avoids global TCP synchronization.
- [ ] Scheduling: FIFO (strict arrival order), Priority (high queue always served first), Round Robin (equal cycle), WFQ (weighted fair share).
- [ ] WFQ Guaranteed Bandwidth: $R_i = R \times \frac{w_i}{\sum w_j}$.
