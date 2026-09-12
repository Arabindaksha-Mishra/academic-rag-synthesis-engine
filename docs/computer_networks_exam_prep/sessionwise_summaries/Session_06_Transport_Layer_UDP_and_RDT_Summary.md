# Computer Networks (BSDCBZC481)
# Session 06: Transport Layer Fundamentals — UDP & Reliable Data Transfer Principles
### Exhaustive Slide-by-Slide Academic Exam Revision Manual & Problem Solving Guide

---

## 1. Session Context & Pedagogical Scope
- **Course Code & Title**: BSDCBZC481 — Computer Networks
- **Instructor**: Dr. K. Kalaiselvi (BITS Pilani)
- **Primary Textbooks**:
  - J.F. Kurose & K.W. Ross, *Computer Networking: A Top-Down Approach*, 5th/6th Edition, Chapter 3 (T1)
  - B.A. Forouzan, *Data Communications and Networking*, 4th Edition, Chapters 23 & 24 (T2)
- **Lecture Slide Mapping**: CS6: Transport Layer — Slides 1 to 40 (Complete Coverage)
- **Core Syllabus Covered**:
  1. Transport Layer Service Abstraction: Process-to-Process vs. Host-to-Host Communication
  2. Multiplexing & Demultiplexing Architecture: 2-Tuple (UDP) vs. 4-Tuple (TCP) Demux
  3. User Datagram Protocol (UDP, RFC 768): Design Philosophy, Header Fields & Zero-State Benefits
  4. The Internet Checksum: One's Complement Arithmetic, End-Around Carry & The End-to-End Argument
  5. Incremental Synthesis of Reliable Data Transfer (RDT):
     - `rdt 1.0`: Reliable Transfer over a Flawless Channel
     - `rdt 2.0`: Error Detection, ACK/NAK & The Fatal Ambiguity Flaw
     - `rdt 2.1`: Resolving Ambiguity via 1-Bit Sequence Numbers (Sender/Receiver FSMs)
     - `rdt 2.2`: NAK-Free Protocol via Cumulative Duplicate ACKs
     - `rdt 3.0`: Countdown Timers, Retransmissions & Alternating-Bit Protocol
  6. The Stop-and-Wait Performance Bottleneck: Utilization Math ($U_{\text{sender}}$) on High-Speed Links
  7. High-Yield Open-Book Exam Traps, Rigorous Numerical Problems & Fast Revision Checklist

---

## 2. Transport Layer Fundamentals & Multiplexing Architecture (Slides 3–11)

### 2.1 Process-to-Process vs. Host-to-Host Communication
- **Network Layer (IP)**: Provides logical communication between **hosts** (end systems). Delivers datagrams to the network interface card of the destination machine.
- **Transport Layer (TCP/UDP)**: Provides logical communication between **processes** running on different hosts. Extends host-to-host delivery to **process-to-process communication** through port numbers.

#### The Kurose & Ross Household Mail Analogy:
- **Houses**: Hosts.
- **Cousins (Kids)**: Processes living inside hosts.
- **Ann & Bill (Household Mail Collectors)**: Transport Layer protocols.
- **Postal Service Carrier**: Network Layer (IP).
Ann and Bill collect outgoing letters from individual kids and place them in the physical mailbox (multiplexing), and sort incoming letters and distribute them directly to the intended kid (demultiplexing).

```
+-------------------------------------------------------------+
| HOST A                                                      |
|   [ Web Browser: Port 52140 ]    [ SSH Client: Port 53211 ]  |
|                 \                      /                    |
|                  v                    v                     |
|           +----------------------------------+              |
|           | TRANSPORT LAYER (Multiplexing)   |              |
|           +----------------------------------+              |
|                            |                                |
|                            v                                |
|           +----------------------------------+              |
|           | NETWORK LAYER (IP: 192.168.1.50) |              |
+-----------+----------------------------------+--------------+
                             |
                             v Internet
                             |
+-------------------------------------------------------------+
| HOST B (Web Server: 128.119.40.186)                         |
|           +----------------------------------+              |
|           | NETWORK LAYER (IP Delivery)      |              |
|           +----------------------------------+              |
|                            |                                |
|                            v                                |
|           +----------------------------------+              |
|           | TRANSPORT LAYER (Demultiplexing) |              |
|           +----------------------------------+              |
|                 /                      \                    |
|                v                        v                   |
|   [ Apache HTTP: Port 80 ]       [ OpenSSH: Port 22 ]       |
+-------------------------------------------------------------+
```

### 2.2 Demultiplexing: Connectionless (UDP) vs. Connection-Oriented (TCP)
A host uses port numbers (16-bit unsigned integers: $0$ to $65,535$) to direct transport segments to the proper socket:
1. **Connectionless Demux (UDP)**:
   - A UDP socket is fully identified by a **2-tuple**:
     $$\text{UDP Socket ID} = (\text{Destination IP Address}, \text{Destination Port Number})$$
   - If two different hosts transmit UDP datagrams to IP `128.119.40.186` on port `9876`, both packets are steered into the **exact same server socket**, regardless of their source IP or source port!
2. **Connection-Oriented Demux (TCP)**:
   - A TCP socket is fully identified by a **4-tuple**:
     $$\text{TCP Socket ID} = (\text{Source IP}, \text{Source Port}, \text{Dest IP}, \text{Dest Port})$$
   - Two arriving TCP segments with identical destination IP and destination port, but differing source IPs or source ports, are steered to **two completely distinct connection sockets**!

---

## 3. User Datagram Protocol (UDP, RFC 768) Deep Dive (Slides 12–15)

UDP is a minimal, lightweight transport protocol that adds almost nothing beyond multiplexing/demultiplexing and basic error checking to IP.

### 3.1 Why Do Applications Choose UDP over TCP?
1. **No Connection Establishment Latency (0-RTT)**: UDP sends data immediately without waiting for a 3-way handshake (crucial for DNS queries).
2. **Zero Connection State**: TCP maintains buffers, congestion windows, sequence numbers, and timers in kernel memory. A UDP server maintains zero connection state and can handle vastly more active clients.
3. **Small Header Overhead**: UDP header is strictly **8 bytes**, compared to TCP's minimum **20 bytes** ($60\%$ header overhead reduction).
4. **Unregulated Sending Rate**: UDP transmits data as fast as the application generates it, unconstrained by TCP congestion control backoffs (ideal for real-time video, VoIP).

### 3.2 The 8-Byte UDP Segment Header Structure (Slide 13)

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     SOURCE PORT (16 bits)     |   DESTINATION PORT (16 bits)  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       LENGTH (16 bits)        |       CHECKSUM (16 bits)      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                  APPLICATION PAYLOAD DATA                     |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

- **Source Port (16 bits)**: Port of the sending process; used for return replies.
- **Destination Port (16 bits)**: Port of the receiving process.
- **Length (16 bits)**: Total length of the UDP segment in bytes (**Header + Payload**). Minimum value is 8.
- **Checksum (16 bits)**: Error detection field protecting header, data, and an IP pseudo-header.

---

## 4. The Internet Checksum Algorithm & One's Complement Math (Slides 14–15)

The checksum provides end-to-end detection of bit flips caused by noise in physical media or memory errors in intermediate router buffers.

### 4.1 Checksum Computation at Sender
1. Treat all contents of the segment (plus an IP pseudo-header) as a sequence of **16-bit integers**.
2. Sum all 16-bit integers together.
3. If an addition produces a carry out of the most significant bit (17th bit), **wrap the carry bit around and add it to the least significant bit** (**One's Complement Addition**).
4. Take the **bitwise NOT (one's complement inversion)** of the final 16-bit sum.
5. Store this result in the Checksum field of the UDP header.

### 4.2 Verification at Receiver
1. Add all 16-bit words of the received segment together, **including the Checksum field**, using one's complement addition.
2. If the segment is completely error-free:
   $$\text{Final Sum} = \text{0xFFFF} \quad (\text{all } 1\text{s: } 1111111111111111_2)$$
3. Inverting the sum gives `0x0000`. If any bit in the inverted sum is non-zero, an error has occurred!

```
SENDER ARITHMETIC EXAMPLE:
Word 1:           01100110 01100000
Word 2:         + 01010101 01010101
-----------------------------------
Sum:              10111011 10110101
Word 3:         + 10001111 00001100
-----------------------------------
Sum with carry:  1 01001010 11000001  (Carry out of 16th bit!)
Wrap carry:     +                  1
-----------------------------------
Wrapped Sum:      01001010 11000010
Bitwise NOT:    ~ 01001010 11000010
-----------------------------------
CHECKSUM:         10110101 00111101  (Placed into UDP header)
```

> [!NOTE]
> **Why do we need a Transport Checksum if Link Layer has CRC?**:
> The **End-to-End Principle (Saltzer, Reed, Clark)**: Link-layer CRCs protect frames across individual physical wires. However, when a packet sits inside an intermediate router's RAM buffer waiting in a queue, faulty router memory chips or bus errors can flip bits. Since link-layer checks are stripped inside routers, only an end-to-end transport checksum can detect router memory corruption!

---

## 5. Incremental Synthesis of Reliable Data Transfer (RDT) (Slides 16–30)

Reliable data transfer provides a clean abstraction of an error-free, lossless channel to the application layer on top of an underlying unreliable physical channel (IP).

```
+-------------------------------------------------------------+
|                      APPLICATION LAYER                      |
|          rdt_send()                     deliver_data()      |
+-------------------------------------------------------------+
               |                                ^
               v                                |
+-------------------------------------------------------------+
|              TRANSPORT LAYER (RDT PROTOCOL)                 |
|          udt_send()                     rdt_rcv()           |
+-------------------------------------------------------------+
               |                                ^
               v                                |
+-------------------------------------------------------------+
|              UNRELIABLE NETWORK CHANNEL (IP)                |
+-------------------------------------------------------------+
```

### 5.1 `rdt 1.0`: Completely Reliable Channel (Slide 17)
- **Channel Assumptions**: No bit errors, no lost packets, perfect in-order delivery.
- **FSM Structure**:
  - Sender has 1 state: `Wait for call from above`. Action: `make_pkt(data)`, `udt_send(packet)`.
  - Receiver has 1 state: `Wait for call from below`. Action: `extract(packet, data)`, `deliver_data(data)`.

---

### 5.2 `rdt 2.0`: Channel with Bit Errors (Slides 18–21)
- **Channel Assumptions**: Packets can suffer bit corruption, but **zero packets are lost**.
- **Mechanisms Introduced**:
  1. **Error Detection**: Checksum field added to packets.
  2. **Receiver Feedback**:
     - `ACK` (Positive Acknowledgment): Packet arrived undamaged.
     - `NAK` (Negative Acknowledgment): Packet corrupted; please retransmit.
  3. **Retransmission**: Sender retransmits packet upon receiving a NAK.

> [!WARNING]
> **The Fatal Flaw of `rdt 2.0` (Slide 21)**:
> What happens if the `ACK` or `NAK` packet itself gets corrupted in transit?
> - The sender cannot decipher whether the receiver said ACK or NAK!
> - If sender blindly retransmits on a corrupted response: The receiver receives a **duplicate packet**. If the original packet was delivered OK, retransmitting injects duplicate data into the application stream!
> - **Conclusion**: Stop-and-Wait protocols cannot handle garbled feedback without sequence numbers!

---

### 5.3 `rdt 2.1`: Handling Garbled ACKs/NAKs via Sequence Numbers (Slides 22–24)
- **Solution**: Sender attaches a **1-bit sequence number** (`0` or `1`) to every data packet.
- **Receiver Rule**: If receiver is waiting for packet `0` and receives a duplicate packet `1`, it discards the payload but re-sends `ACK` to allow the sender to advance!
- **State Space**: Sender doubles from 2 to **4 states**; Receiver doubles from 1 to **2 states**.

```
SENDER FSM STATES FOR rdt 2.1:
[ State 1: Wait for call 0 ] --rdt_send(data)--> [ State 2: Wait for ACK/NAK 0 ]
        ^                                                    |
        | notcorrupt && isACK                                | notcorrupt && isACK
        |                                                    v
[ State 4: Wait for ACK/NAK 1 ] <--rdt_send(data)-- [ State 3: Wait for call 1 ]
```

---

### 5.4 `rdt 2.2`: A NAK-Free Protocol (Slides 25–26)
- **Improvement**: Eliminates explicit `NAK` control packets entirely.
- **Mechanism**: The receiver sends an `ACK` containing the **explicit sequence number** of the last correctly received packet:
  - `make_pkt(ACK, 0, checksum)` or `make_pkt(ACK, 1, checksum)`.
- **Implicit NAK**: If the sender is waiting for `ACK 1` but receives `ACK 0` (duplicate ACK), it recognizes that the receiver did NOT receive packet 1 and immediately retransmits packet 1.

---

### 5.5 `rdt 3.0`: Channels with Bit Errors and Packet Loss (Slides 27–30)
- **Channel Assumptions**: Packets may be corrupted **and completely dropped/lost** by the network fabric.
- **New Mechanism**: **Countdown Timer**.
  - Sender starts a countdown timer when transmitting a packet.
  - If ACK does not arrive before the timer expires (`timeout`), sender retransmits the packet.
  - If an ACK was merely delayed, duplicate packets are detected and filtered by the 1-bit sequence number!
- Also known as the **Alternating-Bit Protocol**.

#### The Four Canonical Timing Traces of `rdt 3.0`:
```
(a) Operation with No Loss:
    Sender transmits pkt 0 (starts timer) ===> Receiver gets pkt 0, sends ack 0 ===>
    Sender receives ack 0 (stops timer), transmits pkt 1.

(b) Packet Loss:
    Sender transmits pkt 1 (starts timer) ===X (Dropped in network!)
    Sender timer expires (timeout!) ===> Sender retransmits pkt 1 ===>
    Receiver gets pkt 1, sends ack 1.

(c) ACK Loss:
    Sender transmits pkt 1 ===> Receiver gets pkt 1, sends ack 1 ===X (Dropped!)
    Sender timer expires (timeout!) ===> Sender retransmits pkt 1 ===>
    Receiver detects duplicate pkt 1, discards payload, re-sends ack 1 ===>
    Sender gets ack 1, advances to pkt 0.

(d) Premature Timeout / Delayed ACK:
    Sender transmits pkt 1 ===> Receiver gets pkt 1, sends ack 1 (delayed in queue)
    Sender timer expires prematurely ===> Sender retransmits pkt 1 ===>
    Original ack 1 arrives at sender ===> Sender advances and sends pkt 0 ===>
    Receiver gets duplicate pkt 1, discards payload, re-sends ack 1 ===>
    Delayed ack 1 arrives at sender while waiting for ack 0 ===> Sender ignores obsolete ACK!
```

---

## 6. Stop-and-Wait Utilization Bottleneck (Slides 31–33)

Although `rdt 3.0` is functionally correct, its throughput performance on high-speed, long-distance links is catastrophic.

### 6.1 Performance Analysis on a Gigabit Satellite/Fiber Link
Consider the slide parameters:
- Link Bandwidth: $R = 1\,\text{Gbps} = 10^9\,\text{bps}$.
- Packet Size: $L = 1\,\text{KB} = 8,000\,\text{bits}$.
- One-way Propagation Delay: $d_{\text{prop}} = 15\,\text{ms}$.
- Round-Trip Time: $RTT = 2 \times d_{\text{prop}} = 30\,\text{ms}$.

#### 1. Transmission Delay:
$$d_{\text{trans}} = \frac{L}{R} = \frac{8,000\,\text{bits}}{10^9\,\text{bps}} = 8 \times 10^{-6}\,\text{s} = 8\,\mu\text{s} = 0.008\,\text{ms}$$

#### 2. Sender Utilization ($U_{\text{sender}}$):
Sender utilization is defined as the fraction of time the sender is actively transmitting bits:
$$U_{\text{sender}} = \frac{d_{\text{trans}}}{RTT + d_{\text{trans}}} = \frac{0.008\,\text{ms}}{30\,\text{ms} + 0.008\,\text{ms}} = \frac{0.008}{30.008} \approx \mathbf{0.000267} \approx \mathbf{0.027\%}$$

#### 3. Effective Throughput:
$$\text{Effective Throughput} = U_{\text{sender}} \times R = 0.000267 \times 1\,\text{Gbps} = \mathbf{267\,\text{kbps}!}$$
On a 1 Gbps physical link, Stop-and-Wait achieves a miserable $267\,\text{kbps}$—the protocol throttles physical infrastructure capacity by **$99.97\%$**!

### 6.2 Solution: Pipelining
Pipelining allows the sender to transmit up to $N$ consecutive packets without waiting for individual ACKs, boosting utilization by a factor of $N$:
$$U_{\text{pipelined}} = \frac{N \times (L / R)}{RTT + (L / R)}$$
To achieve $100\%$ utilization ($U = 1.0$), the window size must satisfy:
$$N \ge \frac{RTT + d_{\text{trans}}}{d_{\text{trans}}} = \frac{30.008}{0.008} \approx \mathbf{3,751\text{ packets in flight}!}$$

---

## 7. Master Protocol Comparison Matrix

| Protocol Mechanism | `rdt 1.0` | `rdt 2.0` | `rdt 2.1` | `rdt 2.2` | `rdt 3.0` (Alternating-Bit) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Channel Assumptions** | Perfect channel | Bit errors only | Bit errors only | Bit errors only | Bit errors AND packet loss |
| **Error Detection** | None | Checksum | Checksum | Checksum | Checksum |
| **Feedback Scheme** | None | ACK & NAK | ACK & NAK | **NAK-Free** (Numbered ACKs) | Numbered ACKs |
| **Sequence Space** | None | None | **1 bit** ($0$ and $1$) | **1 bit** ($0$ and $1$) | **1 bit** ($0$ and $1$) |
| **Timer Hardware** | None | None | None | None | **Countdown Timer** |
| **Handled Flaw** | None | Basic error | Corrupted ACK/NAK | Eliminates NAKs | Lost packets / delayed ACKs |

---

## 8. High-Yield Open-Book Exam Traps & Examiner Tricks

1. **The Checksum Inversion Trap**:
   - *Trap*: Computing the sum of 16-bit words and writing the raw sum into the header.
   - *Fact*: The checksum field is the **bitwise NOT** (one's complement) of the sum. If the sender fails to invert, the receiver's verification algorithm fails.
2. **The End-Around Carry Trap**:
   - *Trap*: Performing standard arithmetic addition and dropping the 17th carry bit.
   - *Fact*: In one's complement arithmetic, any overflow carry bit out of the 16th position **must be wrapped around and added back into the least significant bit**!
3. **The Stop-and-Wait Utilization Trap**:
   - *Question*: *"If we double the packet size from 1 KB to 2 KB on a link where $RTT \gg d_{trans}$, how does utilization change?"*
   - *Fact*: Since $d_{trans} = L/R$, doubling $L$ doubles $d_{trans}$. Because $RTT$ dominates the denominator ($RTT + d_{trans} \approx RTT$), the utilization **doubles**!
4. **The `rdt 2.2` Duplicate ACK Semantic Trap**:
   - *Question*: *"In `rdt 2.2`, what does receiving `ACK 0` mean to a sender that just transmitted packet `1`?"*
   - *Fact*: It is an **implicit NAK 1**. It indicates that the receiver did not receive packet 1 (or received it corrupted) and is still acknowledging the prior packet 0.

---

## 9. Solved High-Yield Numerical Exam Problems

### Problem 1: Internet Checksum Calculation & Verification
**Problem Statement**:
A UDP sender transmits three 16-bit words:
- Word 1: `0x6660` (Binary: `0110 0110 0110 0000`)
- Word 2: `0x5555` (Binary: `0101 0101 0101 0101`)
- Word 3: `0x8F0C` (Binary: `1000 1111 0000 1100`)
1. Compute the exact 16-bit Internet Checksum using one's complement addition with end-around carry.
2. Show step-by-step how the receiving host verifies that no bit errors occurred during transit.

**Step-by-Step Solution**:

1. **Sender Calculation**:
   - Add Word 1 and Word 2:
     $$\begin{array}{r@{\quad}l}
     & 0110\;0110\;0110\;0000 \\
     + & 0101\;0101\;0101\;0101 \\
     \hline
     = & 1011\;1011\;1011\;0101 \quad (\text{Hex: } \text{0xBBB5}, \text{ zero carry})
     \end{array}$$
   - Add Word 3 to the intermediate sum:
     $$\begin{array}{r@{\quad}l}
     & 1011\;1011\;1011\;0101 \\
     + & 1000\;1111\;0000\;1100 \\
     \hline
     = & 1\;0100\;1010\;1100\;0001 \quad (\text{Hex: } \text{0x14AC1})
     \end{array}$$
   - Notice the carry out of the 16th bit (`1`). Perform **End-Around Carry**:
     $$\begin{array}{r@{\quad}l}
     & 0100\;1010\;1100\;0001 \\
     + & 0000\;0000\;0000\;0001 \\
     \hline
     = & 0100\;1010\;1100\;0010 \quad (\text{Hex: } \text{0x4AC2})
     \end{array}$$
   - Compute bitwise NOT (one's complement inversion):
     $$\text{Checksum} = \sim(0100\;1010\;1100\;0010) = \mathbf{1011\;0101\;0011\;1101} \quad (\text{Hex: } \mathbf{\text{0xB53D}})$$

2. **Receiver Verification**:
   - The receiver sums Word 1, Word 2, Word 3, AND the received Checksum (`0xB53D`):
     $$\begin{array}{r@{\quad}l}
     \text{Sum of Words 1, 2, 3} & = 0100\;1010\;1100\;0010 \quad (\text{0x4AC2}) \\
     + \text{Checksum} & = 1011\;0101\;0011\;1101 \quad (\text{0xB53D}) \\
     \hline
     \text{Final Sum} & = \mathbf{1111\;1111\;1111\;1111} \quad (\text{Hex: } \mathbf{\text{0xFFFF}})
     \end{array}$$
   - Inverting the final sum: $\sim(\text{0xFFFF}) = \mathbf{\text{0x0000}}$.
   - Since the inverted result is exactly zero, the receiver concludes the packet has **zero detected bit errors**.

---

### Problem 2: Pipelined Link Window Sizing for Target Utilization
**Problem Statement**:
A cross-country fiber link spans a distance of $d = 4,000\,\text{km}$ with a bandwidth of $R = 100\,\text{Mbps}$.
Data packets have a fixed length of $L = 1,000\,\text{bytes}$.
The speed of signal propagation in fiber is $s = 2 \times 10^8\,\text{m/s}$.
Acknowledgments are 40 bytes (transmission time negligible).
1. Calculate the link Round-Trip Time ($RTT$) and packet transmission delay ($d_{\text{trans}}$).
2. Calculate the link utilization under Stop-and-Wait.
3. What is the minimum window size $N$ needed to achieve a link utilization of at least $80\%$?

**Step-by-Step Solution**:

1. **Compute Delays**:
   - $L = 1,000 \times 8 = 8,000\,\text{bits}$.
   - Transmission delay:
     $$d_{\text{trans}} = \frac{L}{R} = \frac{8,000\,\text{bits}}{100 \times 10^6\,\text{bps}} = 8 \times 10^{-5}\,\text{s} = 0.08\,\text{ms}$$
   - One-way propagation delay:
     $$d_{\text{prop}} = \frac{4,000 \times 10^3\,\text{m}}{2 \times 10^8\,\text{m/s}} = 0.02\,\text{s} = 20\,\text{ms}$$
   - Round-Trip Time:
     $$RTT = 2 \times d_{\text{prop}} = 2 \times 20\,\text{ms} = \mathbf{40\,\text{ms}}$$

2. **Stop-and-Wait Utilization**:
   $$U_{\text{SW}} = \frac{d_{\text{trans}}}{RTT + d_{\text{trans}}} = \frac{0.08\,\text{ms}}{40\,\text{ms} + 0.08\,\text{ms}} = \frac{0.08}{40.08} \approx 0.001996 \approx \mathbf{0.20\%}$$

3. **Window Size for $80\%$ Utilization**:
   $$U = \frac{N \times d_{\text{trans}}}{RTT + d_{\text{trans}}} \ge 0.80$$
   $$N \times 0.08 \ge 0.80 \times 40.08 = 32.064$$
   $$N \ge \frac{32.064}{0.08} = 400.8 \implies \mathbf{N = 401\text{ packets in flight}}$$

---

## 10. Ultra-Fast Exam Revision Checklist
- [ ] Transport layer provides process-to-process communication; Network layer provides host-to-host delivery.
- [ ] UDP demux uses 2-tuple (Dest IP, Dest Port); TCP demux uses 4-tuple (Src IP, Src Port, Dest IP, Dest Port).
- [ ] UDP header is 8 bytes total: Source Port, Dest Port, Length, Checksum (16 bits each).
- [ ] Internet Checksum uses one's complement sum with end-around carry; error-free packet sums to `0xFFFF`.
- [ ] End-to-End argument: Transport checksum is necessary because router memory/bus errors bypass link-layer CRCs.
- [ ] `rdt 2.0` fatal flaw: Corrupted ACK/NAK causes undetected duplicate packet delivery or loss.
- [ ] `rdt 2.1` resolves ambiguity using 1-bit sequence numbers (0 and 1).
- [ ] `rdt 2.2` eliminates NAKs; duplicate numbered ACKs act as implicit NAKs.
- [ ] `rdt 3.0` (Alternating-Bit Protocol) handles lost packets using countdown timers.
- [ ] Stop-and-Wait utilization: $U = \frac{L/R}{RTT + L/R}$. Requires pipelining ($N$ packets) for high throughput.
