# BITS WILP Human Computer Interaction (BSDCBZC365)
## Detailed Session-Wise Exam Importance & Weightage Blueprint

> **Course**: BSDCBZC365 — Human Computer Interaction (HCI)  
> **Exam Nature**: Open Book | **Total Marks**: 40 Marks (40% Course Weightage) | **Duration**: 2½ Hours  
> **Core Texts**: Alan Dix et al., *Human-Computer Interaction*; Don Norman, *The Design of Everyday Things*

---

## 1. Executive Summary & Weightage Distribution

In BITS WILP Human Computer Interaction, the Comprehensive Exam is heavily oriented around **practical design critique, mathematical ergonomic laws, usability metrics, and interface wireframing** applied to unseen domain case studies (e.g., *Elderly Healthcare*, *Kiosk Systems*, *E-Commerce*, *Driver Telematics*).

Post-Midterm sessions (Sessions 08 through 16), along with core foundational principles from Sessions 06 and 07, account for **90% – 100% of the marks**.

```
+-------------------------------------------------------------------------------+
|                    HCI COMPREHENSIVE EXAM MARK SPLIT (40 MARKS)               |
+-------------------------------------------------------------------------------+
| Foundations (Sessions 01 – 05: History, Input Devices, CLI vs WIMP):  0% – 10% |
| Core Design & Heuristics (Sessions 06 – 08: Norman & Nielsen Laws) : 25% – 35% |
| Post-Midterm Applied (Sessions 09 – 16: Mobile, SUS, WCAG, Errors)  : 60% – 70% |
+-------------------------------------------------------------------------------+
```

---

## 2. Complete Session-Wise Importance & Weightage Matrix (CS01 – CS16)

| Session ID | Session Title & Core Focus | Priority Tier | Compre Exam Weightage | Typical Question Format |
| :---: | :--- | :---: | :---: | :--- |
| **Session 14** | **Usability Testing & SUS Score Calculation** | **Tier 1 (Super Critical)** | **15% – 20% (6 – 8 M)** | Compulsory numerical: Calculate System Usability Scale (SUS) score from 10-question questionnaire responses; interpret score percentile against baseline (68). |
| **Session 08** | **Nielsen's 10 Heuristics & Fitts's Law** | **Tier 1 (Super Critical)** | **15% – 20% (6 – 8 M)** | Heuristic evaluation & math: Identify heuristic violations in a given UI mockup; calculate movement time using Fitts's Law $MT = a + b \log_2(2D/W)$. |
| **Session 07** | **Norman's 7 Fundamental Principles & Affordance** | **Tier 1 (Critical)** | **12% – 15% (5 – 6 M)** | Design critique: Apply Affordance, Signifiers, Mapping, Feedback, Constraints, Discoverability, and Conceptual Model to an interface failure. |
| **Session 12** | **Mobile UI Design, Touch Targets & Thumb Zone** | **Tier 1 (Critical)** | **10% – 12% (4 – 5 M)** | Wireframe design: Design a mobile UI applying touch target minimums (48dp/44pt), Thumb Zone ergonomics, and responsive layout guidelines. |
| **Session 15** | **Accessibility Standards (WCAG 2.1) & ISO 9241** | **Tier 1 (Critical)** | **10% – 12% (4 – 5 M)** | Compliance analysis: Evaluate contrast ratios (4.5:1), screen-reader semantics under POUR principles (Perceivable, Operable, Understandable, Robust). |
| **Session 13** | **Error Handling, Forgiving UI & Poka-Yoke** | **Tier 2 (High)** | **8% – 10% (3 – 4 M)** | UI redesign: Redesign error messages and destructive actions using proactive prevention (slips vs mistakes) and 2-step confirmation dialogs. |
| **Session 06** | **Personas, Mental Models & Norman's Gulfs** | **Tier 2 (High)** | **8% – 10% (3 – 4 M)** | User modeling: Construct a persona profile with goals and pain points; bridge the Gulf of Execution and Gulf of Evaluation for a workflow. |
| **Session 11** | **Web UI Design, Visual Hierarchy & Hick's Law** | **Tier 2 (High)** | **5% – 8% (2 – 4 M)** | Layout evaluation: Apply F-pattern vs Z-pattern eye tracking, Hick-Hyman Law $T = b \log_2(n+1)$ to simplify multi-level nested menus. |
| **Session 16** | **Emerging Trends: Conversational UI & VUI** | **Tier 3 (Moderate)** | **0% – 5% (0 – 3 M)** | Emerging interaction: Design voice interaction prompts (turn-taking, error recovery) for hands-free or low-literacy environments. |
| **Session 09 & 10** | **Prototyping Fidelity & Figma Frameworks** | **Tier 3 (Moderate)** | **0% – 5% (0 – 3 M)** | Methodology: Compare Low-fi paper prototypes vs High-fi interactive prototypes; design system token reusability. |
| **Session 01 – 05** | **HCI Basics, Perception, Human Memory** | **Tier 3 (Low)** | **0% – 5% (0 – 2 M)** | Theoretical: Usability goals vs UX goals; Miller's law ($7 \pm 2$) chunking. |

---

## 3. Top-Priority Mathematical Formulas & Derivations

### 1. Fitts's Law (Target Movement Time)
$$MT = a + b \log_2\left(\frac{2D}{W}\right) = a + b \cdot \text{ID}$$
- $D$: Distance from cursor/finger to center of target.
- $W$: Width/size of target along axis of motion.
- $\text{ID} = \log_2(2D/W)$: Index of Difficulty in bits.
- **Exam Rule**: Placing controls on screen corners or edges gives virtual infinite width ($W \to \infty$), reducing $\text{ID} \to 0$!

### 2. System Usability Scale (SUS) Score
$$\text{SUS} = 2.5 \times \left[ \sum_{i \in \text{odd}} (R_i - 1) + \sum_{i \in \text{even}} (5 - R_i) \right]$$
- Odd questions (Positive statements, scale 1 to 5): Contribution $= R_i - 1$.
- Even questions (Negative statements, scale 1 to 5): Contribution $= 5 - R_i$.
- **Scale**: 0 to 100. Average baseline is **68**. A score $\ge 80.3$ is Grade A.

### 3. Hick-Hyman Law (Decision Time)
$$T = b \cdot \log_2(n + 1)$$
- $n$: Number of equal-probability choices.
- **Exam Rule**: Reduce menu clutter by chunking items hierarchically.
