# Computing | Teacher Planner: Micro:bit Physical Computing
*[TS-CO-KS2-008]*

**Subject:** Computing | **Key Stage:** KS2 | **Year group:** Y5, Y6
**Statutory reference:** design, write and debug programs that accomplish specific goals, including controlling or simulating physical systems | **Source document:** Computing (KS1/KS2) - National Curriculum Programme of Study
**Estimated duration:** 6 lessons | **Status:** Convention

**Planner coverage:** 7/10 expected capabilities surfaced

**Available now:** Curriculum anchor, Concept model, Differentiation data, Thinking lens, Lesson structure, Prior knowledge links, Learner scaffolding
**Still thin/missing:** Cross-curricular links, Vocabulary definitions, Success criteria

---

## Concepts

This study delivers **1 primary concept** and **1 secondary concept**.

### Primary concept: Programming: Sequence, Selection and Repetition (CO-KS12-C002)

**Type:** Skill | **Teaching weight:** 2/6

All programs are built from three fundamental control structures: sequence (instructions executed in order, one after another), selection (conditional branches where different instructions execute depending on a condition - if/then/else) and repetition (loops where instructions repeat a specified number of times or while a condition holds). These three structures are sufficient to express any computable algorithm, and mastery of them is the core of programming competence. At KS2, pupils learn to use all three structures in their programs, developing increasingly sophisticated and efficient code.

**Teaching guidance:** Introduce each control structure separately before combining them. Use visual block-based programming environments (Scratch, Blockly) initially to reduce syntax barriers. Progress to text-based languages at upper KS2 to develop more precise understanding of programming syntax. Always connect programming tasks to a genuine purpose: a game, an animation, a simulation. Teach debugging systematically: read the code line by line, trace the execution, identify where actual behaviour diverges from expected behaviour. Celebrate debugging success as much as successful first attempts.

**Key vocabulary:** sequence, selection, repetition, loop, conditional, if, then, else, while, for, variable, input, output, debug, program, code, execute, trace

**Common misconceptions:** Pupils often use loops incorrectly, either not using them when repetition is present (writing the same instruction multiple times) or using them in inappropriate contexts. Explicit comparison of repetitive code versus loop code makes the efficiency benefit clear. Selection (if/then/else) is conceptually more demanding; pupils may write conditions that cannot be true, or miss the else case. Tracing through conditional code step by step makes the logic visible.

#### Differentiation

| Level | What success looks like | Example task | Common errors |
|-------|------------------------|-------------|---------------|
| **Entry** | Creating a simple program using sequence — a series of instructions executed in order — using a block-based programming environment. | Program the sprite to walk forward 100 steps, say 'Hello!' and then turn around. | Putting blocks in the wrong order so the sprite turns before walking; Not connecting blocks together so only the first one runs |
| **Developing** | Using selection (if/then) and repetition (loops) in programs to create more complex behaviour. | Program a character that walks forward and turns when it reaches the edge of the screen. Use a loop and an if statement. | Putting the if-statement outside the loop so it only checks once; Creating an infinite loop without any stopping condition |
| **Expected** | Combining sequence, selection and repetition to create programs that solve problems or meet a design brief, using variables to store and change data. | Create a quiz program that asks three questions, uses a variable to keep score, and gives a different message depending on the final score. | Not initialising the variable at the start (score starts at a random value); Using the wrong comparison operator (= vs >) in the selection |
| **Greater Depth** | Designing modular programs using procedures or functions, explaining how abstraction makes programs easier to understand and maintain. | Refactor your quiz program so each question is handled by a reusable procedure. Why is this better? | Creating procedures that are too specific and not genuinely reusable; Not understanding how parameters pass information into procedures |

> **Model response (Entry):** *I used three blocks: 'move 100 steps', 'say Hello! for 2 seconds', 'turn 180 degrees'. The sprite walked, spoke and turned around.*

> **Model response (Developing):** *I used a 'forever' loop containing: 'move 10 steps', then 'if touching edge then turn 180 degrees'. The character bounces back and forth across the screen without stopping. The loop repeats the instructions and the if-statement checks for the edge each time.*

> **Model response (Expected):** *I created a variable called 'score' set to 0. For each question, I used 'ask' and checked the answer with an if-statement. If correct, I increased score by 1. At the end, I used selection: if score = 3, say 'Perfect!'; if score >= 1, say 'Well done!'; else say 'Try again!'. The program uses sequence (question order), selection (checking answers) and repetition (I could put questions in a loop).*

> **Model response (Greater Depth):** *I created a procedure called 'ask_question' that takes a question and correct answer as inputs. It asks the question, checks the answer, and updates the score. My main program just calls this procedure three times with different questions. This is better because if I want to change how questions work, I only change the procedure once instead of changing code in three places. It is also easier to add more questions.*

### Secondary concept: Decomposition and Computational Thinking (CO-KS12-C006)

**Type:** Skill | **Teaching weight:** 2/6

Computational thinking is a set of problem-solving approaches that involve breaking problems down (decomposition), identifying patterns (pattern recognition), focusing on the most relevant information (abstraction) and developing step-by-step solutions (algorithm design). Decomposition - breaking a complex problem into smaller, manageable sub-problems - is particularly important in programming, as it enables pupils to tackle problems that would otherwise be too large to address as a whole. At KS2, pupils apply decomposition to design programs and to plan complex digital projects.

#### Differentiation

| Level | What success looks like | Common errors |
|-------|------------------------|---------------|
| **Entry** | Breaking a simple problem into smaller, more manageable parts (decomposition). | Making the parts too big (still complex problems rather than simple tasks); Not being able to separate the problem into independent parts |
| **Developing** | Applying decomposition, pattern recognition and abstraction to solve problems: identifying repeated patterns and focusing on the most important information. | Grouping by superficial features (colour, size) rather than meaningful patterns; Not understanding what 'abstraction' means in computing — removing unnecessary detail |
| **Expected** | Applying all aspects of computational thinking (decomposition, pattern recognition, abstraction, algorithm design) to solve a complex problem systematically. | Jumping straight to the algorithm without decomposing and abstracting first; Not recognising that computational thinking is a general problem-solving approach, not just programming |
| **Greater Depth** | Evaluating the effectiveness of computational thinking solutions, identifying limitations and suggesting improvements, and explaining how these approaches are used in real-world computing. | Thinking the first algorithm is the final answer without considering limitations; Not connecting the abstract solution to real-world applications |

---

## Thinking lens: Systems and System Models (primary)

**Key question:** What are the parts of this system, how do they interact, and what happens when something changes?

**Why this lens fits:** Decomposition requires pupils to model a complex problem as a system of smaller interacting parts — understanding that the whole can be broken into components that each perform a defined function is a systems-thinking act.

**Question stems for KS2:**
- What goes into this system, and what comes out?
- If you changed this one part, what else would be affected?
- Where does this system start and end?
- How could we draw a model to explain how this works?

**Secondary lens:** Cause and Effect — Writing and debugging programs with sequence, selection and repetition demands that pupils predict the effect of each control structure — tracing how changing a condition in a selection statement changes what the program does is a direct cause-and-effect analysis.

---

## Session structure: Practical Application

### Practical Application
A hands-on sequence where pupils apply knowledge and skills to solve a practical problem or create a functional outcome. Begins with a real-world context, builds skills through rehearsal, guides design or planning, supports making or problem-solving, and concludes with evaluation against success criteria.

`context` → `skill_rehearsal` → `design` → `make_or_solve` → `evaluate`

**Assessment:** Practical outcome (solution, product, program) evaluated against defined success criteria, with written or verbal explanation of the process and decisions made.

**Teacher note:** Use the PRACTICAL APPLICATION template: set a real-world context or problem that requires pupils to apply knowledge and skills. Rehearse the key skills needed through guided practice. Support pupils in designing their approach, carrying out the practical task, and evaluating their outcome. Encourage them to explain what worked well and what they would improve.

**KS2 question stems:**
- What skills will you need to solve this problem?
- What is your plan, and why did you choose this approach?
- How well did your solution work?
- What would you change if you did it again?

---

## Computing focus

**Programming paradigm:** Block Based
**Software/tool:** Micro:bit
**Computational concepts:** sequence, selection, input output
**Abstraction level:** Visual
**Themes:** physical computing, sensors, programming

---

## Why this study matters

The micro:bit bridges digital programming and the physical world. Pupils program the micro:bit to respond to sensor inputs (button press, tilt, light level, temperature) and produce outputs (LED display, sound). This physical computing connects to DT (control in products) and Science (sensors measuring the environment). The block-based editor makes it accessible while the physical output makes it tangible.

---

## Pitfalls to avoid

1. Too many features at once -- start with one input and one output
2. Not downloading the program to the micro:bit -- test on the simulator first, then download
3. USB connection issues -- teach the download-and-transfer process explicitly

---

## Computational thinking skills (KS2)

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
| microcontroller | |
| sensor | |
| input | |
| output | |
| LED | |
| button | |
| accelerometer | |
| program | |
| download | |
| abstraction | *(from concept key vocabulary)* |
| algorithm | *(from concept key vocabulary)* |
| code | *(from concept key vocabulary)* |
| computational thinking | *(from concept key vocabulary)* |
| conditional | *(from concept key vocabulary)* |
| debug | *(from concept key vocabulary)* |
| decomposition | *(from concept key vocabulary)* |
| design | *(from concept key vocabulary)* |
| else | *(from concept key vocabulary)* |
| execute | *(from concept key vocabulary)* |

## Prior knowledge (retrieval plan)

Pupils should already know the following from earlier units:

| Prior knowledge needed | For concept | Description |
|----------------------|-------------|-------------|
| Algorithms | Programming: Sequence, Selection and Repetition | An algorithm is a precise, unambiguous sequence of instructions for solving a problem or accompli... |
| Programming: Sequence, Selection and Repetition | Decomposition and Computational Thinking | All programs are built from three fundamental control structures: sequence (instructions executed... |

---

## Scaffolding and inclusion (Y5)

| Guideline | Detail |
|-----------|--------|
| Reading level | Fluent Reader (Lexile 450–650) |
| Text-to-speech | Available |
| Max sentence length | 22 words |
| Vocabulary | Academic vocabulary expected. Technical domain vocabulary accessible with in-context clues. Figurative language (metaphor, personification) appropriate. |
| Scaffolding level | Light To Moderate |
| Hint tiers | 4 tiers |
| Session length | 20–30 minutes |
| Worked examples | Required — Text-based. Child completes partial worked examples (fading). Not fully narrated. |
| Feedback tone | Peer Like Respectful |
| Normalize struggle | Yes |
| Example correct feedback | *You recognised that 1/2 is larger than 2/5, and used the common denominator method correctly. The visualiser confirms it — the bar for 1/2 is noticeably longer.* |
| Example error feedback | *The reasoning does not quite hold: you said both fractions are the same because the numerator in 2/5 is double the numerator in 1/2. But the denominator changed too — the pieces got smaller. Converting to tenths: 1/2 = 5/10 and 2/5 = 4/10. Which is larger now?* |

---

## Knowledge organiser

**Key terms:**
- microcontroller
- sensor
- input
- output
- LED
- button
- accelerometer
- program
- download

**Core facts (expected standard):**
- **Programming: Sequence, Selection and Repetition**: Combining sequence, selection and repetition to create programs that solve problems or meet a design brief, using variables to store and change data.

---

## Graph context

**Node type:** `ComputingTopicSuggestion` | **Study ID:** `TS-CO-KS2-008`

**Concept IDs:**
- `CO-KS12-C002`: Programming: Sequence, Selection and Repetition (primary)
- `CO-KS12-C006`: Decomposition and Computational Thinking

**Cypher query:**
```cypher
MATCH (ts:ComputingTopicSuggestion {suggestion_id: 'TS-CO-KS2-008'})
  -[:DELIVERS_VIA]->(c:Concept)
  -[:HAS_DIFFICULTY_LEVEL]->(dl)
RETURN c.name, dl.label, dl.description
```

---

*Generated from the UK Curriculum Knowledge Graph — zero LLM generation.*
