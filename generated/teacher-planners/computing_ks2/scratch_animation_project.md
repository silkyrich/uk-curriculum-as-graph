# Computing | Teacher Planner: Scratch Animation Project
*[TS-CO-KS2-001]*

**Subject:** Computing | **Key Stage:** KS2 | **Year group:** Y3, Y4
**Statutory reference:** design, write and debug programs that accomplish specific goals | **Source document:** Computing (KS1/KS2) - National Curriculum Programme of Study
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

### Secondary concept: Debugging and Logical Reasoning (CO-KS12-C003)

**Type:** Skill | **Teaching weight:** 2/6

Debugging is the process of finding and fixing errors in programs. It requires logical reasoning: the ability to read code, mentally execute it step by step, identify where the actual behaviour diverges from the expected behaviour, and determine what change will fix the error. Logical reasoning about programs is also required to predict what a program will do before running it. At KS1 and KS2, developing debugging skills and the habit of logical, systematic thinking about code is as important as learning to write new code.

#### Differentiation

| Level | What success looks like | Common errors |
|-------|------------------------|---------------|
| **Entry** | Identifying that a program is not working as expected and finding an obvious error by comparing the output with the intended result. | Rewriting the whole program instead of finding and fixing the specific error; Not being able to describe what the program should do versus what it actually does |
| **Developing** | Using logical reasoning to trace through a program step by step, predicting the output and identifying where it goes wrong. | Not updating the variable value between iterations; Tracing through only the first iteration and guessing the rest |
| **Expected** | Systematically debugging programs by testing, identifying errors, hypothesising causes, making changes and retesting. | Fixing one bug without retesting to check it doesn't cause another; Changing multiple things at once and not knowing which change fixed the problem |
| **Greater Depth** | Applying debugging strategies systematically, including using test data, print statements for tracing, and explaining why certain types of bugs are harder to find. | Only testing with one type of input data; Not testing edge cases (empty lists, duplicates, already-sorted data) |

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
**Software/tool:** Scratch
**Computational concepts:** sequence, repetition
**Abstraction level:** Visual
**Themes:** programming, animation, creative computing

---

## Why this study matters

Scratch is the de facto standard block-based programming environment for primary computing. Creating an animation requires sequencing, repetition (loops for animation), and event handling -- three key NC concepts in a single motivating project. The visual output gives immediate feedback on whether code is working correctly. This is typically the first substantial Scratch project at KS2.

---

## Pitfalls to avoid

1. Too ambitious a first project -- start with one sprite doing one thing
2. Not using the green flag event block -- programs do not run without a trigger
3. Repeat loops set to wrong numbers -- test with small numbers first

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
| algorithm | |
| sequence | |
| loop | |
| repeat | |
| event | |
| sprite | |
| stage | |
| block | |
| forever loop | |
| animation | |
| actual | *(from concept key vocabulary)* |
| bug | *(from concept key vocabulary)* |
| check | *(from concept key vocabulary)* |
| code | *(from concept key vocabulary)* |
| conditional | *(from concept key vocabulary)* |
| correct | *(from concept key vocabulary)* |
| debug | *(from concept key vocabulary)* |
| else | *(from concept key vocabulary)* |
| error | *(from concept key vocabulary)* |
| execute | *(from concept key vocabulary)* |

## Prior knowledge (retrieval plan)

Pupils should already know the following from earlier units:

| Prior knowledge needed | For concept | Description |
|----------------------|-------------|-------------|
| Algorithms | Programming: Sequence, Selection and Repetition | An algorithm is a precise, unambiguous sequence of instructions for solving a problem or accompli... |

---

## Scaffolding and inclusion (Y3)

| Guideline | Detail |
|-----------|--------|
| Reading level | Developing Reader (Lexile 150–350) |
| Text-to-speech | Available |
| Max sentence length | 14 words |
| Vocabulary | Subject vocabulary with inline glossary support. Abstract concepts grounded in familiar contexts. Similes and comparisons helpful (e.g., 'solid is like a brick'). |
| Scaffolding level | Moderate To High |
| Hint tiers | 3 tiers |
| Session length | 12–20 minutes |
| Worked examples | Required — Text + diagram narrated. Step-by-step with child input at key points ('What would you do next?'). |
| Feedback tone | Warm Competence Focused |
| Normalize struggle | Yes |
| Example correct feedback | *You spotted the pattern — all the multiples of 6 end in an even number. That is a really useful thing to notice.* |
| Example error feedback | *That one got you — 7×8 trips up a lot of people. Here is a trick: 7×7 is 49, so 7×8 is just 7 more, which gives 56.* |

---

## Knowledge organiser

**Key terms:**
- algorithm
- sequence
- loop
- repeat
- event
- sprite
- stage
- block
- forever loop
- animation

**Core facts (expected standard):**
- **Programming: Sequence, Selection and Repetition**: Combining sequence, selection and repetition to create programs that solve problems or meet a design brief, using variables to store and change data.

---

## Graph context

**Node type:** `ComputingTopicSuggestion` | **Study ID:** `TS-CO-KS2-001`

**Concept IDs:**
- `CO-KS12-C002`: Programming: Sequence, Selection and Repetition (primary)
- `CO-KS12-C003`: Debugging and Logical Reasoning

**Cypher query:**
```cypher
MATCH (ts:ComputingTopicSuggestion {suggestion_id: 'TS-CO-KS2-001'})
  -[:DELIVERS_VIA]->(c:Concept)
  -[:HAS_DIFFICULTY_LEVEL]->(dl)
RETURN c.name, dl.label, dl.description
```

---

*Generated from the UK Curriculum Knowledge Graph — zero LLM generation.*
