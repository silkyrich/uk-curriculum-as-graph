# Computing | Teacher Planner: Boolean Logic and Binary Arithmetic
*[TS-CO-KS3-003]*

**Subject:** Computing | **Key Stage:** KS3 | **Year group:** Y7, Y8
**Statutory reference:** understand simple Boolean logic and some of its uses in circuits and programming | **Source document:** Computing (KS3/KS4) - National Curriculum Programme of Study
**Estimated duration:** 6 lessons | **Status:** Mandatory

**Planner coverage:** 6/10 expected capabilities surfaced

**Available now:** Curriculum anchor, Concept model, Differentiation data, Thinking lens, Lesson structure, Learner scaffolding
**Still thin/missing:** Cross-curricular links, Vocabulary definitions, Success criteria, Prior knowledge links

---

## Concepts

This study delivers **1 primary concept** and **0 secondary concepts**.

### Primary concept: Boolean Logic and Binary (CO-KS34-C002)

**Type:** Knowledge | **Teaching weight:** 3/6

Boolean algebra is the branch of mathematics that deals with variables that can take only two values (true/false, 1/0). Boolean logic operations (AND, OR, NOT, NAND, NOR, XOR) are the fundamental operations of digital computing, implemented in hardware as logic gates. Binary (base 2) is the number system used by digital computers, where all data is represented as sequences of 0s and 1s. Understanding binary representation of integers, converting between binary and decimal, and performing binary arithmetic are foundational to understanding how computers store and process all types of data. Boolean logic connects programming (where logical conditions control program flow) to hardware (where logic gates implement digital circuits).

**Teaching guidance:** Teach Boolean operations through truth tables before connecting to programming and hardware. Use logic gate diagrams to show how Boolean operations are implemented physically. Practice binary-to-decimal and decimal-to-binary conversion systematically. Teach binary addition with carries. Connect to programming: the Boolean conditions in if statements and while loops use the same Boolean logic. Discuss how images, sound and text are encoded in binary: different data types, same underlying representation. Use physical logic gate simulations where possible.

**Key vocabulary:** Boolean, binary, bit, byte, AND, OR, NOT, truth table, logic gate, convert, decimal, hexadecimal, unsigned, signed, twos complement, overflow

**Common misconceptions:** Pupils often confuse binary (a number system) with a code for letters or colours, not realising it is a general-purpose representational system for any data. The fact that 0 and 1 in binary do not mean 'nothing' and 'one' but represent powers of two needs explicit teaching. Boolean AND requiring both inputs to be true (not either), and the counterintuitive behaviour of NAND and NOR gates, are common points of confusion requiring careful attention to truth tables.

#### Differentiation

| Level | What success looks like | Example task | Common errors |
|-------|------------------------|-------------|---------------|
| **Emerging** | Knows that computers use binary (0s and 1s) and can convert small numbers between binary and decimal, but does not understand why binary is used or how it relates to hardware. | Convert the decimal number 13 to binary. Show your working. | Reading the remainders from top to bottom instead of bottom to top; Forgetting to include leading zeros when expressing as a fixed-width byte (e.g., 00001101) |
| **Developing** | Understands Boolean logic operations (AND, OR, NOT), can complete truth tables, and performs binary addition with carries. | Complete the truth table for the expression: A AND (B OR NOT C). Then calculate 0110 + 0011 in binary. | Forgetting to carry the 1 in binary addition when the sum exceeds 1; Confusing AND with OR in the truth table (AND requires both inputs true; OR requires at least one) |
| **Secure** | Connects Boolean logic to both programming (conditional statements) and hardware (logic gates), understands how different data types are represented in binary, and applies binary arithmetic confidently. | Explain how the colour of a single pixel on screen is stored in binary. A pixel uses 24-bit colour. How many different colours can be represented? | Confusing bits and bytes (8 bits per channel, not 8 bytes); Not being able to calculate 2 to the power of 24 or explain what it means in practical terms |
| **Mastery** | Designs logic circuits using multiple gates, understands how binary representation enables all computing operations at the hardware level, and evaluates the limitations and trade-offs of binary systems. | Design a logic circuit using AND, OR and NOT gates that implements a simple security system: the alarm sounds if the door sensor detects 'open' AND the system is armed, OR if the panic button is pressed (regardless of whether the system is armed). | Using an AND gate instead of OR for the final combination, which would mean the panic button only works when the door is also open; Not verifying the circuit with all possible input combinations to check correctness |

> **Model response (Emerging):** *13 divided by 2 = 6 remainder 1. 6 divided by 2 = 3 remainder 0. 3 divided by 2 = 1 remainder 1. 1 divided by 2 = 0 remainder 1. Reading the remainders from bottom to top: 13 in binary is 1101.*

> **Model response (Developing):** *Truth table (A, B, C, NOT C, B OR NOT C, A AND (B OR NOT C)):
0,0,0,1,1,0 | 0,0,1,0,0,0 | 0,1,0,1,1,0 | 0,1,1,0,1,0 | 1,0,0,1,1,1 | 1,0,1,0,0,0 | 1,1,0,1,1,1 | 1,1,1,0,1,1.

Binary addition: 0110 + 0011. Rightmost column: 0+1=1. Second column: 1+1=10, write 0 carry 1. Third column: 1+0+1(carry)=10, write 0 carry 1. Fourth column: 0+0+1(carry)=1. Result: 1001 (which is 9 in decimal: 6+3=9, correct).*

> **Model response (Secure):** *A 24-bit colour pixel uses 8 bits for each of the three colour channels: red, green and blue (RGB). Each channel has 8 bits, giving 2 to the power of 8 = 256 possible intensity levels (0-255) per channel. The total number of different colours is 256 x 256 x 256 = 16,777,216 (approximately 16.7 million). For example, pure red is (11111111, 00000000, 00000000) = (255, 0, 0); white is (11111111, 11111111, 11111111) = (255, 255, 255); black is (00000000, 00000000, 00000000). A 1920x1080 screen has 2,073,600 pixels, each storing 24 bits, so a single uncompressed frame requires approximately 6.2 megabytes of data.*

> **Model response (Mastery):** *Inputs: D = door sensor (1 = open), A = armed (1 = armed), P = panic button (1 = pressed). Output: S = alarm sounds. Boolean expression: S = (D AND A) OR P. Circuit: Wire D and A into an AND gate (output = D AND A). Wire the AND gate output and P into an OR gate (output = (D AND A) OR P). The OR gate output drives the alarm. Verification: Door open + armed + no panic: (1 AND 1) OR 0 = 1 → alarm sounds (correct). Door closed + armed + no panic: (0 AND 1) OR 0 = 0 → no alarm (correct). Door open + not armed: (1 AND 0) OR 0 = 0 → no alarm (correct — the system is disarmed). Panic pressed (any state): anything OR 1 = 1 → alarm always sounds (correct — panic overrides everything). This demonstrates how complex real-world logic is implemented using simple binary gates — every digital system, from alarms to processors, is built from combinations of these fundamental operations.*

---

## Thinking lens: Systems and System Models (primary)

**Key question:** What are the parts of this system, how do they interact, and what happens when something changes?

**Why this lens fits:** Modular programming requires pupils to decompose a system into functions/procedures with defined inputs and outputs — the program as a whole is a system of interacting modules, and the design task is to model the right modular decomposition.

**Question stems for KS3:**
- What feedback loops exist in this system?
- Does this model capture all the important interactions, or does it oversimplify?
- What emergent property arises from these components interacting?
- How would removing or adding a component change the system's behaviour?

**Secondary lens:** Patterns — Sorting and searching algorithms are canonical patterns — pupils study merge sort, binary search and others as reusable solutions to classes of problems, developing the pattern-recognition skill of identifying which algorithmic pattern fits a given problem.

---

## Session structure: Practical Application

### Practical Application
A hands-on sequence where pupils apply knowledge and skills to solve a practical problem or create a functional outcome. Begins with a real-world context, builds skills through rehearsal, guides design or planning, supports making or problem-solving, and concludes with evaluation against success criteria.

`context` → `skill_rehearsal` → `design` → `make_or_solve` → `evaluate`

**Assessment:** Practical outcome (solution, product, program) evaluated against defined success criteria, with written or verbal explanation of the process and decisions made.

**Teacher note:** Use the PRACTICAL APPLICATION template: present a realistic problem context that requires pupils to select and apply relevant knowledge and skills. Expect pupils to rehearse key techniques, design a solution with justification, and carry out the task with attention to accuracy and quality. Guide evaluation that considers both the outcome and the effectiveness of their approach.

**KS3 question stems:**
- What knowledge and skills are relevant to this problem, and how do they connect?
- Why did you choose this approach over alternatives?
- How effectively does your solution address the original problem?
- What would you evaluate as the strengths and weaknesses of your approach?

---

## Computing focus

**Computational concepts:** data representation, boolean logic
**Abstraction level:** Symbolic
**Themes:** binary, Boolean logic, data representation

---

## Why this study matters

Boolean logic (AND, OR, NOT) underpins both programming (conditional expressions) and hardware (logic gates). Binary number representation explains how computers store and process all data. Teaching these together reveals that the logical and mathematical foundations of computing are deeply connected. Unplugged binary counting (with cards showing 1, 2, 4, 8, 16) and logic gate circuits (using simple switches or online simulators) make the abstract concrete.

---

## Pitfalls to avoid

1. Binary treated as pure maths without connection to computing -- always show how binary is used inside the computer
2. Boolean logic taught in isolation from programming -- connect AND/OR/NOT to if-statement conditions
3. Pupils confusing binary addition with decimal -- use column headings (128, 64, 32, 16, 8, 4, 2, 1) consistently

---

## Computational thinking skills (KS3)

These disciplinary skills should be woven through teaching, not taught in isolation:

- **Abstraction (KS1)** — Focus on the most important features of a problem or task while ignoring unnecessary detail; represent real-world actions as simple step-by-step instructions that capture the essential logic without irrelevant specifics.
- **Abstraction (KS2)** — Design programs and digital solutions by identifying the key variables, inputs and outputs relevant to a problem while deliberately ignoring peripheral details; use procedures and functions as abstractions that hide implementation complexity; apply abstraction when planning programs using pseudocode or flowcharts.
- **Abstraction (KS3)** — Design and evaluate computational abstractions that model the state and behaviour of real-world problems and physical systems; select appropriate levels of abstraction for a given problem context; use abstract data types, classes and interfaces to hide implementation detail; understand the layered abstractions present in computing systems from hardware to application.
- **Decomposition (KS1)** — Break a familiar task or problem into a sequence of smaller, ordered steps; understand that a complex instruction can be split into simpler sub-instructions that together achieve the same goal; apply this thinking when giving instructions to a programmable toy or creating a simple program.
- **Decomposition (KS2)** — Decompose a complex programming problem or digital project into distinct, manageable sub-problems that can be developed and tested independently; plan program structure using top-down design before coding; use procedures and functions as the coded expression of decomposed sub-problems.
- **Decomposition (KS3)** — Design and develop modular programs that use procedures and functions to decompose complex problems; apply top-down and bottom-up design strategies; decompose data requirements as well as procedural logic, selecting appropriate data structures for each sub-problem; evaluate how modular decomposition improves code readability, maintainability and reuse.

---

## Vocabulary word mat

| Term | Meaning |
|------|---------|
| binary | |
| bit | |
| byte | |
| AND | |
| OR | |
| NOT | |
| truth table | |
| logic gate | |
| decimal | |
| hexadecimal | |
| overflow | |
| binary addition | |
| Boolean | *(from concept key vocabulary)* |
| convert | *(from concept key vocabulary)* |
| signed | *(from concept key vocabulary)* |
| twos complement | *(from concept key vocabulary)* |
| unsigned | *(from concept key vocabulary)* |

## Scaffolding and inclusion (Y7)

| Guideline | Detail |
|-----------|--------|
| Reading level | Secondary Transition Reader (Lexile 700–950) |
| Text-to-speech | Available |
| Max sentence length | 30 words |
| Vocabulary | Secondary curriculum vocabulary including discipline-specific terms. Etymology and morphology appropriate (e.g., prefixes, roots). Formal academic register expected. |
| Scaffolding level | Light |
| Hint tiers | 4 tiers |
| Session length | 25–40 minutes |
| Worked examples | Required — Text-based. Reference solutions available after independent attempt. |
| Feedback tone | Academic Peer |
| Normalize struggle | Yes |
| Example correct feedback | *Correct — and the implication is worth noting: if this is true, then [connected consequence] should also hold. Does it?* |
| Example error feedback | *That reasoning has a gap: you assumed [X], but the evidence points the other way because [Y]. Revise your argument in light of that.* |

---

## Knowledge organiser

**Key terms:**
- binary
- bit
- byte
- AND
- OR
- NOT
- truth table
- logic gate
- decimal
- hexadecimal
- overflow
- binary addition

**Core facts (expected standard):**
- **Boolean Logic and Binary**: Connects Boolean logic to both programming (conditional statements) and hardware (logic gates), understands how different data types are represented in binary, and applies binary arithmetic confidently.

---

## Graph context

**Node type:** `ComputingTopicSuggestion` | **Study ID:** `TS-CO-KS3-003`

**Concept IDs:**
- `CO-KS34-C002`: Boolean Logic and Binary (primary)

**Cypher query:**
```cypher
MATCH (ts:ComputingTopicSuggestion {suggestion_id: 'TS-CO-KS3-003'})
  -[:DELIVERS_VIA]->(c:Concept)
  -[:HAS_DIFFICULTY_LEVEL]->(dl)
RETURN c.name, dl.label, dl.description
```

---

*Generated from the UK Curriculum Knowledge Graph — zero LLM generation.*
