# BITS WILP Human Computer Interaction (BSDCBZC365)
## Post-Midterm Master Exam Preparation & Open-Book Cheat Sheet

> **Course**: BSDCBZC365 — Human Computer Interaction (HCI)  
> **Exam Nature**: Open Book Comprehensive Exam | **Duration**: 2½ Hours  
> **Coverage**: Sessions 08 through 16 + Norman's & Nielsen's Foundations (Sessions 06, 07, 08)

---

## 1. The Core Interaction Principles (Sessions 07 & 08)

### 1.1 Norman’s 7 Fundamental Principles of Design
1. **Discoverability**: Is it possible to determine what actions are possible and the current state of the device?
2. **Feedback**: Is there full and continuous information about the results of actions and the current state of the system? (Audio chimes, haptic pulses, visual progress rings).
3. **Conceptual Model**: Does the design project an intuitive mental model that matches the user's expectations?
4. **Affordances**: The fundamental properties of an object that determine just how it could possibly be used (e.g., a physical button affords pushing; a flat screen does not physically afford pushing without a signifier).
5. **Signifiers**: Any perceivable indicator that communicates appropriate behavior (e.g., drop shadows on a flat card, an arrow icon, a "Swipe Up" label).
6. **Mappings**: The spatial, analogical relationship between a control and its effect on the physical world (e.g., turning an on-screen dial clockwise increases volume).
7. **Constraints**: Restricting possible interactions to prevent user error (Physical constraints, Cultural constraints, Semantic constraints, Logical constraints).

### 1.2 Norman’s Two Gulfs
- **The Gulf of Execution**: The gap between a user's mental intention and the physical actions allowed by the interface (*"How do I do it?"*). Bridged by: Affordances, Signifiers, Mapping, Constraints.
- **The Gulf of Evaluation**: The gap between the system's physical state change and the user's mental perception of that change (*"Did it work?"*). Bridged by: Immediate Feedback, Visible System Status, Clear Conceptual Model.

### 1.3 Nielsen's 10 Usability Heuristics (Quick Matrix)
1. **Visibility of system status**: Continuous feedback with reasonable speed (e.g., upload percentage).
2. **Match between system and real world**: Familiar language, real-world metaphors (e.g., trash can, shopping cart).
3. **User control and freedom**: Universal "emergency exit" without penalty (Undo, Redo, Cancel).
4. **Consistency and standards**: Same words, situations, or actions mean the same thing across platforms.
5. **Error prevention**: Eliminate error-prone conditions or present a confirmation before committing action (Poka-Yoke).
6. **Recognition rather than recall**: Make elements and options visible so users do not need to remember across screens.
7. **Flexibility and efficiency of use**: Shortcuts, macros, and accelerators for experts without cluttering novice UI.
8. **Aesthetic and minimalist design**: Dialogues should not contain irrelevant or rarely needed information.
9. **Help users recognize, diagnose, and recover from errors**: Plain language error messages indicating the exact solution.
10. **Help and documentation**: Easy to search, focused on user tasks, concise list of concrete steps.

---

## 2. Mathematical Ergonomic Laws (Sessions 08 & 11)

### 2.1 Fitts’s Law Numerical Protocol
$$MT = a + b \log_2\left(\frac{2D}{W}\right)$$
- $MT$: Movement time (milliseconds).
- $D$: Distance to target center.
- $W$: Target width along movement vector.
- **Exam Calculation Example**: If $a = 100\text{ ms}$, $b = 150\text{ ms/bit}$, $D = 200\text{ mm}$, and $W = 20\text{ mm}$:
  $$\text{ID} = \log_2\left(\frac{2 \times 200}{20}\right) = \log_2(20) = \frac{\ln(20)}{\ln(2)} \approx 4.322\text{ bits}$$
  $$MT = 100 + 150 \times 4.322 = 100 + 648.3 = 748.3\text{ ms}$$

### 2.2 System Usability Scale (SUS) Score Protocol
$$\text{SUS} = 2.5 \times \left[ \sum_{i \in \{1,3,5,7,9\}} (R_i - 1) + \sum_{j \in \{2,4,6,8,10\}} (5 - R_j) \right]$$

**Exam Worked Example**: A participant rates the 10 SUS questions (scale 1–5):
`[4, 2, 5, 1, 4, 2, 5, 2, 4, 2]`
1. Sum of odd items: $(4-1) + (5-1) + (4-1) + (5-1) + (4-1) = 3 + 4 + 3 + 4 + 3 = 17$.
2. Sum of even items: $(5-2) + (5-1) + (5-2) + (5-2) + (5-2) = 3 + 4 + 3 + 3 + 3 = 16$.
3. Combined sum: $17 + 16 = 33$.
4. Total SUS Score: $33 \times 2.5 = \mathbf{82.5}$!
5. **Interpretation**: Grade A / Excellent usability (significantly surpasses the industry baseline of 68).

---

## 3. Mobile UI & Accessibility Standards (Sessions 12 & 15)

### 3.1 Mobile Touch Targets & Thumb Zone
- **Apple iOS HIG**: Minimum touch target $\ge 44 \times 44\text{ pt}$.
- **Google Android Material Design**: Minimum touch target $\ge 48 \times 48\text{ dp}$.
- **Steven Hoober's Thumb Zone Ergonomics**:
  - *Natural Zone (Easy)*: Bottom third of screen $\implies$ Place primary navigation and frequent actions here.
  - *Stretch Zone (Reachable)*: Middle third $\implies$ Secondary controls, content cards.
  - *Hard Zone (Difficult)*: Top corners $\implies$ Destructive actions, profile settings (requires two hands).

### 3.2 WCAG 2.1 Accessibility (Level AA)
- **Contrast Ratios**:
  - Normal Body Text ($< 18\text{ pt}$): Minimum contrast $\ge \mathbf{4.5 : 1}$.
  - Large Text ($\ge 18\text{ pt}$ or bold $\ge 14\text{ pt}$): Minimum contrast $\ge \mathbf{3.0 : 1}$.
  - Graphical Objects & UI Components: Contrast $\ge \mathbf{3.0 : 1}$.
- **The 4 POUR Principles**:
  1. *Perceivable*: Available to sight, hearing, and touch (Alt text for images, transcripts for audio).
  2. *Operable*: Keyboard navigable, no timing traps, sufficient touch target size.
  3. *Understandable*: Clear labels, predictable navigation, readable language tags.
  4. *Robust*: Compatible across diverse user agents, screen readers, and assistive technologies.
