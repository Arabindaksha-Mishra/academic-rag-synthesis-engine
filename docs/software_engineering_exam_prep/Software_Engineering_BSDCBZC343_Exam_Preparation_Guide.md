# BITS PILANI WILP — Comprehensive Exam Master Preparation Guide
## Course: Software Engineering (`BSDCBZC343` / `BSDCHZC343`)
**Target Score:** 90% – 95% Marks | **Format:** Open-Book Comprehensive Exam (EC-3 Regular)

---

## 1. Exam Structure & Lecture Weightage Analysis (Sessions 01 to 16)

In the BITS WILP examination system:
- **Mid-Semester Examination** assesses foundational software engineering concepts covered in **Sessions 01 through 07**.
- **Comprehensive Final Examination (EC-3)** carries 40%–50% overall weightage and is **75% to 85% heavily concentrated on Post-Mid-Sem Sessions (Sessions 08 through 16)**. 
- Even when early concepts appear, they are tested through holistic system case studies (e.g., architectural choices or project management considerations).

### Comprehensive Session-by-Session Priority Breakdown

| Priority Tier | Session & Booklet Reference | Curriculum Core Topics | Typical Exam Weightage | Preparation Action |
| :--- | :--- | :--- | :---: | :--- |
| **Tier 1 (Critical)** | [CS09 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS09_Component_Level_Design_4up_Part_01_of_01_sheets_001_008.pdf) | **Component-Level Design**: Class-based design, interfaces, attributes/methods, WebApp asynchronous handling | **10 – 15 Marks** | **Top Priority** |
| **Tier 1 (Critical)** | [CS10 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS10_User_Interface_Design_and_Heuristics_4up_Part_01_of_01_sheets_001_006.pdf) | **User Interface Design**: Theo Mandel's 3 Golden Rules, wireframing, accessibility heuristics | **5 – 10 Marks** | **Top Priority** |
| **Tier 1 (Critical)** | [CS12 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS12_Software_Testing_Strategy_and_Process_4up_Part_01_of_01_sheets_001_008.pdf) & [CS13 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS13_Testing_Methods_WhiteBox_BlackBox_4up_Part_01_of_01_sheets_001_009.pdf) | **Testing Strategies & Methods**: Validation testing, White-Box (Basis Path, $V(G)$), Black-Box (BVA, Equivalence Partitioning) | **10 – 15 Marks** | **Top Priority** |
| **Tier 1 (Critical)** | [CS14 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS14_Software_Quality_Assurance_and_Reviews_4up_Part_01_of_01_sheets_001_009.pdf) | **SQA & Formal Technical Reviews**: FTR roles/goals, SQA activities beyond testing, McCall’s factors | **5 – 10 Marks** | **Top Priority** |
| **Tier 2 (High)** | [CS08 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS08_Architectural_Design_and_Styles_4up_Part_01_of_01_sheets_001_014.pdf) & [CS11 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS11_Design_Patterns_Creational_Structural_4up_Part_01_of_01_sheets_001_009.pdf) | **Architecture & Design Patterns**: MVC, Layered, Observer, Facade, Adapter, Singleton | **5 – 10 Marks** | High Yield |
| **Tier 2 (High)** | [CS15 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS15_Project_Management_Estimation_and_Risk_4up_Part_01_of_01_sheets_001_024.pdf) | **Project Management**: 4 Ps (People, Product, Process, Project), COCOMO, Function Points ($FP$) | **5 – 8 Marks** | High Yield |
| **Tier 2 (High)** | [CS07 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS07_Software_Design_Concepts_and_Principles_4up_Part_01_of_01_sheets_001_010.pdf) | **Design Concepts**: Cohesion spectrum, Coupling types, Modularity, Information Hiding | Sub-questions | High Yield |
| **Tier 3 (Low)** | CS01, CS02, CS04, CS05, CS06 | Process models (Waterfall, Spiral, Agile/Scrum), Requirements, DFDs, Use cases | 0 – 5 Marks | Tested in Mid-Sem |

---

## 2. BITS Open-Book Scoring Protocol (How to Get 90%+)

> [!IMPORTANT]
> **Avoid the Open-Book Copy Trap:**
> In BITS WILP exams, questions are deliberately created around unseen case studies (such as *"ArogyaMitra"*, *"EcoDrive"*, or automated banking). Copying definitions or diagrams directly from the PPT slides earns at most 30%–40% marks.
> Evaluators look for domain grounding, trade-off evaluation, and structured engineering articulation.

### The 3-Step Full-Marks Answering Formula

1. **Step 1: Academic Definition / Core Engineering Principle**
   - State the formal definition from Pressman (e.g., *"According to Pressman, Component-Level design transforms architectural objects into detailed data structures, interfaces, and procedural algorithms"*).
2. **Step 2: Contextual Application to the Scenario**
   - Explicitly tie the theoretical principles to the exam case study entities (e.g., naming actual classes like `PaymentTransactionManager`, identifying exact attributes like `transactionId`, and addressing real rural constraints like 2G/3G intermittent connectivity).
3. **Step 3: Engineering Justification & Trade-Offs**
   - Explain *why* this design choice is technically superior (e.g., how it prevents tight coupling, ensures data privacy compliance under India's DPDP Act, or minimizes memory overhead).

---

## 3. High-Yield Open-Book Topic Summary (Hall Reference)

### A. Cohesion & Coupling ([CS07 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS07_Software_Design_Concepts_and_Principles_4up_Part_01_of_01_sheets_001_010.pdf))
- **Cohesion (Aim for High/Functional)**: Measures the degree to which elements inside a module belong together.
  - *Best*: **Functional Cohesion** (module performs one and only one dedicated business function).
  - *Worst*: **Coincidental Cohesion** (unrelated tasks grouped together).
- **Coupling (Aim for Low/Data)**: Measures the degree of interdependence between software modules.
  - *Best*: **Data Coupling** (components interact solely via passing parameter data/DTOs).
  - *Worst*: **Content Coupling** (one component modifies or relies directly on internal data of another).

### B. Theo Mandel’s 3 Golden Rules of Interface Design ([CS10 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS10_User_Interface_Design_and_Heuristics_4up_Part_01_of_01_sheets_001_006.pdf))
1. **Place the User in Control**:
   - Provide flexible interaction modes; allow operations to be interruptible, undoable, and redoable.
   - Do not trap users in unskippable sequences.
2. **Reduce the User's Memory Load**:
   - Prioritize recognition over recall (Miller’s Law: $7 \pm 2$ chunks).
   - Use meaningful visual metaphors (e.g., stethoscope icon for doctor, envelope for messaging).
   - Provide sensible defaults and multi-lingual voice/vernacular assistance for non-technical users.
3. **Make the Interface Consistent**:
   - Visual consistency (fonts, button styles, standardized iconography).
   - Functional consistency (a back button always behaves the same way everywhere).

### C. Testing Taxonomy ([CS12](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS12_Software_Testing_Strategy_and_Process_4up_Part_01_of_01_sheets_001_008.pdf) & [CS13 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS13_Testing_Methods_WhiteBox_BlackBox_4up_Part_01_of_01_sheets_001_009.pdf))
- **Verification vs. Validation**:
  - *Verification*: *"Are we building the product right?"* (Reviews, static analysis, unit checks).
  - *Validation*: *"Are we building the right product?"* (Demonstrates software satisfies operational user requirements under real-world conditions).
- **White-Box Testing (WBT)**:
  - *Method*: **Basis Path Testing**.
  - *Cyclomatic Complexity Metric*:
    $$V(G) = E - N + 2P = \text{Predicate Nodes} + 1 = \text{Enclosed Regions} + 1$$
    *(where $E$ = edges, $N$ = nodes, $P$ = connected components, usually 1)*.
- **Black-Box Testing (BBT)**:
  - *Method 1*: **Equivalence Partitioning (EP)** (dividing input domain into valid and invalid partitions).
  - *Method 2*: **Boundary Value Analysis (BVA)** (evaluating inputs at the extreme lower, boundary, and upper edges: $min - 1$, $min$, $min + 1$, $nominal$, $max - 1$, $max$, $max + 1$).

### D. Software Quality Assurance & Reviews ([CS14 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS14_Software_Quality_Assurance_and_Reviews_4up_Part_01_of_01_sheets_001_009.pdf))
- **Defect Removal Efficiency (DRE)**:
  $$DRE = \frac{E}{E + D}$$
  *(where $E$ = errors found prior to delivery, $D$ = defects found post-delivery)*.
- **Formal Technical Review (FTR)**:
  - Strict focus on the **work product**, not the author/producer.
  - Duration kept between 90–120 minutes with pre-distributed materials.
  - Mandatory four-role composition: Review Leader, Producer, Reviewers/Inspectors, Recorder.

### E. The 4 Ps of Software Project Management ([CS15 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS15_Project_Management_Estimation_and_Risk_4up_Part_01_of_01_sheets_001_024.pdf))
1. **People**: Project managers, software engineers, UX designers, customers, and field agents.
2. **Product**: Software scope, problem definition, non-functional requirements, technical boundaries.
3. **Process**: SDLC methodology chosen (Agile, Scrum, Waterfall) adapted to project constraints.
4. **Project**: Resource allocation, scheduling milestones, monitoring risk, budget management.

---

## 4. Master Solutions for Comprehensive Exam ([SE_25-S1_CR_QP_BSDCHZC343.pdf](file:///usr/local/google/home/arabindaksha/Desktop/SE_25-S1_CR_QP_BSDCHZC343.pdf))

---

### Question 1: Component and Pattern-Based Design [Total: 15 Marks]

#### Part a) Component-Level Design for Payment Processing [5 Marks]

##### 1. Steps in Component-Level Design (Pressman Principles):
1. **Identify domain-specific classes**: Analyze problem statements to extract core abstraction entities representing the component domain.
2. **Elaborate class details**: Define data attributes, access modifiers, and public/private methods.
3. **Specify interfaces and collaborations**: Establish formal contracts (DTOs, interfaces) decoupling the component from caller modules.
4. **Elaborate procedural logic & algorithmic details**: Define step-by-step algorithms, error handling, state validation, and transactional rollback paths.

##### 2. Primary Class Specification:
- **Class Name**: `PaymentTransactionManager`
- **Key Attributes**:
  1. `transactionId: java.util.UUID` — Immutable globally unique identifier for transaction tracking and idempotency.
  2. `transactionStatus: PaymentStatusEnum` — Tracks execution state (`INITIATED`, `PENDING_GATEWAY`, `SUCCESSFUL`, `FAILED`, `REFUNDED`).
- **Key Operations**:
  1. `initiatePayment(patientId: String, amount: BigDecimal, gatewayType: GatewayEnum): PaymentInitiationResponse`
  2. `verifyGatewaySignature(gatewayCallbackPayload: Map<String, String>): Boolean`
  3. `processRefund(transactionId: UUID, reason: String): RefundReceipt`

##### 3. Cohesion and Coupling Rationale:
- **High Cohesion (Functional Cohesion)**: The class encapsulates *only* financial transaction state operations and verification routines. Ancillary tasks like sending SMS receipt alerts or updating appointment calendars are delegated to independent services (`NotificationService`, `AppointmentScheduler`).
- **Low Coupling (Data Coupling)**: The class interacts with external entities exclusively via typed data transfer objects (DTOs) and interface abstractions (`IPaymentGatewayAdapter`), hiding internal gateway keys and database handles.

---

#### Part b) Pattern-Based Design for Doctor's Secure Web Portal [6 Marks]

##### 1. Justification for Model-View-Controller (MVC):
- **Separation of Clinical Data from Presentation**: Protects core clinical data structures and compliance algorithms (Model) from rapid UI modifications and web front-end framework upgrades (View).
- **Multi-Client Rendering**: A single medical record Model can support multiple Views (e.g., standard desktop monitor view for clinics vs. condensed tablet view for mobile rounds) without rewriting business logic.
- **Centralized Security Enforcement**: The Controller acts as an authentication interceptor verifying doctor session tokens before executing state modifications.

##### 2. MVC Component Mapping for ArogyaMitra:
- **Model**: `PatientHealthRecord`, `ConsultationSession`, `DoctorSlotSchedule`. Manages medical history storage, state transitions, encryption, and persistence.
- **View**: `ScheduleCalendarView.html`, `VideoConsultationPortal.jsx`, `PrescriptionEditor.vue`. Displays medical data and captures doctor user inputs.
- **Controller**: `AppointmentController`, `TeleConsultController`. Intercepts incoming HTTP/WebSocket requests, validates doctor credentials, triggers Model updates, and selects the next view.

##### 3. Secondary Design Pattern: Observer Pattern
- **Pattern Category**: Behavioral Pattern.
- **Application & Justification**: In tele-consultations, doctors require real-time notifications when a patient joins the virtual waiting room, when a payment completes, or when emergency vitals change. Implementing the **Observer Pattern** allows `PatientQueueSubject` to notify multiple active portal widgets (`DoctorWaitingRoomView`, `AudioAlertService`, `NurseDashboard`) instantaneously without tight coupling.

---

#### Part c) Robust WebApp Component Design for Asynchronous File Upload [4 Marks]

Rural Indian healthcare environments frequently encounter unstable 2G/3G connections and sudden network dropouts.

##### Architectural Blueprint:
1. **Client-Side Chunking**: The client browser/app partitions large diagnostic PDF reports into small binary blocks (e.g., 512 KB chunks) using the HTML5 File API.
2. **Session Identification & Idempotency**: The server generates an immutable `UploadSessionId`. Each chunk is dispatched with metadata:
   $$\text{Payload} = \{\text{SessionID}, \text{ChunkIndex}, \text{TotalChunks}, \text{SHA256Hash}\}$$
3. **Server-Side Reassembly & Status Endpoint**: The server acknowledges each chunk and records received chunks in persistent Redis cache.
4. **Exponential Backoff Retry with Local Offline Queue**: If the network connection drops, the client caches pending chunks in IndexedDB/SQLite storage and repeatedly retries with exponential backoff ($t = 2^n \times 500\text{ ms}$) once connectivity is restored, resuming from the exact failed chunk rather than restarting from zero.

---

### Question 2: Interface Design and Software Quality [Total: 15 Marks]

#### Part a) Wireframe & Theo Mandel's 3 Golden Rules for Rural Patient Interface [5 Marks]

```text
+-------------------------------------------------------------+
| [Logo] ArogyaMitra (आरोग्य मित्र)       [🌐 भाषा: हिंदी/ENG] |
+-------------------------------------------------------------+
| Welcome, Ramesh Kumar! (नमस्ते रमेश जी)                      |
| Emergency Help / आपातकालीन सहायता: [ 🚨 108 Direct Dial ]   |
+-------------------------------------------------------------+
|  +-----------------------+     +--------------------------+ |
|  |   [👨‍⚕️ Stethoscope]    |     |      [📁 Folder Icon]    | |
|  |  Book Doctor Video    |     |   My Reports / Upload    | |
|  |  डॉक्टर से बात करें    |     |     जांच रिपोर्ट भेजें    | |
|  +-----------------------+     +--------------------------+ |
|  +-----------------------+     +--------------------------+ |
|  |    [₹ Rupee Note]     |     |     [🎙️ Microphone]      | |
|  |  Pay Fee / बिल भरें   |     |   Speak to Assistant     | |
|  +-----------------------+     +--------------------------+ |
+-------------------------------------------------------------+
| [ 🏠 Home ]        [ 📅 Appointments ]        [ ❓ Help ]   |
+-------------------------------------------------------------+
```

##### Critique Using Theo Mandel’s 3 Golden Rules:
1. **Place User in Control**: Prominent, high-contrast **"Back (वापस)"** and **"Cancel"** actions on every sub-screen prevent users from feeling trapped. Audio help prompts can be paused, replayed, or dismissed at will.
2. **Reduce User Memory Load**: Minimal cognitive effort is required due to large, recognizable visual metaphors (stethoscope for doctor, rupee note for payment, microphone for voice input) accompanied by vernacular text. Eliminates multi-level nested menus.
3. **Make the Interface Consistent**: Standard 4-tile grid across all screens, uniform green accents for confirmative actions, red for emergency/cancellation, and identical layout paradigms across Hindi and English versions.

---

#### Part b) SQA Concepts & Three Non-Testing Activities for Health Privacy [5 Marks]

##### 1. Two Critical Software Quality Concepts:
- **Data Integrity & Confidentiality (McCall’s Integrity)**: Ensuring patient health records and diagnostic documents are protected against unauthorized modification, leakage, or unencrypted transmission.
- **Software Reliability & Fault Tolerance (Availability)**: Telemedicine services must maintain uninterrupted operation during active medical emergencies without unhandled system exceptions or service downtime.

##### 2. Three SQA Activities Beyond Testing for DPDP/DISHA Compliance:
1. **Formal Architectural & Privacy Threat-Modeling Reviews**: Structured design inspections evaluating data-at-rest encryption (AES-256), cryptographic key rotation schemes, and explicit audit logging of every record access by medical personnel.
2. **Automated Static Code Analysis & Vulnerability Auditing (SAST)**: Continuous CI/CD scanning (e.g., using SonarQube or OWASP Dependency Check) to flag hardcoded API credentials, insecure cryptographic libraries, and unvetted SQL queries prior to build stages.
3. **Standard Operating Procedure (SOP) & Consent Process Compliance Audits**: Verifying the software development lifecycle strictly enforces user consent-architecture artifacts, right-to-forget data deletion workflows, and role-based data access policies mandated by the Indian Digital Personal Data Protection (DPDP) Act.

---

#### Part c) Formal Technical Review (FTR) of Payment Module Component Design [5 Marks]

##### 1. Required Review Participants:
- **Review Leader (Chairperson)**: Orchestrates the meeting, ensures pre-circulation of design documentation, keeps discussions focused on agenda items, and prevents personal confrontations.
- **Producer (Author/Designer)**: Senior developer who designed the `PaymentTransactionManager` and explains design rationale.
- **Reviewers / Inspectors**: Security Architect (evaluates token handling, payment gateway integration, and PCI-DSS compliance) and QA Lead (assesses modular testability and error exception coverage).
- **Recorder (Scribe)**: Documents every identified issue, ambiguity, and action item in the formal FTR Issues Log.

##### 2. Core Objectives of the Review Meeting:
- Identify architectural anomalies, deadlocks, and logical oversights in component workflows before coding commences.
- Ensure strict adherence to organizational design standards, high cohesion, low coupling, and secure data handling principles.
- Formally reach a unanimous verdict: **Accept as is**, **Accept conditionally upon minor modifications**, or **Reject and schedule a follow-up review**.

---

### Question 3: Testing and Software Management [Total: 10 Marks]

#### Part a) Validation Testing Strategy for ArogyaMitra [4 Marks]

*Validation ensures the developed software complies with operational end-user requirements.*

| Validation Activity | Specific Operational Focus | Quantifiable Acceptance Criterion |
| :--- | :--- | :--- |
| **Activity 1: Tele-Consultation Quality of Service Validation** | Real-time video/audio consultation stability across degraded network connections. | Video connection latency $< 2.5\text{ s}$ on simulated 3G networks; session drop rate $\le 0.5\%$. |
| **Activity 2: Payment Gateway Integration Validation** | Multi-gateway payment handling (UPI, NetBanking) under peak loads. | Transaction reconciliation accuracy $= 100\%$; payment processing success rate $\ge 99.9\%$. |
| **Activity 3: Rural User Field Usability Validation** | Usability validation with non-technical rural users utilizing bilingual voice assistance. | $\ge 90\%$ of first-time users successfully complete doctor booking within 3 minutes without human intervention. |

---

#### Part b) White-Box Testing (WBT) vs. Black-Box Testing (BBT) [3 Marks]

| Dimension | White-Box Testing (WBT) | Black-Box Testing (BBT) |
| :--- | :--- | :--- |
| **Focus** | Internal logic, control flow paths, conditions, data structures | Functional specifications, inputs and outputs according to requirements |
| **Visibility** | Full visibility into source code internal implementation | No visibility into internal source code (treats system as black box) |

##### Selected Techniques for Payment Processing Component:
- **White-Box Technique: Basis Path Testing (Cyclomatic Complexity)**
  - *Justification*: Computing the control flow graph and cyclomatic complexity $V(G)$ ensures that every branch in the payment verification logic (e.g., token valid vs. invalid, gateway timeout vs. callback, hash mismatch) is executed at least once, uncovering unhandled exception paths and unreachable code.
- **Black-Box Technique: Boundary Value Analysis (BVA)**
  - *Justification*: Financial algorithms most frequently fail at boundary conditions. BVA evaluates minimum allowed amount (₹$1.00$), maximum transaction limit (₹$1,00,000$), zero, negative values, and precision overflow conditions.

---

#### Part c) The "4 Ps" Analysis for ArogyaMitra in the Indian Context [3 Marks]

1. **People**:
   - *Consideration*: Development requires a cross-functional team including vernacular linguistic consultants and rural field researchers to accurately reflect socio-cultural nuances and low digital literacy patterns.
2. **Product**:
   - *Consideration*: Strict scope boundaries prioritizing a lightweight APK footprint ($< 25\text{ MB}$), backward compatibility with entry-level Android devices, and resilient offline-first data synchronization.
3. **Process**:
   - *Consideration*: An Agile/Scrum process with 2-week iterations integrating continuous security and regulatory verification gates to comply with the Ayushman Bharat Digital Mission (ABDM) and the DPDP Act.
4. **Project**:
   - *Consideration*: Proactive risk management addressing dependencies on external telecom reliability, frequent UPI gateway downtime spikes during evening hours, and distributed server latency across rural geographic clusters.

---

## 5. 60-Minute Exam Hall Action Checklist

1. Place the [CS09 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS09_Component_Level_Design_4up_Part_01_of_01_sheets_001_008.pdf), [CS10 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS10_User_Interface_Design_and_Heuristics_4up_Part_01_of_01_sheets_001_006.pdf), [CS13 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS13_Testing_Methods_WhiteBox_BlackBox_4up_Part_01_of_01_sheets_001_009.pdf), and [CS14 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS14_Software_Quality_Assurance_and_Reviews_4up_Part_01_of_01_sheets_001_009.pdf) on top of your printed booklet pile.
2. If asked for a UI critique, immediately anchor your answer on **Theo Mandel's 3 Golden Rules** (User in Control, Reduce Memory Load, Consistency).
3. If asked for component design, specify:
   - Exact Class Name
   - Attributes with types
   - Operations with argument and return types
   - Explicit paragraph demonstrating high functional cohesion and loose data coupling.
4. If asked about testing, clearly separate **WBT (Basis Path / Cyclomatic Complexity)** from **BBT (BVA / Equivalence Partitioning)**.
5. If asked about management, structure your response directly around the **4 Ps (People, Product, Process, Project)**.
