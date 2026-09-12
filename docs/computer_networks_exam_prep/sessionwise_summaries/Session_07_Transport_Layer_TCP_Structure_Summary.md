# Computer Networks (BSDCBZC481)
# Session 07: Principles of Reliable Data Transfer (RDT) & Sliding Window Protocols
### Exhaustive Slide-by-Slide Academic Exam Revision Manual & Problem Solving Guide

---

## 1. Session Context & Pedagogical Scope
- **Course Code & Title**: BSDCBZC481 — Computer Networks
- **Instructor**: Dr. K. Kalaiselvi (BITS Pilani)
- **Lecture Slide Mapping**: CS7: Transport Layer — Slides 1 to 43 (Complete Coverage)
- **Core Syllabus Covered**:
  1. Fundamentals of Reliable Data Transfer (RDT) & Service Interfaces
  2. Incremental Protocol Synthesis: `rdt 1.0` $\to$ `rdt 2.0` $\to$ `rdt 2.1` $\to$ `rdt 2.2` $\to$ `rdt 3.0` (Alternating-Bit Protocol)
  3. Finite State Machine (FSM) Specifications, Event-Action Logic & Fatal Flaw Analysis
  4. Timing & Trace Diagrams for Packet Loss, ACK Loss, and Delayed ACKs
  5. Performance Analysis of Stop-and-Wait vs. Channel Bandwidth-Delay Product
  6. Pipelining Principles & Utilization Speedup Derivations
  7. Go-Back-N (GBN) Protocol: Sender/Receiver FSMs, Cumulative ACKs & Retransmission Wave
  8. Selective Repeat (SR) Protocol: Out-of-Order Buffering, Individual Timers & Window Sliding
  9. The Selective Repeat Dilemma: Mathematical Proof of Window Size vs. Sequence Number Space ($W \le 2^{k-1}$)
  10. Open-Book Examination Traps, Rigorous Numerical Problems & Fast Revision Matrix

---

## 2. Theoretical Foundations of Reliable Data Transfer (RDT)

### 2.1 The Layered Abstraction & Interface Primitives
The transport layer provides a **reliable channel** service abstraction to the application layer, even though the underlying network layer (IP) provides only an **unreliable best-effort** service.

```
+-------------------------------------------------------------+
|                      APPLICATION LAYER                      |
|  Sends data via rdt_send()         Receives via deliver_data() |
+-------------------------------------------------------------+
                            |   ^
                            v   |
+-------------------------------------------------------------+
|              TRANSPORT LAYER (RDT PROTOCOL)                 |
|  Implements checksums, timers, sequence numbers, ACKs/NAKs  |
|  Transmits via udt_send()          Receives via rdt_rcv()   |
+-------------------------------------------------------------+
                            |   ^
                            v   |
+-------------------------------------------------------------+
|               UNRELIABLE NETWORK CHANNEL (IP)               |
|  Channel hazards: bit errors, dropped packets, reordering   |
+-------------------------------------------------------------+
```

### 2.2 Architectural Primitives Dissection (Slides 4–9)
- `rdt_send(data)`: Invoked by the upper application layer to pass data down to the transport layer.
- `udt_send(packet)`: Invoked by the RDT protocol to transmit a formatted packet over the **unreliable data transfer** channel.
- `rdt_rcv(packet)`: Invoked by the lower network layer when a packet arrives across the channel.
- `deliver_data(data)`: Invoked by RDT to hand verified, error-free, in-order application payload up to the receiving process.
- **Unidirectional vs. Bidirectional**: We develop unidirectional *data* transfer protocols, but *control information* (ACKs/NAKs, sequence numbers) must flow bidirectionally.

---

## 3. Step-by-Step Synthesis of RDT Protocols (Slides 10–28)

### 3.1 `rdt 1.0`: Reliable Transfer Over a Perfectly Reliable Channel (Slide 10)
- **Channel Assumption**: Zero bit errors, zero packet drops, perfectly in-order delivery.
- **Sender FSM**:
  - **Single State**: `Wait for call from above`.
  - **Event**: `rdt_send(data)`.
  - **Action**: `packet = make_pkt(data)`; `udt_send(packet)`.
- **Receiver FSM**:
  - **Single State**: `Wait for call from below`.
  - **Event**: `rdt_rcv(packet)`.
  - **Action**: `extract(packet, data)`; `deliver_data(data)`.
- **Evaluation**: Trivial baseline; unrealistic because physical media (copper, fiber, wireless) suffer from noise and buffer overflow.

---

### 3.2 `rdt 2.0`: Channel with Bit Errors (Slides 11–17)
- **Channel Assumption**: Packets may experience bit flips (detected via checksum), but NO packets are lost or dropped.
- **Core Recovery Mechanisms**:
  1. **Error Detection**: Sender computes Internet Checksum and includes it in `make_pkt(data, checksum)`.
  2. **Feedback Control**: Receiver responds with explicit control packets:
     - `ACK` (Positive Acknowledgment): Packet received correctly.
     - `NAK` (Negative Acknowledgment): Packet corrupted (checksum verification failed).
  3. **Retransmission**: Sender retransmits the current packet upon receiving a NAK.
- **Sender FSM (2 States)**:
  - State 1: `Wait for call from above` $\xrightarrow{\text{rdt\_send(data)}} \text{make\_pkt, udt\_send} \to$ State 2.
  - State 2: `Wait for ACK or NAK`:
    - If `rdt_rcv(rcvpkt) && isNAK(rcvpkt)`: `udt_send(sndpkt)` (Retransmit). Remain in State 2.
    - If `rdt_rcv(rcvpkt) && isACK(rcvpkt)`: Do nothing. Transition back to State 1.
- **Receiver FSM (1 State)**:
  - `Wait for call from below`:
    - If `rdt_rcv(rcvpkt) && corrupt(rcvpkt)`: `udt_send(NAK)`.
    - If `rdt_rcv(rcvpkt) && notcorrupt(rcvpkt)`: `extract(rcvpkt, data)`; `deliver_data(data)`; `udt_send(ACK)`.

> [!WARNING]
> **The Fatal Flaw of `rdt 2.0` (Slide 17)**:
> What happens if the `ACK` or `NAK` packet itself gets corrupted during transit?
> - The sender cannot know whether the receiver said ACK or NAK!
> - If sender blindly retransmits on garbled feedback: The receiver receives a **duplicate packet**. If the original packet was delivered OK, retransmitting introduces duplicate data into the application stream!
> - If sender does not retransmit: Potential **data loss** occurs.
> - **Conclusion**: Simple ACK/NAK cannot handle corrupted feedback without packet identification.

---

### 3.3 `rdt 2.1`: Handling Garbled ACKs/NAKs via Sequence Numbers (Slides 18–20)
- **Solution**: Sender adds a **1-bit sequence number** (`0` or `1`) to every data packet header.
- **Receiver Duty**: If receiver is waiting for packet `0` and receives a duplicate packet `1`, it discards the packet but re-transmits `ACK` to allow the sender to advance!
- **Sender FSM (4 States)**:
  1. `Wait for call 0 from above`: On `rdt_send(data)` $\to$ `sndpkt = make_pkt(0, data, checksum)`, `udt_send(sndpkt)` $\to$ goto State 2.
  2. `Wait for ACK or NAK 0`:
     - If `corrupt(rcvpkt) || isNAK(rcvpkt)` $\to$ `udt_send(sndpkt)` (Retransmit packet 0).
     - If `notcorrupt(rcvpkt) && isACK(rcvpkt)` $\to$ goto State 3.
  3. `Wait for call 1 from above`: On `rdt_send(data)` $\to$ `sndpkt = make_pkt(1, data, checksum)`, `udt_send(sndpkt)` $\to$ goto State 4.
  4. `Wait for ACK or NAK 1`:
     - If `corrupt(rcvpkt) || isNAK(rcvpkt)` $\to$ `udt_send(sndpkt)` (Retransmit packet 1).
     - If `notcorrupt(rcvpkt) && isACK(rcvpkt)` $\to$ goto State 1.
- **Receiver FSM (2 States)**:
  1. `Wait for 0 from below`:
     - If `notcorrupt && has_seq0(rcvpkt)`: `deliver_data`, `udt_send(ACK)` $\to$ goto State 2.
     - If `corrupt`: `udt_send(NAK)`.
     - If `notcorrupt && has_seq1(rcvpkt)`: Duplicate! Discard data, `udt_send(ACK)` (Re-ACK packet 1).
  2. `Wait for 1 from below`:
     - Symmetrical logic for packet 1.

---

### 3.4 `rdt 2.2`: A NAK-Free Protocol (Slides 21–22)
- **Improvement**: Eliminates explicit `NAK` packets completely.
- **Mechanism**: Receiver sends `ACK` containing the **explicit sequence number** of the last correctly received packet:
  - `make_pkt(ACK, 0, checksum)` or `make_pkt(ACK, 1, checksum)`.
- **Implicit NAK**: If the sender receives a **duplicate ACK** (e.g., sender is waiting for ACK 1 but receives ACK 0), it interprets this as an implicit NAK and immediately retransmits packet 1.

---

### 3.5 `rdt 3.0`: Channels with Bit Errors and Packet Loss (Slides 23–28)
- **Channel Assumption**: The underlying network can corrupt packets **and drop/lose packets** entirely (data packets or ACKs).
- **New Mechanism**: **Countdown Timer**.
  - Sender starts a countdown timer when transmitting a packet.
  - If ACK does not arrive within a specified timeout interval, sender assumes packet was lost and retransmits.
  - If packet/ACK was merely delayed (not lost), the retransmission produces a duplicate, but the 1-bit sequence number in `rdt 2.2` already handles duplicate filtering!
- **Also Known As**: **Alternating-Bit Protocol** (because sequence numbers alternate between 0 and 1).

#### The Four Timing Scenarios of `rdt 3.0` in Action (Slides 27–28)
1. **Scenario (a): Operation with No Loss**:
   - Sender sends `pkt0` $\to$ Receiver receives `pkt0`, sends `ack0` $\to$ Sender receives `ack0`, stops timer, sends `pkt1` $\to$ Receiver receives `pkt1`, sends `ack1`.
2. **Scenario (b): Packet Loss**:
   - Sender sends `pkt1` $\to$ Packet is dropped by network router.
   - Sender timer expires (`timeout`) $\to$ Sender retransmits `pkt1` $\to$ Receiver receives `pkt1`, sends `ack1`.
3. **Scenario (c): ACK Loss**:
   - Sender sends `pkt1` $\to$ Receiver receives `pkt1`, sends `ack1` $\to$ `ack1` is dropped by network.
   - Sender timer expires (`timeout`) $\to$ Sender retransmits `pkt1`.
   - Receiver detects duplicate sequence number `1`, discards payload, and re-sends `ack1` $\to$ Sender receives `ack1` and advances.
4. **Scenario (d): Premature Timeout / Delayed ACK**:
   - Sender sends `pkt1`. Timer expires prematurely before `ack1` arrives.
   - Sender retransmits `pkt1`.
   - Original `ack1` arrives at sender $\to$ Sender shifts to sending `pkt0`.
   - Receiver receives duplicate `pkt1`, discards it, and re-sends `ack1`.
   - Delayed `ack1` arrives at sender while waiting for `ack0` $\to$ Sender detects obsolete sequence number and silently ignores it!

---

## 4. Performance Bottleneck of Stop-and-Wait (Slides 29–31)

### 4.1 Transmission Delay vs. Propagation Delay
- **Packet Length ($L$)**: $8,000\text{ bits}$ ($1\text{ KB}$).
- **Link Bandwidth ($R$)**: $1\text{ Gbps} = 10^9\text{ bits/sec}$.
- **One-Way Propagation Delay ($d_{prop}$)**: $15\text{ ms}$.
- **Round-Trip Time ($RTT$)**: $2 \times d_{prop} = 30\text{ ms}$.

$$D_{trans} = \frac{L}{R} = \frac{8,000\text{ bits}}{10^9\text{ bits/sec}} = 8 \times 10^{-6}\text{ sec} = 8\text{ µs} = 0.008\text{ ms}$$

### 4.2 Sender Utilization ($U_{sender}$) Derivation
Sender utilization is defined as the fraction of time the sender is actively pumping bits into the physical channel:

$$U_{sender} = \frac{D_{trans}}{RTT + D_{trans}} = \frac{L / R}{RTT + L / R}$$

Plugging in the numerical values from Slide 31:
$$U_{sender} = \frac{0.008\text{ ms}}{30\text{ ms} + 0.008\text{ ms}} = \frac{0.008}{30.008} \approx 0.000267 \approx 0.027\%$$

> [!NOTE]
> **Slide 31 Verdict**:
> *"rdt 3.0 protocol performance stinks! The protocol limits the performance of the underlying physical infrastructure by $99.97\%$!"*
> On a 1 Gbps link, the effective throughput achieved is only:
> $$\text{Throughput} = U_{sender} \times R = 0.000267 \times 1\text{ Gbps} = 267\text{ kbps}!$$

---

## 5. Pipelined Protocols & Sliding Window Architecture (Slides 32–33)

### 5.1 Pipelining Mechanics
Instead of Stop-and-Wait, the sender is permitted to transmit up to $N$ consecutive packets without waiting for an ACK.
- Increases the range of allowable sequence numbers from 1 bit to $k$ bits ($0$ to $2^k - 1$).
- Requires buffering at the sender and/or receiver.

### 5.2 Utilization Under $N$-Packet Pipelining
For a window of $N$ packets in flight:
$$U_{sender} = \frac{N \cdot (L / R)}{RTT + (L / R)}$$

For $N = 3$ packets (Slide 33):
$$U_{sender} = \frac{3 \times 0.008}{30.008} = \frac{0.024}{30.008} \approx 0.00081 \approx 0.081\% \quad (3\times\text{ increase})$$

To achieve $100\%$ link utilization ($U_{sender} = 1.0$):
$$N \ge \frac{RTT + L/R}{L/R} = \frac{30.008}{0.008} \approx 3,751\text{ packets in flight}!$$

---

## 6. Go-Back-N (GBN) Deep Dive (Slides 34–36)

### 6.1 Sender Window Structure & Variables
The sender maintains a sliding window of size $N$ over a $k$-bit sequence space:

```
                  [<------------------ N ------------------->]
+-----------------+-------------------+---------------------+------------------+
| already ACKed   | sent, unACKed     | usable, not yet sent| cannot be used   |
+-----------------+-------------------+---------------------+------------------+
                  ^                   ^                     ^
                  |                   |                     |
               send_base          nextseqnum            send_base + N
```

- `send_base`: Sequence number of the oldest unacknowledged packet.
- `nextseqnum`: Smallest unused sequence number (next packet to send).
- Window Constraints:
  - Sequence numbers in $[0, \text{send\_base}-1]$: Fully transmitted and acknowledged.
  - Sequence numbers in $[\text{send\_base}, \text{nextseqnum}-1]$: Sent, in flight, awaiting ACK.
  - Sequence numbers in $[\text{nextseqnum}, \text{send\_base} + N - 1]$: Available to send immediately if data arrives from above.
  - Sequence numbers $\ge \text{send\_base} + N$: Cannot be used until the window slides forward.

### 6.2 Sender Event-Action Logic
1. **Invocation from Above (`rdt_send(data)`)**:
   - If $\text{nextseqnum} < \text{send\_base} + N$: Create packet, `udt_send(packet)`. If $\text{send\_base} == \text{nextseqnum}$, start timer. Increment `nextseqnum`.
   - If window is full: Refuse data or buffer for later transmission.
2. **Timeout Event (`timeout`)**:
   - Retransmit **ALL $N$ packets** currently in flight ($[\text{send\_base}, \text{nextseqnum}-1]$).
   - Restart the single timer.
3. **Receipt of ACK (`rdt_rcv(rcvpkt) && notcorrupt(rcvpkt)`)**:
   - GBN uses **Cumulative ACKs**: `ACK(n)` acknowledges all packets up to and including sequence number $n$.
   - Set $\text{send\_base} = n + 1$.
   - If there are still unacknowledged packets in flight ($\text{send\_base} \ne \text{nextseqnum}$), restart timer; otherwise stop timer.

### 6.3 Receiver Logic & Out-of-Order Handling (Slide 35)
- **Receiver Window Size**: **Strictly $1$**.
- Maintains single variable: `expectedseqnum`.
- **In-Order Arrival**: If received packet has sequence number equal to `expectedseqnum`:
  - `deliver_data(data)`.
  - Send `ACK(expectedseqnum)`.
  - Increment `expectedseqnum`.
- **Out-of-Order Arrival (Gap or Duplicate)**:
  - **Discard the packet** (do not buffer!).
  - Re-transmit `ACK` for the highest in-order sequence number (`expectedseqnum - 1`).

### 6.4 GBN Execution Trace (Slide 36 Walkthrough)
- Sender window $N = 4$. Sender transmits `pkt0, pkt1, pkt2, pkt3`.
- `pkt0` and `pkt1` arrive safely $\to$ Receiver replies with `ack0` and `ack1`. Window slides forward; sender sends `pkt4` and `pkt5`.
- **Loss Event**: `pkt2` is lost in transit!
- `pkt3` arrives at receiver $\to$ Receiver expects `2`, sees `3`. Discards `pkt3`, re-sends `ack1`.
- `pkt4` arrives $\to$ Discarded; receiver re-sends `ack1`.
- `pkt5` arrives $\to$ Discarded; receiver re-sends `ack1`.
- **Timeout on `pkt2`**: Sender's single timer for `pkt2` expires.
- **Go-Back-N Action**: Sender retransmits `pkt2, pkt3, pkt4, pkt5` (all 4 packets in the window!).

---

## 7. Selective Repeat (SR) Deep Dive (Slides 37–40)

### 7.1 Motivation for Selective Repeat
In high bandwidth-delay networks, GBN's policy of retransmitting the entire window when a single packet drops causes massive bandwidth wastage. Selective Repeat avoids unnecessary retransmissions by having the receiver individually acknowledge all correctly received packets.

### 7.2 Sender & Receiver Window Structure (Slide 38)
- Both sender and receiver maintain sliding windows of size $N$.
- Receiver possesses **internal memory buffers** to hold out-of-order packets until the preceding missing packets arrive.
- Sender maintains an **independent countdown timer for each in-flight packet**.

```
Sender View:
[ ACKed ] [ unACKed (timer running) ] [ usable not sent ] [ outside window ]
          ^
       send_base

Receiver View:
[ Delivered ] [ Buffered out-of-order ] [ Expected / Acceptable ] [ outside ]
              ^
           rcv_base
```

### 7.3 Event-Action Rules (Slide 39)

#### Sender Events:
1. **Data from Above**: If next sequence number is within window, transmit packet, start its dedicated timer.
2. **Timeout on packet $n$**: Retransmit **ONLY packet $n$**, restart packet $n$'s timer. (Do not retransmit other packets!).
3. **ACK($n$) Arrives in $[\text{send\_base}, \text{send\_base} + N - 1]$**:
   - Mark packet $n$ as received.
   - If $n == \text{send\_base}$, advance `send_base` forward to the sequence number of the next unacknowledged packet.

#### Receiver Events:
1. **Packet $n$ arrives in $[\text{rcv\_base}, \text{rcv\_base} + N - 1]$**:
   - Send selective `ACK(n)`.
   - If out-of-order: Store in local buffer.
   - If in-order ($n == \text{rcv\_base}$): Deliver packet $n$ and any consecutive previously buffered packets to the application layer. Advance `rcv_base` accordingly.
2. **Packet $n$ arrives in $[\text{rcv\_base} - N, \text{rcv\_base} - 1]$**:
   - **Crucial Rule**: Must re-send `ACK(n)`! Even though the receiver already delivered it, the sender's ACK may have been lost. If the receiver does not re-ACK, the sender's window will never advance!
3. **Otherwise**: Ignore packet.

### 7.4 SR Execution Trace (Slide 40 Walkthrough)
- Sender window $N = 4$. Sender transmits `pkt0, pkt1, pkt2, pkt3`.
- `pkt0` and `pkt1` arrive $\to$ Receiver sends `ack0, ack1`, delivers to app.
- **Loss Event**: `pkt2` is dropped.
- `pkt3` arrives $\to$ Receiver buffers `pkt3`, transmits individual `ack3`.
- Sender window slides to base 2 on receipt of `ack0, ack1`. Sends `pkt4, pkt5`.
- `pkt4` and `pkt5` arrive $\to$ Receiver buffers `pkt4, pkt5`, transmits `ack4, ack5`.
- **Timeout on `pkt2`**: Sender timer for `pkt2` expires.
- **Selective Repeat Action**: Sender retransmits **ONLY `pkt2`** (not 3, 4, 5!).
- Receiver receives `pkt2`. It now has `pkt2` plus buffered `pkt3, pkt4, pkt5`! It delivers all 4 packets in order to the application layer, and advances `rcv_base` by 4!

---

## 8. The Selective Repeat Dilemma: Sequence Space Proof (Slides 41–42)

### 8.1 The Ambiguity Problem
If the sequence number space is too small relative to the window size, the receiver cannot distinguish whether an incoming packet is a **brand-new packet** or a **retransmitted duplicate of an old packet**.

#### Concrete Counterexample from Slide 41:
- Sequence numbers: $0, 1, 2, 3$ ($k = 2$ bits, sequence space $S = 2^2 = 4$).
- Window size: $N = 3$.

```
SCENARIO A (Normal Operation):
Sender transmits pkts 0, 1, 2.
Receiver receives 0, 1, 2. Sends ack0, ack1, ack2.
Receiver window shifts from [0, 1, 2] to [3, 0, 1].
Sender receives all ACKs. Sender window shifts to [3, 0, 1].
Sender transmits pkt 3, then pkt 0 (NEW incarnation).
Receiver sees pkt 0, accepts it as NEW packet 0. (Correct!)

SCENARIO B (Catastrophic Collision):
Sender transmits pkts 0, 1, 2.
Receiver receives 0, 1, 2. Sends ack0, ack1, ack2.
Receiver window shifts from [0, 1, 2] to [3, 0, 1].
DISASTER: All three ACKs (ack0, ack1, ack2) are lost in the network!
Sender times out on pkt 0.
Sender retransmits OLD pkt 0.
Receiver receives pkt 0.
Because receiver's window is [3, 0, 1], pkt 0 falls inside the acceptable window!
Receiver accepts OLD duplicate pkt 0 as brand-new data!
```

### 8.2 Mathematical Proof & General Theorem
In Selective Repeat, the receiver's window and the sender's window can be shifted relative to each other by at most $W$ positions.
- The highest sequence number the receiver might be willing to accept is $\text{rcv\_base} + W_r - 1$.
- The lowest sequence number the sender might retransmit is $\text{send\_base} = \text{rcv\_base} - W_s$.
- The total range of sequence numbers that can be concurrently active is:
$$\text{Span} = W_s + W_r$$

To prevent the sequence numbers from wrapping around and overlapping:
$$W_s + W_r \le S = 2^k$$

Assuming symmetric windows ($W_s = W_r = N$):
$$2N \le 2^k \implies N \le 2^{k-1}$$

> [!IMPORTANT]
> **Summary of Sequence Space Constraints**:
> - **Selective Repeat (SR)**: $\mathbf{N \le 2^{k-1}}$ (Window size cannot exceed **half** the sequence space!).
> - **Go-Back-N (GBN)**: Since $W_r = 1$, $W_s + 1 \le 2^k \implies \mathbf{N \le 2^k - 1}$ (Window size can be at most **one less** than sequence space!).
> - **Stop-and-Wait**: $W_s = 1, W_r = 1 \implies 1 + 1 \le 2^1 \implies k = 1\text{ bit}$ (0 and 1 suffice).

---

## 9. Master Architectural Comparison Matrix

| Technical Metric | `rdt 3.0` (Stop-and-Wait) | Go-Back-N (GBN) | Selective Repeat (SR) |
| :--- | :--- | :--- | :--- |
| **Sender Window Size ($W_s$)** | $1$ | $N > 1$ | $N > 1$ |
| **Receiver Window Size ($W_r$)** | $1$ | **$1$ (Strictly)** | **$N > 1$ (Buffered)** |
| **Acknowledgment Scheme** | Individual ACK | **Cumulative ACK** (`ACK(n)` covers $\le n$) | **Individual ACK** (`ACK(n)` covers only $n$) |
| **Out-of-Order Handling** | Discarded | **Discarded silently** (re-ACK highest in-order) | **Buffered in memory** until hole filled |
| **Timer Hardware** | 1 single timer | **1 timer** for oldest in-flight packet (`send_base`) | **$N$ independent timers** (1 per unACKed packet) |
| **Retransmission Scope** | Single packet | **All $N$ packets** in the sender window | **Only the single timed-out packet** |
| **Sequence Space Rule** | $k \ge 1\text{ bit}$ ($0, 1$) | $N \le 2^k - 1$ | $N \le 2^{k-1}$ |
| **Channel Bandwidth Efficiency** | Extremely poor ($< 0.1\%$) | Moderate (wasted bandwidth on error) | **Optimal** (minimal retransmissions) |
| **Implementation Complexity** | Minimal | Low (receiver requires 0 buffer) | High (receiver buffer management & multiple timers) |

---

## 10. High-Yield Open-Book Exam Traps & Examiner Tricks

1. **The Duplicate ACK Semantic Trap**:
   - In GBN, receiving duplicate `ACK(k)` means the receiver got an out-of-order packet (higher than $k$).
   - In SR, receiving an ACK for a packet already acknowledged is simply an old delayed ACK; sender ignores it.
2. **The Sequence Space Overlap Trap**:
   - Question: *"A protocol uses 4-bit sequence numbers. What is the maximum window size for GBN and SR?"*
   - Answer: $k = 4 \implies 2^k = 16$.
     - $\text{GBN}: N_{max} = 16 - 1 = \mathbf{15}$.
     - $\text{SR}: N_{max} = 16 / 2 = \mathbf{8}$.
3. **GBN Timer Reset Rule**:
   - In GBN, the timer is NOT started for every packet! The timer is started when $\text{send\_base} == \text{nextseqnum}$. When an ACK arrives that advances `send_base`, the timer is restarted **only if there are remaining unACKed packets**; otherwise it is stopped.
4. **SR Receiver Re-ACK Rule**:
   - Question: *"Why does the SR receiver ACK packets below `rcv_base`?"*
   - Answer: Because the sender's previous ACK might have been lost. If the receiver ignores duplicate packets below its window, the sender will time out indefinitely and stall!

---

## 11. Solved High-Yield Numerical Exam Problems

### Problem 1: Link Utilization and Optimal Window Sizing
**Problem Statement**:
A satellite channel has a bandwidth of $10\text{ Mbps}$ and a one-way propagation delay of $250\text{ ms}$. Data frames are $2,000\text{ bytes}$ long. Acknowledgments are piggybacked and negligible in size ($40\text{ bytes}$, transmission time can be neglected).
1. Calculate the link utilization under Stop-and-Wait protocol.
2. What is the minimum window size $N$ needed to achieve at least $90\%$ link utilization?
3. How many bits are required in the sequence number field for both GBN and SR to achieve this $90\%$ utilization?

**Step-by-Step Solution**:
1. **Compute Delays**:
   - $L = 2000 \times 8 = 16,000\text{ bits}$.
   - $R = 10 \times 10^6\text{ bps} = 10^7\text{ bps}$.
   - $D_{trans} = \frac{16,000}{10^7} = 1.6 \times 10^{-3}\text{ sec} = 1.6\text{ ms}$.
   - $RTT = 2 \times 250\text{ ms} = 500\text{ ms}$.
2. **Stop-and-Wait Utilization**:
   $$U_{SW} = \frac{D_{trans}}{RTT + D_{trans}} = \frac{1.6}{500 + 1.6} = \frac{1.6}{501.6} \approx 0.00319 \approx \mathbf{0.32\%}$$
3. **Minimum Window Size for $90\%$ Utilization**:
   $$U = \frac{N \times D_{trans}}{RTT + D_{trans}} \ge 0.90 \implies N \times 1.6 \ge 0.90 \times 501.6 = 451.44$$
   $$N \ge \frac{451.44}{1.6} = 282.15 \implies \mathbf{N = 283\text{ packets}}$$
4. **Sequence Number Bits Required**:
   - For **Go-Back-N**:
     $$N \le 2^k - 1 \implies 2^k \ge N + 1 = 284 \implies k \ge \lceil\log_2(284)\rceil = \mathbf{9\text{ bits}} \quad (2^9 = 512 > 284)$$
   - For **Selective Repeat**:
     $$N \le 2^{k-1} \implies 2^{k-1} \ge 283 \implies k - 1 \ge \lceil\log_2(283)\rceil = 9 \implies k \ge \mathbf{10\text{ bits}} \quad (2^{10-1} = 512 > 283)$$

---

### Problem 2: Sequence Number and Window State Tracking Under GBN
**Problem Statement**:
Host A uses Go-Back-N with window size $N = 4$ and a $3$-bit sequence space ($0$ to $7$). At time $t = 0$, `send_base = 0` and `nextseqnum = 0`. Host A sends packets $0, 1, 2, 3$.
- Packet $0$ arrives safely; ACK $0$ arrives at A.
- Packet $1$ is lost in the network.
- Packets $2$ and $3$ arrive safely at Host B.
Trace the exact sequence of packets transmitted, packets buffered/discarded, ACKs returned, window state updates, and retransmissions.

**Step-by-Step Solution**:
1. Host A transmits `pkt0, pkt1, pkt2, pkt3`. `send_base = 0`, `nextseqnum = 4`. Timer started for packet 0.
2. Host B receives `pkt0` (in-order, expected 0). B sends `ack0`, increments `expectedseqnum` to 1.
3. Host A receives `ack0`. `send_base` updates from $0$ to $1$. Window is now $[1, 4]$. A immediately transmits `pkt4`. `nextseqnum` becomes 5. Timer restarted for packet 1.
4. `pkt1` is lost.
5. Host B receives `pkt2`. Expected is 1, received 2 (gap!). B discards `pkt2` and re-sends `ack0`.
6. Host B receives `pkt3`. Discarded; B re-sends `ack0`.
7. Host B receives `pkt4`. Discarded; B re-sends `ack0`.
8. Host A receives the duplicate `ack0`s and ignores them.
9. Timer for `pkt1` expires.
10. **Go-Back-N Action**: Host A retransmits all unacknowledged packets currently in window: `pkt1, pkt2, pkt3, pkt4`. Timer restarted for packet 1.

---

## 12. Ultra-Fast Exam Revision Checklist
- [ ] `rdt 1.0`: Underlying channel perfectly reliable (no errors, no drops).
- [ ] `rdt 2.0`: Channel flips bits. Checksum + ACK/NAK. Flaw: Corrupted ACK/NAK causes duplicate delivery or data loss.
- [ ] `rdt 2.1`: Sequence numbers (0 and 1) added to packets to detect duplicates when ACKs/NAKs are garbled.
- [ ] `rdt 2.2`: NAK-free. ACKs carry explicit sequence numbers; duplicate ACK acts as implicit NAK.
- [ ] `rdt 3.0`: Handles lost packets using countdown timers. Alternating-bit protocol.
- [ ] Stop-and-Wait utilization: $U = \frac{L/R}{RTT + L/R}$. Poor utilization on long-distance high-speed links.
- [ ] Pipelining utilization: $U = \frac{N \cdot (L/R)}{RTT + L/R}$.
- [ ] GBN uses cumulative ACKs, single timer on `send_base`, receiver window $= 1$, retransmits ALL $N$ packets on timeout.
- [ ] SR uses individual ACKs, individual timers per packet, receiver window $= N$ with out-of-order buffering, retransmits ONLY timed-out packet.
- [ ] Sequence space rule: GBN requires $N \le 2^k - 1$; SR requires $N \le 2^{k-1}$.
