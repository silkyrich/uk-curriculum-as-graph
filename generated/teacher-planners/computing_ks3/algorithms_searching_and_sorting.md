# Computing | Teacher Planner: Algorithms: Searching and Sorting
*[TS-CO-KS3-002]*

**Subject:** Computing | **Key Stage:** KS3 | **Year group:** Y8, Y9
**Statutory reference:** understand several key algorithms that reflect computational thinking; use logical reasoning to compare the utility of alternative algorithms for the same problem | **Source document:** Computing (KS3/KS4) - National Curriculum Programme of Study
**Estimated duration:** 8 lessons | **Status:** Mandatory

**Planner coverage:** 7/10 expected capabilities surfaced

**Available now:** Curriculum anchor, Concept model, Differentiation data, Thinking lens, Lesson structure, Prior knowledge links, Learner scaffolding
**Still thin/missing:** Cross-curricular links, Vocabulary definitions, Success criteria

---

## Concepts

This study delivers **1 primary concept** and **0 secondary concepts**.

### Primary concept: Algorithms: Sorting, Searching and Complexity (CO-KS34-C001)

**Type:** Knowledge | **Teaching weight:** 3/6

Classic algorithms for sorting (bubble sort, merge sort, quick sort) and searching (linear search, binary search) represent fundamental computational problems with well-understood solutions of different efficiencies. Algorithm complexity - how the time or space required by an algorithm grows as the input size grows - is expressed using Big O notation (O(n), O(n log n), O(n^2)). Understanding that different algorithms solving the same problem have different performance characteristics, and that the choice of algorithm matters at scale, is a key insight of computer science. At KS3, pupils study these algorithms, understand how they work and begin to compare their relative efficiency.

**Teaching guidance:** Implement sorting and searching algorithms in code and trace their execution with small data sets. Use physical activities (sorting cards, searching for a name in a list) to make the algorithms tangible before coding. Compare the steps required by linear and binary search for different list sizes to develop intuitive understanding of efficiency. Trace merge sort recursively to understand divide-and-conquer approaches. Connect to real applications: how does a database search work? Why does Google search so quickly? Introduce Big O notation as a way of expressing relative efficiency.

**Key vocabulary:** algorithm, sort, search, bubble sort, merge sort, binary search, linear search, efficiency, complexity, Big O, trace, comparison, swap, iteration, recursion

**Common misconceptions:** Pupils may assume the algorithm they first learned is the best for all cases. Exploring performance with different input sizes and orders demonstrates that no single algorithm is always optimal. Binary search's requirement for a sorted list is often overlooked; understanding the preconditions of an algorithm is part of understanding the algorithm. Tracing recursive algorithms like merge sort can be confusing; explicit tree diagrams that show recursive calls make the structure visible.

#### Differentiation

| Level | What success looks like | Example task | Common errors |
|-------|------------------------|-------------|---------------|
| **Emerging** | Understands that algorithms are step-by-step instructions for solving a problem, and can trace through a simple algorithm with small inputs, but cannot compare algorithms or explain efficiency. | Here is a list of 5 numbers: [8, 3, 5, 1, 9]. Trace through a bubble sort, showing the list after each pass. | Not comparing adjacent pairs systematically, skipping some comparisons; Stopping after one pass and declaring the list sorted when it is not |
| **Developing** | Can explain how several sorting and searching algorithms work, and recognises that different algorithms solve the same problem with different efficiency, though cannot yet quantify this using Big O notation. | Explain how binary search works and why it is faster than linear search for a sorted list of 1000 items. | Forgetting to mention that binary search requires a sorted list as a precondition; Saying binary search 'splits the list in two' without explaining which half is discarded and why |
| **Secure** | Implements sorting and searching algorithms in code, uses Big O notation to describe algorithmic complexity, and selects appropriate algorithms for given problem constraints. | Compare bubble sort and merge sort in terms of their time complexity. For a list of 1 million items, explain which you would choose and why. | Stating the Big O complexity without explaining what it means in practical terms; Not mentioning the space complexity trade-off (merge sort uses more memory than bubble sort) |
| **Mastery** | Analyses algorithmic trade-offs in real-world contexts, understands that no single algorithm is optimal for all situations, and evaluates algorithm choice based on input characteristics, constraints and requirements. | A hospital database needs to search patient records in real time during emergencies. The database contains 50 million records. Evaluate the algorithm and data structure choices that would make this possible. | Recommending a single algorithm without considering the different types of queries the system needs to support; Not recognising that real-world systems combine multiple algorithms and data structures |

> **Model response (Emerging):** *Pass 1: Compare 8,3 → swap → [3,8,5,1,9]. Compare 8,5 → swap → [3,5,8,1,9]. Compare 8,1 → swap → [3,5,1,8,9]. Compare 8,9 → no swap → [3,5,1,8,9]. Pass 2: Compare 3,5 → no swap. Compare 5,1 → swap → [3,1,5,8,9]. Compare 5,8 → no swap. Compare 8,9 → no swap → [3,1,5,8,9]. Pass 3: Compare 3,1 → swap → [1,3,5,8,9]. Remaining comparisons → no swaps. List is now sorted.*

> **Model response (Developing):** *Linear search checks each item from the beginning until it finds the target — in the worst case, it checks all 1000 items. Binary search starts in the middle of the sorted list, checks if the target is higher or lower, then eliminates half the remaining items. It repeats this halving process. For 1000 items: first check eliminates 500, second eliminates 250, then 125, 63, 32, 16, 8, 4, 2, 1 — so binary search needs at most about 10 comparisons instead of 1000. Binary search requires the list to be sorted first, which is a precondition that linear search does not need.*

> **Model response (Secure):** *Bubble sort has time complexity O(n squared): for each of n items, it may need to make up to n comparisons, giving n times n operations. For 1 million items, this is approximately 1 trillion operations — far too slow for practical use. Merge sort has time complexity O(n log n): it repeatedly divides the list in half (log n divisions) and merges the halves (n operations per merge level). For 1 million items, log base 2 of 1 million is approximately 20, so merge sort needs about 20 million operations — roughly 50,000 times faster than bubble sort. I would choose merge sort because O(n log n) scales far better than O(n squared). However, merge sort uses additional memory (to store the split sublists), so if memory is extremely limited, I might consider in-place algorithms like quicksort.*

> **Model response (Mastery):** *Linear search at O(n) would require checking up to 50 million records — unacceptable for emergency response. Binary search at O(log n) would need about 26 comparisons, which is fast enough, but requires the data to be sorted. For a database that changes frequently (new patients, updated records), maintaining sort order is costly. A better approach is a hash table: using the patient's NHS number as a key, a hash function maps it directly to a memory location in O(1) average time — effectively instant lookup regardless of database size. However, hash tables have weaknesses: they do not support range queries (find all patients aged 30-40) and hash collisions degrade performance. A balanced binary search tree (e.g., B-tree, used in real database indexes) offers O(log n) search with efficient insertion and deletion, and supports range queries. In practice, hospital databases use B-tree indexes on key fields (NHS number, name, date of birth) combined with hash indexes for exact-match lookups. The choice depends on the query type: exact match (hash), range (B-tree), or full-text (inverted index). No single algorithm covers all needs.*

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

**Programming paradigm:** Text Based
**Software/tool:** Python
**Computational concepts:** algorithm, efficiency, comparison
**Abstraction level:** Symbolic
**Themes:** algorithms, computational thinking, efficiency

---

## Why this study matters

The NC specifically requires pupils to understand key algorithms including sorting and searching. Linear search and binary search demonstrate that algorithm choice affects efficiency dramatically (binary search is O(log n) vs O(n)). Bubble sort, insertion sort and merge sort show that the same problem (ordering data) can be solved in fundamentally different ways with different performance characteristics. Unplugged activities (sorting pupils by height, searching for a card) make abstract algorithms concrete before implementing in code.

---

## Pitfalls to avoid

1. Teaching algorithms as abstract flowcharts without physical activity -- pupils must sort real objects first
2. Not comparing efficiency -- the whole point is that different algorithms perform differently; time them
3. Pupils memorising steps without understanding why -- ask 'what is this algorithm doing at each step and why?'

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
| algorithm | |
| linear search | |
| binary search | |
| bubble sort | |
| insertion sort | |
| merge sort | |
| efficiency | |
| comparison | |
| swap | |
| iteration | |
| recursion | |
| Big O notation | |
| Big O | *(from concept key vocabulary)* |
| complexity | *(from concept key vocabulary)* |
| search | *(from concept key vocabulary)* |
| sort | *(from concept key vocabulary)* |
| trace | *(from concept key vocabulary)* |

## Prior knowledge (retrieval plan)

Pupils should already know the following from earlier units:

| Prior knowledge needed | For concept | Description |
|----------------------|-------------|-------------|
| Algorithms | Algorithms: Sorting, Searching and Complexity | An algorithm is a precise, unambiguous sequence of instructions for solving a problem or accompli... |

---

## Scaffolding and inclusion (Y8)

| Guideline | Detail |
|-----------|--------|
| Reading level | Established Secondary Reader (Lexile 850–1100) |
| Text-to-speech | Available |
| Vocabulary | Specialist vocabulary in each discipline. Metalanguage about text (e.g., 'the author's implicit bias') appropriate. |
| Scaffolding level | Minimal |
| Hint tiers | 3 tiers |
| Session length | 30–45 minutes |
| Feedback tone | Academic Critical |
| Normalize struggle | Yes |
| Example correct feedback | *Your method is correct and your reasoning is sound. The extension question: does this generalise? Try with a different case.* |
| Example error feedback | *Your approach identifies the right method but fails at step 3. The error is [specific]. A complete answer would [what is required].* |

---

## Knowledge organiser

**Key terms:**
- algorithm
- linear search
- binary search
- bubble sort
- insertion sort
- merge sort
- efficiency
- comparison
- swap
- iteration
- recursion
- Big O notation

**Core facts (expected standard):**
- **Algorithms: Sorting, Searching and Complexity**: Implements sorting and searching algorithms in code, uses Big O notation to describe algorithmic complexity, and selects appropriate algorithms for given problem constraints.

---

## Graph context

**Node type:** `ComputingTopicSuggestion` | **Study ID:** `TS-CO-KS3-002`

**Concept IDs:**
- `CO-KS34-C001`: Algorithms: Sorting, Searching and Complexity (primary)

**Cypher query:**
```cypher
MATCH (ts:ComputingTopicSuggestion {suggestion_id: 'TS-CO-KS3-002'})
  -[:DELIVERS_VIA]->(c:Concept)
  -[:HAS_DIFFICULTY_LEVEL]->(dl)
RETURN c.name, dl.label, dl.description
```

---

*Generated from the UK Curriculum Knowledge Graph — zero LLM generation.*
