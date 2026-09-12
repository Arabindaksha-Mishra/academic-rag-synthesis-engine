# BITS WILP Software Engineering (BSDCBZC343 / BSDCHZC343)
## Post-Midterm Master Exam Preparation & Open-Book Cheat Sheet (Sessions 08 – 16)

> **Exam Focus**: Post-Midterm Sessions (CS08 through CS16 + CS07 Foundation)  
> **Course**: BSDCBZC343 / BSDCHZC343 — Software Engineering  
> **Weightage in Comprehensive Exam**: **85% – 100% of Total Marks** (Tested on real unseen case studies like *ArogyaMitra*, *EcoDrive*, *SmartFleet*)  
> **Core Textbook**: Roger S. Pressman & Bruce R. Maxim, *Software Engineering: A Practitioner's Approach*, McGraw-Hill

---

## 0. The Open-Book Exam Scoring Protocol (How to Score 90%+)

> [!IMPORTANT]
> **The Open-Book Copy Trap:**
> In BITS WILP Comprehensive Exams, questions are designed around unseen domain case studies. Merely copying slide definitions or generic textbook diagrams will yield at most **30%–40%** marks.
> Evaluators award maximum marks for domain adaptation, architectural rationale, and engineering rigor.

### The 3-Step Full-Marks Answering Architecture:
1. **Step 1: Formal Pressman Engineering Principle / Academic Definition**
   - State the authoritative principle (e.g., *"According to Pressman, component-level design transforms architectural components into detailed procedural algorithms, data structures, and interface definitions"*).
2. **Step 2: Concrete Mapping to the Exam Case Study**
   - Use the domain entities from the question (e.g., name real classes like `PaymentTransactionManager`, define explicit typed attributes like `transactionId: UUID`, declare methods with arguments and return types, draw wireframes with domain labels).
3. **Step 3: Engineering Rationale & Trade-off Evaluation**
   - Explain *why* this choice is optimal (e.g., *"High functional cohesion prevents cascading failures, while loose data coupling via DTOs shields the core system from external payment gateway schema changes"*).

---

## 1. Session 07 & 09: Component-Level Design & Core Design Concepts

### 1.1 The Nature of a Component (3 Views)
- **Object-Oriented View**: A component is a set of collaborating classes encapsulating state, behavior, and interfaces.
- **Conventional (Procedural) View**: A component is a functional element (subroutine, module) with internal logic, data structures, and an interface.
- **Process-Related View**: A reusable off-the-shelf software building block (e.g., payment gateway SDK, Redis cache connector).

### 1.2 Step-by-Step Component-Level Design Process
When an exam question asks: *"Detail the steps involved in Component-Level Design for a Class-Based Component"*:
1. **Identify All Classes & Objects**: Extract candidate domain classes from analysis models and architectural specifications.
2. **Elaborate Attributes & Data Structures**: Specify data attributes, data types, accessibility modifiers (`private`, `protected`), and default values.
3. **Elaborate Operations & Algorithmic Mechanics**: Define public operations, input parameter types, return signatures, preconditions, and postconditions.
4. **Specify Interfaces & Contracts**: Establish formal interfaces (e.g., `IPaymentGatewayAdapter`) to decouple components and enforce Dependency Inversion.
5. **Manage State & Collaboration**: Model dynamic behavior using state machine diagrams or sequence interactions; handle exception states and rollbacks.

### 1.3 Cohesion Spectrum (Order from Best to Worst)
*Definition: Cohesion is the degree to which all elements within a single module belong together and serve a single unified purpose.*

| Cohesion Level | Quality | Description & Exam Example |
| :--- | :---: | :--- |
| **Functional Cohesion** | **IDEAL (Highest)** | Module performs one and only one dedicated business or mathematical computation. Example: `calculateTaxAmount(amount, taxRate)`. |
| **Sequential Cohesion** | High | Output of one operation forms the direct input to the next operation in the same module. Example: `parsePrescription() -> validateDosage() -> generateBill()`. |
| **Communicational Cohesion** | Moderate-High | Operations share and modify the exact same internal data structure or dataset. Example: `updatePatientRecord()`, `readPatientRecord()`. |
| **Procedural Cohesion** | Moderate | Operations must execute in a specific sequential order, but do not share identical data. |
| **Temporal Cohesion** | Low | Operations are grouped solely because they must execute at the same point in time (e.g., `initializeSystem()`, `appStartup()`). |
| **Logical Cohesion** | Low | Operations perform logically similar tasks selected by a control flag (e.g., `processFile(flag)` where flag=1 does PDF, flag=2 prints, flag=3 deletes). |
| **Coincidental Cohesion** | **WORST** | Unrelated tasks grouped arbitrarily without meaningful relationships (e.g., `utilModule` with string formatting, database query, and audio playback). |

### 1.4 Coupling Spectrum (Order from Best to Worst)
*Definition: Coupling is the degree of interdependence between separate software components.*

| Coupling Level | Quality | Description & Exam Example |
| :--- | :---: | :--- |
| **Data Coupling** | **IDEAL (Lowest)** | Modules communicate exclusively by passing atomic data parameters or typed Data Transfer Objects (DTOs). No internal implementation is shared. |
| **Stamp Coupling** | Acceptable | Modules pass a composite data structure (e.g., entire `PatientRecord` object), but the receiving module only uses a few fields (`patientAge`). |
| **Control Coupling** | Low-Moderate | One module passes a control flag or boolean to another module, explicitly directing its internal decision execution path. |
| **External Coupling** | Moderate | Modules depend on external communication formats, OS tools, or vendor-specific protocols. |
| **Common Coupling** | High (Poor) | Multiple modules read and write to the same shared global variable, shared memory block, or un-abstracted database table. |
| **Content Coupling** | **WORST** | One module directly accesses, branches into, or modifies the private internal state, memory, or code of another module. |

### 1.5 WebApp Component Design: Asynchronous & Resilient Architecture
*Exam Scenario: Handling unstable 2G/3G connectivity, intermittent power, or large file uploads (diagnostic reports, medical scans) in low-bandwidth regions.*

```
[ Client App ] --(HTML5 File API / Binary Chunking 512KB)--> [ IndexedDB Queue ]
     |
     +---(Step 1: Handshake -> Obtain UploadSessionId)-----------------> [ Server ]
     +---(Step 2: Send Chunk [Index, Total, Hash])---------------------> [ Redis Cache ]
     +---(Step 3: Network Drops -> Retry with Exponential Backoff)-----> [ S3 / GCS ]
```

1. **Client-Side File Chunking**: Partition files into deterministic chunks (e.g., 512 KB) using browser HTML5 File API or mobile stream buffers.
2. **Session Handshake & Idempotency**:
   $$\text{Session Token} = \text{UUID}, \quad \text{Payload} = \{\text{SessionID}, \text{ChunkIndex}, \text{TotalChunks}, \text{MD5/SHA256}\}$$
3. **Persistent Local Buffer (Offline-First)**: Store pending chunks in client IndexedDB or SQLite so page refreshes or device reboots do not lose progress.
4. **Exponential Backoff Reconnection**:
   $$t_{\text{retry}} = \min(2^n \times \text{BaseDelay}, \text{MaxDelay}) + \text{Jitter}$$
5. **Server-Side Reassembly & State Tracking**: Server acknowledges individual chunk indices in Redis; reassembles full file and verifies aggregate checksum only when all chunks arrive.

---

## 2. Session 08 & 11: Architectural Design & Design Patterns

### 2.1 Major Architectural Styles & Taxonomies

| Architectural Style | Core Mechanics | Strengths | Typical Use Cases |
| :--- | :--- | :--- | :--- |
| **Data-Centered (Repository)** | Shared central data store accessed by independent client components. | Scalable data storage, central data governance and backup. | Database management systems, AI knowledge bases. |
| **Data-Flow (Pipes and Filters)** | Series of independent processing components (filters) connected by data streams (pipes). | Reusability, pipeline parallelism, ease of substitution. | Audio/video streaming, ETL batch pipelines, compilers. |
| **Call and Return (Layered)** | Rigid hierarchical layers (Presentation, Business Logic, Persistence, Database). | Decoupling, maintainability, testability. | Enterprise web applications, operating system kernels. |
| **Event-Driven (Pub-Sub)** | Asynchronous event emitters publish events to brokers; consumers subscribe without coupling. | High responsiveness, dynamic scaling, loose coupling. | IoT telemetry, real-time messaging, financial tickers. |

### 2.2 Model-View-Controller (MVC) Pattern
* **Why MVC is chosen**:
  1. **Decoupling**: Decouples domain logic (Model) from presentation mechanisms (View), allowing UI overhauls without modifying database or business validation logic.
  2. **Multi-View Support**: Multiple distinct views (e.g., Doctor Web Portal, Doctor Mobile App, Prescription PDF export) can bind to the same underlying Model.
  3. **Security & Session Interception**: The Controller acts as an authentication interceptor verifying doctor credentials and session tokens before Model state mutation.
* **Component Mapping Blueprint**:
  - **Model**: Encapsulates state and business logic (`DoctorSchedule`, `PatientMedicalRecord`, `Prescription`). Manages persistence, encryption, and transactional integrity.
  - **View**: Presentation layer rendered to the user (`DoctorPortalDashboard.jsx`, `PatientVitalsGraph.html`). Renders Model data and forwards user gestures to Controller.
  - **Controller**: Mediation layer (`AppointmentController`, `TeleConsultController`). Receives HTTP/WebSocket requests, validates permissions, invokes Model business methods, and selects the next View.

### 2.3 Gang of Four (GoF) Design Patterns Quick Exam Reference

#### A. Creational Patterns (Object Creation)
- **Factory Method**: Defines an interface for creating an object, but lets subclasses decide which class to instantiate. *Use case: Creating different payment adapters (`UPIAdapter`, `NetBankingAdapter`, `CreditCardAdapter`)*.
- **Singleton**: Ensures a class has only one instance and provides a global access point. *Use case: Database connection pool, system logger, hardware device handle*.

#### B. Structural Patterns (Class/Object Composition)
- **Adapter**: Converts the interface of a class into another interface clients expect. *Use case: Wrapping third-party bank payment APIs with a unified application interface*.
- **Facade**: Provides a simplified, high-level interface to a complex subsystem. *Use case: A single `TeleConsultationFacade` coordinating VideoService, BillingService, and MedicalHistoryService*.
- **Proxy**: Provides a surrogate or placeholder for another object to control access to it. *Use case: Virtual proxy for lazy-loading heavy high-resolution MRI scans; protection proxy for access control*.

#### C. Behavioral Patterns (Object Interaction & Responsibility)
- **Observer (Publish-Subscribe)**: Defines a one-to-many dependency so that when one object changes state, all its dependents are notified automatically. *Use case: Real-time doctor waiting room alerts when a patient enters or cancels*.
- **Strategy**: Defines a family of algorithms, encapsulates each one, and makes them interchangeable at runtime. *Use case: Dynamic routing of video streams using different compression algorithms based on current network bandwidth*.

---

## 3. Session 10: User Interface Design and Usability Heuristics

### 3.1 Theo Mandel's 3 Golden Rules (Exam Goldmine)

```
                       THEO MANDEL'S 3 GOLDEN RULES
                                     |
    +--------------------------------+--------------------------------+
    |                                |                                |
[ 1. Place User in Control ]   [ 2. Reduce User Memory Load ]   [ 3. Make Interface Consistent ]
• Provide Undo / Redo / Cancel • Recognition over Recall        • Uniform Visual Hierarchy
• Flexible Interaction Modes   • Miller's Law (7 ± 2 Chunks)    • Standardized Navigation
• Make Actions Interruptible   • Intuitive Real-World Metaphors • Universal Action Semantics
```

#### Rule 1: Place the User in Control
- **Do not force user into fixed sequences**: Allow users to navigate freely, pause tasks, or exit workflows without penalty.
- **Provide forgiving interactions**: Implement universal **Undo**, **Redo**, and explicit confirmation prompts for destructive actions.
- **Support varied interaction modes**: Allow navigation via touch, mouse, keyboard shortcuts, or voice inputs.
- **Keep system status visible**: Display clear progress indicators during long operations (e.g., file upload percentage).

#### Rule 2: Reduce the User's Memory Load
- **Prioritize recognition over recall**: Users should not have to remember information from one screen to another; present choices visibly.
- **Chunking (Miller's Law)**: Organize information into manageable groups of $7 \pm 2$ items (e.g., group form fields into 3 logical steps).
- **Establish meaningful visual metaphors**: Use real-world iconography (stethoscope for consultation, folder for reports, rupee note for payments).
- **Provide sensible defaults & autocomplete**: Auto-populate location, language, and date to minimize typing for low-literacy users.

#### Rule 3: Make the Interface Consistent
- **Visual consistency**: Standardize font families, color palettes, button border radiuses, and alert styling across all screens.
- **Functional consistency**: If a chevron arrow signifies "expand details" on one screen, it must not trigger navigation on another.
- **Layout and navigation consistency**: Menus, headers, breadcrumbs, and back buttons must occupy the exact same physical coordinates.

### 3.2 Exam Wireframing Architecture (ASCII Blueprint)

When asked to design an interface for non-technical, rural, or emergency users:
```text
+-------------------------------------------------------------------+
| [Logo] ArogyaMitra (आरोग्य मित्र)              [🌐 भाषा: हिंदी/ENG] |
+-------------------------------------------------------------------+
| Welcome, Ramesh Kumar! (नमस्ते रमेश जी)                            |
| 🚨 EMERGENCY DOCTOR CALL: [ CALL 108 NOW / तुरंत कॉल करें ]       |
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
|   |    Pay Bill / रसीद देखें  |     |    Speak to Assistant    |   |
|   |       फीस जमा करें       |     |     बोलकर मदद पाएं       |   |
|   +--------------------------+     +--------------------------+   |
|                                                                   |
+-------------------------------------------------------------------+
| [ 🏠 Home ]     [ 📅 Appointments ]     [ 💬 Chat ]     [ ❓ Help ]|
+-------------------------------------------------------------------+
```

---

## 4. Session 12 & 13: Software Testing Strategy & Methods

### 4.1 Verification vs. Validation (Boehm's Formal Axiom)
- **Verification**: *"Are we building the product right?"*  
  Evaluates intermediate artifacts (code, design models, specifications) against predefined phase inputs. Performed via static analysis, code reviews, and unit test suites.
- **Validation**: *"Are we building the right product?"*  
  Evaluates the executing software against actual end-user operational needs and environment constraints. Performed via acceptance testing, field trials, and usability evaluations.

### 4.2 Validation Testing Strategy & Quantifiable Acceptance Criteria
When an exam demands a *Validation Testing Strategy with Quantifiable Acceptance Criteria*, structure your answer as a formal matrix:

| Validation Activity | Specific Operational Objective | Quantifiable Acceptance Criterion |
| :--- | :--- | :--- |
| **1. Bandwidth Adaptation Validation** | Verify video call continuity over throttled 3G networks. | Video latency $\le 2.0\text{ s}$; audio jitter $\le 30\text{ ms}$; disconnect rate $\le 0.5\%$. |
| **2. High-Concurrency Payment Validation** | Verify gateway processing under flash traffic surges. | Zero dropped transactions; reconciliation accuracy $= 100\%$; throughput $\ge 500\text{ TPS}$. |
| **3. Usability & Field Literacy Validation** | Ensure rural non-technical users can book appointments. | $\ge 90\%$ of first-time test users book within 3 minutes using vernacular voice prompts. |
| **4. Security & Privacy Validation** | Verify health records are encrypted and audit-logged. | 100% encryption of data-at-rest (AES-256) and in-transit (TLS 1.3); zero unlogged record accesses. |

### 4.3 White-Box Testing (WBT): Basis Path Testing & Cyclomatic Complexity

#### Control Flow Graph (CFG) Construction Rules:
- **Node**: Represents one or more sequential procedural statements.
- **Edge**: Represents control flow between nodes (branches).
- **Predicate Node**: A decision node with 2 or more outgoing branches (e.g., `if`, `while`, `case`).
- **Enclosed Region**: Area bounded by edges and nodes (including outer unbounded region).

#### Cyclomatic Complexity $V(G)$ — 3 Equivalent Formulas:
$$V(G) = E - N + 2P$$
$$V(G) = P_{\text{redicate Nodes}} + 1$$
$$V(G) = \text{Number of Enclosed Regions}$$
*(where $E$ = edges, $N$ = nodes, $P$ = connected components, standard single module $P = 1$)*.

#### Step-by-Step Basis Path Derivation:
1. Draw the Control Flow Graph (CFG) from the procedural algorithm.
2. Calculate $V(G)$ using all 3 formulas to verify consistency.
3. Determine the **Basis Set** of independent execution paths:
   - Path 1: Baseline path (simplest path through code).
   - Path 2, 3, ..., $V(G)$: Paths flipping one predicate branch at a time.
4. Design concrete test case inputs to execute every independent path at least once.

### 4.4 Black-Box Testing (BBT): Equivalence Partitioning & Boundary Value Analysis

#### Equivalence Partitioning (EP):
Divides the input domain of a module into valid and invalid equivalence classes.
- *Example*: Patient Consultation Age field ($0 \le \text{Age} \le 120$).
  - Valid Class: $[0, 120]$ (e.g., input $= 35$).
  - Invalid Class 1: $\text{Age} < 0$ (e.g., input $= -5$).
  - Invalid Class 2: $\text{Age} > 120$ (e.g., input $= 135$).
  - Invalid Class 3: Non-numeric strings (e.g., input = `"abc"`).

#### Boundary Value Analysis (BVA):
Tests the extreme boundaries where the vast majority of software defects cluster.
- **Single-Variable 5-Point Test Set**:
  $$\{Min, \quad Min + 1, \quad Nominal, \quad Max - 1, \quad Max\}$$
- **Robust 7-Point Test Set (Includes Out-of-Bounds)**:
  $$\{Min - 1, \quad Min, \quad Min + 1, \quad Nominal, \quad Max - 1, \quad Max, \quad Max + 1\}$$
- *Payment Processing Example* (Valid range: ₹1 to ₹100,000):
  - Test Inputs: ₹0, ₹1, ₹2, ₹5,000, ₹99,999, ₹100,000, ₹100,001.

---

## 5. Session 14: Software Quality Assurance (SQA) & Reviews

### 5.1 McCall's Quality Factors (The Quality Triangle)

```
                           McCALL'S QUALITY FACTORS
                                      |
       +------------------------------+------------------------------+
       |                              |                              |
[ PRODUCT OPERATION ]        [ PRODUCT REVISION ]        [ PRODUCT TRANSITION ]
• Correctness                • Maintainability           • Portability
• Reliability                • Flexibility               • Reusability
• Efficiency                 • Testability               • Interoperability
• Integrity (Security)
• Usability
```

### 5.2 Critical SQA Activities Beyond Testing (Mandatory 5-Mark Question)
When asked for *SQA activities beyond testing (especially for privacy/security)*:
1. **Formal Technical Reviews (FTR) & Architecture Inspections**: Regular structured reviews of requirements, architecture, and module designs before code is written.
2. **Automated Static Application Security Testing (SAST)**: Automated CI/CD scanning (SonarQube, Checkmarx) to identify cryptographic flaws, hardcoded credentials, and SQL injection risks without executing code.
3. **Regulatory & Compliance Auditing**: Formal audits verifying compliance with data privacy mandates (India DPDP Act 2023, HIPAA, GDPR), checking user consent tracking, data anonymization, and right-to-forget workflows.
4. **Software Configuration Management (SCM) Audits**: Ensuring all production deployments trace back to approved, digitally-signed commit hashes and configuration baselines.
5. **Standard Operating Procedure (SOP) Verification**: Verifying developers follow clean coding standards, secure API conventions, and threat-modeling protocols.

### 5.3 Formal Technical Review (FTR) Protocol (Pressman Standard)

#### Key Participants & Their Roles:
1. **Review Leader (Chairperson / Moderator)**: Organizes the review, pre-distributes materials 24–48 hours in advance, moderates discussions, keeps focus strictly on agenda items, and prevents personal confrontations.
2. **Producer (Author)**: The engineer who created the artifact (design spec, code module). Explains the technical design, answers technical questions, and receives feedback.
3. **Reviewers / Inspectors (2 to 4 Peers)**: Domain specialists (e.g., Security Architect, Database Administrator, QA Lead) who inspect the document in advance and identify defects, ambiguities, and compliance gaps.
4. **Recorder (Scribe)**: Documents every identified issue, ambiguity, and action item in the formal **Review Issues List**; does not participate in the critique.

#### FTR Rules of Conduct (Pressman's Review Heuristics):
- **Review the product, not the producer**: Critique the design, not the author.
- **Set an agenda and maintain it**: Never exceed 2 hours (ideal: 90 minutes).
- **Limit advance preparation and meeting scope**: Focus on 100–200 LOC or 5–10 pages of design specs.
- **Uncover problems, don't attempt to solve them**: The meeting is for defect detection; solving defects is the producer's post-meeting task.
- **Produce written meeting minutes and an issues list**.
- **Reach a formal unanimous verdict**:
  1. *Accept the work product without further modification*.
  2. *Accept the work product provisionally subject to minor corrections*.
  3. *Reject the work product (schedule a follow-up review after major rework)*.

---

## 6. Session 15: Software Project Management, Estimation & Risk

### 6.1 The "4 Ps" of Software Management (Indian / Domain Context)

| The "P" | Academic Definition | Exam Case-Study Contextualization (e.g., ArogyaMitra) |
| :--- | :--- | :--- |
| **1. People** | Organization, leadership, and empowerment of human resources (developers, testers, clients). | Building cross-functional teams including medical consultants and vernacular linguists to address rural usability and dialectal differences. |
| **2. Product** | Defining project scope, technical requirements, and product decomposition. | Prioritizing low-bandwidth footprint ($< 25\text{ MB}$ APK), backward compatibility with Android 7.0+, and offline queueing for spotty connectivity. |
| **3. Process** | The software process framework, methodology, and milestone tracking. | Adopting an Agile/Scrum process with 2-week sprints and mandatory compliance checks for Ayushman Bharat Digital Mission (ABDM) and DPDP Act. |
| **4. Project** | Planning, risk management, scheduling, monitoring, and quality control. | Managing severe external risks: third-party UPI payment gateway downtime during peak evening hours and intermittent rural telecom connectivity. |

### 6.2 Function Point (FP) Estimation Reference
$$FP = \text{Count Total} \times \left[0.65 + 0.01 \times \sum_{i=1}^{14} F_i\right]$$
* **5 Information Domain Characteristics**:
  1. External Inputs ($EI$)
  2. External Outputs ($EO$)
  3. External Inquiries ($EQ$)
  4. Internal Logical Files ($ILF$)
  5. External Interface Files ($EIF$)
* **Complexity Weighting Table**:
  - $EI$: Low (3), Avg (4), High (6)
  - $EO$: Low (4), Avg (5), High (7)
  - $EQ$: Low (3), Avg (4), High (6)
  - $ILF$: Low (7), Avg (10), High (15)
  - $EIF$: Low (5), Avg (7), High (10)
* $\sum(F_i)$ is the sum of 14 General System Characteristics (rated 0 to 5 each, yielding range $0 \le \sum F_i \le 70$).

### 6.3 COCOMO Estimation Models
* **Basic COCOMO**:
  $$E = a \times (\text{KLOC})^b \quad [\text{Person-Months}]$$
  $$T_{\text{dev}} = c \times (E)^d \quad [\text{Months}]$$
  - *Organic Mode*: $a=2.4, b=1.05, c=2.5, d=0.38$ (Small teams, familiar environment).
  - *Semi-Detached Mode*: $a=3.0, b=1.12, c=2.5, d=0.35$ (Medium team, mixed experience).
  - *Embedded Mode*: $a=3.6, b=1.20, c=2.5, d=0.32$ (Strict hardware/software/regulatory constraints).

---

## 7. Session 16: Emerging Trends & DevOps

- **DevOps Triad**: People, Process, and Tools working collaboratively across Development and Operations.
- **CI/CD Pipeline Flow**:
  $$\text{Code Commit} \to \text{Static Analysis (SAST)} \to \text{Unit Tests} \to \text{Container Build} \to \text{Deploy to Staging} \to \text{Automated E2E Tests} \to \text{Production Canary}$$
- **Key Exam Principle**: Continuous Quality gates ensure that no code moves to production without passing automated static security and performance regression benchmarks.

---

## 8. Summary Table of Booklets & Hall Action Blueprint

| Topic Area | Sessions | Key Booklets to Stack on Desk | Essential Diagram / Formula to Draw |
| :--- | :---: | :--- | :--- |
| **Component Design** | CS07, CS09 | [CS09 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS09_Component_Level_Design_4up_Part_01_of_01_sheets_001_008.pdf), [CS07 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS07_Software_Design_Concepts_and_Principles_4up_Part_01_of_01_sheets_001_010.pdf) | Class diagram (attributes, operations), chunked upload flow |
| **UI & Wireframing** | CS10 | [CS10 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS10_User_Interface_Design_and_Heuristics_4up_Part_01_of_01_sheets_001_006.pdf) | 4-tile mobile home wireframe, 3 Golden Rules critique |
| **Patterns & Architecture** | CS08, CS11 | [CS08 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS08_Architectural_Design_and_Styles_4up_Part_01_of_01_sheets_001_014.pdf), [CS11 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS11_Design_Patterns_Creational_Structural_4up_Part_01_of_01_sheets_001_009.pdf) | MVC block diagram, Observer pattern pub-sub interaction |
| **Testing Strategies** | CS12, CS13 | [CS12 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS12_Software_Testing_Strategy_and_Process_4up_Part_01_of_01_sheets_001_008.pdf), [CS13 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS13_Testing_Methods_WhiteBox_BlackBox_4up_Part_01_of_01_sheets_001_009.pdf) | CFG diagram, $V(G) = E - N + 2P$, BVA 5-point input test table |
| **SQA & Formal Reviews** | CS14 | [CS14 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS14_Software_Quality_Assurance_and_Reviews_4up_Part_01_of_01_sheets_001_009.pdf) | McCall's Quality Triangle, FTR 4-role table & issues log |
| **Project Management** | CS15 | [CS15 Booklet](file:///usr/local/google/home/arabindaksha/Modify-pdf/print_materials/1_Software_Engineering_BSDCBZC343/sessionwise_4up_booklets/CS15_Project_Management_Estimation_and_Risk_4up_Part_01_of_01_sheets_001_024.pdf) | 4 Ps table (People, Product, Process, Project), FP formula |
