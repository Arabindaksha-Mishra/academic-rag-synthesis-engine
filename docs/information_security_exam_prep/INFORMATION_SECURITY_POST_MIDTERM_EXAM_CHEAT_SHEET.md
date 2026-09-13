# BITS WILP Information Security (BSDCBZC311)
## Post-Midterm Master Exam Preparation & Open-Book Cheat Sheet

> **Course**: BSDCBZC311 — Information Security  
> **Exam Nature**: Open Book Comprehensive Exam | **Duration**: 2½ Hours  
> **Coverage**: Sessions 08 through 16 + Cryptographic & Access Control Foundations (Sessions 04, 05, 06)

---

## 1. Quantitative Risk Assessment Formulas (Session 13)

### 1.1 Single Loss Expectancy (SLE)
$$\text{SLE} = \text{Asset Value (AV)} \times \text{Exposure Factor (EF)}$$
- $\text{AV}$: Monopolistic or replacement worth of the asset (e.g., ₹50,00,000).
- $\text{EF}$: Percentage of asset value lost in a single incident ($0 \le \text{EF} \le 1.0$). If a fire destroys 40% of the datacenter, $\text{EF} = 0.40$.

### 1.2 Annualized Loss Expectancy (ALE)
$$\text{ALE} = \text{SLE} \times \text{ARO}$$
- $\text{ARO}$: Annualized Rate of Occurrence (estimated frequency of the threat event occurring per year).
  - Occurs once every 10 years $\implies \text{ARO} = 0.1$.
  - Occurs 5 times a year $\implies \text{ARO} = 5.0$.

### 1.3 Safeguard Cost-Benefit Analysis
$$\text{Net Annual Benefit} = (\text{ALE}_{\text{prior}} - \text{ALE}_{\text{post}}) - \text{ACS}$$
- $\text{ACS}$: Annual Cost of Safeguard (including software licensing, hardware amortized cost, and maintenance).
- **Decision Rule**: Implement countermeasure only if $\text{Net Benefit} > 0$.

---

## 2. Asymmetric Cryptography & Key Exchange (Session 04 & 05)

### 2.1 The RSA Algorithm Step-by-Step
1. **Key Generation**:
   - Choose two distinct large prime numbers: $p$ and $q$.
   - Calculate modulus: $n = p \times q$.
   - Calculate Euler's Totient: $\phi(n) = (p - 1)(q - 1)$.
   - Choose public exponent $e$: $1 < e < \phi(n)$ such that $\gcd(e, \phi(n)) = 1$ (Commonly $e = 65537$ or $e = 3$).
   - Compute private exponent $d$:
     $$d \times e \equiv 1 \pmod{\phi(n)} \iff d = e^{-1} \pmod{\phi(n)}$$
     *(Use Extended Euclidean Algorithm)*.
   - **Public Key**: $(e, n)$ | **Private Key**: $(d, n)$.
2. **Encryption & Decryption**:
   $$\text{Ciphertext } C = M^e \pmod n$$
   $$\text{Plaintext } M = C^d \pmod n$$
3. **Digital Signature**:
   $$\text{Signature } S = [H(M)]^d \pmod n$$
   $$\text{Verification: Compute } V = S^e \pmod n; \quad \text{Check if } V \stackrel{?}{=} H(M)$$

### 2.2 Diffie-Hellman Key Exchange Protocol
- **Public Domain Parameters**: Large prime $p$, primitive root modulo $p$: $g$.
- **Step 1 (Alice)**: Selects private secret $a$ ($1 \le a < p$). Computes public value $A = g^a \pmod p$. Sends $A$ to Bob.
- **Step 2 (Bob)**: Selects private secret $b$ ($1 \le b < p$). Computes public value $B = g^b \pmod p$. Sends $B$ to Alice.
- **Step 3 (Shared Secret Computation)**:
  - Alice computes: $K = B^a \pmod p = (g^b)^a \pmod p = g^{ab} \pmod p$.
  - Bob computes: $K = A^b \pmod p = (g^a)^b \pmod p = g^{ab} \pmod p$.
- **Vulnerability**: Vulnerable to Man-in-the-Middle (MitM) if unauthenticated. Solved via Digital Certificates (PKI).

---

## 3. Mandatory Access Control Models (Session 06)

### 3.1 Bell-LaPadula Model (Confidentiality / Military)
*Focus: Enforcing data secrecy through security levels (Top Secret > Secret > Confidential > Unclassified).*
1. **Simple Security Property (ss-property)**:
   $$\text{"No Read Up" (NRU)} \implies \text{Subject } S \text{ can read Object } O \iff L(S) \ge L(O)$$
2. **$\star$-Property (Star Property)**:
   $$\text{"No Write Down" (NWD)} \implies \text{Subject } S \text{ can write to Object } O \iff L(S) \le L(O)$$
   *(Prevents higher-cleared subjects from leaking secret data into public objects)*.

### 3.2 Biba Integrity Model (Commercial Integrity)
*Focus: Preventing unauthorized corruption or modification of critical business records.*
1. **Simple Integrity Property**:
   $$\text{"No Read Down" (NRD)} \implies \text{Subject } S \text{ can read Object } O \iff I(S) \le I(O)$$
   *(Prevents corrupted data from flowing into high-integrity subjects)*.
2. **$\star$-Integrity Property**:
   $$\text{"No Write Up" (NWU)} \implies \text{Subject } S \text{ can write to Object } O \iff I(S) \ge I(O)$$
   *(Prevents untrusted low-integrity subjects from contaminating high-integrity databases)*.

---

## 4. Disaster Recovery & Business Continuity (Session 14)

### 4.1 RPO vs. RTO Timeline

```
[ Normal Ops ] -----( Incident Occurs )------------------------( System Restored )
      |                        |                                      |
      |<--- RPO Threshold ---->|<----------- RTO Threshold ---------->|
         (Max Data Loss)                        (Downtime Duration)
```

- **Recovery Point Objective (RPO)**: The maximum acceptable age of files that must be recovered from backup storage for normal operations to resume. Focuses on **data loss**.
- **Recovery Time Objective (RTO)**: The maximum acceptable duration of time that a system can remain down after an outage before significant business loss occurs. Focuses on **downtime**.

### 4.2 Recovery Site Comparison

| Site Category | Setup Cost | RTO | Hardware Status | Data Status |
| :--- | :---: | :---: | :--- | :--- |
| **Hot Site** | Very High | **Minutes to < 1 hr** | Fully provisioned & running | Real-time synchronous replication |
| **Warm Site** | Medium | **Hours to 1 day** | Pre-installed hardware/OS | Restores from periodic backup tape/snapshots |
| **Cold Site** | Low | **Days to weeks** | Empty space, power & cooling | No pre-configured hardware or live data |

---

## 5. Incident Response Lifecycle — NIST SP 800-61 (Session 15)

```
        +-------------------------------------------------------------+
        |                 1. PREPARATION                              |
        |  Policies, CSIRT Team, Tooling (SIEM/EDR), Threat Intel      |
        +------------------------------+------------------------------+
                                       |
        +------------------------------v------------------------------+
        |                 2. DETECTION & ANALYSIS                     |
        |  Triaging Alerts, IOC Identification, Attack Scoping        |
        +------------------------------+------------------------------+
                                       |
        +------------------------------v------------------------------+
        |                 3. CONTAINMENT, ERADICATION & RECOVERY      |
        |  Isolate Subnets -> Remove Malware -> Rebuild & Staged Sync |
        +------------------------------+------------------------------+
                                       |
        +------------------------------v------------------------------+
        |                 4. POST-INCIDENT ACTIVITY                   |
        |  Lessons Learned, Evidence Archive, Policy Adjustments      |
        +-------------------------------------------------------------+
```

---

## 6. Database Security & SQL Injection Prevention (Session 10)

### 6.1 The Vulnerable Pattern (Dynamic Concatenation)
```python
# HIGHLY VULNERABLE: Direct string interpolation allows attacker to inject SQL statements
query = f"SELECT * FROM users WHERE username = '{user_input}' AND password = '{pwd}'"
# Attacker enters username: admin' --
# Query executes: SELECT * FROM users WHERE username = 'admin' --' AND password = '...'
```

### 6.2 The Secure Pattern (Parameterized Prepared Statements)
```python
# SECURE: Database engine pre-compiles query structure; user input is bound strictly as data literal
cursor.execute(
    "SELECT id, role, hash FROM users WHERE username = %s AND password_hash = %s",
    (sanitized_username, hashed_password)
)
```
