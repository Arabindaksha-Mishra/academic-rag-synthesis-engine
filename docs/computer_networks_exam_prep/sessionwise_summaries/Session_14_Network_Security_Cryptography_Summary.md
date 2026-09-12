# Computer Networks (BSDCBZC481)
# Session 14: Network Security — Cryptography, RSA, TLS, IPsec & Firewalls
### Exhaustive Slide-by-Slide Academic Exam Revision Manual & Problem Solving Guide

---

## 1. Session Context & Pedagogical Scope
- **Course Code & Title**: BSDCBZC481 — Computer Networks
- **Instructor**: Dr. K. Kalaiselvi (BITS Pilani)
- **Primary Textbooks**:
  - J.F. Kurose & K.W. Ross, *Computer Networking: A Top-Down Approach*, 5th/6th Edition, Chapter 8 (T1)
  - B.A. Forouzan, *Data Communications and Networking*, 4th Edition, Chapters 30, 31, & 32 (T2)
- **Lecture Slide Mapping**: CS14: Network Security — Slides 1 to 61 (Complete Coverage)
- **Core Syllabus Covered**:
  1. Foundational Security Objectives: Confidentiality, Integrity, Authentication & Non-Repudiation (CIA)
  2. Symmetric Key Cryptography: Caesar, Monoalphabetic, Polyalphabetic & Modern Block Ciphers (DES, 3DES, AES)
  3. Block Cipher Operating Modes: Electronic Codebook (ECB) Vulnerabilities vs. Cipher Block Chaining (CBC)
  4. Asymmetric Cryptography: Number-Theoretic Foundations & Mathematical Derivation of RSA
  5. Cryptographic Hash Functions (MD5, SHA-256), HMAC & Digital Signatures ($S = K_A^-(H(m))$)
  6. Public Key Infrastructure (PKI): Certification Authorities (CA), X.509 Certificates & MitM Mitigation
  7. Transport Layer Security (SSL/TLS): Handshake Negotiation, ECDHE Key Exchange & The Record Protocol
  8. Network Layer Security (IPsec): Authentication Header (AH) vs. Encapsulating Security Payload (ESP)
  9. IPsec Modes of Operation: Transport Mode vs. Tunnel Mode & Security Associations (SA)
  10. Operational Network Security: Stateless Packet Filtering Firewalls, Stateful SPI, and Application Gateways
  11. High-Yield Open-Book Exam Traps, Rigorous Numerical Problems & Fast Revision Checklist

---

## 2. Foundational Principles of Network Security (Slides 3–9)

Network security protects communication channels against adversaries capable of eavesdropping (sniffing), intercepting, injecting, altering, or impersonating packets.

```
+-------------------------------------------------------------------------+
|                       THE CORE PILLARS OF SECURITY                      |
|                                                                         |
| 1. CONFIDENTIALITY: Only the sender and intended receiver can decipher   |
|    the contents of the transmitted message.                             |
| 2. INTEGRITY: The receiver can verify that the message was not altered, |
|    tampered with, or injected during transit.                           |
| 3. ENDPOINT AUTHENTICATION: Both sender and receiver can definitively   |
|    verify each other's identity (preventing impersonation/spoofing).    |
| 4. NON-REPUDIATION: The sender cannot later falsely deny having sent     |
|    the message (achieved via asymmetric digital signatures).            |
| 5. AVAILABILITY: Communication services remain operational and accessible|
|    despite malicious denial-of-service (DoS/DDoS) floods.               |
+-------------------------------------------------------------------------+
```

---

## 3. Symmetric Key Cryptography & Block Cipher Modes (Slides 10–24)

In symmetric encryption, the sender and receiver share the **exact same secret key** ($K_s$):
$$\text{Encryption: } c = K_s(m) \qquad \text{Decryption: } m = K_s(c)$$

### 3.1 Historical Ciphers vs. Modern Ciphers
- **Caesar Cipher**: Shifts each character by $k$ positions: $c = (m + k) \bmod 26$. Key space is trivial ($25$ keys), broken in milliseconds via brute-force.
- **Monoalphabetic Substitution Cipher**: Arbitrary permutation of 26 letters. Key space is $26! \approx 4 \times 10^{26}$, but easily broken using **Letter Frequency Analysis** (in English, letters `E`, `T`, `A`, `O`, `I`, `N` occur with predictable statistical frequencies).
- **Data Encryption Standard (DES, 1977)**: 64-bit block size, 56-bit key, 16 Feistel rounds. Completely insecure today (broken via brute force in hours).
- **Advanced Encryption Standard (AES - Rijndael, 2001)**: 128-bit block size; key sizes of 128, 192, and 256 bits. Uses a Substitution-Permutation Network (SPN: `SubBytes`, `ShiftRows`, `MixColumns`, `AddRoundKey`). 10, 12, or 14 rounds. Current global industry benchmark.

### 3.2 Block Cipher Modes of Operation (Slides 20–24)
A block cipher encrypts a fixed block of data (e.g., 128 bits). For longer messages, the operating mode dictates how consecutive blocks are encrypted:

```
1. ELECTRONIC CODEBOOK (ECB) MODE (FATAL FLAW!):
   Plaintext Block 1 ===[ Encrypt Ks ]===> Ciphertext Block 1
   Plaintext Block 2 ===[ Encrypt Ks ]===> Ciphertext Block 2
   (Identical plaintext blocks produce IDENTICAL ciphertext blocks! Leaks structure!)

2. CIPHER BLOCK CHAINING (CBC) MODE (SECURE):
   Plaintext Block 1 ----(+)======[ Encrypt Ks ]====> Ciphertext Block 1 ----\
                          ^                                                   |
                          | (IV)                                              v
   Plaintext Block 2 ----(+)======[ Encrypt Ks ]====> Ciphertext Block 2 ----(+)
```

- **Electronic Codebook (ECB)**:
  $$c_i = E_{K_s}(m_i)$$
  - **Catastrophic Vulnerability**: If two plaintext blocks are identical ($m_1 = m_2$), their ciphertexts are identical ($c_1 = c_2$). This exposes structural patterns (e.g., encrypting a bitmap image reveals the exact outline of the image).
- **Cipher Block Chaining (CBC)**:
  - Generates a random **Initialization Vector (IV)** for the first block:
    $$c_1 = E_{K_s}(m_1 \oplus \text{IV})$$
    $$c_i = E_{K_s}(m_i \oplus c_{i-1}) \quad \forall i \ge 2$$
  - Decryption: $m_i = D_{K_s}(c_i) \oplus c_{i-1}$.
  - Even if all plaintext blocks are identical, chaining produces completely pseudorandom ciphertext blocks!

---

## 4. Asymmetric Cryptography: The RSA Algorithm (Slides 25–35)

Asymmetric encryption decouples the key into a **Public Key ($K^+$)** (distributed openly) and a **Private Key ($K^-$)** (kept strictly confidential by the owner):
$$m = K^-(K^+(m)) \quad \text{and} \quad m = K^+(K^-(m))$$

### 4.1 Mathematical Derivation of RSA
Developed in 1977 by Ron Rivest, Adi Shamir, and Leonard Adleman, RSA is grounded in the computational intractability of **factoring the product of two large prime numbers**.

```
+-----------------------------------------------------------------------------------------+
|                              THE RSA KEY GENERATION ALGORITHM                           |
|                                                                                         |
| 1. Select two distinct large prime numbers:              p  and  q                      |
| 2. Compute the RSA modulus:                              n = p * q                      |
| 3. Compute Euler's Totient Function:                     phi(n) = (p - 1) * (q - 1)     |
| 4. Select an encryption exponent e such that:            1 < e < phi(n)                 |
|                                                          gcd(e, phi(n)) = 1 (Coprime)   |
| 5. Compute the decryption exponent d such that:          e * d = 1 (mod phi(n))         |
|    (d is the modular multiplicative inverse of e):       d = e^-1 mod phi(n)            |
|                                                                                         |
| PUBLIC KEY:   K+ = (e, n)                                                               |
| PRIVATE KEY:  K- = (d, n)                                                               |
|                                                                                         |
| ENCRYPTION:   c = m^e mod n      (where 0 <= m < n)                                     |
| DECRYPTION:   m = c^d mod n                                                             |
+-----------------------------------------------------------------------------------------+
```

### 4.2 Proof of Correctness (Euler's Totient Theorem)
By Euler's Totient Theorem, if $\gcd(m, n) = 1$:
$$m^{\phi(n)} \equiv 1 \pmod n$$
Since $e \cdot d \equiv 1 \pmod{\phi(n)}$, there exists an integer $k$ such that $e \cdot d = k \cdot \phi(n) + 1$.
$$c^d \equiv (m^e)^d \equiv m^{ed} \equiv m^{k\phi(n) + 1} \equiv (m^{\phi(n)})^k \cdot m^1 \equiv (1)^k \cdot m \equiv \mathbf{m \pmod n}$$
Decryption mathematically recovers the original plaintext message $m$.

---

## 5. Message Integrity, Hashes & Digital Signatures (Slides 36–44)

### 5.1 Cryptographic Hash Functions
A cryptographic hash function $H(m)$ maps an arbitrary-length message $m$ to a fixed-size digest (e.g., $256\text{ bits}$ for SHA-256):
1. **One-Way Property (Pre-Image Resistance)**: Given digest $h$, it is computationally impossible to invert and find $m$ such that $H(m) = h$.
2. **Collision Resistance**: It is computationally impossible to find any two distinct inputs $x \ne y$ such that $H(x) = H(y)$.

### 5.2 Digital Signatures
A digital signature provides **integrity, authenticity, and non-repudiation**:
- **Signing**: The sender hashes the message and encrypts the digest with their **Private Key**:
  $$\text{Signature } (S) = K_A^-(H(m))$$
- **Verification**: The receiver decrypts the signature using the sender's **Public Key** and compares it to a locally computed hash of the message:
  $$H'(m) \stackrel{?}{=} K_A^+(S)$$
  If $H'(m) == K_A^+(S)$, the signature is valid!

```
SENDER (Alice):                                 RECEIVER (Bob):
Message (m) ---> [ Hash H() ] ---> Digest (h)   Message (m) ---> [ Hash H() ] ---> Local Digest (h)
                                      |                                                |
                               [ Encrypt Ka- ]                                         | (Must Match!)
                                      |                                                v
                                Signature (S) -----------------> [ Decrypt Ka+ ] -> Signature Digest
```

### 5.3 Public Key Infrastructure (PKI) & X.509 Certificates
- **The Man-in-the-Middle (MitM) Vulnerability**: An attacker (Trudy) intercepts Bob's public key and substitutes her own public key, tricking Alice into encrypting messages for Trudy.
- **Solution**: **Certification Authorities (CAs)** (e.g., Let's Encrypt, DigiCert).
- A CA verifies an entity's domain ownership and issues an **X.509 Digital Certificate** containing:
  $$\text{Certificate} = [ \text{Entity Identity (Domain)}, K_{\text{Entity}}^+, \text{Issuer}, \text{Validity} ] + \mathbf{K_{\text{CA}}^-(H(\text{Data}))}$$
- Browsers ship with pre-installed Root CA public keys to verify certificate authenticity.

---

## 6. Transport Layer Security (SSL / TLS) (Slides 45–50)

TLS (RFC 8446 - TLS 1.3) sits directly between the application layer and TCP, securing protocols like HTTPS, IMAPS, and SMTPS.

```
+-------------------------------------------------------------+
|                      APPLICATION LAYER (HTTP)               |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|               TRANSPORT LAYER SECURITY (SSL/TLS)            |
|  - Handshake Protocol: Authenticates server, derives keys   |
|  - Record Protocol: Symmetric encryption + HMAC integrity   |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                 TRANSPORT LAYER (TCP Port 443)              |
+-------------------------------------------------------------+
```

### 6.1 The TLS Handshake Exchange
1. **Client Hello**: Proposes supported TLS versions, cryptographic cipher suites (e.g., `TLS_AES_256_GCM_SHA384`), and a random nonce $R_C$.
2. **Server Hello**: Selects cipher suite, provides server random nonce $R_S$, and presents the **Server X.509 Digital Certificate**.
3. **Key Exchange**: Client verifies certificate using Root CA. Client and server execute an Ephemeral Elliptic Curve Diffie-Hellman (ECDHE) exchange to derive a shared **Pre-Master Secret (PMS)**.
4. **Master Secret Derivation**: Both sides independently compute:
   $$\text{Master Secret} = \text{PRF}(\text{PMS}, R_C, R_S)$$
   Four symmetric keys are generated:
   - Client write encryption key ($K_{\text{CW}}$) & Server write encryption key ($K_{\text{SW}}$).
   - Client write MAC key ($M_{\text{CW}}$) & Server write MAC key ($M_{\text{SW}}$).
5. **Finished (Encrypted)**: Both parties verify handshake message integrity and switch to symmetric encryption.

---

## 7. Network Layer Security: IPsec (Slides 51–56)

IPsec provides transparent cryptographic security for **all network-layer datagrams** between communicating nodes.

### 7.1 Two Core IPsec Protocols
1. **Authentication Header (AH, Protocol 51)**:
   - Provides data integrity, source authentication, and anti-replay protection.
   - **ZERO Confidentiality**: Transmits data in plaintext (**No encryption!**).
2. **Encapsulating Security Payload (ESP, Protocol 50)**:
   - Provides **confidentiality (encryption)**, data integrity, and authentication.

### 7.2 Transport Mode vs. Tunnel Mode (Crucial Exam Concept!)

```
ORIGINAL IP DATAGRAM:
[ Original IP Header (Src: A, Dst: B) ] [ TCP / Payload Data ]

1. IPSEC TRANSPORT MODE (Host-to-Host):
[ Orig IP Hdr (Proto=50) ] [ ESP Header ] [ TCP / Payload (Encrypted) ] [ ESP Trailer ] [ ESP Auth ]
(Only upper layer transport payload is encrypted; original IP addresses visible)

2. IPSEC TUNNEL MODE (Gateway-to-Gateway / Site-to-Site VPN):
[ New IP Hdr (Gateway IPs) ] [ ESP Hdr ] [ Orig IP Hdr (Encrypted) ] [ Payload (Enc) ] [ ESP Trl ] [ ESP Auth ]
(Entire original datagram is encrypted; hidden inside outer tunnel IP header!)
```

| IPsec Mode | Encapsulation Scope | Endpoint Identity Privacy | Primary Deployment |
| :--- | :--- | :--- | :--- |
| **Transport Mode** | Encrypts payload only. Original IP header is unaltered. | Host IP addresses visible on wire. | Direct Host-to-Host communication. |
| **Tunnel Mode** | Encrypts **entire original IP datagram** (including original IP header). Appends brand new outer IP header. | Original host IPs completely concealed; only VPN gateway IPs visible. | **Site-to-Site VPNs** and Remote Access VPNs. |

---

## 8. Operational Defenses: Firewalls & Intrusion Detection (Slides 57–61)

```
+-----------------------------------------------------------------------------------------+
|                                    FIREWALL TAXONOMY                                    |
|                                                                                         |
| 1. STATELESS PACKET FILTER:                                                             |
|    - Filters individual packets independently based on 5-tuple:                         |
|      (Source IP, Dest IP, Protocol, Source Port, Dest Port, TCP Flags).                 |
|    - Example Rule: "Drop incoming TCP packets with ACK=0 (blocks external SYNs)".       |
|                                                                                         |
| 2. STATEFUL PACKET INSPECTION (SPI):                                                    |
|    - Tracks connection state in an internal connection state table.                     |
|    - Automatically permits incoming return packets only if they match an active         |
|      outbound connection initiated from inside the trusted LAN!                         |
|                                                                                         |
| 3. APPLICATION GATEWAY (PROXY):                                                         |
|    - Reconstructs and inspects application-layer data (Layer 7).                        |
|    - Example: Terminates HTTP, scans payloads for SQL injection or malware, re-encrypts.|
+-----------------------------------------------------------------------------------------+
```

---

## 9. Master Protocol Comparison Matrix

| Protocol | OSI Layer | Confidentiality (Encryption) | Integrity & Auth | Key Negotiation Protocol |
| :--- | :---: | :---: | :---: | :--- |
| **HTTPS (TLS)** | Layer 4 / 7 | Yes (AES-GCM) | Yes (HMAC / AEAD) | TLS Handshake (ECDHE) |
| **IPsec AH** | Layer 3 | **No (Plaintext!)** | Yes (HMAC-SHA256) | IKEv2 |
| **IPsec ESP** | Layer 3 | Yes (AES-CBC/GCM) | Yes (HMAC-SHA256) | IKEv2 |
| **PGP / S-MIME**| Layer 7 | Yes (Hybrid RSA+AES) | Yes (Digital Signature)| Manual / Web-of-Trust |

---

## 10. High-Yield Open-Book Exam Traps & Examiner Tricks

1. **The IPsec AH Confidentiality Trap**:
   - *Question*: *"Does IPsec Authentication Header (AH) encrypt payload data?"*
   - *Fact*: **NO!** AH provides authentication and integrity, but **zero confidentiality**. To encrypt data, IPsec **ESP** must be used.
2. **The Digital Signature Key Inversion Trap**:
   - *Trap*: Stating that a digital signature is encrypted using the recipient's public key.
   - *Fact*: A digital signature is created using the **sender's PRIVATE key** ($K_{\text{sender}}^-$) and verified using the **sender's PUBLIC key** ($K_{\text{sender}}^+$).
3. **The RSA Prime Modulus Constraint**:
   - *Question*: *"In RSA, why must the plaintext message $m$ satisfy $m < n$?"*
   - *Fact*: Arithmetic is performed modulo $n$. If $m \ge n$, $m \bmod n$ would produce an identical value to $(m - n)$, destroying uniqueness and making decryption ambiguous.

---

## 11. Solved High-Yield Numerical Exam Problems

### Problem 1: Complete RSA Key Generation, Encryption & Decryption
**Problem Statement**:
An RSA cryptosystem is initialized using small prime numbers $p = 7$ and $q = 17$.
1. Compute the modulus $n$ and Euler's totient function $\phi(n)$.
2. If the public encryption exponent is chosen as $e = 5$, verify that $e$ is valid and compute the private decryption exponent $d$.
3. A sender transmits plaintext message $m = 12$. Compute the ciphertext $c$.
4. Show step-by-step decryption of ciphertext $c$ to recover message $m$.

**Step-by-Step Solution**:

1. **Modulus and Totient**:
   $$n = p \times q = 7 \times 17 = \mathbf{119}$$
   $$\phi(n) = (p - 1) \times (q - 1) = (7 - 1) \times (17 - 1) = 6 \times 16 = \mathbf{96}$$

2. **Verify $e$ and Compute $d$**:
   - Check coprimality: $\gcd(5, 96) = 1$ (Valid because $96$ is not divisible by 5).
   - Find $d$ such that $e \cdot d \equiv 1 \pmod{\phi(n)} \implies 5d \equiv 1 \pmod{96}$.
   - We solve $5d - 96k = 1$:
     - For $k = 1$: $5d = 97$ (not divisible).
     - For $k = 2$: $5d = 193$ (not divisible).
     - For $k = 3$: $5d = 289$ (not divisible).
     - For $k = 4$: $5d = 385 \implies d = \frac{385}{5} = \mathbf{77}$.
   - Check: $5 \times 77 = 385 = (4 \times 96) + 1 \equiv 1 \pmod{96}$.
   - **Public Key**: $(e = 5, n = 119)$.
   - **Private Key**: $(d = 77, n = 119)$.

3. **Encryption ($m = 12$)**:
   $$c = m^e \bmod n = 12^5 \bmod 119$$
   - Break down exponentiation:
     $$12^2 = 144 \equiv 144 - 119 = 25 \pmod{119}$$
     $$12^4 = (12^2)^2 \equiv 25^2 = 625 \pmod{119}$$
     $$625 = 5 \times 119 + 30 \equiv 30 \pmod{119}$$
     $$c = 12^5 = 12^4 \times 12 \equiv 30 \times 12 = 360 \pmod{119}$$
     $$360 = 3 \times 119 + 3 = 357 + 3 \equiv \mathbf{3} \pmod{119}$$
   - **Ciphertext $c = 3$**.

4. **Decryption ($c = 3$)**:
   $$m = c^d \bmod n = 3^{77} \bmod 119$$
   - Binary representation of exponent $77$: $77 = 64 + 8 + 4 + 1$.
   - Repeated squaring modulo 119:
     - $3^1 = 3$
     - $3^2 = 9$
     - $3^4 = 9^2 = 81 \equiv -38 \pmod{119}$
     - $3^8 = (-38)^2 = 1444 \equiv 1444 - (12 \times 119) = 1444 - 1428 = 16 \pmod{119}$
     - $3^{16} = 16^2 = 256 \equiv 256 - 238 = 18 \pmod{119}$
     - $3^{32} = 18^2 = 324 \equiv 324 - 238 = 86 \equiv -33 \pmod{119}$
     - $3^{64} = (-33)^2 = 1089 \equiv 1089 - (9 \times 119) = 1089 - 1071 = 18 \pmod{119}$
   - Multiply components:
     $$3^{77} = 3^{64} \times 3^8 \times 3^4 \times 3^1 \pmod{119}$$
     $$= 18 \times 16 \times 81 \times 3 \pmod{119}$$
     $$18 \times 16 = 288 \equiv 288 - 238 = 50 \pmod{119}$$
     $$81 \times 3 = 243 \equiv 243 - 238 = 5 \pmod{119}$$
     $$m \equiv 50 \times 5 = 250 \pmod{119}$$
     $$250 = (2 \times 119) + 12 = 238 + 12 \equiv \mathbf{12} \pmod{119}$$
   - **Plaintext $m = 12$ successfully decrypted!**

---

### Problem 2: Cipher Block Chaining (CBC) Error Propagation Analysis
**Problem Statement**:
An 8-block message is encrypted using AES in Cipher Block Chaining (CBC) mode.
During transmission over a noisy channel, a single bit flip error occurs in the transmission of ciphertext block $c_3$.
1. Which plaintext blocks are corrupted upon decryption at the receiver?
2. Explain why the remaining plaintext blocks are decrypted completely error-free.

**Step-by-Step Solution**:

1. **CBC Decryption Equation**:
   $$m_i = D_{K_s}(c_i) \oplus c_{i-1}$$

2. **Evaluate Impact on Each Block**:
   - For $i = 3$:
     $$m_3 = D_{K_s}(c_3) \oplus c_2$$
     Because $c_3$ is corrupted, passing it into the non-linear decryption function $D_{K_s}$ scrambles the entire output block completely. **Plaintext $m_3$ is $100\%$ garbled garbage**.
   - For $i = 4$:
     $$m_4 = D_{K_s}(c_4) \oplus c_3$$
     Here, $c_4$ is completely uncorrupted. However, it is XORed with the corrupted $c_3$. Because XOR is a linear bit-by-bit operation, the specific bit position that flipped in $c_3$ flips the **exact corresponding bit in $m_4$**! **Plaintext $m_4$ has a 1-bit error**.
   - For $i = 5, 6, 7, 8$:
     $$m_5 = D_{K_s}(c_5) \oplus c_4$$
     Neither $c_5$ nor $c_4$ contains errors. **$m_5$ through $m_8$ are decrypted with $100\%$ precision!**
   - *Conclusion*: A 1-bit error in ciphertext block $c_i$ corrupts **all of $m_i$** and causes a **single bit error in $m_{i+1}$**. It does NOT propagate to $m_{i+2}$ onwards (**Self-Synchronizing Property**).

---

## 12. Ultra-Fast Exam Revision Checklist
- [ ] CIA Triad: Confidentiality (encryption), Integrity (hashes), Authentication (signatures/certificates).
- [ ] ECB mode is insecure because identical plaintext blocks produce identical ciphertext blocks; CBC uses chaining with an IV.
- [ ] RSA Key Generation: $n = pq$, $\phi(n) = (p-1)(q-1)$, $e \cdot d \equiv 1 \pmod{\phi(n)}$; encrypt $c = m^e \bmod n$, decrypt $m = c^d \bmod n$.
- [ ] Digital Signatures: Sender encrypts hash with their PRIVATE key; receiver decrypts with sender's PUBLIC key.
- [ ] X.509 Certificates: Binds public key to domain identity; cryptographically signed by a trusted CA.
- [ ] TLS Handshake negotiates cipher suites and derives symmetric keys via ECDHE; Record protocol encrypts TCP payload.
- [ ] IPsec AH (Protocol 51) provides integrity/auth with NO encryption; ESP (Protocol 50) provides encryption AND auth.
- [ ] IPsec Tunnel Mode encrypts entire original datagram and adds new outer IP header; used for site-to-site VPNs.
- [ ] Stateful Firewalls (SPI) maintain a state table of active connections to dynamically permit legitimate return traffic.
