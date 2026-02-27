# Computing | Teacher Planner: BeeBot Programming
*[TS-CO-KS1-002]*

**Subject:** Computing | **Key Stage:** KS1 | **Year group:** Y1
**Statutory reference:** create and debug simple programs | **Source document:** Computing (KS1/KS2) - National Curriculum Programme of Study
**Estimated duration:** 4 lessons | **Status:** Convention

**Planner coverage:** 7/10 expected capabilities surfaced

**Available now:** Curriculum anchor, Concept model, Differentiation data, Thinking lens, Lesson structure, Prior knowledge links, Learner scaffolding
**Still thin/missing:** Cross-curricular links, Vocabulary definitions, Success criteria

---

## Concepts

This study delivers **2 primary concepts** and **0 secondary concepts**.

### Primary concept: Algorithms (CO-KS12-C001)

**Type:** Knowledge | **Teaching weight:** 1/6

An algorithm is a precise, unambiguous sequence of instructions for solving a problem or accomplishing a task. Algorithms are more general than programs: an algorithm describes what needs to be done, while a program is a specific implementation of an algorithm in a particular programming language. Algorithms must be correct (they produce the right output), precise (each step is unambiguous), and finite (they eventually reach a conclusion). At KS1 and KS2, pupils learn to write and recognise algorithms, understand their properties, and implement them as programs.

**Teaching guidance:** Begin with unplugged algorithm activities before moving to digital programming. Teach pupils to write step-by-step instructions for everyday tasks (making a sandwich, brushing teeth) to illustrate the precision required in algorithms. Use robot or turtle-following activities where pupils give instructions and observe the results of ambiguity or incorrect ordering. Discuss what happens when an algorithm has an error: the program does what we said, not what we meant. Introduce the idea of testing algorithms with different inputs to check they work in all cases.

**Key vocabulary:** algorithm, instruction, sequence, step, precise, unambiguous, input, output, process, program, implement, order, correct, test, debug

**Common misconceptions:** Pupils may think that an algorithm is the same as a program; clarifying that an algorithm is the idea or plan, while a program is the specific coded implementation, is important. Pupils may not appreciate that algorithms need to be unambiguous; activities where deliberately ambiguous instructions lead to unexpected results make this vivid. The idea that a computer does exactly what it is told, rather than what we intended, is a fundamental shift in thinking that needs explicit attention.

#### Differentiation

| Level | What success looks like | Example task | Common errors |
|-------|------------------------|-------------|---------------|
| **Entry** | Following a set of step-by-step instructions (an algorithm) to complete a task, understanding that the order matters. | Follow these instructions to draw a house: 1. Draw a square. 2. Draw a triangle on top. 3. Draw a rectangle door. 4. Draw two square windows. Did the order matter? | Skipping steps or doing them out of order; Not understanding that algorithms must be followed precisely |
| **Developing** | Writing simple algorithms as a sequence of instructions for a familiar task, identifying when instructions are ambiguous or incomplete. | Write instructions for making a jam sandwich that a robot could follow exactly. Test your instructions with a partner. | Writing instructions that are too vague for a computer to follow precisely; Assuming the reader knows things that are not explicitly stated |
| **Expected** | Designing algorithms to solve problems, comparing different approaches and evaluating their efficiency. | Write two different algorithms for sorting five numbered cards into order. Which is more efficient? | Writing algorithms that only work for the specific example, not the general case; Not being able to trace through an algorithm step by step to check it works |
| **Greater Depth** | Analysing the efficiency of algorithms, predicting how they perform with larger inputs, and explaining the concepts of algorithm design to others. | If Algorithm 1 (checking pairs) takes 10 comparisons to sort 5 cards, roughly how many might it take for 10 cards? Why does it take longer? | Assuming the time doubles when the input doubles (it often grows faster); Not connecting algorithm efficiency to real-world computing problems |

> **Model response (Entry):** *I followed each step in order and drew the house. The order matters because I needed the square first to know where to put the triangle roof on top.*

> **Model response (Developing):** *1. Pick up the bread bag. 2. Take out two slices. 3. Put them on the plate. 4. Pick up the knife. 5. Open the jam jar. 6. Put the knife in the jam. 7. Spread jam on one slice. 8. Put the other slice on top. When my partner tested them, they asked 'which side up?' for step 3 — I needed to add 'flat side up'.*

> **Model response (Expected):** *Algorithm 1 (Checking pairs): Compare each pair of cards from left to right. If they are in the wrong order, swap them. Repeat until no swaps are needed. Algorithm 2 (Finding smallest): Find the smallest card and put it first. Find the next smallest and put it second. Continue until all are sorted. Algorithm 2 requires fewer comparisons for this small set, making it more efficient. But Algorithm 1 is simpler to understand.*

> **Model response (Greater Depth):** *For 10 cards, it could take many more comparisons — maybe around 45 or more — because each pass through the list compares 9 pairs, and you might need many passes. The number of comparisons grows much faster than the number of cards. This is why computer scientists care about efficiency — a slow algorithm that works fine for 5 items might be too slow for 1000 items.*

### Primary concept: Debugging and Logical Reasoning (CO-KS12-C003)

**Type:** Skill | **Teaching weight:** 2/6

Debugging is the process of finding and fixing errors in programs. It requires logical reasoning: the ability to read code, mentally execute it step by step, identify where the actual behaviour diverges from the expected behaviour, and determine what change will fix the error. Logical reasoning about programs is also required to predict what a program will do before running it. At KS1 and KS2, developing debugging skills and the habit of logical, systematic thinking about code is as important as learning to write new code.

**Teaching guidance:** Model debugging strategies explicitly: read the error message (if any), read the code, trace through it step by step, check each part's contribution, hypothesise a fix, test. Give pupils deliberately buggy programs and ask them to identify and fix the errors before writing their own. Normalise bugs: frame them as a necessary part of programming rather than a sign of failure. Develop pupils' metacognitive awareness by asking them to articulate their reasoning when debugging. Use pair programming as a debugging strategy: talking through code with a partner helps identify errors.

**Key vocabulary:** debug, error, bug, syntax error, logic error, trace, execute, predict, fix, test, check, correct, output, expected, actual, reasoning

**Common misconceptions:** Pupils may feel that having errors in their code means they have failed. Reframing debugging as a normal and creative part of programming is essential. Pupils may try random changes hoping something will fix a bug rather than reasoning about the cause; teaching systematic debugging strategies builds more effective habits. Some pupils struggle to 'read' code as an execution trace; explicit tracing activities develop this skill.

#### Differentiation

| Level | What success looks like | Example task | Common errors |
|-------|------------------------|-------------|---------------|
| **Entry** | Identifying that a program is not working as expected and finding an obvious error by comparing the output with the intended result. | This program should make the sprite draw a square, but it draws a triangle. Look at the code — what is wrong? | Rewriting the whole program instead of finding and fixing the specific error; Not being able to describe what the program should do versus what it actually does |
| **Developing** | Using logical reasoning to trace through a program step by step, predicting the output and identifying where it goes wrong. | Trace through this program and predict what it will output: set x to 5, repeat 3 times (set x to x + 2, say x). | Not updating the variable value between iterations; Tracing through only the first iteration and guessing the rest |
| **Expected** | Systematically debugging programs by testing, identifying errors, hypothesising causes, making changes and retesting. | This game program has two bugs: the score doesn't increase when you collect a coin, and the character can walk through walls. Find and fix both bugs. | Fixing one bug without retesting to check it doesn't cause another; Changing multiple things at once and not knowing which change fixed the problem |
| **Greater Depth** | Applying debugging strategies systematically, including using test data, print statements for tracing, and explaining why certain types of bugs are harder to find. | A classmate's sorting program works for most lists but gives wrong results for some. How would you systematically find the bug? | Only testing with one type of input data; Not testing edge cases (empty lists, duplicates, already-sorted data) |

> **Model response (Entry):** *The loop only repeats 3 times instead of 4. A square has 4 sides, so I need to change the repeat from 3 to 4.*

> **Model response (Developing):** *Start: x = 5. First time through the loop: x becomes 5 + 2 = 7, it says 7. Second time: x becomes 7 + 2 = 9, it says 9. Third time: x becomes 9 + 2 = 11, it says 11. The program will say 7, then 9, then 11.*

> **Model response (Expected):** *Bug 1: The score variable is being set to 1 each time instead of increased by 1. I changed 'set score to 1' to 'change score by 1'. Bug 2: The wall collision check uses 'if touching wall colour' but the wall colour in the code doesn't match the actual wall colour on the screen. I used the colour picker to get the exact colour. After fixing both, I tested by collecting three coins (score went 1, 2, 3) and walking into a wall (character stopped).*

> **Model response (Greater Depth):** *I would test with several types of input: a sorted list, a reversed list, a list with duplicates, a list with one item, and an empty list. I would add print statements inside the loop to show the state of the list after each step, so I can see where it goes wrong. I would trace the failing case step by step. Some bugs only appear with specific inputs — these are harder to find because the program seems to work most of the time.*

---

## Thinking lens: Cause and Effect (primary)

**Key question:** What caused this to happen, and how do we know?

**Why this lens fits:** Debugging requires pupils to trace how each instruction in a program causes a specific change in output — identifying which instruction is the cause of the unexpected behaviour is the core cognitive act.

**Question stems for KS1:**
- What made that happen?
- What will happen if...?
- Why did it change?
- Can you finish: it happened because...?

**Secondary lens:** Patterns — Logical reasoning about program behaviour involves recognising that the same sequence of instructions will always produce the same result, establishing the notion of predictable, repeatable computational patterns.

---

## Session structure: Practical Application

### Practical Application
A hands-on sequence where pupils apply knowledge and skills to solve a practical problem or create a functional outcome. Begins with a real-world context, builds skills through rehearsal, guides design or planning, supports making or problem-solving, and concludes with evaluation against success criteria.

`context` → `skill_rehearsal` → `design` → `make_or_solve` → `evaluate`

**Assessment:** Practical outcome (solution, product, program) evaluated against defined success criteria, with written or verbal explanation of the process and decisions made.

---

## Computing focus

**Programming paradigm:** Unplugged
**Software/tool:** BeeBot
**Computational concepts:** algorithm, sequence, debugging
**Abstraction level:** Physical
**Themes:** programming, directional language, debugging

---

## Why this study matters

BeeBots (or similar floor robots) bridge the gap between unplugged algorithms and screen-based programming. Pupils program the robot to navigate a floor mat by pressing directional buttons (forward, back, left, right). The physical movement of the robot provides immediate, visible feedback -- did it go where you intended? Debugging means watching where it went wrong and adjusting the sequence. The tangible, spatial nature of floor robots matches KS1 developmental stage.

---

## Pitfalls to avoid

1. Pupils pressing GO before the full sequence is entered -- teach plan-first, execute-second
2. Confusion about left and right from the robot's perspective -- stand behind the robot to match orientation
3. Not clearing the previous program -- teach the clear button habit

---

## Computational thinking skills (KS1)

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
| program | |
| instruction | |
| forward | |
| backward | |
| left | |
| right | |
| debug | |
| sequence | |
| predict | |
| actual | *(from concept key vocabulary)* |
| algorithm | *(from concept key vocabulary)* |
| bug | *(from concept key vocabulary)* |
| check | *(from concept key vocabulary)* |
| correct | *(from concept key vocabulary)* |
| error | *(from concept key vocabulary)* |
| execute | *(from concept key vocabulary)* |
| expected | *(from concept key vocabulary)* |
| fix | *(from concept key vocabulary)* |
| implement | *(from concept key vocabulary)* |

## Prior knowledge (retrieval plan)

Pupils should already know the following from earlier units:

| Prior knowledge needed | For concept | Description |
|----------------------|-------------|-------------|
| Algorithms | Debugging and Logical Reasoning | An algorithm is a precise, unambiguous sequence of instructions for solving a problem or accompli... |

---

## Scaffolding and inclusion (Y1)

| Guideline | Detail |
|-----------|--------|
| Reading level | Pre-reader / Emergent |
| Text-to-speech | Required |
| Max sentence length | 8 words |
| Vocabulary | Concrete nouns and action verbs only. No abstract concepts without physical anchor. Examples: dog, apple, jump, big, one more. |
| Scaffolding level | Maximum |
| Hint tiers | 2 tiers |
| Session length | 5–12 minutes |
| Worked examples | Required — Animated, narrated walkthrough with no text. Character models the thinking aloud. |
| Feedback tone | Warm Nurturing |
| Normalize struggle | Yes |
| Example correct feedback | *The frog jumped exactly four spaces — you counted perfectly!* |
| Example error feedback | *Oh, let us count again together! [animation demonstrates]* |

---

## Knowledge organiser

**Key terms:**
- program
- instruction
- forward
- backward
- left
- right
- debug
- sequence
- predict

**Core facts (expected standard):**
- **Algorithms**: Designing algorithms to solve problems, comparing different approaches and evaluating their efficiency.
- **Debugging and Logical Reasoning**: Systematically debugging programs by testing, identifying errors, hypothesising causes, making changes and retesting.

---

## Graph context

**Node type:** `ComputingTopicSuggestion` | **Study ID:** `TS-CO-KS1-002`

**Concept IDs:**
- `CO-KS12-C001`: Algorithms (primary)
- `CO-KS12-C003`: Debugging and Logical Reasoning (primary)

**Cypher query:**
```cypher
MATCH (ts:ComputingTopicSuggestion {suggestion_id: 'TS-CO-KS1-002'})
  -[:DELIVERS_VIA]->(c:Concept)
  -[:HAS_DIFFICULTY_LEVEL]->(dl)
RETURN c.name, dl.label, dl.description
```

---

*Generated from the UK Curriculum Knowledge Graph — zero LLM generation.*
