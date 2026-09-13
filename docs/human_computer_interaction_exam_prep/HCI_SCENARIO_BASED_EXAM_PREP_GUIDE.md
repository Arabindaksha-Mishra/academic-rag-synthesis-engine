# BITS WILP Human Computer Interaction (BSDCBZC365)
# Master Scenario-Based Exam Preparation Guide (Sessions 08 – 16)

> **Course**: BSDCBZC365 — Human Computer Interaction (HCI)  
> **Exam Nature**: Open Book | **Total Marks**: 40 Marks | **Duration**: 2½ Hours  
> **Core Focus**: Scenario Analysis, Persona Modeling, UI Wireframing, and Heuristic Evaluation

---

## 1. Universal HCI Scenario Extraction Framework

HCI case studies evaluate human sensory capabilities, task environments, and device ergonomics.
Extract these 4 dimensions in the first 3 minutes:
1. **Target User Persona**: Demographic age, technical literacy, physical/cognitive impairments (e.g., elderly rural patients, high-stress stock traders, warehouse forklift drivers).
2. **Context of Use**: Ambient lighting (bright outdoor glare), physical vibration, split-attention tasks, intermittent network.
3. **Hardware Modality**: Small mobile touch screen, public outdoor kiosk, smart watch, voice assistant (VUI).
4. **Safety & Error Consequences**: Reversible e-commerce cart vs. irreversible financial transaction or medical dosage dispatch.

---

## 2. Session-Wise Scenario Answering Blueprints

---

### SCENARIO TOPIC 1: Wireframe Design & Norman's 7 Principles Critique (Session 07 & 12)
*Exam Prompt*: *"Design the mobile wireframe for an Elderly Patient Medicine Reminding App ('MedAlert'). The persona has declining eyesight, mild arthritis, and low digital confidence. Draw the wireframe and critique your interface using Norman's 7 Principles."*

#### Step 1: Draw the Scenario Wireframe (ASCII Diagram)
```text
+-------------------------------------------------------------------+
| [☀️ Morning / सुबह] MedAlert Reminders        [🔊 Voice Reading]   |
+-------------------------------------------------------------------+
| Hello, Dadiji! (नमस्ते दादी जी)                                     |
| Next Medicine Due at 9:00 AM (अगली दवाई का समय):                   |
+-------------------------------------------------------------------+
|                                                                   |
|   +-----------------------------------------------------------+   |
|   |  [💊 Big Blue Capsule Icon]                                |   |
|   |  BP Medicine - Amlodipine (5mg)                           |   |
|   |  1 Tablet after breakfast with water                      |   |
|   +-----------------------------------------------------------+   |
|                                                                   |
|   +-----------------------------------------------------------+   |
|   |  [✅ BIG GREEN BUTTON (Height: 64dp)]                      |   |
|   |  I HAVE TAKEN THIS MEDICINE (मैंने दवाई ले ली)             |   |
|   +-----------------------------------------------------------+   |
|                                                                   |
|   +-----------------------------------------------------------+   |
|   |  [⏰ SNOOZE / बाद में याद दिलाएं (15 mins)]                 |   |
|   +-----------------------------------------------------------+   |
|                                                                   |
+-------------------------------------------------------------------+
| [ 🏠 Home / दवाई ]       [ 👨‍⚕️ Call Doctor ]       [ ❓ Help / मदद ] |
+-------------------------------------------------------------------+
```

#### Step 2: Critique Using Norman’s 7 Principles:
1. **Discoverability**: The primary upcoming pill card and the high-contrast green confirmation button are immediately visible above the fold without scrolling.
2. **Feedback**: Pressing the green button triggers three synchronized feedback signals: a distinct audible chime, a soft haptic vibration pulse, and an animated green checkmark on screen.
3. **Conceptual Model**: The interface mirrors a physical daily pill organizer box; color-coded morning (sun), afternoon, and evening sections match real-world routine.
4. **Affordance**: The massive green pill confirmation box physically invites a finger press due to raised elevation shadows.
5. **Signifiers**: High-contrast icon badges (capsule, telephone, audio speaker) clearly signal clickable actions for low-vision users.
6. **Mapping**: The confirm button is positioned directly adjacent to and below the specific pill photo it validates.
7. **Constraints**: Destructive or complex settings are intentionally constrained in a separate, PIN-protected caregiver submenu, preventing accidental schedule deletion.

---

### SCENARIO TOPIC 2: Heuristic Evaluation of a Broken UI (Session 08)
*Exam Prompt*: *"A travel booking website presents users with a 40-field form on a single page without progress indicators. Clicking 'Submit' resets all fields if one date format is wrong, with an alert box stating 'Error 0x4B3'. Conduct a Heuristic Evaluation using Nielsen's 10 Heuristics."*

1. **Violation 1: Visibility of System Status (Heuristic #1)**:
   - *Issue*: A single 40-field screen provides no progress bar or multi-step indicator.
   - *Fix*: Decompose form into a 3-step wizard (*Flight $\to$ Passenger $\to$ Payment*) with a step progress meter.
2. **Violation 2: Error Prevention (Heuristic #5)**:
   - *Issue*: Free-text inputs allow malformed dates.
   - *Fix*: Restrict input via an interactive calendar picker and enforce inline validation mask (`DD/MM/YYYY`).
3. **Violation 3: Help Users Recognize, Diagnose, and Recover from Errors (Heuristic #9)**:
   - *Issue*: "Error 0x4B3" is obscure system jargon that frustrates the user. Resetting the whole form erases valid work.
   - *Fix*: Provide plain-language inline notice (*"Departure date cannot be after return date"*) while preserving all entered valid form data.
4. **Violation 4: Recognition Rather Than Recall (Heuristic #6)**:
   - *Issue*: User must remember flight numbers and baggage rules across screens.
   - *Fix*: Sticky sidebar summary displaying selected flight itinerary and live total price.

---

### SCENARIO TOPIC 3: Usability Testing Plan & Think-Aloud Protocol (Session 14)
*Exam Prompt*: *"Design a Usability Testing Plan for a new Fintech Mobile App. Outline test goals, participant criteria, tasks, Think-Aloud instructions, and SUS score evaluation."*

1. **Participant Selection**: 5 to 8 target representative users (Jakob Nielsen’s rule: 5 users uncover 85% of usability defects).
2. **Task Scenarios (Concrete & Non-Leading)**:
   - *Task 1*: *"You owe ₹450 to your friend Ravi for dinner. Use the app to locate Ravi in your contacts and transfer the amount."*
3. **Think-Aloud Protocol Instructions**:
   - Instruct users to continuously verbalize their thoughts, expectations, hesitations, and frustrations while interacting (*"Say what you are looking for, what you expect to happen, and where you feel confused"*). The moderator remains neutral without giving hints.
4. **Metrics Collected**:
   - Objective: Task Completion Rate ($\ge 90\%$), Time on Task (Goal $< 45\text{ s}$), Error Frequency.
   - Subjective: Post-test **System Usability Scale (SUS)** score (Target $\ge 80$).

---

## 3. Plug-and-Play Domain Conversion Table

| HCI Concept | Healthcare App | Banking & ATM Kiosk | E-Commerce Platform |
| :--- | :--- | :--- | :--- |
| **Primary User Persona** | Elderly patient / Nurse | Everyday citizen / Commuter | Shopper on mobile |
| **Top Fitts’s Law Focus** | Emergency call button | Big Cash Dispense button | "Add to Cart" sticky bar |
| **Error Prevention (Poka-Yoke)** | Confirm dangerous dosage | 2-step transfer confirmation | Out-of-stock disablement |
| **Recognition vs Recall** | Show pill photograph | Display account balance visibly | Persistent cart preview |
| **Accessibility Focus** | Audio narration, $\ge 4.5:1$ contrast | Screen glare shield, braille keys | Zoomable images, keyboard nav |
