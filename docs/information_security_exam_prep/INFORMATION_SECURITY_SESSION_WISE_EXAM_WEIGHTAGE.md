# BITS WILP Information Security (BSDCBZC311)
## Detailed Session-Wise Exam Importance & Weightage Blueprint

> **Course**: BSDCBZC311 — Information Security  
> **Exam Nature**: Open Book | **Total Marks**: 40 Marks (40% Course Weightage) | **Duration**: 2½ Hours  
> **Core Texts**: William Stallings, *Cryptography and Network Security*; Matt Bishop, *Computer Security: Art and Science*

---

## 1. Executive Summary & Weightage Distribution

In the BITS WILP Information Security curriculum, the **Comprehensive Examination (EC-3 Regular)** is an open-book exam administered after the midterm. 
The comprehensive exam paper exhibits an overwhelming concentration on **Post-Midterm sessions (Sessions 08 through 16)** along with critical mathematical foundations from Sessions 03, 04, 05, and 06.

```
+-------------------------------------------------------------------------------+
|                 COMPREHENSIVE EXAM MARK DISTRIBUTION (40 MARKS)              |
+-------------------------------------------------------------------------------+
| Pre-Midterm Theory (Sessions 01 – 03: Basics, Architecture, DMZ)  :  5% – 15% |
| Mathematical Foundations (Sessions 04 – 06: Crypto, Hashes, Auth) : 25% – 35% |
| Post-Midterm Applied (Sessions 08 – 16: Forensics, Risk, Incident): 55% – 70% |
+-------------------------------------------------------------------------------+
```

---

## 2. Complete Session-Wise Importance & Weightage Matrix (CS01 – CS16)

| Session ID | Session Title & Core Focus | Priority Tier | Compre Exam Weightage | Typical Question Format |
| :---: | :--- | :---: | :---: | :--- |
| **Session 13** | **Security Operations & Quantitative Risk (ALE, SLE)** | **Tier 1 (Super Critical)** | **15% – 20% (6 – 8 M)** | Compulsory numerical: Calculate Single Loss Expectancy (SLE) and Annualized Loss Expectancy (ALE), justify Safeguard Cost-Benefit. |
| **Session 04** | **Asymmetric & Symmetric Cryptography (RSA, AES, DH)** | **Tier 1 (Super Critical)** | **15% – 20% (6 – 8 M)** | Mathematical step-by-step: RSA key generation, modular arithmetic $e \cdot d \equiv 1 \pmod{\phi(n)}$, Diffie-Hellman key exchange. |
| **Session 15** | **Incident Response Lifecycle (NIST SP 800-61)** | **Tier 1 (Critical)** | **12% – 15% (5 – 6 M)** | Scenario-based: Formulate a 4-phase incident response plan (Preparation, Detection, Containment, Post-Incident) for ransomware or data breach. |
| **Session 14** | **SIEM, Disaster Recovery, RPO & RTO, BCP** | **Tier 1 (Critical)** | **10% – 12% (4 – 5 M)** | Scenario trade-off: Calculate RPO/RTO thresholds, Hot vs Warm vs Cold site selection, SIEM correlation rule formulation. |
| **Session 06** | **Authentication, Access Control (RBAC, BLP, Biba)** | **Tier 1 (Critical)** | **10% – 12% (4 – 5 M)** | Scenario security model: Apply Bell-LaPadula (No Read Up, No Write Down) vs Biba (No Read Down, No Write Up); Kerberos ticket exchange. |
| **Session 10** | **Database & Storage Security (SQLi Prevention)** | **Tier 2 (High)** | **8% – 10% (3 – 5 M)** | Code/scenario vulnerability: Identify SQL injection vulnerability, write parameterized prepared statements, role-based database privileges. |
| **Session 05** | **Hashes, HMAC, Digital Signatures, PGP** | **Tier 2 (High)** | **8% – 10% (3 – 5 M)** | Protocol mechanics: Digital signature generation ($S = H(M)^d \pmod n$), collision resistance, PGP hybrid encryption flow. |
| **Session 08** | **Ethical Hacking & Digital Forensics** | **Tier 2 (High)** | **8% – 10% (3 – 5 M)** | Forensic investigation: Chain of custody protocol, volatile memory acquisition (RAM dump), anti-forensics mitigation. |
| **Session 16** | **Security Governance, ISO 27001, Compliance** | **Tier 2 (High)** | **5% – 8% (2 – 4 M)** | Governance scenario: ISO 27001 PDCA cycle, GDPR / DPDP Act regulatory compliance requirements, security policy hierarchy. |
| **Session 03** | **Network Security Protocols (IPSec, TLS)** | **Tier 3 (Moderate)** | **5% – 8% (2 – 4 M)** | Protocol walkthrough: IPSec AH vs ESP (Transport vs Tunnel mode), TLS 1.3 Handshake sequence. |
| **Session 02** | **Secure Architecture, DMZ & Firewalls** | **Tier 3 (Moderate)** | **0% – 5% (0 – 3 M)** | Network diagram: Dual-homed DMZ subnetting, Next-Gen Firewall (NGFW) rule set evaluation. |
| **Session 07** | **Cloud & IoT Security (Shared Responsibility)** | **Tier 3 (Low)** | **0% – 5% (0 – 3 M)** | Cloud model: IaaS vs PaaS vs SaaS Shared Responsibility matrix, IoT edge security constraints. |
| **Session 01** | **CIA Triad & STRIDE Threat Modeling** | **Tier 3 (Foundation)** | **0% – 4% (0 – 2 M)** | Foundational: STRIDE threat decomposition table applied to case study. |

---

## 3. High-Yield Post-Midterm Deep Dive

### Session 13: Quantitative Risk Assessment & Security Operations
* **Primary Topic**: Financial impact calculation of security breaches and countermeasure ROI.
* **Core Equations**:
  $$\text{SLE} = \text{Asset Value (AV)} \times \text{Exposure Factor (EF)}$$
  $$\text{ALE} = \text{SLE} \times \text{Annualized Rate of Occurrence (ARO)}$$
  $$\text{Cost-Benefit} = (\text{ALE}_{\text{prior}} - \text{ALE}_{\text{post}}) - \text{Annual Cost of Safeguard (ACS)}$$
* **Common Trap**: Confusing Exposure Factor (percentage $0.0$ to $1.0$) with ARO (frequency per year).

### Session 14: Disaster Recovery & Business Continuity (BCP)
* **Primary Topic**: Balancing data loss tolerance against recovery budgets.
* **Core Metrics**:
  - **Recovery Point Objective (RPO)**: Maximum tolerable data loss measured in time (e.g., $\le 15\text{ mins}$ requiring continuous replication).
  - **Recovery Time Objective (RTO)**: Maximum tolerable downtime before business resumption (e.g., $\le 2\text{ hours}$).
  - **Recovery Sites**: Hot Site (minutes, mirrors data live), Warm Site (hours, hardware ready, data restored from backup), Cold Site (days, shell facility).

### Session 15: Incident Response Lifecycle (NIST SP 800-61 Rev. 2)
* **Primary Topic**: Systematic handling of active security incidents.
* **The 4 Standard Phases**:
  1. *Preparation*: Policy formulation, tool deployment (EDR, SIEM), incident response team (CSIRT) training.
  2. *Detection & Analysis*: Triaging alerts, indicators of compromise (IOCs), scoping attack vector.
  3. *Containment, Eradication & Recovery*: Short-term containment (network isolation), eradication of persistence mechanisms, staged restoration.
  4. *Post-Incident Activity (Lessons Learned)*: Evidence retention, root cause analysis (RCA), policy refinement.

---

## 4. Priority Revision Order for Exam Hall

1. **Numericals First**: Master **RSA modular math**, **Diffie-Hellman equations**, and **ALE / Cost-Benefit risk equations**.
2. **Models & Frameworks**: Memorize **Bell-LaPadula rules**, **Biba rules**, **NIST 4-phase incident lifecycle**, and **STRIDE matrix**.
3. **Database & Code Security**: Be ready to write **Prepared Statements** preventing SQL injection.
