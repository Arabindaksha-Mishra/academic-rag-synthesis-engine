# Computer Networks (BSDCBZC481)
# Session 12: Link Layer — Error Detection (CRC), Multiple Access (CSMA/CD), MAC & Switches
### Exhaustive Slide-by-Slide Academic Exam Revision Manual & Problem Solving Guide

---

## 1. Session Context & Pedagogical Scope
- **Course Code & Title**: BSDCBZC481 — Computer Networks
- **Instructor**: Dr. K. Kalaiselvi (BITS Pilani)
- **Primary Textbooks**:
  - J.F. Kurose & K.W. Ross, *Computer Networking: A Top-Down Approach*, 5th/6th Edition, Chapter 5 (T1)
  - B.A. Forouzan, *Data Communications and Networking*, 4th Edition, Chapters 10, 11, 12, & 14 (T2)
- **Lecture Slide Mapping**: CS12: Link Layer — Slides 1 to 49 (Complete Coverage)
- **Core Syllabus Covered**:
  1. Link Layer Services: Framing, Medium Access Control (MAC), Flow Control & Error Handling
  2. Error Detection Paradigms: 2D Parity Checks & Single-Bit Error Correction
  3. Cyclic Redundancy Check (CRC / Polynomial Codes): Modulo-2 Arithmetic & Hardware XOR Division
  4. Multiple Access Protocols Taxonomy: Channel Partitioning (TDMA/FDMA/CDMA) vs. Taking-Turns
  5. Random Access Evolution: Pure ALOHA ($18.4\%$), Slotted ALOHA ($36.8\%$), CSMA & CSMA/CD
  6. Binary Exponential Backoff Mathematics & The 64-Byte Minimum Ethernet Frame Limit
  7. Link-Layer Addressing: 48-Bit MAC Addresses vs. 32-Bit IP Addresses
  8. Address Resolution Protocol (ARP, RFC 826): Broadcast Query, Unicast Reply & Off-Subnet Routing
  9. Ethernet (IEEE 802.3): Frame Format, Preamble Synchronization & Minimum Payload Padding
  10. Link-Layer Switches: Self-Learning Switch Tables, Selective Forwarding & Flood Prevention
  11. High-Yield Open-Book Exam Traps, Rigorous Numerical Problems & Fast Revision Checklist

---

## 2. Link Layer Fundamentals & Error Detection (Slides 3–12)

While the network layer transfers packets end-to-end between source and destination hosts, the data link layer is responsible for transporting frames between **immediately adjacent network nodes** across a single physical communication link.

### 2.1 Two-Dimensional Parity Checks (Slide 7)
- Data bits are arranged in a matrix of $i$ rows and $j$ columns.
- Parity is computed for each row and for each column:

```
    d1,1  d1,2  ...  d1,j  |  Row Parity 1
    d2,1  d2,2  ...  d2,j  |  Row Parity 2
     :     :          :    |      :
    di,1  di,2  ...  di,j  |  Row Parity i
   ------------------------+---------------
    Col1  Col2  ...  Colj  |  Parity Bit
```

- **Error Detection & Correction**: A single bit flip creates a parity violation in exactly **one row** and **one column**. The intersection of the faulty row and faulty column uniquely pinpoints the corrupted bit, allowing the receiver to **detect and automatically correct** the bit without retransmission (**Forward Error Correction - FEC**)!
- Can detect any combination of **2 bit errors** anywhere in the block.

---

## 3. Cyclic Redundancy Check (CRC / Polynomial Codes) (Slides 8–12)

CRC is an extremely powerful, hardware-implemented error-detection technique based on polynomial modulo-2 arithmetic.

```
+-------------------------------------------------------------------------+
|                              CRC ARITHMETIC                             |
|                                                                         |
| Sender Data (d bits):             D                                     |
| Generator Polynomial (r+1 bits):  G  (Most significant bit must be 1)   |
| Transmitted Frame (d+r bits):     < D, R >                              |
|                                                                         |
| Mathematical Goal:                                                      |
| Choose r CRC bits (R) such that < D, R > is EXACTLY divisible by G     |
| using Modulo-2 Arithmetic:                                              |
|                                                                         |
|              ( D * 2^r ) XOR R = n * G                                  |
|              R = remainder of [ ( D * 2^r ) / G ]                       |
+-------------------------------------------------------------------------+
```

### 3.1 The Rules of Modulo-2 Arithmetic
- Modulo-2 addition and subtraction are **identical** and equivalent to the bitwise **XOR operation**:
  $$0 \oplus 0 = 0, \quad 0 \oplus 1 = 1, \quad 1 \oplus 0 = 1, \quad 1 \oplus 1 = 0$$
- **There are zero carries in addition and zero borrows in subtraction!**

### 3.2 Step-by-Step CRC Generation Algorithm
1. Let the generator polynomial $G$ contain $r + 1$ bits.
2. Append $r$ zeros to the right of the data string $D$, forming $D \cdot 2^r$.
3. Divide $D \cdot 2^r$ by $G$ using modulo-2 long division.
4. The resulting $r$-bit remainder is $R$.
5. The transmitted frame is formed by concatenating $D$ and $R$: $\text{Frame} = \langle D, R \rangle$.

### 3.3 Receiver Verification Algorithm
1. The receiver receives the frame $\langle D, R \rangle$.
2. It divides $\langle D, R \rangle$ by the identical generator $G$ using modulo-2 long division.
3. **If the remainder is non-zero**: A bit error occurred $\implies$ Frame is discarded.
4. **If the remainder is all zeros**: The frame is accepted as error-free.

---

## 4. Multiple Access Protocols Taxonomy (Slides 13–27)

When multiple nodes share a single broadcast link (e.g., traditional coaxial Ethernet, wireless Wi-Fi, satellite channels), simultaneous transmissions collide, garbling all signals. Multiple Access Control (MAC) protocols coordinate transmission.

```
                            MULTIPLE ACCESS PROTOCOLS
                                        |
        +-------------------------------+-------------------------------+
        |                               |                               |
CHANNEL PARTITIONING             RANDOM ACCESS                    TAKING TURNS
- TDMA (Time slots)              - Pure ALOHA (18.4%)             - Polling (Master-Slave)
- FDMA (Frequency bands)         - Slotted ALOHA (36.8%)          - Token Ring Passing
- CDMA (Orthogonal codes)        - CSMA & CSMA/CD (Ethernet)
```

### 4.1 Channel Partitioning vs. Random Access
- **Channel Partitioning (TDMA/FDMA)**: Divides channel into fixed slices. Eliminates collisions completely, but wastes bandwidth when traffic is bursty (a single active node is throttled to $R/N$ even when the remaining $N-1$ channels are completely idle).
- **Random Access Protocols**: Nodes transmit at the full link rate $R$. Collisions can occur; protocols specify how to detect collisions and recover.

---

## 5. Evolution of Random Access: ALOHA to CSMA/CD (Slides 16–25)

### 5.1 Pure ALOHA vs. Slotted ALOHA
1. **Pure ALOHA (Slide 17)**:
   - When a node has data, it transmits immediately.
   - A frame transmitted at $t_0$ collides with any frame sent in the interval $[t_0 - T_{\text{frame}}, t_0 + T_{\text{frame}}]$.
   - Vulnerable period $= 2 \times T_{\text{frame}}$.
   - Maximum Channel Efficiency $= \frac{1}{2e} \approx \mathbf{18.4\%}$.
2. **Slotted ALOHA (Slide 18–19)**:
   - Time is divided into discrete slots of length $T_{\text{frame}}$. Nodes transmit only at slot boundaries.
   - Vulnerable period cut in half: $= 1 \times T_{\text{frame}}$.
   - Maximum Channel Efficiency $= \frac{1}{e} \approx \mathbf{36.8\%}$.

### 5.2 Carrier Sense Multiple Access (CSMA) (Slide 20)
- **Principle**: *"Listen before speaking"*.
- A node listens to the channel before transmitting. If the channel is sensed busy, transmission is deferred; if idle, the node transmits.
- **Why Collisions Still Occur in CSMA**: **Propagation delay**! If Node A transmits at $t = 0$, Node B at the opposite end of the cable cannot hear A's signal until the electromagnetic wave propagates across distance $d$ ($t = d/s$). If B senses the link at $t = 0.5 \cdot d_{\text{prop}}$, it senses the channel idle and transmits, causing a collision!

### 5.3 CSMA with Collision Detection (CSMA/CD, IEEE 802.3) (Slides 21–25)
- **Principle**: *"Listen while transmitting"*.
- If a transmitting node detects an interfering signal on the wire:
  1. **Aborts transmission immediately** (avoids wasting time transmitting the rest of a doomed packet).
  2. Transmits a **48-bit Jam Signal** to ensure all other transmitting nodes detect the collision.
  3. Enters **Binary Exponential Backoff**.

```
Node A ---------------------------------------------------------------- Node B
  | (Transmits at t=0)                                                    |
  |=========================>                                             |
  |                        \                                              |
  |                         \ (Collision occurs at midpoint!)             |
  |                          X <==========================================| (Transmits at t=prop-eps)
  |                         /                                             |
  |<=======================/                                              |
  | (Detects collision at t=2*prop!)                                      |
  | Transmits 48-bit Jam Signal                                           |
```

### 5.4 Binary Exponential Backoff Algorithm (Slide 23)
- After the $m^{\text{th}}$ collision for a frame:
  - The node chooses an integer $K$ uniformly at random from the set:
    $$K \in \{0, 1, 2, \dots, 2^m - 1\}$$
  - The backoff exponent $m$ is capped at $10$ ($\max K = 2^{10} - 1 = 1,023$).
  - The node waits $K \times 512\,\text{bit times}$ (Slot Time $= 51.2\,\mu\text{s}$ on $10\,\text{Mbps}$ Ethernet) before re-sensing the link.
  - After $16$ consecutive collisions, the frame is aborted and dropped.

### 5.5 The 64-Byte Minimum Ethernet Frame Constraint
To guarantee that a sender detects a collision before it finishes transmitting the frame, the packet transmission time must be at least twice the maximum propagation delay:
$$d_{\text{trans}} \ge 2 \times d_{\text{prop, max}}$$
$$\frac{L_{\min}}{R} \ge 2 \times \frac{d_{\max}}{s} \implies L_{\min} \ge 2 \times \frac{d_{\max} \cdot R}{s}$$
On classical $10\,\text{Mbps}$ coaxial Ethernet spanning $2,500\,\text{m}$ with 4 repeaters, this mandates a **minimum frame length of 64 bytes (512 bits)**. If payload is $< 46\,\text{bytes}$, the link layer must add padding bytes!

---

## 6. Link-Layer Addressing & ARP (RFC 826) (Slides 28–36)

### 6.1 MAC Addresses vs. IP Addresses (Slides 28–29)
- **MAC Address (48 bits / 6 bytes)**:
  - Expressed as 6 hexadecimal octets: `1A-2F-BB-45-9C-E2`.
  - Burned into NIC hardware ROM by the manufacturer (IEEE manages the first 24 bits as the OUI - Organizationally Unique Identifier).
  - **Flat topology**: A MAC address does not change when moving a laptop from New York to Tokyo (portable identifier, like a Social Security Number).
- **IP Address (32 bits)**:
  - **Hierarchical topology**: Defines network attachment point; changes dynamically when moving across subnets (like a postal address).

### 6.2 Address Resolution Protocol (ARP) (Slides 30–33)
ARP dynamically maps a destination IPv4 address to its physical MAC address on the same local subnet.

```
HOST A (192.168.1.1, MAC: 00-AA...)             HOST B (192.168.1.2, MAC: 00-BB...)
       |                                                               |
       |--- ARP REQUEST (Broadcast Frame) ---------------------------->|
       |    Dst MAC: FF-FF-FF-FF-FF-FF, Target IP: 192.168.1.2         |
       |    (Processed by ALL nodes on local LAN segment)              |
       |                                                               |
       |<-- ARP REPLY (Unicast Frame) ---------------------------------|
       |    Src MAC: 00-BB-22-33-44-55, Src IP: 192.168.1.2           |
       |    Dst MAC: 00-AA-11-22-33-44                                 |
       v                                                               v
(Host A caches entry in local ARP Table with TTL = 20 minutes)
```

### 6.3 Routing to Another Subnet (Crucial Exam Concept! Slides 34–36)
When Host A (`192.168.1.10`) sends an IP datagram to Host B on a **different subnet** (`10.0.0.5`):
1. Host A determines that Host B is off-subnet using its subnet mask.
2. Host A addresses the IP datagram to destination `10.0.0.5`.
3. **The Link-Layer Action**: Host A encapsulates the datagram in an Ethernet frame with **Destination MAC set to the First-Hop Default Gateway Router's MAC address**, NOT Host B's MAC address!
4. The router receives the frame, extracts the IP packet, looks up the next hop in its routing table, and re-encapsulates the packet into a new frame with Destination MAC set to Host B's NIC!

---

## 7. Ethernet Architecture & Link-Layer Switches (Slides 37–49)

### 7.1 IEEE 802.3 Ethernet Frame Format (Slide 38)

```
+---------------+---------------+---------------+-------+---------------+---------------+
| PREAMBLE (8B) | DEST MAC (6B) | SRC MAC (6B)  |TYPE(2)| PAYLOAD (46-  | CRC-32 (4B)   |
|               |               |               |       |  1500 Bytes)  |               |
+---------------+---------------+---------------+-------+---------------+---------------+
```
- **Preamble (8 bytes)**: 7 bytes of alternating `10101010` followed by 1 byte Start Frame Delimiter (`10101011`). Synchronizes receiver clock circuitry.
- **Type (2 bytes)**: Multiplexing tag identifying the upper layer protocol (`0x0800` for IPv4, `0x0806` for ARP).
- **CRC-32 (4 bytes)**: 32-bit cyclic redundancy check.

### 7.2 Link-Layer Switches & Self-Learning (Slides 41–46)
A switch is an active, multi-port Layer 2 device that isolates collision domains, providing dedicated full-duplex bandwidth to every connected host.

```
+-------------------------------------------------------------------------+
|                       SWITCH SELF-LEARNING ALGORITHM                    |
|                                                                         |
| When a frame arrives on Interface x with Source MAC S and Dest MAC D:   |
|                                                                         |
| 1. RECORD LEARNING ENTRY:                                               |
|    Switch table stores: (MAC Address S, Port Interface x, Current Time) |
|                                                                         |
| 2. FORWARDING DECISION:                                                 |
|    If Dest MAC D is in switch table for Port y:                         |
|        If y == x:                                                       |
|            FILTER (Drop frame; destination is already on same segment)  |
|        Else:                                                            |
|            FORWARD frame out strictly on Interface y                    |
|    Else:                                                                |
|        FLOOD frame out ALL interfaces EXCEPT incoming Interface x!      |
+-------------------------------------------------------------------------+
```

---

## 8. Master Device Comparison Matrix

| Technical Feature | Hub (Repeater) | Link-Layer Switch | Network Router |
| :--- | :--- | :--- | :--- |
| **Operating Layer** | **Layer 1 (Physical)** | **Layer 2 (Data Link)** | **Layer 3 (Network)** |
| **Traffic Separation** | Single shared collision domain | **Isolates collision domains** (each port dedicated) | **Isolates broadcast domains** and collision domains |
| **Addressing Used** | None (repeats raw electrical bits) | **48-bit MAC Addresses** | **32-bit/128-bit IP Addresses**|
| **Forwarding Table** | None | Switch Table (Self-learning) | Forwarding Table (OSPF/BGP) |
| **Throughput Capacity**| Degrades with collisions | High (simultaneous switching) | High (wire-speed ASICs) |

---

## 9. High-Yield Open-Book Exam Traps & Examiner Tricks

1. **The Modulo-2 Subtraction Trap**:
   - *Trap*: Performing ordinary borrowing during CRC division.
   - *Fact*: Modulo-2 subtraction has **zero borrows**; it is identical to bitwise XOR!
2. **The Off-Subnet ARP Destination Trap**:
   - *Question*: *"Host A wants to ping Host B across the Internet. Does Host A broadcast an ARP query for Host B's MAC address?"*
   - *Fact*: **NO!** ARP broadcasts are blocked by routers. Host A broadcasts an ARP query for the **MAC address of its local default gateway router**.
3. **The Switch Collision Domain Myth**:
   - *Question*: *"Do hosts connected to a modern Ethernet switch run CSMA/CD?"*
   - *Fact*: **No!** Modern switches provide dedicated full-duplex point-to-point links (separate Tx and Rx pairs). Collisions are physically impossible, so CSMA/CD is completely disabled!

---

## 10. Solved High-Yield Numerical Exam Problems

### Problem 1: Cyclic Redundancy Check (CRC) Calculation & Verification
**Problem Statement**:
A link-layer sender wants to transmit a 6-bit data word $D = 101001_2$.
The sender and receiver agree on the generator polynomial $G(x) = x^3 + x + 1$, which corresponds to the 4-bit bit pattern $G = 1011_2$.
1. Compute the exact 3-bit CRC code ($R$) using modulo-2 long division.
2. Formulate the final 9-bit transmitted frame.
3. Demonstrate that the receiver detects no errors if the frame arrives uncorrupted.

**Step-by-Step Solution**:

1. **Prepare Dividend**:
   - Generator $G = 1011$ has $r + 1 = 4$ bits $\implies r = 3$ bits.
   - Append $r = 3$ zeros to $D$:
     $$D \cdot 2^3 = 101001000_2$$

2. **Perform Modulo-2 Long Division**:
   Divide $101001000$ by $1011$:
   ```text
                100111  (Quotient)
         -------------
   1011 ) 101001000
          1011
          ----
          000101000  -> 001001000 (drop down bits)
            1011
            ----
            0011000
              1011
              ----
              01110
               1011
               ----
               0101  (Last 3 bits are 101)
   ```
   Detailed XOR subtraction steps:
   - $1010 \oplus 1011 = 0001$. Bring down 0 $\to 0010$. Bring down 1 $\to 00100$.
   - Bring down until leading 1: $1001 \oplus 1011 = 0010$.
   - Bring down 0 $\to 0100$. Bring down 0 $\to 1000$.
   - $1000 \oplus 1011 = 0011$. Bring down 0 $\to 0110$.
   - Let's do bit-by-bit aligned arithmetic carefully:
     - Dividend: `1 0 1 0 0 1 0 0 0`
     - Step 1: `1010` XOR `1011` = `0001`. Bring down `0` $\to$ `0010`.
     - Step 2: `0010` cannot divide by `1011` (leading bit 0). Bring down `1` $\to$ `0101`.
     - Step 3: `0101` cannot divide by `1011`. Bring down `0` $\to$ `1010`.
     - Step 4: `1010` XOR `1011` = `0001`. Bring down `0` $\to$ `0010`.
     - Step 5: `0010` cannot divide. Bring down `0` $\to$ `0100`.
     - Final remainder $= \mathbf{011}$?
     Let's verify by multiplying:
     Let $D \cdot 2^3 = 101001000_2 = 328_{10}$.
     $G = 1011_2$.
     Let's divide manually:
     `101001000`
     `1011` (over bits 1-4)
     `-----`
     `000101000` -> `101000`
     ` 1011`
     ` ----`
     ` 000100` -> `100`
     Wait! Let's trace column by column:
     `101001000`
     XOR `101100000`
     `----------`
     `000101000` = `101000`
     XOR ` 101100`
     `----------`
     ` 000100` = `100` (length 3).
     Remainder $R = \mathbf{100}_2$!
   - Verify:
     Frame $= D \cdot 2^3 \oplus R = 101001000 \oplus 100 = \mathbf{101001100}$.
     Divide $101001100$ by $1011$:
     $101001100 \oplus 101100000 = 000101100$.
     $000101100 \oplus 000101100 = \mathbf{000000000}$.
     Remainder is **000**! Perfectly verified.
   - Therefore, Remainder $R = \mathbf{100}_2$.
   - **Transmitted Frame**: $\mathbf{101001100}_2$.

---

### Problem 2: Binary Exponential Backoff Collision Probability
**Problem Statement**:
Two hosts, A and B, simultaneously transmit on a shared $10\,\text{Mbps}$ CSMA/CD Ethernet bus.
A collision occurs. Both hosts enter Binary Exponential Backoff.
1. What is the set of possible delay values (in bit times) each host can choose after this first collision ($m = 1$)?
2. What is the probability that they collide again on their very next attempt?
3. If they collide a second time ($m = 2$), what is the probability of a third consecutive collision?

**Step-by-Step Solution**:

1. **First Collision ($m = 1$)**:
   - Random backoff integer set:
     $$K \in \{0, 1, \dots, 2^1 - 1\} = \{0, 1\}$$
   - Possible waiting times:
     - $K = 0 \implies 0 \times 512 = \mathbf{0\text{ bit times}}$
     - $K = 1 \implies 1 \times 512 = \mathbf{512\text{ bit times}} \quad (51.2\,\mu\text{s})$

2. **Probability of Immediate Second Collision**:
   - Host A chooses $K_A \in \{0, 1\}$ with probability $1/2$ each.
   - Host B chooses $K_B \in \{0, 1\}$ with probability $1/2$ each.
   - A collision occurs if and only if both choose the **exact same value** ($K_A = K_B$):
     $$P(K_A = K_B) = P(0, 0) + P(1, 1) = \left(\frac{1}{2} \times \frac{1}{2}\right) + \left(\frac{1}{2} \times \frac{1}{2}\right) = \frac{1}{4} + \frac{1}{4} = \frac{2}{4} = \mathbf{0.50} \quad (\mathbf{50\%})$$

3. **Probability of Third Collision ($m = 2$)**:
   - Random backoff integer set:
     $$K \in \{0, 1, 2, 3\}$$
   - Total possible outcome pairs: $4 \times 4 = 16$.
   - Collision occurs if $K_A = K_B \in \{(0,0), (1,1), (2,2), (3,3)\}$ ($4$ collision outcomes):
     $$P(\text{Collision}) = \frac{4}{16} = \frac{1}{4} = \mathbf{0.25} \quad (\mathbf{25\%})$$

---

## 11. Ultra-Fast Exam Revision Checklist
- [ ] Link layer delivers frames across a single physical hop; NIC implements physical and link layers.
- [ ] 2D Parity can detect and correct single-bit errors (FEC), and detect 2-bit errors.
- [ ] CRC uses modulo-2 long division (XOR); transmitted frame is $\langle D, R \rangle$; remainder is 0 if error-free.
- [ ] Slotted ALOHA max efficiency is $1/e \approx 36.8\%$; Pure ALOHA is $1/(2e) \approx 18.4\%$.
- [ ] CSMA/CD: Listen before transmitting; listen while transmitting; abort and send 48-bit Jam Signal on collision.
- [ ] Binary Exponential Backoff: Chooses $K \in \{0, 1, \dots, 2^m - 1\}$; waits $K \times 512$ bit times.
- [ ] Minimum Ethernet frame is 64 bytes (mandated by $d_{\text{trans}} \ge 2 d_{\text{prop}}$).
- [ ] MAC addresses are 48 bits, flat, and hardware-burned; IP addresses are 32 bits and hierarchical.
- [ ] ARP translates IP to MAC via broadcast query (`FF:FF:FF:FF:FF:FF`) and unicast response.
- [ ] Switches self-learn MAC tables: match $\implies$ forward/filter; unknown $\implies$ flood.
