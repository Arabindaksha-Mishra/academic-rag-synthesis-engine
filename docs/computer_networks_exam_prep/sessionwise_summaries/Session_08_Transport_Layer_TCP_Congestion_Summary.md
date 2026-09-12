# Computer Networks (BSDCBZC481)
# Session 08: Transport Layer — TCP Architecture, Flow Control & AIMD Congestion Control
### Exhaustive Slide-by-Slide Academic Exam Revision Manual & Problem Solving Guide

---

## 1. Session Context & Pedagogical Scope
- **Course Code & Title**: BSDCBZC481 — Computer Networks
- **Instructor**: Dr. K. Kalaiselvi (BITS Pilani)
- **Primary Textbooks**:
  - J.F. Kurose & K.W. Ross, *Computer Networking: A Top-Down Approach*, 5th/6th Edition, Chapter 3 (T1)
  - B.A. Forouzan, *Data Communications and Networking*, 4th Edition, Chapter 24 (T2)
- **Lecture Slide Mapping**: CS8: Transport Layer — Slides 1 to 49 (Complete Coverage)
- **Core Syllabus Covered**:
  1. Transmission Control Protocol (TCP, RFC 793): Point-to-Point, Full-Duplex & Byte Stream Abstraction
  2. TCP Segment Header Architecture: Sequence Numbers, Cumulative ACKs & The 6 Control Flags
  3. Round-Trip Time (RTT) Estimation: EWMA, Jacobson's Algorithm, DevRTT & Exponential Timer Backoff
  4. Reliable Data Transfer in TCP: Single Timer Model & Fast Retransmit on 3 Duplicate ACKs
  5. Flow Control Architecture: Advertised Window (`rwnd`) & The Zero-Window Probe Mechanism
  6. TCP Connection Management: 3-Way Handshake, 4-Way FIN Teardown & The `TIME_WAIT` State ($2\text{MSL}$)
  7. Denial of Service: SYN Flood Attacks & Stateless Cryptographic SYN Cookies
  8. Principles of Congestion Control: Queuing Costs, Dropped Packets & Unnecessary Retransmissions
  9. Additive-Increase Multiplicative-Decrease (AIMD) Mechanics & The "Sawtooth" Waveform
  10. TCP Congestion Control State Machine: Slow Start, Congestion Avoidance & Fast Recovery
  11. Architectural Comparison: TCP Tahoe vs. TCP Reno vs. TCP NewReno
  12. Macroscopic TCP Throughput Formulation & Bandwidth Fairness Convergence Proof
  13. High-Yield Open-Book Exam Traps, Rigorous Numerical Problems & Fast Revision Checklist

---

## 2. TCP Architecture & Segment Header Format (Slides 3–10)

TCP is an end-to-end, connection-oriented, full-duplex protocol providing a **reliable byte-stream channel** over an unreliable best-effort network layer.

```
+-------------------------------------------------------------------------+
|                              TCP SENDER                                 |
|   App writes bytes ===> [ TCP Send Buffer ] ===> Segments (MSS Chunks)  |
+-------------------------------------------------------------------------+
                                     |
                                     v IP Datagrams across network
                                     |
+-------------------------------------------------------------------------+
|                             TCP RECEIVER                                |
|   App reads bytes  <=== [ TCP Receive Buffer ] <=== In-Order Reassembly |
+-------------------------------------------------------------------------+
```

- **Maximum Segment Size (MSS)**: Maximum amount of application data (excluding TCP/IP headers) that can be placed in a single segment. Typically $1,460\,\text{bytes}$, derived from the standard Ethernet Maximum Transmission Unit (MTU) of $1,500\,\text{bytes}$ minus $20\,\text{bytes}$ IPv4 header minus $20\,\text{bytes}$ TCP header.

### 2.1 The 20-Byte Fixed TCP Segment Header Structure (Slide 5)

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          SOURCE PORT (16)     |       DESTINATION PORT (16)   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        SEQUENCE NUMBER (32)                   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    ACKNOWLEDGMENT NUMBER (32)                 |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|DATA |       |U|A|P|R|S|F|                                     |
|OFFST|RSVD(6)|R|C|S|S|Y|I|             RECEIVE WINDOW (16)     |
| (4) |       |G|K|H|T|N|N|                                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          CHECKSUM (16)        |         URGENT POINTER (16)   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    OPTIONS (Variable, 0 to 40 bytes)          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    PAYLOAD DATA (Variable length)             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### Detailed Header Field Breakdown:
1. **Sequence Number (32 bits)**: The byte-stream number of the **very first data byte** in the segment's payload. TCP views data as an unstructured, ordered stream of bytes, NOT discrete packets.
2. **Acknowledgment Number (32 bits)**: The byte-stream number of the **next byte expected** from the peer. It is **strictly cumulative** (an ACK of $500$ confirms all bytes up to $499$).
3. **Data Offset (Header Length, 4 bits)**: Specifies the length of the TCP header in **32-bit (4-byte) words**. Minimum value is $5$ ($5 \times 4 = 20\,\text{bytes}$); maximum value is $15$ ($15 \times 4 = 60\,\text{bytes}$).
4. **The Six Core Control Flags (1 bit each)**:
   - `URG`: Urgent pointer field is valid (rarely used).
   - `ACK`: Acknowledgment field is valid (set on all packets except the initial SYN).
   - `PSH`: Receiver should push data to application immediately without waiting for buffer to fill.
   - `RST`: Abort and reset the connection immediately (abnormal termination).
   - `SYN`: Synchronize sequence numbers; initiates a new connection.
   - `FIN`: Sender has finished transmitting data; initiates connection teardown.
5. **Receive Window (`rwnd`, 16 bits)**: Flow control mechanism. The receiver advertises the exact number of bytes of free buffer space it currently has available.

---

## 3. RTT Estimation & Jacobson’s Adaptive Timeout Algorithm (Slides 11–15)

TCP sets its retransmission timeout (RTO) dynamically based on measured Round-Trip Times. Setting RTO too short causes premature timeouts and duplicate retransmissions; setting RTO too long causes sluggish recovery when packets drop.

```
RTT (ms)
  ^
  |        /\
  |  SampleRTT (Noisy, instantaneous)
  |      /    \  /\
  |     /      \/  \
  |    /____________\_____ EstimatedRTT (Smooth EWMA)
  +----------------------------------------------------> Time
```

### 3.1 SampleRTT & Karn's Algorithm
- `SampleRTT`: Measured elapsed time from segment transmission until receipt of its ACK.
- **Karn's Algorithm**: Never measure `SampleRTT` for retransmitted segments! (Impossible to know if ACK corresponds to the original or retransmitted segment).

### 3.2 Exponentially Weighted Moving Average (EWMA)
To smooth out transient network jitter, TCP computes an EWMA (Slide 13):
$$\text{EstimatedRTT} = (1 - \alpha) \cdot \text{EstimatedRTT} + \alpha \cdot \text{SampleRTT}$$
- Recommended standard weight: $\mathbf{\alpha = 0.125} = 1/8$.
- Recent samples carry an exponentially decaying weight: $(1 - \alpha)^k$.

### 3.3 Safety Margin: Estimating RTT Variance ($\text{DevRTT}$)
TCP measures the absolute deviation of `SampleRTT` from `EstimatedRTT` (Slide 14):
$$\text{DevRTT} = (1 - \beta) \cdot \text{DevRTT} + \beta \cdot \left|\text{SampleRTT} - \text{EstimatedRTT}\right|$$
- Recommended standard weight: $\mathbf{\beta = 0.25} = 1/4$.

### 3.4 Jacobson's Retransmission Timeout Formulation
The retransmission timeout interval is set to the estimated average plus a four-sigma safety margin:
$$\text{TimeoutInterval} = \text{EstimatedRTT} + 4 \cdot \text{DevRTT}$$

> [!IMPORTANT]
> **Exponential Timer Backoff on Consecutive Timeouts**:
> If a timeout occurs, TCP immediately doubles the timeout interval for the retransmitted segment:
> $$\text{TimeoutInterval}_{\text{new}} = 2 \times \text{TimeoutInterval}_{\text{old}}$$
> This exponential backoff mimics congestion control, preventing the sender from hammering an already collapsed network fabric.

---

## 4. TCP Reliable Data Transfer & Fast Retransmit (Slides 16–21)

TCP uses a **hybrid sliding window protocol** that blends features of Go-Back-N and Selective Repeat:
- Maintains a **single retransmission timer** associated with the oldest unacknowledged segment.
- Uses **Cumulative ACKs** (like GBN).
- Receivers buffer out-of-order segments (like SR).

### 4.1 Fast Retransmit on Triple Duplicate ACKs (Slides 20–21)
Because the network often experiences long timeouts, waiting for the timer to expire introduces dead time. 
- If a single segment is lost while subsequent segments arrive safely, the receiver sends a **duplicate ACK** for every out-of-order segment arriving.
- **Fast Retransmit Rule**: If the sender receives **three duplicate ACKs** for the same byte (meaning 4 identical ACKs total), it concludes the missing segment was lost rather than merely reordered.
- **Action**: Retransmits the missing segment **immediately**, without waiting for the retransmission timer to expire!

```
Sender                                                    Receiver
  |--- Seg 1 (seq=1, 100B) ------------------------------->| (Expects 101, sends ACK 101)
  |<-- ACK 101 --------------------------------------------|
  |--- Seg 2 (seq=101, 100B) ------X (LOST IN NETWORK!)    |
  |--- Seg 3 (seq=201, 100B) ----------------------------->| (Out of order! Re-sends ACK 101)
  |<-- ACK 101 (Duplicate ACK 1) --------------------------|
  |--- Seg 4 (seq=301, 100B) ----------------------------->| (Out of order! Re-sends ACK 101)
  |<-- ACK 101 (Duplicate ACK 2) --------------------------|
  |--- Seg 5 (seq=401, 100B) ----------------------------->| (Out of order! Re-sends ACK 101)
  |<-- ACK 101 (Duplicate ACK 3) --------------------------|
  |                                                        |
  | *** 3 DUPLICATE ACKS DETECTED! FAST RETRANSMIT! ***   |
  |--- Seg 2 (seq=101, 100B) [Retransmitted] ------------->| (Hole filled! Receives Seg 2, 3, 4, 5)
  |<-- ACK 501 (Cumulative ACK for all buffered data!) ----|
```

---

## 5. TCP Flow Control: The Advertised Window (`rwnd`) (Slides 22–24)

Flow control is a speed-matching service that prevents a fast sender from overflowing the buffer of a slow receiver.

```
RECEIVER BUFFER LAYOUT:
+------------------------------------+-----------------------------+
| Buffered Data (waiting to be read) | Free Buffer Space (rwnd)    |
+------------------------------------+-----------------------------+
^                                    ^                             ^
|                                    |                             |
LastByteRead                         LastByteRcvd                  RcvBuffer End
```

### 5.1 Flow Control Mathematical Formulation
Let `RcvBuffer` be the total allocated buffer size.
$$\text{Free Buffer Space } (\text{rwnd}) = \text{RcvBuffer} - (\text{LastByteRcvd} - \text{LastByteRead})$$
- The receiver places `rwnd` into the 16-bit Receive Window field of every returned TCP header.
- **Sender Constraint**: The sender ensures that the total unacknowledged data in flight never exceeds `rwnd`:
  $$\text{LastByteSent} - \text{LastByteAcked} \le \text{rwnd}$$

### 5.2 The Zero-Window Deadlock & Persistence Timer
- If the receiver process stops reading data, `rwnd` shrinks to **0**. The sender halts transmission.
- Once the receiver application drains its buffer, it sends an ACK advertising `rwnd > 0`.
- **The Deadlock Trap**: If this update ACK is lost, the sender waits forever for `rwnd > 0`, while the receiver waits forever for incoming data!
- **Solution**: The sender maintains a **Persistence Timer**. When `rwnd = 0`, the sender periodically transmits a **1-byte probe segment**. The receiver's response to this probe informs the sender of the updated `rwnd`!

---

## 6. TCP Connection Lifecycle & FSM Transitions (Slides 25–30)

### 6.1 Three-Way Handshake (Connection Establishment)
Before transferring data, client and server establish state variables (initial sequence numbers, buffer allocations):

```
CLIENT (initiator)                                          SERVER (listener)
CLOSED                                                      LISTEN
  |                                                           |
  |-- (1) SYN=1, Seq=client_isn ----------------------------->| SYN_RCVD
  |   (Client enters SYN_SENT)                                |
  |                                                           |
  |<-- (2) SYN=1, ACK=1, Seq=server_isn, Ack=client_isn + 1 --|
  |   (Client enters ESTABLISHED)                             |
  |                                                           |
  |-- (3) ACK=1, Seq=client_isn + 1, Ack=server_isn + 1 ---->| ESTABLISHED
  |   (May carry application payload data!)                   |
```

> [!NOTE]
> **SYN Flood Defense: Stateless SYN Cookies**:
> Attackers flood a server with spoofed `SYN` requests, consuming all kernel connection backlog memory. 
> With **SYN Cookies**, the server does NOT allocate memory upon receiving a SYN. Instead, it generates an initial sequence number ($server\_isn$) that is a cryptographic hash of the client IP, client port, secret key, and timestamp. Only when the client returns a valid ACK matching this cookie does the server allocate memory!

### 6.2 Connection Teardown & The `TIME_WAIT` State

```
CLIENT (initiates close)                                    SERVER
ESTABLISHED                                                 ESTABLISHED
  |-- (1) FIN=1, Seq=u -------------------------------------->| CLOSE_WAIT
  |   (Enters FIN_WAIT_1)                                     |
  |<-- (2) ACK=1, Ack=u + 1 ----------------------------------| (Server can still send data!)
  |   (Enters FIN_WAIT_2)                                     |
  |                                                           |
  |<-- (3) FIN=1, Seq=v --------------------------------------| LAST_ACK
  |                                                           |
  |-- (4) ACK=1, Ack=v + 1 ---------------------------------->| CLOSED
  |   (Enters TIME_WAIT for 2 * MSL)                          |
  v                                                           |
CLOSED (After timer expires)
```

- **Why is `TIME_WAIT` ($2 \times \text{MSL}$) Mandatory?**:
  1. **Ensure Graceful Closure**: If Client's final ACK (4) is lost, Server retransmits FIN (3). If Client were already CLOSED, it would reply with `RST`, causing the server to report an unnatural connection error.
  2. **Drain Old Duplicate Segments**: Maximum Segment Lifetime ($\text{MSL} \approx 30-60\,\text{s}$). Waiting $2 \times \text{MSL}$ ensures all wandering packets from the old connection incarnation die out before a new connection reuses the same port pair.

---

## 7. TCP Congestion Control & The AIMD Engine (Slides 31–49)

While Flow Control protects the receiver, Congestion Control protects the **intermediate network fabric**.

### 7.1 Effective Sending Window
The sender limits in-flight bytes to the minimum of the flow control window and the congestion window:
$$\text{Effective Window } (W) = \min(cwnd, rwnd)$$

### 7.2 Additive-Increase Multiplicative-Decrease (AIMD) (Slide 37)
- **Additive Increase**: Increase $cwnd$ by **$1\text{ MSS}$ every RTT** in the absence of packet loss.
- **Multiplicative Decrease**: Cut $cwnd$ in **half** ($cwnd \leftarrow cwnd / 2$) upon detecting loss.
- Produces the characteristic **Sawtooth Congestion Waveform**:

```
cwnd (MSS)
  ^
  |        /\              /\              /\
  |       /  \            /  \            /  \
  |      /    \          /    \          /    \
  |     /      \        /      \        /      \
  |    /        \      /        \      /        \
  |   /          \    /          \    /          \
  +----------------------------------------------------> Time
```

### 7.3 The Three Congestion Control Phases (Slides 40–44)

```
+-----------------------------------------------------------------------------------------+
|                           TCP CONGESTION CONTROL PHASES                                 |
|                                                                                         |
| 1. SLOW START:                                                                          |
|    - Initial State: cwnd = 1 MSS.                                                       |
|    - Growth: cwnd doubles every RTT (exponential growth: 1 -> 2 -> 4 -> 8 -> 16).       |
|    - Each received ACK increases cwnd by 1 MSS: cwnd = cwnd + MSS.                      |
|    - Threshold: When cwnd >= ssthresh, transition to Congestion Avoidance.              |
|                                                                                         |
| 2. CONGESTION AVOIDANCE:                                                                |
|    - Growth: Linear growth of 1 MSS per RTT.                                            |
|    - Each received ACK increments: cwnd = cwnd + MSS * (MSS / cwnd).                    |
|                                                                                         |
| 3. LOSS EVENT REACTIONS:                                                                |
|    (a) TIMEOUT (Severe Congestion):                                                     |
|        - ssthresh = cwnd / 2                                                            |
|        - cwnd = 1 MSS                                                                   |
|        - Re-enter SLOW START.                                                           |
|                                                                                         |
|    (b) TRIPLE DUPLICATE ACKS (Mild Congestion):                                         |
|        - TCP TAHOE: Treats 3 dup ACKs same as timeout (ssthresh=cwnd/2, cwnd=1).        |
|        - TCP RENO: Fast Recovery! Sets ssthresh = cwnd / 2, sets cwnd = ssthresh + 3,   |
|          and continues linear growth (skips Slow Start!).                               |
+-----------------------------------------------------------------------------------------+
```

```
TCP RENO CONGESTION EVOLUTION:
cwnd (MSS)
  ^
32|                   * Loss (3 Dup ACKs)
  |                  / \
  |                 /   \___ ssthresh = 16
16|        * ssthresh   /   \
  |       /|           /     \
 8|      / |          /       \
 4|     /  |         /
 2|    /   |        /
 1|---/----+-------+----------------------------------> RTT Rounds
   [Slow Start] [Congestion Avoidance] [Fast Recovery]
```

### 7.4 Macroscopic TCP Throughput Formulation (Slide 47)
During Congestion Avoidance, $cwnd$ fluctuates between $W/2$ and $W$.
$$\text{Average Window} = \frac{3}{4} W$$
$$\text{Average Throughput} \approx \frac{1.22 \times \text{MSS}}{\text{RTT} \times \sqrt{L}}$$
where $L$ is the fraction of lost packets.

---

## 8. Master Comparison Matrix: TCP Variants

| Dimension | TCP Tahoe (1988) | TCP Reno (1990) | TCP NewReno (1999) |
| :--- | :--- | :--- | :--- |
| **Timeout Event** | $ssthresh = cwnd / 2$, $cwnd = 1$ | $ssthresh = cwnd / 2$, $cwnd = 1$ | $ssthresh = cwnd / 2$, $cwnd = 1$ |
| **3 Duplicate ACKs** | Cuts $cwnd = 1\text{ MSS}$ (Slow Start) | **Fast Recovery**: $cwnd = ssthresh + 3$ | Refined Fast Recovery for multiple losses in one window |
| **Recovery Efficiency** | Terrible (stalls on loss) | Excellent for single packet loss | Excellent for multiple packet losses |
| **Throughput Waveform** | Repetitive drops to 1 MSS | Smooth sawtooth around $ssthresh$ | Smooth sawtooth |

---

## 9. High-Yield Open-Book Exam Traps & Examiner Tricks

1. **The Sequence Number Indexing Trap**:
   - *Trap*: Numbering sequence numbers by packet count ($0, 1, 2, 3$).
   - *Fact*: TCP sequence numbers track **bytes, NOT packets**! If packet 1 has `Seq = 1` and length $1,000\,\text{bytes}$, packet 2 has `Seq = 1001`.
2. **The 3-Duplicate ACK Counting Trap**:
   - *Trap*: Thinking Fast Retransmit triggers on the 3rd ACK.
   - *Fact*: It triggers on the **3rd DUPLICATE ACK** (which is the **4th identical ACK** received).
3. **The Slow Start Misnomer Trap**:
   - *Question*: *"Why is it called Slow Start if it grows exponentially?"*
   - *Fact*: It starts "slowly" from a tiny window of $1\text{ MSS}$ (compared to blasting full link capacity), but its growth rate is the fastest possible (exponential doubling every RTT).
4. **The `TIME_WAIT` Originator Trap**:
   - *Question*: *"Which host enters the `TIME_WAIT` state?"*
   - *Fact*: The host that **initiates the active close** (sends the first `FIN`). The passive closer transitions directly from `LAST_ACK` to `CLOSED`.

---

## 10. Solved High-Yield Numerical Exam Problems

### Problem 1: Jacobson's Adaptive Timeout Calculation
**Problem Statement**:
A TCP connection has a current `EstimatedRTT = 40 ms` and `DevRTT = 5 ms`.
A new sample is measured: `SampleRTT = 60 ms`.
Standard parameters are used: $\alpha = 0.125$, $\beta = 0.25$.
1. Calculate the new `EstimatedRTT`.
2. Calculate the new `DevRTT`.
3. Compute the new `TimeoutInterval`.

**Step-by-Step Solution**:

1. **Compute New EstimatedRTT**:
   $$\text{EstimatedRTT}_{\text{new}} = (1 - \alpha) \cdot \text{EstimatedRTT} + \alpha \cdot \text{SampleRTT}$$
   $$\text{EstimatedRTT}_{\text{new}} = (1 - 0.125) \times 40 + 0.125 \times 60 = 0.875 \times 40 + 7.5 = 35 + 7.5 = \mathbf{42.5\,\text{ms}}$$

2. **Compute New DevRTT**:
   $$\text{Sample Difference} = |\text{SampleRTT} - \text{EstimatedRTT}_{\text{old}}| = |60 - 40| = 20\,\text{ms}$$
   $$\text{DevRTT}_{\text{new}} = (1 - \beta) \cdot \text{DevRTT} + \beta \cdot |\text{SampleRTT} - \text{EstimatedRTT}_{\text{old}}|$$
   $$\text{DevRTT}_{\text{new}} = (1 - 0.25) \times 5 + 0.25 \times 20 = 3.75 + 5.0 = \mathbf{8.75\,\text{ms}}$$

3. **Compute New TimeoutInterval**:
   $$\text{TimeoutInterval} = \text{EstimatedRTT}_{\text{new}} + 4 \cdot \text{DevRTT}_{\text{new}}$$
   $$\text{TimeoutInterval} = 42.5 + (4 \times 8.75) = 42.5 + 35.0 = \mathbf{77.5\,\text{ms}}$$

---

### Problem 2: TCP Tahoe vs. Reno Congestion Window Trace
**Problem Statement**:
A TCP connection has an initial threshold $ssthresh = 16\,\text{MSS}$ and begins at Round 1 with $cwnd = 1\,\text{MSS}$.
- At Round 8, a triple duplicate ACK event occurs when $cwnd$ has reached $20\,\text{MSS}$.
- At Round 13, a retransmission timeout occurs.
Construct the complete window trace table for both **TCP Tahoe** and **TCP Reno** from Round 1 through Round 15.

**Step-by-Step Solution**:

1. **Trace Rules**:
   - **Slow Start**: $cwnd$ doubles each round while $cwnd < ssthresh$.
   - **Congestion Avoidance**: $cwnd$ increments by $1\,\text{MSS}$ each round when $cwnd \ge ssthresh$.
   - **Triple Dup ACKs at Round 8 ($cwnd = 20$)**:
     - New threshold: $ssthresh = 20 / 2 = 10\,\text{MSS}$.
     - Tahoe: drops to $cwnd = 1\,\text{MSS}$ (Slow Start).
     - Reno: enters Fast Recovery, sets $cwnd = ssthresh + 3 = 13$, defers to $cwnd = 10$ and increases linearly.
   - **Timeout at Round 13**:
     - Both Tahoe and Reno set $ssthresh = cwnd / 2$ and drop to $cwnd = 1\,\text{MSS}$.

2. **Round-by-Round Execution Table**:

| Round # | Phase (Reno) | Tahoe $cwnd$ | Reno $cwnd$ | Reno $ssthresh$ | Explanation |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1** | Slow Start | 1 | 1 | 16 | Exponential growth starts |
| **2** | Slow Start | 2 | 2 | 16 | Doubled |
| **3** | Slow Start | 4 | 4 | 16 | Doubled |
| **4** | Slow Start | 8 | 8 | 16 | Doubled |
| **5** | Slow Start | 16 | 16 | 16 | Hits $ssthresh$ |
| **6** | Congestion Avoidance | 17 | 17 | 16 | Linear growth (+1) |
| **7** | Congestion Avoidance | 18 | 18 | 16 | Linear growth (+1) |
| **8** | Congestion Avoidance | 20 | 20 | 16 | **Loss: 3 Dup ACKs occur!** |
| **9** | Recovery / Slow Start | **1** | **11** | **10** | Tahoe $\to 1$; Reno $\to ssthresh+1 = 11$ |
| **10** | Linear / Slow Start | 2 | 12 | 10 | Tahoe doubles (SS); Reno grows linearly |
| **11** | Linear / Slow Start | 4 | 13 | 10 | Tahoe doubles (SS); Reno grows linearly |
| **12** | Linear / Slow Start | 8 | 14 | 10 | Tahoe doubles (SS); Reno grows linearly |
| **13** | **Timeout Event!** | 10 | 15 | 10 | **Timeout occurs!** |
| **14** | Slow Start | **1** | **1** | **7** | Both set $ssthresh = 15/2 = 7$, $cwnd = 1$ |
| **15** | Slow Start | 2 | 2 | 7 | Both double in Slow Start |

---

## 11. Ultra-Fast Exam Revision Checklist
- [ ] TCP provides point-to-point, full-duplex, reliable byte stream service; MSS typically 1,460 bytes.
- [ ] TCP header is 20 bytes fixed (up to 60 bytes with options); Sequence and ACK numbers are 32 bits and byte-oriented.
- [ ] Fast Retransmit: Triggered by 3 duplicate ACKs (4 identical ACKs total), avoiding timeout delay.
- [ ] Flow Control: Receiver advertises available buffer in `rwnd`; sender ensures unacknowledged data $\le rwnd$.
- [ ] Zero-Window Deadlock: Solved by sender transmitting 1-byte probe packets using persistence timer.
- [ ] Handshake: 3-way SYN $\to$ SYN-ACK $\to$ ACK; Teardown: 4-way FIN $\to$ ACK $\to$ FIN $\to$ ACK.
- [ ] `TIME_WAIT`: State held by active closer for $2 \times \text{MSL}$ to ensure final ACK delivery and drain duplicate packets.
- [ ] AIMD: Additive increase by $1\text{ MSS}$ per RTT; multiplicative decrease by $50\%$ on loss.
- [ ] Slow Start: Starts at $1\text{ MSS}$, doubles every RTT until $cwnd \ge ssthresh$.
- [ ] Tahoe drops to $cwnd = 1$ on 3 dup ACKs; Reno sets $cwnd = ssthresh$ (Fast Recovery) and continues linear growth.
