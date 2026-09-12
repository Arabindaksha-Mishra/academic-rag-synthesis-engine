# BITS WILP Software Engineering (BSDCBZC343 / BSDCHZC343)
# Master Scenario-Based Exam Preparation Guide (Sessions 08 – 16)

> **Exam Nature**: Open Book | **Total Marks**: 40 Marks (Weightage: 40%) | **Duration**: 2½ Hours  
> **Course**: BSDCBZC343 / BSDCHZC343 — Software Engineering  
> **Targeted Strategy**: Scenario-Wise & Case-Study Driven Answering Framework  
> **Benchmark Exam Paper**: [`SE_25-S1_CR_QP_BSDCHZC343.docx`](file:///usr/local/google/home/arabindaksha/Downloads/SE_25-S1_CR_QP_BSDCHZC343.docx) (*ArogyaMitra Healthcare Case Study*)

---

## 1. Anatomy of a BITS WILP Scenario-Based Question Paper

In BITS WILP Comprehensive Exams, examiners do **NOT** ask abstract textbook questions. The entire question paper is anchored around an **unseen case study** (e.g., Healthcare, FinTech, Autonomous Logistics, EdTech, Smart Grid).

Every single question directly tests your ability to **translate software engineering principles (Sessions 08–16)** into the specific operational realities of that scenario.

```
+-----------------------------------------------------------------------------------------+
|                              TYPICAL EXAM SCENARIO STRUCTURE                            |
+-----------------------------------------------------------------------------------------+
| 1. The Enterprise: Name of company & project (e.g., MedSolve developing "ArogyaMitra")  |
| 2. Target Personas: End-users (e.g., Rural patients vs Urban Specialist Doctors)         |
| 3. Operational Channels: Mobile app (Android/iOS) + Web Portal + Payment/Third-party API|
| 4. Environmental Constraints: Low bandwidth (2G/3G), multi-lingual, privacy regulations |
| 5. Critical Subsystems: Payment processing, real-time video, large file uploads, queues |
+-----------------------------------------------------------------------------------------+
```

---

## 2. Universal Scenario Decomposition Blueprint (First 5 Minutes of Exam)

Whenever you open the exam paper and read the case study, perform this 60-second entity extraction on rough paper before writing answers:

```
[ SCENARIO EXTRACTION MATRIX ]
├── Core Subsystems:        Subsystem 1 (e.g., Payments), Subsystem 2 (e.g., Video), Subsystem 3 (e.g., Reports)
├── Primary End-Users:      End-User A (Non-technical / Rural / Customer), End-User B (Specialist / Admin)
├── Critical Non-Functional: Bandwidth limits, 99.99% availability, DPDP/PCI-DSS privacy, Data integrity
└── Failure Modes:          Network drop during transaction/upload, server overload, unauthorized data leak
```

---

## 3. Session-by-Session Scenario Answering Blueprints (Sessions 08 – 16)

---

### SESSION 09 & 07: Component-Level Design & Design Concepts
**Typical Exam Weightage**: **9 – 12 Marks (Highest Yield Question Q1a & Q1c)**

#### Scenario Trigger 1: "Design a Class-Based Component for a Subsystem" (5 Marks)
*Exam Prompt*: *"Using Pressman's principles, detail the steps in Component-Level Design for a Class-Based Component responsible for [Subsystem X, e.g., Payment / Booking / Telemetry]. Specify 2 attributes, 3 operations, and explain cohesion and coupling."*

##### Step-by-Step Scenario Answering Formula:
1. **Name the Primary Class with Domain Precision**: Avoid generic names like `Manager`. Use `PaymentTransactionManager`, `ConsultationSessionController`, `DispatchOrderCoordinator`.
2. **Specify 2 Domain Attributes with Explicit Types & Visibility**:
   - Attribute 1 (Identity/Audit): `private transactionId: java.util.UUID` (Immutable globally unique transaction trace).
   - Attribute 2 (Lifecycle State): `private transactionStatus: PaymentStatusEnum` (`INITIATED`, `PENDING_GATEWAY`, `SUCCESSFUL`, `FAILED`, `REFUNDED`).
3. **Specify 3 Operations with Full Signatures**:
   - Operation 1 (Initiation): `public initiateTransaction(userId: String, amount: BigDecimal, gatewayType: GatewayEnum): TransactionToken`
   - Operation 2 (Verification/Callback): `public verifyGatewayResponse(callbackPayload: Map<String, String>, signatureHash: String): Boolean`
   - Operation 3 (Exception/Rollback): `public executeRefund(transactionId: UUID, failureReason: String): RefundReceiptDTO`
4. **Scenario-Grounded Cohesion Justification (Aim: Functional Cohesion)**:
   - *"This class exhibits strict **Functional Cohesion** because every attribute and operation is dedicated exclusively to managing financial transaction state transitions. Ancillary tasks such as sending SMS/WhatsApp confirmation alerts or updating doctor schedules are deliberately delegated to external services (`NotificationService`, `ScheduleService`)."*
5. **Scenario-Grounded Coupling Justification (Aim: Data Coupling)**:
   - *"This class maintains **Low Data Coupling** by communicating with third-party gateways and client controllers solely through typed Data Transfer Objects (`PaymentRequestDTO`, `PaymentReceiptDTO`) and abstract interface contracts (`IPaymentGatewayAdapter`), hiding all internal database connections and secret encryption keys."*

---

#### Scenario Trigger 2: "Component Design for Web Applications under Hostile Network Conditions" (4 Marks)
*Exam Prompt*: *"Patient/User needs to upload a large diagnostic report (PDF/DICOM/Video). Outline a Component Design for WebApps that ensures robustness against network interruptions typical in rural/intermittent contexts."*

##### The 4-Pillar Resilient WebApp Architecture:

```
[ Client Device ]                                                 [ Backend Server & Storage ]
      |                                                                       |
      |--- 1. Partition File into 512KB Binary Chunks (HTML5 File API) ------>|
      |--- 2. Request Session Token: UUID + TotalChunks + Checksum ---------->| Server issues SessionId
      |--- 3. Transmit Chunks via Async Worker: {SessionId, Index, Hash} ---->| Ack stored in Redis
      |                                                                       |
      x <-- [NETWORK DROP DETECTED: Offline-First Local Queue (IndexedDB)] --> x
      |                                                                       |
      |--- 4. Network Restored: Retry with Exponential Backoff + Jitter ----->| Resume from Chunk Index N
      |--- 5. Final Chunk Transmitted --------------------------------------->| Assemble & Verify SHA256
```

1. **Client-Side Binary Chunking**: Using HTML5 File API or mobile stream buffers, partition the large PDF into uniform binary blocks (e.g., 512 KB per chunk).
2. **Session Identification & Idempotency Metadata**:
   $$\text{Handshake Payload} = \{\text{SessionUUID}, \text{ChunkIndex}, \text{TotalChunks}, \text{SHA256Hash}\}$$
3. **Local Offline-First Queue (IndexedDB / SQLite)**: Store un-uploaded chunk references locally on the client device so app crashes, tab refreshes, or device battery drains do not lose upload state.
4. **Exponential Backoff Reconnection Algorithm**:
   $$t_{\text{retry}} = \min\left(2^n \times 500\text{ ms}, 30000\text{ ms}\right) + \text{RandomJitter}$$
5. **Server-Side Reassembly**: The server tracks received chunk indices in a fast memory cache (Redis). Once all chunk indices arrive, the server concatenates blocks into the final document and verifies the aggregate SHA-256 checksum.

---

### SESSION 08 & 11: Architectural Design & Pattern-Based Design
**Typical Exam Weightage**: **6 – 8 Marks (Question Q1b)**

#### Scenario Trigger 1: "Why Model-View-Controller (MVC) for a Specific Portal?"
*Exam Prompt*: *"The team is considering MVC for the Doctor's Secure Web Portal. Explain WHY MVC is appropriate for this specific portal, and map system requirements to View, Controller, and Model."*

##### 1. Why MVC is Appropriate for This Specific Scenario:
- **Separation of Concerns**: Clinical decision rules and sensitive patient records (Model) are completely isolated from dynamic front-end web framework changes (View).
- **Multi-Client Rendering**: A single medical record Model supports multiple distinct Views (e.g., Doctor Desktop Web Portal, Doctor Tablet App, Prescription PDF export) without rewriting business logic.
- **Centralized Security Enforcement**: The Controller acts as a centralized authentication and access-control gatekeeper verifying doctor digital signatures and session tokens before state modifications.

##### 2. Scenario-to-MVC Mapping Matrix:

| MVC Element | ArogyaMitra Healthcare Scenario | FinTech / Banking Scenario | Smart Logistics Scenario |
| :--- | :--- | :--- | :--- |
| **Model** | `PatientHealthRecord`, `DoctorSchedule`, `Prescription` | `BankAccount`, `TransactionLedger`, `FraudRulesEngine` | `VehicleTelemetry`, `ConsignmentManifest`, `DriverRoute` |
| **View** | `DoctorPortalDashboard.jsx`, `VideoCallWindow.html`, `VitalsChart.vue` | `AccountStatementView.html`, `TransferConfirmationModal.jsx` | `LiveGPSMapView.jsx`, `DispatchScheduleTable.html` |
| **Controller** | `AppointmentController`, `TeleConsultController`, `AuthInterceptor` | `FundTransferController`, `KYCVerificationController` | `RouteOptimizationController`, `FleetDispatchController` |

---

#### Scenario Trigger 2: "Suggest and Justify a Second Design Pattern for the System"
*Exam Prompt*: *"Suggest a second suitable design pattern (Architecture, Component, or UI) and justify its application to a different aspect (e.g., real-time alerts, gateway integration, error logging)."*

Pick from these three plug-and-play pattern justifications based on the scenario need:

##### Option A: The Observer Pattern (Behavioral) — For Real-Time Queues / Alerts
- **Where Applied**: Tele-consultation virtual waiting room or order status broadcast.
- **Scenario Justification**: When a patient joins the video call waiting room, enters an emergency vitals spike, or completes a payment, the `ConsultationQueueSubject` notifies multiple listening UI components (`DoctorWaitingRoomView`, `AudioAlertService`, `NurseMonitoringDashboard`) in real-time without tight coupling.

##### Option B: The Adapter Pattern (Structural) — For Multi-Gateway / External Vendor Integration
- **Where Applied**: Integrating diverse Indian payment systems (UPI, Paytm, Razorpay, SBI NetBanking).
- **Scenario Justification**: External banking APIs expose conflicting function signatures. Implementing `IPaymentGatewayAdapter` allows `PaymentTransactionManager` to call a single uniform method `executePayment()`, while concrete adapters (`UPIAdapter`, `NetBankingAdapter`) translate calls to vendor-specific protocols.

##### Option C: The Facade Pattern (Structural) — For Complex Multi-Subsystem Workflows
- **Where Applied**: One-click consultation checkout or booking workflow.
- **Scenario Justification**: Coordinates `BillingService`, `ScheduleService`, `NotificationService`, and `VideoTokenService` behind a single clean entry-point `ConsultationFacade.bookSession()`.

---

### SESSION 10: User Interface Design and Heuristics
**Typical Exam Weightage**: **5 – 8 Marks (Question Q2a)**

#### Scenario Trigger: "Design Wireframe & Critique Using Theo Mandel's 3 Golden Rules"
*Exam Prompt*: *"Design the initial wireframe for the Patient Interface Home Screen. Critique your design by selecting and applying THREE specific Golden Rules and explaining how they enhance UX for non-technical/rural users."*

##### Step 1: Draw the Scenario Wireframe (ASCII Diagram)
Ensure your wireframe contains large icons, vernacular bilingual labels, and emergency shortcuts:

```text
+-------------------------------------------------------------------+
| [Logo] ArogyaMitra (आरोग्य मित्र)              [🌐 भाषा: हिंदी/ENG] |
+-------------------------------------------------------------------+
| Welcome, Ramesh Kumar! (नमस्ते रमेश जी)                            |
| 🚨 EMERGENCY / आपातकालीन सहायता: [ CALL 108 NOW / तुरंत कॉल करें ] |
+-------------------------------------------------------------------+
|                                                                   |
|   +--------------------------+     +--------------------------+   |
|   |    [👨‍⚕️ Big Stethoscope]  |     |     [📁 Big Folder Icon]  |   |
|   |   Talk to Doctor (Video) |     |   My Reports / Upload    |   |
|   |    डॉक्टर से बात करें     |     |     जांच रिपोर्ट भेजें    |   |
|   +--------------------------+     +--------------------------+   |
|                                                                   |
|   +--------------------------+     +--------------------------+   |
|   |      [₹ Rupee Note]      |     |     [🎙️ Big Microphone]   |   |
|   |    Pay Fee / रसीद देखें   |     |    Speak to Assistant    |   |
|   |       फीस जमा करें       |     |     बोलकर मदद पाएं       |   |
|   +--------------------------+     +--------------------------+   |
|                                                                   |
+-------------------------------------------------------------------+
| [ 🏠 Home ]     [ 📅 Appointments ]     [ 💬 Chat ]     [ ❓ Help ]|
+-------------------------------------------------------------------+
```

##### Step 2: The 3 Golden Rules Critique (Scenario-Grounded):
1. **Rule 1: Place the User in Control**:
   - *Application*: For non-technical or anxiety-prone users, all operations feature prominent **"Cancel / रद्द करें"** and **"Back / वापस"** navigation. Audio explanations can be paused, replayed, or silenced at any moment. Destructive actions (canceling an appointment) require explicit confirmation prompts.
2. **Rule 2: Reduce the User's Memory Load**:
   - *Application*: Rural users with low digital literacy cannot navigate complex nested menus. The design replaces abstract technical text with **real-world visual metaphors** (stethoscope for doctor video call, rupee currency note for payment, microphone for voice search) paired with vernacular audio prompts, adhering to Miller’s Law ($7 \pm 2$ cognitive chunks).
3. **Rule 3: Make the Interface Consistent**:
   - *Application*: Standard 4-tile grid maintained across all screens; identical color psychology (green for confirmative booking, red for medical emergency/cancel, blue for informational reports); button physical coordinates remain fixed between Hindi and English language toggles.

---

### SESSION 14: Software Quality Assurance (SQA) & Reviews
**Typical Exam Weightage**: **10 – 12 Marks (Question Q2b & Q2c — Super High Yield)**

#### Scenario Trigger 1: "Critical Quality Concepts & SQA Activities Beyond Testing" (5 Marks)
*Exam Prompt*: *"Describe 2 distinct Software Quality Concepts most critical for [Scenario, e.g., ArogyaMitra Health Data] and outline 3 specific SQA activities (beyond testing) for Indian data privacy standards."*

##### 1. Two Critical Software Quality Concepts (from McCall's Model):
- **Data Integrity & Confidentiality (McCall's Integrity)**: Ensuring patient diagnostic reports, doctor notes, and identity tokens are protected from unauthorized interception, alteration, or unencrypted storage at rest and in transit.
- **Software Reliability & High Availability (McCall's Reliability)**: The emergency consultation service and payment gateway must maintain continuous 24/7 uptime without runtime exceptions during peak tele-consultation traffic or medical crises.

##### 2. Three SQA Activities Beyond Testing for DPDP / Regulatory Compliance:
1. **Formal Architectural & Privacy Threat-Modeling Reviews**: Structured design inspections evaluating data-at-rest encryption (AES-256), end-to-end video encryption (WebRTC SRTP), cryptographic key rotation policies, and strict role-based data access (RBAC).
2. **Automated Static Application Security Testing (SAST)**: Automated CI/CD scanning (using SonarQube, Checkmarx, or OWASP Dependency-Check) on every commit to flag hardcoded database passwords, unvetted SQL queries, and vulnerable third-party dependencies before compilation.
3. **Consent Architecture & SOP Compliance Audits**: Verifying the software engineering workflow strictly incorporates explicit user consent logging, anonymization pipelines for clinical research, and verified "Right-to-be-Forgotten" record purge mechanisms mandated by the Indian Digital Personal Data Protection (DPDP) Act.

---

#### Scenario Trigger 2: "Formal Technical Review (FTR) of a Component Design" (5 Marks)
*Exam Prompt*: *"As Project Manager, conduct a Formal Technical Review of the Component Design for [Payment / Booking Module]. List key participants and detail main objectives."*

##### 1. Key Participants & Their Review Responsibilities:
- **Review Leader (Chairperson / Moderator)**: Organizes the review, circulates design documents 48 hours in advance, enforces strict 90-minute time limits, keeps focus strictly on agenda items, and prevents personal attacks.
- **Producer (Designer / Author)**: The senior software engineer who authored the `PaymentTransactionManager` component design. Presents the technical design and answers technical queries.
- **Reviewers / Inspectors (2–4 Domain Specialists)**:
  - *Security Architect*: Inspects token handling, cryptographic hashing, and compliance with RBI / PCI-DSS rules.
  - *QA Lead*: Evaluates component testability, exception handling branches, and mock readiness.
- **Recorder (Scribe)**: Documents every uncovered defect, ambiguity, and action item in the formal **Review Issues List**. Does not participate in the critique.

##### 2. Main Objectives of the FTR Meeting:
1. **Early Defect Detection**: Uncover algorithmic omissions, deadlock possibilities, and transaction rollback vulnerabilities before coding begins.
2. **Design Standards Compliance**: Verify adherence to high functional cohesion, loose data coupling, and architectural constraints.
3. **Formal Unanimous Decision**: Formally vote and sign off on one of three verdicts:
   - *Accept the design as is*.
   - *Accept conditionally upon verification of minor corrections*.
   - *Reject the design and schedule a follow-up review after major redesign*.

---

### SESSION 12 & 13: Software Testing Strategies & Methods
**Typical Exam Weightage**: **7 – 10 Marks (Question Q3a & Q3b)**

#### Scenario Trigger 1: "Validation Testing Strategy with Quantifiable Criteria" (4 Marks)
*Exam Prompt*: *"Develop a Validation Testing Strategy for [Scenario]. Identify 3 distinct validation activities and specify a quantifiable criterion (success rate, latency, etc.) for each."*

Structure your answer using this rigorous validation matrix:

| Validation Activity | Specific Scenario Focus | Quantifiable Acceptance Criterion |
| :--- | :--- | :--- |
| **1. Bandwidth Adaptation Validation** | Real-time video/audio consultation stability across degraded rural 3G networks. | Video latency $\le 2.0\text{ s}$; audio jitter $\le 30\text{ ms}$; call disconnect rate $\le 0.5\%$. |
| **2. Peak Load Payment Validation** | Multi-gateway payment handling (UPI, Net Banking) during high-traffic evening surges. | Transaction reconciliation accuracy $= 100\%$; payment processing throughput $\ge 500\text{ TPS}$. |
| **3. Non-Technical User Usability Validation** | Usability field validation with non-literate rural patients using voice assistant features. | $\ge 90\%$ of first-time test subjects successfully book a doctor within 3 minutes without assistance. |

---

#### Scenario Trigger 2: "White-Box vs. Black-Box Testing on a Specific Component" (3 Marks)
*Exam Prompt*: *"Explain difference between WBT and BBT. Propose 1 specific WBT and 1 specific BBT technique to apply to [Payment Component], justifying choice for maximum coverage."*

##### 1. Core Distinction:
- **White-Box Testing (Glass-Box)**: Examines internal procedural logic, control paths, branches, and data structures of the source code.
- **Black-Box Testing (Behavioral)**: Treats the system as an opaque box; derives test cases solely from functional specifications, inputs, and expected outputs without internal code knowledge.

##### 2. Selected WBT Technique: Basis Path Testing (Cyclomatic Complexity)
- **Justification for Payment Processing**: Payment code contains complex nested conditional logic (e.g., signature valid? account balance sufficient? gateway timeout? idempotency duplicate check?). Constructing the Control Flow Graph (CFG) and computing Cyclomatic Complexity:
  $$V(G) = E - N + 2P = \text{Predicate Nodes} + 1$$
  guarantees that every independent decision branch and exception handler is executed at least once, uncovering unreachable error-recovery code.

##### 3. Selected BBT Technique: Boundary Value Analysis (BVA)
- **Justification for Payment Processing**: Financial modules frequently fail at boundary limits. BVA tests the edges of the transaction amount parameter (e.g., allowed consultation fee: ₹10 to ₹10,000):
  $$\text{Test Set} = \{₹9.99\text{ (Invalid)}, ₹10.00\text{ (Min Valid)}, ₹10.01, ₹500\text{ (Nominal)}, ₹9,999.99, ₹10,000\text{ (Max Valid)}, ₹10,000.01\text{ (Invalid)}\}$$

---

### SESSION 15: Software Project Management, Estimation & Risk
**Typical Exam Weightage**: **3 – 5 Marks (Question Q3c)**

#### Scenario Trigger: "The 4 Ps Analysis in Domain / Geographical Context" (3 Marks)
*Exam Prompt*: *"Use the '4 Ps' of Software Management to analyze the [Scenario] project. For each 'P', provide a specific management consideration or challenge relevant to this context (e.g., Indian context, cultural differences, regulations)."*

| The "P" | Management Dimension | Specific Contextual Challenge (e.g., ArogyaMitra / India) |
| :--- | :--- | :--- |
| **1. People** | Human resource organization, team structure, user stakeholders | Assembling cross-functional squads containing bilingual linguists and rural public health workers to account for dialectal differences, low digital literacy, and socio-cultural barriers. |
| **2. Product** | Product scope, decomposition, technical constraints | Restricting Android APK package size ($< 25\text{ MB}$) for low-tier smartphones, architecting offline-first local queues, and ensuring low battery/data consumption. |
| **3. Process** | Lifecycle model, agile sprints, compliance verification gates | Adopting an Agile/Scrum process with 2-week sprints, integrating mandatory compliance checks for Ayushman Bharat Digital Mission (ABDM) and DPDP Act before each release. |
| **4. Project** | Risk management, scheduling, telecom dependencies | Managing external critical failure dependencies: high frequency of third-party UPI gateway downtime spikes between 7 PM–10 PM and intermittent rural cell tower dropouts. |

---

## 4. Plug-and-Play Domain Translation Guide

If the exam scenario changes from Healthcare (*ArogyaMitra*) to another domain, use this instant conversion table:

| Engineering Concept | Telemedicine (*ArogyaMitra*) | FinTech / Digital Banking (*DigiBank*) | Smart Fleet / Logistics (*SmartFleet*) | E-Commerce Marketplace |
| :--- | :--- | :--- | :--- | :--- |
| **Core Class** | `PaymentTransactionManager` | `FundTransferController` | `TripDispatchManager` | `OrderFulfillmentEngine` |
| **Model** | `PatientHealthRecord` | `CustomerAccount`, `Ledger` | `VehicleGPSLog`, `Waybill` | `InventoryItem`, `Cart` |
| **View** | Doctor Consultation Portal | Branch Cashier Dashboard | Fleet Map Tracking UI | Product Catalog & Checkout |
| **Controller** | `AppointmentController` | `TransactionValidator` | `RouteOptimizationService` | `PaymentGatewayDispatcher` |
| **Observer Pattern** | Waiting room alerts | High-value fraud alert | Vehicle breakdown alert | Flash sale stock change |
| **Adapter Pattern** | Multi-hospital EHR API | Multi-bank NEFT/RTGS/UPI | GPS tracker hardware SDK | Multi-courier tracking API |
| **Offline WebApp** | Uploading 20MB MRI scan | Uploading KYC ID photo | Uploading offline trip log | Syncing cart in poor network |
| **WBT Basis Path** | Tele-consult billing path | Loan eligibility engine | Dynamic fuel route decision | Dynamic promo-code engine |
| **BVA Limits** | Consultation fee (₹50–₹5000) | Daily transfer (₹1–₹200,000) | Cargo payload (1kg–5000kg) | Order quantity (1 to 10 items)|
| **SQA Standard** | DPDP Act, ABDM, HIPAA | RBI IT Framework, PCI-DSS | AIS-140 GPS, ISO 27001 | Consumer Protection Act |

---

## 5. 15-Minute Exam Hall Quick-Check Protocol

1. **Check Case Study Entities**: Identify the specific service being designed (e.g., Payment, Booking, GPS telemetry) and use its exact names in class diagrams.
2. **Attribute and Operation Signatures**: Always write types (`amount: BigDecimal`, `transactionId: UUID`) and return types (`: PaymentReceiptDTO`). Untyped variables lose 50% marks.
3. **The 3 Golden Rules**: Always cite Theo Mandel by name. Quote the 3 rules verbatim: *Place User in Control*, *Reduce User Memory Load*, *Make Interface Consistent*.
4. **Quantifiable Criteria**: When asked for testing validation, always provide a numerical benchmark ($\le 2\text{ s}$, $\ge 99.9\%$, $100\%$).
5. **FTR Roles**: Always list all 4 roles: Review Leader, Producer, Reviewers/Inspectors, Recorder.
