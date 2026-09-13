# BITS WILP Information Security (BSDCBZC311)
# Master Session-by-Session & Topic-Wise YouTube Video Playlist
### Ranked Strictly in Exam Priority Order (Highest Comprehensive Exam Weightage First)

> [!TIP]
> **HOW TO USE THIS PLAYLIST FOR LAST-MINUTE EXAM PREP**:
> - Watch videos at **1.5× playback speed**.
> - Prioritize **Tiers 1 & 2 (Sessions 13, 04, 15, 14, 06, 10, 05, 08)** where **90%+ of the comprehensive exam marks** are concentrated.
> - Pay special attention to **RSA calculation steps**, **Diffie-Hellman protocol**, and **ALE risk calculation tables**.

---

## Quick Priority Navigation Table

| Priority Rank | Session ID & Title | Exam Weightage | Typical Mark Range | Core Exam Focus |
| :---: | :--- | :---: | :---: | :--- |
| **Priority 1** | [Session 13 — Quantitative Risk Assessment (SLE, ALE)](#priority-1-session-13--security-operations--quantitative-risk-sle-ale) | **15% – 20%** | **6 – 8 Marks** | Quantitative Risk, SLE, ALE, Cost-Benefit Safeguard ROI |
| **Priority 2** | [Session 04 — Asymmetric & Symmetric Crypto (RSA, DH, AES)](#priority-2-session-04--asymmetric--symmetric-crypto-rsa-aes-diffie-hellman) | **15% – 20%** | **6 – 8 Marks** | RSA Math, Diffie-Hellman Key Exchange, AES vs DES |
| **Priority 3** | [Session 15 — Incident Response Lifecycle (NIST SP 800-61)](#priority-3-session-15--incident-response-lifecycle-nist-sp-800-61) | **12% – 15%** | **5 – 6 Marks** | 4-Phase NIST Lifecycle: Preparation, Detection, Containment |
| **Priority 4** | [Session 14 — SIEM, Disaster Recovery, RPO/RTO & BCP](#priority-4-session-14--siem-disaster-recovery-rporto--bcp) | **10% – 12%** | **4 – 5 Marks** | RPO vs RTO Thresholds, Hot/Warm/Cold Sites, SIEM Rules |
| **Priority 5** | [Session 06 — Authentication & Access Control (RBAC, BLP)](#priority-5-session-06--authentication--access-control-models-blp-biba) | **10% – 12%** | **4 – 5 Marks** | Bell-LaPadula (NRU/NWD), Biba (NRD/NWU), Kerberos Tickets |
| **Priority 6** | [Session 10 — Database & Storage Security (SQL Injection)](#priority-6-session-10--database--storage-security-sql-injection) | **8% – 10%** | **3 – 5 Marks** | SQLi Mechanics, Parameterized Prepared Statements, Encryption |
| **Priority 7** | [Session 05 — Cryptographic Hashes, Signatures & PGP](#priority-7-session-05--cryptographic-hashes-digital-signatures--pgp) | **8% – 10%** | **3 – 5 Marks** | SHA-256, HMAC, Digital Signature Generation, PGP Hybrid |
| **Priority 8** | [Session 08 — Ethical Hacking & Digital Forensics](#priority-8-session-08--ethical-hacking--digital-forensics) | **8% – 10%** | **3 – 5 Marks** | Chain of Custody, Volatile Memory RAM Dump, Recon Phases |
| **Priority 9** | [Session 16 — Security Governance & ISO 27001](#priority-9-session-16--security-governance-iso-27001--compliance) | **5% – 8%** | **2 – 4 Marks** | ISO 27001 ISMS, PDCA Cycle, DPDP / GDPR Compliance |
| **Priority 10** | [Session 03 — Network Protocols (IPSec, TLS Handshake)](#priority-10-session-03--network-security-protocols-ipsec-tls) | **5% – 8%** | **2 – 4 Marks** | IPSec AH vs ESP, Tunnel vs Transport, TLS 1.3 Handshake |
| **Priority 11** | [Session 02 — Secure Architecture, DMZ & Firewalls](#priority-11-session-02--secure-architecture-dmz--firewalls) | **0% – 5%** | **0 – 3 Marks** | Dual-Homed DMZ Design, Packet Filtering vs NGFW |
| **Priority 12** | [Session 07 — Cloud Security & Shared Responsibility](#priority-12-session-07--cloud-security--shared-responsibility) | **0% – 5%** | **0 – 3 Marks** | IaaS vs PaaS vs SaaS Security Responsibility, IoT Threats |
| **Priority 13** | [Session 01 — Security Basics & STRIDE Model](#priority-13-session-01--security-basics-cia-triad--stride) | **0% – 4%** | **0 – 2 Marks** | CIA Triad, STRIDE Threat Model Matrix |

---

### Priority 1: Session 13 — Security Operations & Quantitative Risk (SLE, ALE)
* **Exam Weightage**: **15% – 20%** (Compulsory Numerical Problem)

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **Quantitative Risk Calculation (SLE, ALE)** | [Gate Smashers – Quantitative Risk Analysis SLE ALE ARO](https://www.youtube.com/results?search_query=Gate+Smashers+Quantitative+Risk+Analysis+SLE+ALE+ARO) | Gate Smashers (~12m) | $\text{SLE} = \text{AV} \times \text{EF}$, $\text{ALE} = \text{SLE} \times \text{ARO}$ formulas |
| **Cost-Benefit Analysis for Security Controls** | [Knowledge Gate – Cost Benefit Analysis of Safeguards](https://www.youtube.com/results?search_query=Knowledge+Gate+Cost+Benefit+Analysis+Security+Safeguards) | Knowledge Gate (~11m) | $(\text{ALE}_{\text{prior}} - \text{ALE}_{\text{post}}) - \text{Cost}$, Safeguard decision rule |
| **Qualitative vs Quantitative Risk Matrix** | [PowerCert – Risk Assessment Explained](https://www.youtube.com/watch?v=kYJqD9bO9g8) | PowerCert (~10m) | Likelihood vs Impact heat map, Risk appetite & tolerance |

---

### Priority 2: Session 04 — Asymmetric & Symmetric Crypto (RSA, AES, Diffie-Hellman)
* **Exam Weightage**: **15% – 20%** (Guaranteed Mathematical Derivation)

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **RSA Algorithm Step-by-Step Numerical** | [Gate Smashers – RSA Algorithm with Example](https://www.youtube.com/watch?v=d_kACkUaUqA) | Gate Smashers (~14m) | $n = pq$, $\phi(n)$, finding $d \equiv e^{-1} \pmod{\phi(n)}$, modular exponentiation |
| **Diffie-Hellman Key Exchange** | [Gate Smashers – Diffie Hellman Key Exchange Algorithm](https://www.youtube.com/watch?v=YEBfamv-_do) | Gate Smashers (~12m) | Shared parameters $p, g$, calculating $A, B$, shared key $K = g^{ab} \pmod p$ |
| **AES Cipher Working & Rounds** | [Computerphile – AES Rijndael Cipher Explained](https://www.youtube.com/watch?v=O4xNJsbiN6s) | Computerphile (~14m) | SubBytes, ShiftRows, MixColumns, AddRoundKey transformations |

---

### Priority 3: Session 15 — Incident Response Lifecycle (NIST SP 800-61)
* **Exam Weightage**: **12% – 15%** (Scenario-Based Plan Formulation)

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **NIST Incident Response 4-Phase Lifecycle** | [IBM Technology – Incident Response Process Explained](https://www.youtube.com/watch?v=gT5-8u5F6bE) | IBM Technology (~10m) | Preparation $\to$ Detection $\to$ Containment $\to$ Post-Incident Activity |
| **Ransomware Incident Containment** | [John Hammond – Investigating Real Ransomware](https://www.youtube.com/results?search_query=John+Hammond+Ransomware+Incident+Response) | John Hammond (~15m) | Preserving RAM vs network isolation, eradication & recovery |
| **Evidence Handling & Chain of Custody** | [Professor Messer – Forensic Chain of Custody](https://www.youtube.com/results?search_query=Professor+Messer+Chain+of+Custody+Forensics) | Professor Messer (~8m) | Integrity hashing (MD5/SHA), tamper-evident evidence log |

---

### Priority 4: Session 14 — SIEM, Disaster Recovery, RPO/RTO & BCP
* **Exam Weightage**: **10% – 12%** (Disaster Recovery Trade-Offs)

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **RPO vs RTO in Disaster Recovery** | [IBM Technology – RPO vs RTO Explained](https://www.youtube.com/watch?v=KzVj0n8gE4M) | IBM Technology (~8m) | Maximum data loss vs downtime tolerance, backup schedules |
| **Disaster Recovery Sites (Hot, Warm, Cold)** | [PowerCert – Disaster Recovery Sites Explained](https://www.youtube.com/watch?v=7hXzB9A1j7c) | PowerCert (~9m) | Synchronous replication vs tape restore, facility costs |
| **SIEM Architecture & Log Correlation** | [IBM Technology – What is a SIEM?](https://www.youtube.com/watch?v=d_k_y0pU8A8) | IBM Technology (~10m) | Centralized syslog collection, behavioral correlation rules |

---

### Priority 5: Session 06 — Authentication & Access Control Models (BLP, Biba)
* **Exam Weightage**: **10% – 12%** (Model Policy Formulation)

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **Bell-LaPadula Model (Confidentiality)** | [Gate Smashers – Bell LaPadula Model in Security](https://www.youtube.com/results?search_query=Gate+Smashers+Bell+LaPadula+Model) | Gate Smashers (~11m) | Simple Security (No Read Up), $\star$-Property (No Write Down) |
| **Biba Integrity Model** | [Gate Smashers – Biba Integrity Model](https://www.youtube.com/results?search_query=Gate+Smashers+Biba+Integrity+Model) | Gate Smashers (~10m) | Simple Integrity (No Read Down), $\star$-Integrity (No Write Up) |
| **Kerberos 3-Way Authentication** | [Gate Smashers – Kerberos Protocol Working](https://www.youtube.com/watch?v=5N242YCb354) | Gate Smashers (~13m) | AS, TGS, Ticket Granting Ticket (TGT), Service Ticket exchange |

---

### Priority 6: Session 10 — Database & Storage Security (SQL Injection)
* **Exam Weightage**: **8% – 10%** (Vulnerability & Defensive Code)

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **SQL Injection Mechanics & Exploitation** | [Computerphile – SQL Injection Explained](https://www.youtube.com/watch?v=_jKylhJtPmI) | Computerphile (~11m) | Tautology `' OR '1'='1`, comment syntax `--`, Union-based queries |
| **Preventing SQLi with Prepared Statements** | [Web Dev Simplified – SQL Injection Prevention in Code](https://www.youtube.com/watch?v=cbswflflv58) | Web Dev Simplified (~10m) | Parameter binding vs string concatenation, ORM query builders |
| **Database Access Control & Encryption** | [Gate Smashers – Database Security in DBMS](https://www.youtube.com/results?search_query=Gate+Smashers+Database+Security) | Gate Smashers (~12m) | Principle of least privilege, TDE (Transparent Data Encryption), RBAC |

---

### Priority 7: Session 05 — Cryptographic Hashes, Digital Signatures & PGP
* **Exam Weightage**: **8% – 10%** (Integrity & Non-Repudiation)

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **Cryptographic Hash Functions (SHA-256)** | [Computerphile – SHA-256 Hash Algorithm](https://www.youtube.com/watch?v=DMtFhACPnTY) | Computerphile (~11m) | Collision resistance, pre-image resistance, avalanche effect |
| **HMAC & Message Authentication Codes** | [Computerphile – HMAC Keyed Hashing](https://www.youtube.com/watch?v=wlSG3pEiQdc) | Computerphile (~9m) | Keyed hashing: $\text{HMAC}(K, M) = H((K \oplus opad) \parallel H((K \oplus ipad) \parallel M))$ |
| **Digital Signature Generation & Verification** | [Gate Smashers – Digital Signatures in Cryptography](https://www.youtube.com/watch?v=s22eJ1eVLTU) | Gate Smashers (~12m) | Signing with private key $S = H(M)^d \pmod n$, verifying with public key $e$ |
| **Pretty Good Privacy (PGP) Architecture** | [Gate Smashers – PGP Protocol in Network Security](https://www.youtube.com/results?search_query=Gate+Smashers+PGP+Protocol) | Gate Smashers (~13m) | Hybrid encryption: Session key encrypted via RSA, payload via symmetric AES |

---

### Priority 8: Session 08 — Ethical Hacking & Digital Forensics
* **Exam Weightage**: **8% – 10%** (Forensic Evidence & Recon)

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **Digital Forensics & Order of Volatility** | [Professor Messer – Forensic Procedures & Volatility](https://www.youtube.com/results?search_query=Professor+Messer+Order+of+Volatility) | Professor Messer (~9m) | Volatility hierarchy: CPU registers/cache $\to$ RAM $\to$ Swap $\to$ Disk $\to$ Backups |
| **Forensic Imaging & Chain of Custody** | [John Hammond – Creating a Forensic Disk Image](https://www.youtube.com/results?search_query=John+Hammond+Forensic+Disk+Image+dd) | John Hammond (~12m) | Write-blockers, bit-stream image (RAW/dd), MD5/SHA verification hashes |
| **Ethical Hacking 5-Phase Methodology** | [Edureka – Ethical Hacking Phases in 15 Minutes](https://www.youtube.com/watch?v=3Kq1MIfTWCE) | Edureka (~15m) | Reconnaissance $\to$ Scanning $\to$ Gaining Access $\to$ Maintaining $\to$ Clearing Tracks |

---

### Priority 9: Session 16 — Security Governance, ISO 27001 & Compliance
* **Exam Weightage**: **5% – 8%** (Security Policies & Audit)

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **ISO/IEC 27001 ISMS Framework** | [IT Governance – ISO 27001 Explained](https://www.youtube.com/watch?v=b4lZf8z8s9Y) | IT Governance (~10m) | Information Security Management System (ISMS), PDCA cycle, Annex A controls |
| **Security Policy Hierarchy** | [PowerCert – Policies, Standards, Baselines, Guidelines](https://www.youtube.com/watch?v=6O6rWw-w6a4) | PowerCert (~9m) | Mandatory policies vs technical standards vs voluntary guidelines |
| **Regulatory Privacy Compliance (DPDP & GDPR)** | [Simplilearn – What is GDPR & Data Protection?](https://www.youtube.com/watch?v=q6t8Z0h5G2E) | Simplilearn (~12m) | Right-to-forget, user consent lifecycle, 6-hour breach disclosure (CERT-In) |

---

### Priority 10: Session 03 — Network Security Protocols (IPSec, TLS)
* **Exam Weightage**: **5% – 8%** (Transport & Network Layer)

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **IPSec Architecture: AH vs ESP** | [Gate Smashers – IPSec Protocol in Computer Networks](https://www.youtube.com/watch?v=9jC9R1G-k9I) | Gate Smashers (~14m) | Authentication Header (AH) vs Encapsulating Security Payload (ESP) |
| **IPSec Modes: Tunnel vs Transport** | [PowerCert – IPSec Tunnel vs Transport Mode](https://www.youtube.com/watch?v=7zZc_U0M7Z8) | PowerCert (~10m) | Host-to-host (Transport) vs Gateway-to-gateway (Tunnel) packet structure |
| **TLS 1.3 Handshake Protocol** | [ByteByteGo – TLS 1.3 Handshake Explained](https://www.youtube.com/watch?v=1uDYPkmTe_k) | ByteByteGo (~8m) | 1-RTT handshake, Diffie-Hellman key derivation, deprecated RSA key exchange |

---

### Priority 11: Session 02 — Secure Architecture, DMZ & Firewalls
* **Exam Weightage**: **0% – 5%** (Perimeter Defense)

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **Demilitarized Zone (DMZ) Architecture** | [PowerCert – DMZ (Demilitarized Zone) Explained](https://www.youtube.com/watch?v=9_n8t9f5_7o) | PowerCert (~8m) | Dual-firewall DMZ topology, isolating public web servers from intranet DB |
| **Firewall Types: Packet Filter to NGFW** | [Gate Smashers – Firewalls in Network Security](https://www.youtube.com/watch?v=eYk1s5D8QzM) | Gate Smashers (~12m) | Stateless packet filtering, stateful inspection, Next-Gen application filtering |

---

### Priority 12: Session 07 — Cloud Security & Shared Responsibility
* **Exam Weightage**: **0% – 5%** (Cloud & Edge)

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **Cloud Shared Responsibility Model** | [IBM Technology – Shared Responsibility Model in Cloud](https://www.youtube.com/watch?v=2e6g6v4b6YI) | IBM Technology (~9m) | Who owns security at IaaS, PaaS, and SaaS tiers |
| **IoT Security Challenges & Constraints** | [IBM Technology – IoT Security Challenges](https://www.youtube.com/watch?v=9w9d5s_5k9k) | IBM Technology (~8m) | Low CPU/memory constraints, unencrypted firmware, lack of patchability |

---

### Priority 13: Session 01 — Security Basics, CIA Triad & STRIDE
* **Exam Weightage**: **0% – 4%** (Foundational)

| Topic / Concept | Recommended Video Link | Channel & Duration | Key Exam Focus |
| :--- | :--- | :---: | :--- |
| **The CIA Triad Explained** | [PowerCert – CIA Triad (Confidentiality, Integrity, Availability)](https://www.youtube.com/watch?v=7u7t0c1_e1A) | PowerCert (~9m) | Core security objectives and real-world countermeasure mappings |
| **STRIDE Threat Modeling Methodology** | [Microsoft Security – STRIDE Threat Modeling](https://www.youtube.com/results?search_query=Microsoft+STRIDE+Threat+Modeling) | Microsoft Security (~11m) | Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation of Privilege |
