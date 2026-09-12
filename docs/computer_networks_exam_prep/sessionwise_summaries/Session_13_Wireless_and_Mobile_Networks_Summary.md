# Computer Networks (BSDCBZC481)
# Session 13: Wireless & Mobile Networks — 802.11 (Wi-Fi), CDMA, Cellular & Mobile IP
### Exhaustive Slide-by-Slide Academic Exam Revision Manual & Problem Solving Guide

---

## 1. Session Context & Pedagogical Scope
- **Course Code & Title**: BSDCBZC481 — Computer Networks
- **Instructor**: Dr. K. Kalaiselvi (BITS Pilani)
- **Primary Textbooks**:
  - J.F. Kurose & K.W. Ross, *Computer Networking: A Top-Down Approach*, 5th/6th Edition, Chapter 6 (T1)
  - B.A. Forouzan, *Data Communications and Networking*, 4th Edition, Chapters 14, 16, & 22 (T2)
- **Lecture Slide Mapping**: CS13: Wireless and Mobile Networks — Slides 1 to 41 (Complete Coverage)
- **Core Syllabus Covered**:
  1. Wireless Physical Link Characteristics: Path Loss ($1/d^2$), Multipath Propagation & Interference
  2. Code Division Multiple Access (CDMA): Orthogonal Chip Sequences & Algebraic Inner Product Decoding
  3. IEEE 802.11 (Wi-Fi) Architecture: Basic Service Sets (BSS), Access Points (AP) & Passive/Active Scanning
  4. The Hidden Terminal & Exposed Terminal Phenomena
  5. CSMA/CA Protocol Mechanics: DIFS, SIFS, Random Backoff & The RTS/CTS Reservation Handshake
  6. The Network Allocation Vector (NAV) & Virtual Carrier Sensing
  7. Cellular Network Architecture Evolution: 2G/3G/4G LTE (EPC Core) & 5G NR (Massive MIMO, Slicing)
  8. Mobility Architecture & Mobile IP (RFC 5944): Home Agents, Foreign Agents & Care-of-Addresses (CoA)
  9. Indirect Routing (IP-in-IP Encapsulation Tunneling) vs. Direct Routing & Triangle Inefficiencies
  10. High-Yield Open-Book Exam Traps, Rigorous Numerical Problems & Fast Revision Checklist

---

## 2. Wireless Physical Link Characteristics & CDMA (Slides 3–11)

### 2.1 The Physics of Wireless Channels
Unlike shielded wired copper or fiber optic conduits, wireless electromagnetic transmission faces severe physical propagation hazards:
1. **Path Loss & Attenuation**: As an unguided radio wave expands outward, its power density attenuates according to the inverse-square law:
   $$P_r \propto \frac{P_t}{d^n} \quad (n \approx 2 \text{ in free space, } 3-4 \text{ in urban environments})$$
2. **Multipath Propagation**: Radio waves reflect off buildings, terrain, and walls. Reflected copies arrive at the receiver slightly delayed in time with varying phase shifts, causing destructive interference, fading, and **Inter-Symbol Interference (ISI)**.
3. **Interference from Competing Emitters**: The unlicensed $2.4\,\text{GHz}$ Industrial, Scientific, and Medical (ISM) band is simultaneously populated by 802.11b/g/n Wi-Fi, Bluetooth, microwave ovens, and cordless phones.
4. **SNR vs. BER Tradeoff**: Higher transmission rates demand higher Signal-to-Noise Ratios (SNR) to maintain acceptable Bit Error Rates (BER). Modern Wi-Fi interfaces dynamically adapt modulation schemes (e.g., switching from 64-QAM to QPSK when moving away from an AP).

---

## 3. Code Division Multiple Access (CDMA) Mathematical Formulation (Slides 8–11)

CDMA is a channel-partitioning technique where multiple transmitters share the **exact same frequency spectrum simultaneously**, separating signals algebraically via unique orthogonal codes.

```
+-------------------------------------------------------------------------+
|                              CDMA ENCODING                              |
|                                                                         |
| Let sender m be assigned an M-bit chip sequence:                        |
|                     d_m in { -1, +1 }^M                                 |
|                                                                         |
| Orthogonality Condition:                                                |
| For any two different senders i and j:                                  |
|                     (1 / M) * ( d_i . d_j ) = 0   (when i != j)         |
|                     (1 / M) * ( d_i . d_i ) = 1   (self inner product)  |
|                                                                         |
| Encoding Rule:                                                          |
| If sender m wants to transmit data bit 1:    Transmits:  +d_m           |
| If sender m wants to transmit data bit 0:    Transmits:  -d_m           |
| If sender m is idle:                         Transmits:   0             |
+-------------------------------------------------------------------------+
```

### 3.1 Composite Signal Over the Air
When $N$ senders transmit concurrently, their signals superimpose linearly over the shared physical channel:
$$S = \sum_{m=1}^N Z_m \cdot \mathbf{d}_m$$
where $Z_m \in \{+1, -1, 0\}$ represents sender $m$'s data bit.

### 3.2 Receiver Algebraic Decoding
To extract the data bit transmitted by sender $i$, the receiver computes the normalized inner product of the received composite signal $S$ with sender $i$'s known chip sequence $\mathbf{d}_i$:
$$\text{Decoded Bit } Z_i = \frac{1}{M} (S \cdot \mathbf{d}_i) = \frac{1}{M} \left( \sum_{m=1}^N Z_m \mathbf{d}_m \right) \cdot \mathbf{d}_i$$
$$= \frac{1}{M} \left( Z_i (\mathbf{d}_i \cdot \mathbf{d}_i) + \sum_{m \ne i} Z_m (\mathbf{d}_m \cdot \mathbf{d}_i) \right)$$
Since all other chip sequences are orthogonal ($\mathbf{d}_m \cdot \mathbf{d}_i = 0$ for $m \ne i$) and $\frac{1}{M}(\mathbf{d}_i \cdot \mathbf{d}_i) = 1$:
$$Z_i = Z_i (1) + 0 = \mathbf{Z_i}$$
All competing transmissions vanish algebraically!

---

## 4. IEEE 802.11 (Wi-Fi) Architecture & Scanning (Slides 12–19)

### 4.1 Architectural Entities
- **Basic Service Set (BSS)**: The fundamental building block of an 802.11 LAN. Contains one or more wireless stations (STAs) and a central **Access Point (AP)** in infrastructure mode.
- **Service Set Identifier (SSID)**: Human-readable name assigned to the BSS (e.g., `BITS-Campus-WiFi`).
- **Extended Service Set (ESS)**: Multiple interconnected BSSs joined together via a wired distribution network (switched Ethernet), allowing seamless roaming under a single SSID.

```
+-------------------------------------------------------------------------+
|                    EXTENDED SERVICE SET (ESS)                           |
|                                                                         |
|   [ BSS 1 ]                                            [ BSS 2 ]        |
|  [Host A]                                            [Host B]           |
|     \                                                   /               |
|    [ AP 1 ] <====== Distribution Switch (Ethernet) =====> [ AP 2 ]      |
+-------------------------------------------------------------------------+
```

### 4.2 Passive vs. Active Scanning
1. **Passive Scanning**: APs periodically broadcast **Beacon Frames** containing the AP's SSID, supported data rates, and MAC address. The wireless host passively listens across channels to discover available networks.
2. **Active Scanning**: The wireless client actively broadcasts a **Probe Request frame** on each radio channel. APs within transmission range respond with a unicast **Probe Response frame**.

---

## 5. The Hidden & Exposed Terminal Problems (Slides 20–22)

### 5.1 The Hidden Terminal Problem
Consider three nodes $A$, $B$, and $C$:

```
[ Node A ] --------------> [ Access Point B ] <-------------- [ Node C ]
 (Range of A: Covers B,                             (Range of C: Covers B,
  Does NOT reach C)                                  Does NOT reach A)
```
- Node A can transmit to AP B; Node C can transmit to AP B.
- However, physical distance or a physical obstacle (e.g., concrete wall) prevents Node A and Node C from hearing each other's radio transmissions.
- **The Catastrophe**: Node A senses the channel idle and transmits to B. Node C also senses the channel idle and transmits to B at the same time. **A severe collision occurs at AP B**, destroying both transmissions! Standard CSMA fails completely.

### 5.2 The Exposed Terminal Problem
- Node B is transmitting to Node A.
- Node C wishes to transmit to Node D (where D is out of range of B and A).
- Node C senses the channel, hears Node B's transmission, and falsely assumes the channel is occupied. Node C needlessly defers its transmission to D, wasting channel throughput!

---

## 6. CSMA/CA Protocol & The RTS/CTS Mechanism (Slides 23–27)

### 6.1 Why Wi-Fi Cannot Use Collision Detection (CSMA/CD)
1. **Transmitter Saturation**: The energy transmitted by a wireless NIC is orders of magnitude greater than incoming received signals ($100,000\times$ stronger). A transmitting radio drowns out its own receiver circuitry, making it hardware-impossible to detect a weak colliding signal while transmitting (half-duplex constraint).
2. **Hidden Terminals**: Even if a station could detect collisions locally, collisions occur at the **receiver (AP)**, not at the transmitter!

### 6.2 CSMA/CA Protocol Timeline (Slide 24)

```
Sender                                                    Receiver (AP)
  |                                                           |
  |--- Senses link idle for DIFS interval ------------------->|
  |    (Selects random backoff timer)                         |
  |--- Transmits Data Frame --------------------------------->|
  |                                                           |--- Processes Frame (SIFS)
  |<-- Receives ACK (Confirms error-free delivery) -----------|
```
- **DIFS (Distributed Inter-Frame Space)**: Mandatory idle period sender must observe before transmitting or counting down backoff.
- **SIFS (Short Inter-Frame Space)**: Ultra-short turnaround delay reserved exclusively for high-priority immediate control responses (ACKs, CTS). Because $\text{SIFS} < \text{DIFS}$, ACKs always preempt new data transmissions!

### 6.3 Virtual Carrier Sensing via RTS/CTS (Slides 25–27)
To completely eliminate collisions from hidden terminals, 802.11 employs short channel reservation frames:

```
Sender (Host A)            Receiver (AP B)            Hidden Terminal (Host C)
  |                               |                              |
  |--- (1) RTS (Duration=500us)-> |                              | (Cannot hear RTS)
  |                               |                              |
  |                               |--- (2) CTS (Duration=450us)->| (Hears CTS!)
  |<-- Receives CTS --------------|                              | Sets NAV = 450us!
  |                               |                              | (Enters silence)
  |=== (3) Transmits Data Frame =>|                              |
  |                               |                              |
  |<-- (4) Receives ACK ----------|                              | NAV expires
  v                               v                              v (Resumes sensing)
```

1. Host A broadcasts a short **Request to Send (RTS)** frame ($20\,\text{bytes}$) specifying the total time required to transmit the data frame and receive the ACK.
2. AP B broadcasts a **Clear to Send (CTS)** frame ($14\,\text{bytes}$) granting exclusive transmission rights.
3. **Network Allocation Vector (NAV)**: Node C (the hidden terminal) hears the CTS broadcast by AP B. It inspects the duration field and sets its internal **NAV countdown timer**. Node C remains completely silent until the entire data frame and ACK have concluded, **preventing collisions completely**!

---

## 7. Cellular Network Architecture Evolution (Slides 28–32)

Cellular systems divide geographic territory into hexagonal cells, each serviced by a cellular base station transceiver.

```
+-------------------------------------------------------------------------+
|                  CELLULAR 4G LTE ARCHITECTURE (E-UTRAN)                 |
|                                                                         |
|  [ Mobile UE ]                                                          |
|       \ (LTE-Uu Radio)                                                  |
|     [ eNodeB Base Station ]                                             |
|          |                                                              |
|          +--------------------+---------------------+                   |
|          | S1-MME (Control)   | S1-U (Data)         |                   |
|          v                    v                     v                   |
|        [ MME ]            [ S-GW ]              [ HSS ]                 |
|   (Mobility Mgmt)      (Serving Gateway)    (Home Subscriber)           |
|                               |                     |                   |
|                               v                     v                   |
|                           [ P-GW ] ===========> [ Public Internet ]     |
|                       (Packet Gateway)                                  |
+-------------------------------------------------------------------------+
```

### 7.1 Generations Breakdown
- **2G (GSM)**: Digital circuit-switched voice ($9.6-14.4\,\text{kbps}$); GPRS/EDGE added packet switching.
- **3G (UMTS / CDMA2000)**: Mobile broadband ($384\,\text{kbps}-2\,\text{Mbps}$) integrating voice and data.
- **4G LTE (Long Term Evolution)**: Complete all-IP flat architecture. Replaced circuit switching entirely with packet switching (VoLTE). Employs Orthogonal Frequency Division Multiple Access (OFDMA) and MIMO antenna arrays ($100\,\text{Mbps}-1\,\text{Gbps}$).
- **5G New Radio (NR)**: Ultra-dense small cells, Millimeter Wave (mmWave: $24-100\,\text{GHz}$), Beamforming, Massive MIMO ($64\times64$), and **Network Slicing** (tailoring virtual networks for eMBB, mMTC, and URLLC with $< 1\,\text{ms}$ latency).

---

## 8. Mobile IP & Mobility Management (Slides 33–41)

### 8.1 The Fundamental Mobility Problem
A mobile laptop travels from its home university network (`128.119.40.0/24`) to a hotel Wi-Fi network (`192.168.1.0/24`).
- If the mobile host changes its IP address to match the hotel subnet, all existing active TCP connections break immediately (because TCP sockets are permanently bound to the 4-tuple: `(Src IP, Src Port, Dst IP, Dst Port)`).
- If the mobile host retains its home IP address, the hotel's edge routers cannot route packets to it because the Internet routes packets based on destination IP prefix!

### 8.2 Architectural Entities (Slide 35)
1. **Mobile Node (MN)**: The roaming host.
2. **Permanent Home Address**: Permanent IP address assigned to MN in its home network.
3. **Home Agent (HA)**: A router inside MN's home network that maintains location tracking and intercepts packets.
4. **Foreign Agent (FA)**: A router in the visited foreign network that assists the mobile node.
5. **Care-of-Address (CoA)**: A temporary IP address associated with the MN while visiting the foreign network.

### 8.3 Indirect Routing (Triangle Routing) Walkthrough (Slides 37–39)

```
CORRESPONDENT                                HOME NETWORK
(Wants to send to MN)                       [ Home Agent ]
        |                                          |
        |--- (1) IP Datagram (Dst: Home Address) ->| (Intercepts packet via Proxy ARP)
        |                                          |
        |                                          |--- (2) Tunnels datagram inside new
        |                                          |    outer IP header (Dst: CoA)
        |                                          |    (IP-in-IP Encapsulation)
        |                                          v
        |                                    FOREIGN NETWORK
        |<-- (4) Sends reply directly ------ [ Foreign Agent ]
        |    (Dst: Correspondent IP)               | (Decapsulates packet)
        |                                          v
        |                                    [ Mobile Node ]
```

1. **Registration**: Upon arriving in foreign network, MN acquires a CoA from FA and registers it with its Home Agent via a secure registration message.
2. **Step 1 (Transmission)**: Correspondent sends datagrams addressed to MN's permanent Home Address.
3. **Step 2 (Interception & Encapsulation)**: The Home Agent advertises proxy ARP for MN, intercepts the packets, and wraps them in a new IP header directed to the CoA (**IP-in-IP Tunneling**).
4. **Step 3 (Decapsulation)**: Foreign Agent extracts the original datagram and hands it to MN.
5. **Step 4 (Direct Egress Reply)**: MN replies directly to the Correspondent without traversing the home network.

> [!WARNING]
> **Triangle Routing Inefficiency**:
> Datagrams destined for the mobile node must travel a massive detour through the home agent, even if the Correspondent and Mobile Node are sitting in the same room on the same foreign subnet!

---

## 9. Master Architectural Comparison Matrix

| Dimension | Wired Ethernet (802.3) | Wireless Wi-Fi (802.11) | Mobile Cellular (4G LTE) |
| :--- | :--- | :--- | :--- |
| **Physical Medium** | Copper twisted pair / Fiber | Radio RF ($2.4\,\text{GHz}, 5\,\text{GHz}$) | Licensed cellular spectrum |
| **Multiple Access** | **CSMA/CD** (Collision Detect) | **CSMA/CA** (Collision Avoidance) | **OFDMA / SC-FDMA** |
| **Collision Resolution**| Aborts immediately; Jam Signal | Random backoff; RTS/CTS reservation | Centralized scheduled resource blocks |
| **Addressing** | 48-bit MAC Address | 48-bit MAC Address (4 address fields)| IMSI / GUTI / IP Address |
| **Mobility Support** | None (stationary cables) | Local BSS roaming within ESS | **Seamless high-speed hard/soft handover**|
| **Link Reliability** | High ($BER \approx 10^{-12}$) | Low/Variable ($BER \approx 10^{-4}$)| Controlled via HARQ ($BER \approx 10^{-6}$)|

---

## 10. High-Yield Open-Book Exam Traps & Examiner Tricks

1. **The Wi-Fi Collision Detection Trap**:
   - *Question*: *"Why does 802.11 implement Collision Avoidance (CA) instead of Collision Detection (CD)?"*
   - *Fact*: Wireless transmitters drown out their own receiver circuitry (half-duplex hardware constraint), and collisions occur at the remote receiver due to hidden terminals.
2. **The RTS/CTS Overhead Trap**:
   - *Question*: *"Does 802.11 use RTS/CTS frames for every single data packet?"*
   - *Fact*: **NO!** RTS/CTS incurs significant protocol overhead ($2 \times RTT$). Wi-Fi uses an **RTS Threshold**; only data packets *larger* than the threshold (e.g., $> 2,346\,\text{bytes}$) trigger RTS/CTS reservation.
3. **The Mobile IP Correspondent Trap**:
   - *Question*: *"In standard indirect Mobile IP, must the Correspondent update its networking software to communicate with a mobile node?"*
   - *Fact*: **No!** The entire mobility process is completely transparent to the Correspondent. The Correspondent sends standard datagrams to the static Home Address; the Home Agent handles all tunneling.

---

## 11. Solved High-Yield Numerical Exam Problems

### Problem 1: CDMA Encoding & Inner Product Decoding
**Problem Statement**:
Two CDMA transmitters, A and B, share a wireless channel.
They are assigned the following 8-bit orthogonal chip sequences:
- Sender A: $\mathbf{d}_A = (+1, +1, +1, -1, +1, -1, -1, -1)$
- Sender B: $\mathbf{d}_B = (+1, -1, +1, +1, +1, +1, -1, +1)$
1. Verify that the chip sequences $\mathbf{d}_A$ and $\mathbf{d}_B$ are mathematically orthogonal.
2. Sender A wants to transmit data bit $1$; Sender B wants to transmit data bit $0$. Write down the resulting composite signal $S$ transmitted over the channel.
3. Show step-by-step how a receiver extracts Sender A's data bit from the composite signal $S$.

**Step-by-Step Solution**:

1. **Verify Orthogonality**:
   $$\mathbf{d}_A \cdot \mathbf{d}_B = \sum_{k=1}^8 d_A(k) \cdot d_B(k)$$
   - Element-by-element product:
     - $k=1$: $(+1)(+1) = +1$
     - $k=2$: $(+1)(-1) = -1$
     - $k=3$: $(+1)(+1) = +1$
     - $k=4$: $(-1)(+1) = -1$
     - $k=5$: $(+1)(+1) = +1$
     - $k=6$: $(-1)(+1) = -1$
     - $k=7$: $(-1)(-1) = +1$
     - $k=8$: $(-1)(+1) = -1$
   - Sum: $(+1) + (-1) + (+1) + (-1) + (+1) + (-1) + (+1) + (-1) = \mathbf{0}$.
   - Normalized: $\frac{1}{8}(0) = \mathbf{0}$. **Orthogonality verified!**

2. **Generate Transmitted Signals**:
   - Sender A transmits bit $1 \implies \mathbf{S}_A = +1 \cdot \mathbf{d}_A = (+1, +1, +1, -1, +1, -1, -1, -1)$.
   - Sender B transmits bit $0 \implies \mathbf{S}_B = -1 \cdot \mathbf{d}_B = (-1, +1, -1, -1, -1, -1, +1, -1)$.
   - Composite over-the-air signal:
     $$\mathbf{S} = \mathbf{S}_A + \mathbf{S}_B = (0, +2, 0, -2, 0, -2, 0, -2)$$

3. **Decode Sender A's Data Bit**:
   $$\text{Decoded Value} = \frac{1}{8} (\mathbf{S} \cdot \mathbf{d}_A)$$
   - Compute inner product:
     - $k=1$: $(0)(+1) = 0$
     - $k=2$: $(+2)(+1) = +2$
     - $k=3$: $(0)(+1) = 0$
     - $k=4$: $(-2)(-1) = +2$
     - $k=5$: $(0)(+1) = 0$
     - $k=6$: $(-2)(-1) = +2$
     - $k=7$: $(0)(-1) = 0$
     - $k=8$: $(-2)(-1) = +2$
   - Sum $= 0 + 2 + 0 + 2 + 0 + 2 + 0 + 2 = \mathbf{+8}$.
   - Normalized result:
     $$\text{Result} = \frac{+8}{8} = \mathbf{+1} \implies \mathbf{\text{Bit 1 received!}}$$

---

### Problem 2: Wi-Fi RTS/CTS Channel Reservation Timing
**Problem Statement**:
An 802.11b station transmits a $1,500\text{-byte}$ data frame using RTS/CTS reservation on an $11\,\text{Mbps}$ channel.
- Frame parameters:
  - RTS frame $= 20\,\text{bytes}$.
  - CTS frame $= 14\,\text{bytes}$.
  - ACK frame $= 14\,\text{bytes}$.
  - Data frame $= 1,500\,\text{bytes}$.
- Timing parameters:
  - $\text{SIFS} = 10\,\mu\text{s}$.
  - $\text{DIFS} = 50\,\mu\text{s}$.
  - Propagation delay $d_{\text{prop}} = 1\,\mu\text{s}$.
Calculate the exact Network Allocation Vector (NAV) value contained in the RTS frame.

**Step-by-Step Solution**:

1. **Calculate Frame Transmission Times**:
   - $R = 11\,\text{Mbps} = 11 \times 10^6\,\text{bps}$.
   - $T_{\text{CTS}} = \frac{14 \times 8}{11 \times 10^6} = \frac{112}{11 \times 10^6} \approx 10.18\,\mu\text{s}$.
   - $T_{\text{Data}} = \frac{1,500 \times 8}{11 \times 10^6} = \frac{12,000}{11 \times 10^6} \approx 1,090.91\,\mu\text{s}$.
   - $T_{\text{ACK}} = \frac{14 \times 8}{11 \times 10^6} \approx 10.18\,\mu\text{s}$.

2. **RTS Duration (NAV) Definition**:
   The RTS duration field reserves the entire sequence following the RTS:
   $$\text{NAV}_{\text{RTS}} = \text{SIFS} + T_{\text{CTS}} + d_{\text{prop}} + \text{SIFS} + T_{\text{Data}} + d_{\text{prop}} + \text{SIFS} + T_{\text{ACK}} + d_{\text{prop}}$$
   - Summing components:
     - 3 SIFS intervals $= 3 \times 10\,\mu\text{s} = 30\,\mu\text{s}$.
     - 3 Propagation delays $= 3 \times 1\,\mu\text{s} = 3\,\mu\text{s}$.
     - Transmission times $= 10.18 + 1,090.91 + 10.18 = 1,111.27\,\mu\text{s}$.
   $$\text{NAV}_{\text{RTS}} = 30 + 3 + 1,111.27 = \mathbf{1,144.27\,\mu\text{s}}$$

---

## 12. Ultra-Fast Exam Revision Checklist
- [ ] Wireless challenges: Path loss ($1/d^2$), multipath propagation (ISI/fading), interference ($2.4\,\text{GHz}$).
- [ ] CDMA: All users share same spectrum; separate via orthogonal chip sequences ($\mathbf{d}_i \cdot \mathbf{d}_j = 0$).
- [ ] 802.11 cannot use CSMA/CD due to transmitter power saturation and hidden terminals; uses CSMA/CA.
- [ ] Hidden Terminal: Nodes cannot hear each other; collide at AP. Solved by RTS/CTS reservation and NAV timer.
- [ ] Exposed Terminal: Node defers unnecessarily when hearing neighbor's transmission to another target.
- [ ] Inter-Frame Spaces: $\text{SIFS} < \text{DIFS}$. SIFS gives priority to immediate ACKs and CTS.
- [ ] 4G LTE EPC Core: MME (mobility), S-GW (data), P-GW (Internet gateway), HSS (subscriber database).
- [ ] Mobile IP: Permanent Home Address + temporary Care-of-Address (CoA) in foreign network.
- [ ] Triangle Routing: Correspondent $\to$ Home Agent $\to$ (IP-in-IP tunnel) $\to$ Foreign Agent $\to$ Mobile Node.
