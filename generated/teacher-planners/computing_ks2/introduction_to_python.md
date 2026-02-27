# Computing | Teacher Planner: Introduction to Python
*[TS-CO-KS2-009]*

**Subject:** Computing | **Key Stage:** KS2 | **Year group:** Y6
**Statutory reference:** design, write and debug programs that accomplish specific goals | **Source document:** Computing (KS1/KS2) - National Curriculum Programme of Study
**Estimated duration:** 6 lessons | **Status:** Convention

**Planner coverage:** 7/10 expected capabilities surfaced

**Available now:** Curriculum anchor, Concept model, Differentiation data, Thinking lens, Lesson structure, Prior knowledge links, Learner scaffolding
**Still thin/missing:** Cross-curricular links, Vocabulary definitions, Success criteria

---

## Concepts

This study delivers **1 primary concept** and **2 secondary concepts**.

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

**Programming paradigm:** Text Based
**Software/tool:** Python
**Computational concepts:** sequence, selection, repetition, variable
**Abstraction level:** Symbolic
**Themes:** text-based programming, Python

---

## Why this study matters

The NC requires experience of at least one text-based programming language at KS2. Python is the standard choice because its syntax is readable and forgiving, it is used professionally (motivation for older pupils), and it connects directly to KS3 computing. Starting with simple programs (print statements, input, variables, if-else) and building to loops prepares pupils for secondary school programming.

---

## Pitfalls to avoid

1. Syntax errors causing frustration -- teach that error messages are helpful, not punishing
2. Typing speed too slow -- accept that text-based coding is slower at first; it develops with practice
3. Copy-paste without understanding -- require pupils to explain what each line does

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
| Python | |
| syntax | |
| variable | |
| string | |
| integer | |
| print | |
| input | |
| if | |
| else | |
| loop | |
| indentation | |
| abstraction | *(from concept key vocabulary)* |
| actual | *(from concept key vocabulary)* |
| algorithm | *(from concept key vocabulary)* |
| bug | *(from concept key vocabulary)* |
| check | *(from concept key vocabulary)* |
| code | *(from concept key vocabulary)* |
| computational thinking | *(from concept key vocabulary)* |
| conditional | *(from concept key vocabulary)* |
| correct | *(from concept key vocabulary)* |
| debug | *(from concept key vocabulary)* |

## Prior knowledge (retrieval plan)

Pupils should already know the following from earlier units:

| Prior knowledge needed | For concept | Description |
|----------------------|-------------|-------------|
| Algorithms | Programming: Sequence, Selection and Repetition | An algorithm is a precise, unambiguous sequence of instructions for solving a problem or accompli... |
| Programming: Sequence, Selection and Repetition | Decomposition and Computational Thinking | All programs are built from three fundamental control structures: sequence (instructions executed... |

---

## Scaffolding and inclusion (Y6)

| Guideline | Detail |
|-----------|--------|
| Reading level | Proficient Reader (Lexile 600–800) |
| Text-to-speech | Available |
| Max sentence length | 25 words |
| Vocabulary | Academic vocabulary expected without scaffolding. Literary vocabulary (connotation, imagery, personification) established. Etymology useful for unfamiliar vocabulary. |
| Scaffolding level | Light |
| Hint tiers | 4 tiers |
| Session length | 25–40 minutes |
| Worked examples | Required — Student-completed faded examples. Text-based. Example solutions shown for comparison after independent attempt. |
| Feedback tone | Intellectual Peer |
| Normalize struggle | Yes |
| Example correct feedback | *Your rhythmic analysis correctly identified the iambic pattern in lines 2 and 4, and you rightly noted the disruption in line 3. The question is: why might Shakespeare have broken the metre there?* |
| Example error feedback | *There is a problem with that interpretation: you suggested the character is happy at the end, but the meter becomes irregular in the final couplet — what might that irregularity signal about their emotional state?* |

---

## Knowledge organiser

**Key terms:**
- Python
- syntax
- variable
- string
- integer
- print
- input
- if
- else
- loop
- indentation

**Core facts (expected standard):**
- **Programming: Sequence, Selection and Repetition**: Combining sequence, selection and repetition to create programs that solve problems or meet a design brief, using variables to store and change data.

---

## Graph context

**Node type:** `ComputingTopicSuggestion` | **Study ID:** `TS-CO-KS2-009`

**Concept IDs:**
- `CO-KS12-C002`: Programming: Sequence, Selection and Repetition (primary)
- `CO-KS12-C003`: Debugging and Logical Reasoning
- `CO-KS12-C006`: Decomposition and Computational Thinking

**Cypher query:**
```cypher
MATCH (ts:ComputingTopicSuggestion {suggestion_id: 'TS-CO-KS2-009'})
  -[:DELIVERS_VIA]->(c:Concept)
  -[:HAS_DIFFICULTY_LEVEL]->(dl)
RETURN c.name, dl.label, dl.description
```

---

*Generated from the UK Curriculum Knowledge Graph — zero LLM generation.*
