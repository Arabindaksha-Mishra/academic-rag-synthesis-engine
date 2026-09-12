# Computer Networks (BSDCBZC481)
# Session 15: Physical Layer Transmission, Multiplexing & Comprehensive Course Review
### Exhaustive Slide-by-Slide Academic Exam Revision Manual & Problem Solving Guide

---

## 1. Session Context & Pedagogical Scope
- **Course Code & Title**: BSDCBZC481 — Computer Networks
- **Instructor**: Dr. K. Kalaiselvi (BITS Pilani)
- **Primary Textbooks**:
  - B.A. Forouzan, *Data Communications and Networking*, 4th Edition, Chapters 3, 4, 5, 6, & 7 (T2)
  - J.F. Kurose & K.W. Ross, *Computer Networking: A Top-Down Approach*, 5th/6th Edition, Chapters 1 & 9 (T1)
- **Lecture Slide Mapping**: CS15: Physical Layer and Medium — Slides 1 to 45 (Complete Coverage)
- **Core Syllabus Covered**:
  1. Data & Signal Fundamentals: Analog vs. Digital Signals, Sine Waves, Frequency, Period, Phase & Wavelength
  2. Theoretical Channel Capacity Bounds: Nyquist Maximum Bit Rate & Shannon Noisy Channel Capacity
  3. Digital Transmission & Analog-to-Digital Conversion: Pulse Code Modulation (PCM) & Nyquist Sampling
  4. Digital-to-Analog Modulation: ASK, FSK, PSK, QAM & Constellation Diagrams
  5. Multiplexing Paradigms: Frequency-Division Multiplexing (FDM), Wavelength-Division Multiplexing (WDM) & Time-Division Multiplexing (TDM)
  6. Guided Physical Media: Twisted Pair (UTP/STP, RJ-45), Coaxial (RG Ratings, BNC) & Optical Fiber Physics
  7. Optical Fiber Propagation Modes: Step-Index, Graded-Index, Single-Mode & Fiber Connectors (SC, ST, MT-RJ)
  8. Unguided Physical Media: Radio Waves ($3\,\text{kHz}-1\,\text{GHz}$), Microwaves ($1-300\,\text{GHz}$) & Infrared ($300\,\text{GHz}-400\,\text{THz}$)
  9. Comprehensive Course Synthesis: End-to-End Walkthrough of the 5-Layer Internet Protocol Stack
  10. High-Yield Open-Book Exam Traps, Rigorous Numerical Problems & Fast Revision Checklist

---

## 2. Data & Signals Fundamentals (Slide 3)

The physical layer is the lowest layer of the OSI and TCP/IP protocol suites, responsible for transmitting raw, unstructured bits over physical communication channels.

### 2.1 Analog vs. Digital Signals
- **Analog Signal**: A continuous wave that varies smoothly and continuously over time, capable of taking an infinite number of values within a given range (e.g., human voice).
- **Digital Signal**: A discrete signal that can take only a limited number of defined amplitude values (typically binary: high voltage representing bit 1, low voltage representing bit 0).

```
ANALOG SINE WAVE:                              DIGITAL SQUARE WAVE:
Voltage                                        Voltage
  ^     /\          /\                           ^     +---+       +---+
  |    /  \        /  \                          |     |   |       |   |
  |---/----\------/----\---> Time                |-----|---|-------|---|---> Time
  |  /      \    /      \                        |     |   |       |   |
  v          \__/        \__/                    v     +   +---+   +   +---+
```

### 2.2 Mathematical Characteristics of a Sine Wave
An analog signal is characterized by the sinusoidal equation:
$$s(t) = A \sin(2\pi f t + \phi)$$

1. **Peak Amplitude ($A$)**: The absolute maximum value of the signal voltage or electrical field strength (measured in Volts).
2. **Period ($T$)**: The time (in seconds) required for a signal to complete one full cycle.
3. **Frequency ($f$)**: The number of complete cycles per second (measured in Hertz, $\text{Hz}$):
   $$f = \frac{1}{T} \quad \text{and} \quad T = \frac{1}{f}$$
4. **Phase ($\phi$)**: The relative position of the wave at time $t = 0$, measured in degrees or radians ($360^\circ = 2\pi\text{ radians}$).
5. **Wavelength ($\lambda$)**: The physical distance an electromagnetic wave travels in one period:
   $$\lambda = \frac{c}{f} = c \times T$$
   where $c$ is the speed of light in the medium ($\approx 2 \times 10^8\,\text{m/s}$ in copper/glass, $3 \times 10^8\,\text{m/s}$ in vacuum).

---

## 3. Theoretical Limits of Data Transmission (Slide 3)

Two foundational mathematical laws dictate the absolute theoretical upper limit of data transmission across any communication channel.

### 3.1 Nyquist Maximum Bit Rate (Noiseless Channel)
Formulated in 1928 by Harry Nyquist, this theorem determines the maximum theoretical bit rate of an ideal channel completely free of noise:
$$\mathbf{C_{\text{Nyquist}} = 2B \log_2(M) \quad \text{(bps)}}$$
- $B$: Bandwidth of the channel in Hertz ($\text{Hz}$).
- $M$: Number of discrete signal voltage levels used to represent data.
- *Pedagogical Insight*: Increasing the number of discrete signal levels $M$ allows each signal transition to carry more bits ($\log_2 M$ bits per signal element), boosting data rate without requiring more bandwidth.

### 3.2 Shannon Channel Capacity Theorem (Noisy Channel)
Formulated in 1948 by Claude Shannon, this theorem determines the absolute physical upper bound on data transmission across a channel corrupted by thermal (white Gaussian) noise:
$$\mathbf{C_{\text{Shannon}} = B \log_2\left(1 + \text{SNR}\right) \quad \text{(bps)}}$$
- $B$: Channel bandwidth in Hertz.
- $\text{SNR}$: Signal-to-Noise Ratio (linear power ratio: $\text{Signal Power} / \text{Noise Power}$).
- **Decibel Conversion ($\text{SNR}_{\text{dB}}$)**:
  $$\text{SNR}_{\text{dB}} = 10 \log_{10}(\text{SNR}) \iff \text{SNR} = 10^{\text{SNR}_{\text{dB}} / 10}$$

> [!IMPORTANT]
> **Nyquist vs. Shannon Exam Distinction**:
> - **Shannon Capacity** gives the **absolute physical capacity limit** of the channel imposed by noise. No technology can exceed this limit!
> - **Nyquist Theorem** tells engineers **how many signal levels ($M$)** must be architected into the hardware transceivers to achieve that theoretical capacity.

---

## 4. Digital Transmission & Modulation Techniques (Slide 3)

### 4.1 Pulse Code Modulation (PCM)
PCM is the standard method used in telecommunications to convert continuous analog signals (e.g., human voice) into digital bit streams.

```
Analog Voice Wave ===> [ 1. SAMPLING ] ===> [ 2. QUANTIZATION ] ===> [ 3. ENCODING ] ===> Digital Bits
                       (Nyquist Rate:        (Map samples to          (Convert levels
                        fs >= 2 * fmax)       discrete levels)         to binary words)
```

1. **Sampling**: The analog signal is sampled at regular time intervals.
   - **Nyquist Sampling Theorem**: The sampling frequency ($f_s$) must be at least **twice the highest frequency component** present in the analog signal:
     $$f_s \ge 2 f_{\max}$$
   - *Example*: Human telephone voice is bandlimited to $4\,\text{kHz}$. Sampling rate must be at least $f_s = 2 \times 4,000 = \mathbf{8,000\text{ samples/sec}}$.
2. **Quantization**: Each continuous sampled amplitude is rounded to the nearest discrete quantization level. For $n_b$ bits per sample, there are $L = 2^{n_b}$ levels.
   - Introduces **Quantization Error / Noise**.
   - Signal-to-Quantization-Noise Ratio:
     $$\text{SNR}_{q\text{, dB}} \approx 6.02 n_b + 1.76\,\text{dB}$$
3. **Encoding**: Each quantized sample is converted to an $n_b$-bit binary code.
   - For standard telephone voice ($8\text{ bits/sample}$ at $8,000\text{ samples/s}$):
     $$\text{Voice Bit Rate} = 8,000 \times 8 = \mathbf{64\,\text{kbps}} \quad (\text{DS0 standard})$$

### 4.2 Digital-to-Analog Modulation (Shift Keying)
Modulating digital bits onto high-frequency analog carrier waves for transmission across bandpass channels (radio, cable):
1. **Amplitude Shift Keying (ASK)**: Binary 1 is represented by a carrier sine wave; binary 0 is represented by absence of carrier (On-Off Keying - OOK). Vulnerable to noise.
2. **Frequency Shift Keying (FSK)**: Binary 1 and 0 are represented by two distinct carrier frequencies ($f_1$ and $f_2$).
3. **Phase Shift Keying (PSK)**: Phase of carrier is altered to represent data. Binary PSK (BPSK, 2 phases: $0^\circ$ and $180^\circ$); Quadrature PSK (QPSK, 4 phases: $45^\circ, 135^\circ, 225^\circ, 315^\circ$, carrying 2 bits per baud).
4. **Quadrature Amplitude Modulation (QAM)**: Combines ASK and PSK concurrently. 16-QAM carries 4 bits per symbol; 256-QAM carries 8 bits per symbol.

---

## 5. Multiplexing Paradigms: FDM, WDM & TDM (Slides 4–11)

Multiplexing is the set of techniques that allows the simultaneous transmission of multiple independent signals across a single shared physical data link.

```
+-------------------------------------------------------------------------+
|                        CATEGORIES OF MULTIPLEXING                       |
|                                                                         |
|        +-----------------------+-----------------------+                |
|        |                       |                       |                |
|       FDM                     WDM                     TDM               |
| (Frequency-Division)   (Wavelength-Division)   (Time-Division)          |
|    [ ANALOG ]              [ OPTICAL ]           [ DIGITAL ]            |
+-------------------------------------------------------------------------+
```

### 5.1 Frequency-Division Multiplexing (FDM, Slides 7–9)
- **Analog Technique**: Applied when link physical bandwidth (in Hz) is greater than the combined bandwidths of the signals to be transmitted.
- Each source signal modulates a different carrier frequency ($f_1, f_2, f_3$).
- **Guard Bands**: Channels are separated by strips of unused frequency bandwidth called guard bands to prevent adjacent signal spectral overlap and crosstalk.
- **Demultiplexing**: Employs a bank of analog bandpass filters followed by demodulators.

```
MUX Input:                                            DEMUX Output:
Source 1 (Baseband) --[ Modulate f1 ]--\              /--[ Filter f1 ]--[ Demod ]--> Out 1
Source 2 (Baseband) --[ Modulate f2 ]----+== Link ===+---[ Filter f2 ]--[ Demod ]--> Out 2
Source 3 (Baseband) --[ Modulate f3 ]--/              \--[ Filter f3 ]--[ Demod ]--> Out 3
```

### 5.2 Wavelength-Division Multiplexing (WDM, Slide 10)
- **Optical Analog of FDM**: Applied to high-capacity optical fiber cables.
- Combines optical light signals of different wavelengths (frequencies: $\lambda_1, \lambda_2, \lambda_3$) using an optical prism / diffraction multiplexer into a single composite beam of light.
- Extremely high frequencies ($\approx 193\,\text{THz}$, wavelengths in the $1,550\,\text{nm}$ low-loss window).
- **Dense WDM (DWDM)**: Packs hundreds of independent wavelength channels onto a single fiber strand, achieving multi-terabit speeds.

### 5.3 Time-Division Multiplexing (TDM, Slide 11)
- **Digital Technique**: Applied when data transmission rate capacity of the medium exceeds the required data rates of transmitting devices.
- Instead of sharing frequency bands, **time is shared**.
- The physical link operates at high speed; each connection occupies the entire link bandwidth for a recurring discrete time slot within repetitive frames.

---

## 6. Guided Transmission Media (Slides 12–35)

Guided transmission media provide a physical conduit containing and directing electromagnetic energy between devices.

```
                            GUIDED MEDIA
                                 |
        +------------------------+------------------------+
        |                        |                        |
   TWISTED PAIR               COAXIAL                FIBER OPTIC
  - UTP (Unshielded)        - RG-59 (75 Ohm, TV)    - Step-Index (Multimode)
  - STP (Shielded)          - RG-58 (50 Ohm, Thin)  - Graded-Index (Multimode)
  - RJ-45 Connector         - RG-11 (50 Ohm, Thick) - Single-Mode (Core ~9 um)
                            - BNC Connectors        - SC, ST, MT-RJ Connectors
```

### 6.1 Twisted-Pair Cable (Slides 15–20)
- Consists of two insulated copper conductors twisted around each other in a regular helical pattern.
- **Physics of Twisting (Slide 17)**: If wires run in parallel, the wire closer to an external noise source absorbs higher electromagnetic induction than the farther wire, creating a net voltage difference at the receiver. By twisting the wires, each conductor alternates between being closer to and farther from noise sources; external noise affects both wires equally and is **canceled out** by the receiver's differential operational amplifier!
- **UTP vs. STP (Slides 18–19)**:
  - **UTP (Unshielded Twisted Pair)**: Common, flexible, low-cost. Categories: Cat 5e ($1\,\text{Gbps}$ up to $100\,\text{m}$), Cat 6 ($10\,\text{Gbps}$).
  - **STP (Shielded Twisted Pair)**: Each pair is encased in a metal foil or braided mesh sheath. Maximum noise immunity, but bulkier, rigid, and more expensive.
- **Connector**: Standard 8-pin **RJ-45 (Registered Jack-45)** male connector and female jack.

### 6.2 Coaxial Cable (Slides 21–25)
- **Construction**: Central copper core conductor, thick plastic dielectric insulation, outer braided metallic shield (serves as ground return and EMI barrier), protective plastic jacket.
- **Radio Government (RG) Ratings (Slide 23)**:
  - **RG-59**: $75\,\Omega$ impedance; used for Cable TV distribution.
  - **RG-58**: $50\,\Omega$ impedance; used for Thin Ethernet (10Base2).
  - **RG-11**: $50\,\Omega$ impedance; used for Thick Ethernet (10Base5).
- **BNC Connectors (Slides 24–25)**: Bayonet Neill-Concelman (BNC) connector, BNC T-connector (attaching host taps to bus), and BNC $50\,\Omega$ Terminator (absorbs signal reflections at cable endpoints).

### 6.3 Fiber-Optic Cable (Slides 26–35)
- **Physics of Light**: Uses **Total Internal Reflection** to guide light through a glass or plastic core surrounded by a cladding of **less dense** optical material ($n_{\text{core}} > n_{\text{cladding}}$).
- If the angle of incidence exceeds the **Critical Angle** ($\theta_c$), light is completely reflected back into the core without refracting into the cladding.

```
TOTAL INTERNAL REFLECTION:
 Cladding (Lower density, n2)
---------------------------------------------
 Core (Higher density, n1)     /\          /\
                              /  \        /  \
=============================/====\======/====\=====> Light ray
                            /      \    /      \
---------------------------/--------\--/--------\----
 Cladding (n2)
```

#### Propagation Modes (Slides 29–30):
1. **Multimode Step-Index**: Large core diameter ($\sim 50-62.5\,\mu\text{m}$). Light rays bounce at varying angles, arriving at different times (**Modal Dispersion**). Limited to short distances ($< 2\,\text{km}$).
2. **Multimode Graded-Index**: Density of core decreases parabolically from center to edge. Light traveling along outer paths bends smoothly and travels faster, arriving at nearly the same time as center rays. Reduces modal dispersion.
3. **Single-Mode Fiber**: Ultra-thin core diameter ($\sim 8-10\,\mu\text{m}$). Permits only a single axial light mode to propagate (zero modal dispersion!). Driven by semiconductor injection lasers. Spans tens of kilometers without repeaters.

#### Optical Fiber Connectors (Slides 32–33):
- **SC (Subscriber Channel)**: Push/pull locking system; common in cable TV and data networks.
- **ST (Straight Tip)**: Bayonet twist-lock mechanism; highly reliable.
- **MT-RJ**: Duplex connector featuring transmit and receive fibers in the exact same footprint as an RJ-45 jack.

---

## 7. Unguided Transmission Media: Wireless (Slides 36–44)

Unguided media transport electromagnetic waves through free space without physical conductors, spanning frequencies from $3\,\text{kHz}$ to $900\,\text{THz}$.

```
+-----------------------------------------------------------------------------------------+
|                              ELECTROMAGNETIC SPECTRUM                                   |
|                                                                                         |
| 3 kHz                      1 GHz                     300 GHz                   400 THz  |
|   |                          |                          |                         |     |
|   +------- RADIO WAVES ------+------- MICROWAVES -------+------- INFRARED --------+     |
|   | Omnidirectional          | Unidirectional Line-of-Sight Room-Bound                  |
|   | Ground / Sky wave        | Parabolic Dish / Horn    | Remote controls         |     |
|   | Penetrates walls         | Blocked by obstacles     | Blocked by walls        |     |
+-----------------------------------------------------------------------------------------+
```

1. **Radio Waves ($3\,\text{kHz} - 1\,\text{GHz}$, Slides 37–38)**:
   - **Omnidirectional**: Radiates in all directions from an omnidirectional whip antenna; sender and receiver antennas do not need alignment.
   - Propagates via ground waves and ionospheric sky waves. Easily penetrates building walls (suitable for FM radio, mobile devices).
2. **Microwaves ($1\,\text{GHz} - 300\,\text{GHz}$, Slides 39–42)**:
   - **Unidirectional**: Electromagnetic waves can be narrowly focused into tight beams. Requires precise line-of-sight alignment between transmitting and receiving antennas.
   - Uses **Parabolic Dish Antennas** (focuses parallel beams to a single point) and **Horn Antennas** (waveguide feed).
   - Very high frequencies cannot penetrate solid masonry walls. Curvature of the Earth mandates tall repeater towers every $\sim 50\,\text{km}$.
   - Massive bandwidth ($\approx 299\,\text{GHz}$ band), supporting multi-gigabit cellular backhauls and satellite uplinks.
3. **Infrared Waves ($300\,\text{GHz} - 400\,\text{THz}$, Slides 43–44)**:
   - Extremely high frequencies with wavelengths from $1\,\text{mm}$ to $770\,\text{nm}$.
   - **Cannot penetrate walls**: A short-range TV remote control in one room will never interfere with a neighboring TV next door (high spatial isolation and security).
   - **Limitation**: Useless for outdoor communication because sunlight contains intense infrared radiation that swamps detectors.

---

## 8. Master Media Comparison Matrix

| Physical Medium | Typical Bandwidth | Maximum Segment Distance | Noise & EMI Immunity | Primary Application |
| :--- | :--- | :--- | :--- | :--- |
| **UTP (Cat 6)** | Up to $10\,\text{Gbps}$ | $100\,\text{meters}$ | Moderate (cancels via twists)| Enterprise LAN workstation connections |
| **STP** | Up to $10\,\text{Gbps}$ | $100\,\text{meters}$ | High (metal foil shielding) | Industrial noise-heavy factory floors |
| **Coaxial (RG-58/59)**| Up to $1\,\text{Gbps}$ (broadband) | $185\,\text{m} - 500\,\text{m}$ | High (braided ground shield) | Cable TV broadband internet, legacy LANs |
| **Single-Mode Fiber**| $100+\,\text{Gbps}$ | Tens of kilometers ($> 40\,\text{km}$) | **Total Immunity** (optical light)| Telco backbones, trans-oceanic cables |
| **Terrestrial Microwave**| Hundreds of Mbps | $\sim 50\,\text{km}$ (line-of-sight)| Weather/rain fade sensitivity| Cellular tower backhauls, remote spans |

---

## 9. Comprehensive 5-Layer Course Synthesis Review

To succeed in the BITS WILP examination, students must synthesize how data moves across all five layers simultaneously:

```
+-----------------------------------------------------------------------------------------+
|                  THE 5-LAYER INTERNET END-TO-END DATA JOURNEY                           |
|                                                                                         |
| 1. APPLICATION LAYER:                                                                   |
|    - User interacts with HTTP/SMTP/DNS. Message M created.                              |
|    - Name resolved to IP via DNS hierarchy (Root -> TLD -> Authoritative).             |
|                                                                                         |
| 2. TRANSPORT LAYER:                                                                     |
|    - TCP 3-way handshake established (SYN -> SYN-ACK -> ACK).                          |
|    - Pipelining sliding windows, AIMD congestion control (Slow Start, cwnd).            |
|    - Flow control via rwnd. Header Ht (20B) appended -> Segment.                        |
|                                                                                         |
| 3. NETWORK LAYER:                                                                       |
|    - Routing algorithms (Dijkstra/OSPF, Bellman-Ford, BGP) compute global paths.       |
|    - Router ASICs execute Longest Prefix Matching (LPM) on forwarding table.            |
|    - Datagram Hn (20B) appended. TTL decremented at each hop.                           |
|                                                                                         |
| 4. DATA LINK LAYER:                                                                     |
|    - ARP resolves next-hop router's IP to 48-bit MAC address.                           |
|    - Frame Hl appended, CRC-32 computed for error detection. Switch self-learns table.  |
|                                                                                         |
| 5. PHYSICAL LAYER:                                                                      |
|    - Digital bits modulated onto analog carrier waves (QAM, PCM, ASK/FSK/PSK).          |
|    - Electromagnetic waves propagate across fiber (total internal reflection), copper,   |
|      or wireless free space bounded by Nyquist and Shannon channel limits.              |
+-----------------------------------------------------------------------------------------+
```

---

## 10. High-Yield Open-Book Exam Traps & Examiner Tricks

1. **The Nyquist vs. Shannon Formula Trap**:
   - *Trap*: Using the Nyquist formula when noise is present, or using Shannon when calculating required voltage levels.
   - *Fact*: Shannon calculates the **theoretical capacity ceiling of a noisy link**. Nyquist calculates the **required signal levels ($M$)** needed to hit that target.
2. **The dB Power to Linear Ratio Trap**:
   - *Trap*: Plugging a $30\,\text{dB}$ SNR directly into $\log_2(1 + \text{SNR})$ as $30$.
   - *Fact*: $30\,\text{dB} = 10 \log_{10}(\text{SNR}) \implies \text{SNR} = 10^{30/10} = 10^3 = \mathbf{1,000}$! You must plug $1,000$ into the formula.
3. **The Single-Mode vs. Multi-Mode Dispersion Trap**:
   - *Question*: *"Why does Single-Mode Fiber support vastly longer distances than Multi-Mode Fiber?"*
   - *Fact*: Because its core is so narrow ($\sim 9\,\mu\text{m}$) that light travels along a single axial path, **completely eliminating Modal Dispersion**.

---

## 11. Solved High-Yield Numerical Exam Problems

### Problem 1: Combined Shannon Capacity & Nyquist Signal Levels
**Problem Statement**:
A telephone line has a channel bandwidth of $B = 4\,\text{kHz}$ ($4,000\,\text{Hz}$). The Signal-to-Noise Ratio is measured at $\text{SNR}_{\text{dB}} = 30\,\text{dB}$.
1. Calculate the theoretical maximum channel capacity using Shannon's theorem.
2. If an engineer designs a modem to achieve this exact capacity over this channel, how many discrete voltage levels ($M$) must the modem transceiver support according to Nyquist's theorem?

**Step-by-Step Solution**:

1. **Convert SNR from dB to Linear Ratio**:
   $$\text{SNR}_{\text{dB}} = 10 \log_{10}(\text{SNR}) = 30\,\text{dB}$$
   $$\log_{10}(\text{SNR}) = 3 \implies \text{SNR} = 10^3 = \mathbf{1,000}$$

2. **Compute Shannon Capacity ($C_{\text{Shannon}}$)**:
   $$C = B \log_2(1 + \text{SNR}) = 4,000 \times \log_2(1 + 1,000) = 4,000 \times \log_2(1,001)$$
   - Since $2^9 = 512$ and $2^{10} = 1,024$, $\log_2(1,001) \approx 9.967$:
     $$C = 4,000 \times 9.967 = \mathbf{39,869\,\text{bps}} \approx \mathbf{39.9\,\text{kbps}}$$

3. **Determine Required Nyquist Signal Levels ($M$)**:
   Equate Nyquist bit rate to Shannon capacity:
   $$C_{\text{Nyquist}} = 2B \log_2(M) = C_{\text{Shannon}} = 39,869\,\text{bps}$$
   $$2 \times 4,000 \times \log_2(M) = 39,869$$
   $$8,000 \log_2(M) = 39,869 \implies \log_2(M) = \frac{39,869}{8,000} \approx 4.98$$
   $$M = 2^{4.98} \approx \mathbf{32\text{ discrete signal levels}} \quad (2^5 = 32)$$
   - *Conclusion*: A 32-level modulation scheme (e.g., 32-QAM carrying 5 bits per symbol) achieves the channel's maximum theoretical limit!

---

### Problem 2: Pulse Code Modulation (PCM) Bit Rate & Bandwidth
**Problem Statement**:
An analog audio signal has a frequency spectrum ranging from $20\,\text{Hz}$ to $20\,\text{kHz}$ (CD quality).
The signal is digitized using Pulse Code Modulation (PCM) with $16\text{ bits per sample}$ across $2$ audio channels (stereo).
1. What is the minimum Nyquist sampling rate ($f_s$)?
2. Calculate the resulting uncompressed digital bit rate in Mbps.
3. What is the minimum theoretical channel bandwidth required to transmit this digital signal using binary encoding ($M = 2$)?

**Step-by-Step Solution**:

1. **Calculate Minimum Nyquist Sampling Rate**:
   - Highest frequency component $f_{\max} = 20\,\text{kHz} = 20,000\,\text{Hz}$.
   - Nyquist sampling rate:
     $$f_s = 2 \times f_{\max} = 2 \times 20,000 = \mathbf{40,000\text{ samples/second}}$$
     *(Standard audio CDs use $44,100\,\text{samples/s}$ to provide a guard band for analog anti-aliasing filters).*

2. **Calculate Digital Bit Rate**:
   - Bits per sample $= 16\,\text{bits}$.
   - Number of channels $= 2$ (stereo).
   - Sampling rate $= 44,100\,\text{samples/sec}$.
   $$\text{Bit Rate} = 44,100 \times 16 \times 2 = 1,411,200\,\text{bps} = \mathbf{1.4112\,\text{Mbps}}$$

3. **Compute Minimum Required Channel Bandwidth**:
   - Using Nyquist formula with binary levels ($M = 2 \implies \log_2 2 = 1$):
     $$\text{Bit Rate} = 2B \log_2(2) = 2B$$
     $$B = \frac{\text{Bit Rate}}{2} = \frac{1,411,200\,\text{bps}}{2} = \mathbf{705,600\,\text{Hz}} = \mathbf{705.6\,\text{kHz}}$$

---

## 12. Ultra-Fast Exam Revision Checklist
- [ ] Sine wave: $s(t) = A \sin(2\pi f t + \phi)$; frequency $f = 1/T$, wavelength $\lambda = c/f$.
- [ ] Nyquist formula (noiseless): $C = 2B \log_2 M$; Shannon formula (noisy): $C = B \log_2(1 + \text{SNR})$.
- [ ] Decibel SNR conversion: $\text{SNR} = 10^{\text{SNR}_{\text{dB}} / 10}$.
- [ ] PCM steps: Sampling ($f_s \ge 2f_{\max}$), Quantization ($L = 2^{n_b}$), Encoding ($n_b$ bits).
- [ ] FDM and WDM are analog multiplexing techniques; TDM is a digital multiplexing technique.
- [ ] Twisted pair: Twisting cancels external noise via differential reception; UTP vs STP (foil shielded).
- [ ] Coaxial cable: RG-58 ($50\,\Omega$ thin), RG-59 ($75\,\Omega$ TV); terminates with $50\,\Omega$ BNC terminator.
- [ ] Optical fiber: Total internal reflection requires $n_{\text{core}} > n_{\text{cladding}}$; Single-mode eliminates modal dispersion.
- [ ] Radio waves ($3\,\text{kHz}-1\,\text{GHz}$) are omnidirectional; Microwaves ($1-300\,\text{GHz}$) are line-of-sight unidirectional; Infrared is blocked by walls.
