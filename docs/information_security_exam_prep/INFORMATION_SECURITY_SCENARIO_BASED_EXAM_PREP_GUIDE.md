# BITS WILP Information Security (BSDCBZC311)
# Master Scenario-Based Exam Preparation Guide (Sessions 08 – 16)

> **Course**: BSDCBZC311 — Information Security  
> **Exam Nature**: Open Book | **Total Marks**: 40 Marks | **Duration**: 2½ Hours  
> **Core Strategy**: Case-Study & Scenario Answering Framework

---

## 1. Universal Security Scenario Extraction Framework

In BITS WILP Information Security exams, questions are framed around enterprise case studies (e.g., *"FinSafe Digital Bank"*, *"ArogyaCloud Telemedicine"*, *"LogiTrack Autonomous Fleet"*).

Before answering, extract these 4 core dimensions from the prompt:
1. **Critical Assets**: Customer PII, Financial Ledgers, Electronic Health Records (EHR), Cryptographic Private Keys.
2. **Threat Actors & Vectors**: Disgruntled insider, external ransomware syndicate, SQL injection via public web API, unsegmented supply-chain vendor network.
3. **Regulatory Constraints**: DPDP Act 2023 (India), RBI IT Framework, HIPAA, PCI-DSS Level 1.
4. **Primary Security Objectives**: High availability under DDoS, strict confidentiality of records, undeniable audit logs (non-repudiation).

---

## 2. Session-Wise Scenario Answering Blueprints

---

### SCENARIO TOPIC 1: Quantitative Risk Assessment & Business Case (Session 13)
*Exam Prompt*: *"FinSafe Bank holds an online database containing 1,000,000 customer accounts valued at ₹2,000 each. An external audit estimates a ransomware attack has an Exposure Factor of 30% and occurs once every 4 years. A cloud-native automated immutable backup & EDR solution costs ₹1,50,000 annually and reduces the Exposure Factor to 5% with an occurrence of once every 10 years. Perform a quantitative risk analysis and advise the Board."*

#### Structured Answering Steps:
1. **Calculate Baseline Risk ($\text{ALE}_{\text{prior}}$)**:
   - Asset Value $\text{AV} = 1,000,000 \times ₹2,000 = ₹2,000,000,000$ (200 Crores).
   - Single Loss Expectancy:
     $$\text{SLE}_{\text{prior}} = \text{AV} \times \text{EF}_{\text{prior}} = ₹2,000,000,000 \times 0.30 = ₹600,000,000$$
   - Annualized Rate of Occurrence: $\text{ARO}_{\text{prior}} = \frac{1}{4} = 0.25$.
   - Baseline Annualized Loss Expectancy:
     $$\text{ALE}_{\text{prior}} = \text{SLE}_{\text{prior}} \times \text{ARO}_{\text{prior}} = ₹600,000,000 \times 0.25 = ₹150,000,000$$

2. **Calculate Mitigated Risk ($\text{ALE}_{\text{post}}$)**:
   - $\text{SLE}_{\text{post}} = \text{AV} \times \text{EF}_{\text{post}} = ₹2,000,000,000 \times 0.05 = ₹100,000,000$.
   - $\text{ARO}_{\text{post}} = \frac{1}{10} = 0.10$.
   - $$\text{ALE}_{\text{post}} = ₹100,000,000 \times 0.10 = ₹10,000,000$$

3. **Cost-Benefit Justification**:
   $$\text{Gross Annual Savings} = \text{ALE}_{\text{prior}} - \text{ALE}_{\text{post}} = ₹150,000,000 - ₹10,000,000 = ₹140,000,000$$
   $$\text{Net Annual Benefit} = \text{Gross Savings} - \text{ACS} = ₹140,000,000 - ₹1,50,000 = ₹139,850,000$$
   - **Board Recommendation**: Strongly recommend immediate procurement. The safeguard yields an extraordinary net annual risk reduction of over ₹13.98 Crores against an annual outlay of only ₹1.5 Lakhs.

---

### SCENARIO TOPIC 2: Incident Response to a Ransomware Outbreak (Session 15)
*Exam Prompt*: *"A healthcare provider discovers that workstations in the radiology department are displaying ransom notes and files are encrypted with .locked extension. Apply NIST SP 800-61 to manage the crisis."*

```
[ PHASE 1: PREPARATION ]
• Maintain off-site, air-gapped immutable backups.
• Pre-define CSIRT roles (Incident Commander, Forensic Lead, Legal Counsel, PR Officer).

[ PHASE 2: DETECTION & ANALYSIS ]
• Identify patient zero via SIEM logs (abnormal SMB traffic on port 445).
• Extract IOCs: file hashes, C2 IP addresses, suspicious PowerShell command lines.
• Scope infection boundary: Determine which subnets, servers, and EHR databases are impacted.

[ PHASE 3: CONTAINMENT, ERADICATION & RECOVERY ]
• Short-Term Containment: Sever physical/VLAN network connections; disable affected active directory accounts (Do NOT power off machines to preserve RAM forensics).
• Eradication: Re-image compromised endpoints from known-good gold images; revoke and rotate all Kerberos krbtgt and admin credentials.
• Recovery: Restore medical databases from verified clean snapshots; test in isolated staging sandbox; bring online with continuous telemetry monitoring.

[ PHASE 4: POST-INCIDENT ACTIVITY (LESSONS LEARNED) ]
• Conduct formal Root Cause Analysis (RCA) meeting within 72 hours.
• Submit mandatory regulatory breach notification to CERT-In / Data Protection Board within 6 hours as required by Indian cybersecurity directives.
```

---

### SCENARIO TOPIC 3: Access Control Model Justification (Session 06)
*Exam Prompt*: *"The Ministry of Defence or a High-Security Hospital requires an access control policy where doctors can read patient history but cannot leak classified diagnoses to public portals, while lab machines cannot corrupt verified doctor records. Evaluate Bell-LaPadula vs. Biba."*

1. **For Confidentiality Protection $\implies$ Bell-LaPadula (BLP)**:
   - Assign security clearances: Doctor (Secret), Patient Portal (Unclassified).
   - Apply **Simple Security (No Read Up)**: Doctor cannot read Top Secret research without clearance.
   - Apply **$\star$-Property (No Write Down)**: A Doctor logged into the Secret EHR system is strictly prohibited from writing or exporting medical summaries down to an Unclassified public portal or external email.
2. **For Data Integrity & Accuracy $\implies$ Biba Model**:
   - Assign integrity levels: Board Specialist Doctor (High Integrity), Public Web Form / Automated IoT Sensor (Low Integrity).
   - Apply **Simple Integrity (No Read Down)**: High-integrity diagnosis algorithms will not consume unverified, untrusted raw inputs directly.
   - Apply **$\star$-Integrity (No Write Up)**: Low-integrity web clients or guest users cannot write to or alter the high-integrity master patient database.

---

### SCENARIO TOPIC 4: Database Defense & SQL Injection Mitigation (Session 10)
*Exam Prompt*: *"An e-commerce checkout platform was breached via a login page bypass. Detail the vulnerability mechanics, provide the vulnerable query, and show the defensive code implementation."*

1. **Vulnerability Mechanics**: Dynamic query string concatenation causes un-escaped user input to be interpreted as SQL syntax rather than literal data.
2. **Vulnerable Code**:
   ```sql
   SELECT * FROM accounts WHERE email = 'victim@mail.com' AND pass = 'any' OR '1'='1';
   ```
3. **Remediation via Parameterized Prepared Statement (Defense-in-Depth)**:
   - **Primary Control**: Parameterized binding separating SQL structure from untrusted input values.
   - **Secondary Control**: Principle of Least Privilege (DB user has only `SELECT` privileges, cannot execute `DROP` or `UNION` across administrative tables).
   - **Tertiary Control**: Web Application Firewall (WAF) rule blocking SQL meta-characters (`'`, `--`, `;`).

---

## 3. Universal Domain Translation Table

| Security Dimension | Banking / FinTech | Healthcare Telemedicine | Smart Grid / IoT |
| :--- | :--- | :--- | :--- |
| **Top Threat** | Account takeover, wire fraud | Patient EHR data theft, ransomware | Substation command hijacking |
| **Primary Goal** | Transaction integrity & non-repudiation | Strict privacy (DPDP/HIPAA) | Operational availability & low latency |
| **Crypto Choice** | RSA-4096 / AES-256-GCM | TLS 1.3 / AES-256 at rest | Elliptic Curve (ECDSA) for low-power |
| **Access Control** | Role-Based Access Control (RBAC) | Discretionary + Attribute-Based (ABAC) | Zero-Trust Network Access (ZTNA) |
| **Recovery SLA** | $\text{RPO} \le 0\text{ s}$ (Synchronous), $\text{RTO} < 1\text{ hr}$ | $\text{RPO} < 15\text{ mins}$, $\text{RTO} < 2\text{ hrs}$ | $\text{RTO} < 5\text{ mins}$ (Real-time grid) |
