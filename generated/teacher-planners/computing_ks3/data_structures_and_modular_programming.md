# Computing | Teacher Planner: Data Structures and Modular Programming
*[TS-CO-KS3-005]*

**Subject:** Computing | **Key Stage:** KS3 | **Year group:** Y8, Y9
**Statutory reference:** make appropriate use of data structures | **Source document:** Computing (KS3/KS4) - National Curriculum Programme of Study
**Estimated duration:** 10 lessons | **Status:** Convention

**Planner coverage:** 7/10 expected capabilities surfaced

**Available now:** Curriculum anchor, Concept model, Differentiation data, Thinking lens, Lesson structure, Prior knowledge links, Learner scaffolding
**Still thin/missing:** Cross-curricular links, Vocabulary definitions, Success criteria

---

## Concepts

This study delivers **1 primary concept** and **1 secondary concept**.

### Primary concept: Data Structures and Modular Programming (CO-KS34-C003)

**Type:** Skill | **Teaching weight:** 3/6

Data structures are ways of organising and storing data in a program so that it can be accessed and modified efficiently. Common data structures include arrays (indexed collections of items of the same type), lists (dynamic ordered collections), stacks (last-in, first-out collections), queues (first-in, first-out collections), and dictionaries/hash maps (key-value pair collections). Modular programming organises code into self-contained procedures or functions, each responsible for a specific task. This improves readability, enables reuse and simplifies debugging. At KS3, pupils learn to choose appropriate data structures and to design modular programs using procedures and functions.

**Teaching guidance:** Introduce data structures through problems they naturally solve: arrays for storing a list of scores, a stack for undo operations, a queue for a print job buffer. Teach pupils to choose data structures based on the operations required. Model modular program design: identify distinct tasks, write a function for each, test functions independently. Practice refactoring flat programs into modular ones. Connect data structures to real applications: how does a social media platform store users' friend lists? Develop understanding of the difference between accessing an element by index and searching through a list.

**Key vocabulary:** data structure, array, list, stack, queue, dictionary, record, index, procedure, function, parameter, return, modular, reuse, encapsulate

**Common misconceptions:** Pupils may not see the need for data structures beyond simple variables, especially in small programs. Showing how programs that use appropriate data structures scale to larger problems motivates their use. The difference between passing data to a function by value and by reference is a subtle but important concept that affects program behaviour. Functions that return values are often confused with procedures that only produce side effects; consistent terminology and practice develops clarity.

#### Differentiation

| Level | What success looks like | Example task | Common errors |
|-------|------------------------|-------------|---------------|
| **Emerging** | Can write simple programs using variables, sequence and basic selection (if/else), but does not use data structures beyond single variables or organise code into procedures or functions. | Write a program that asks the user for their age and tells them whether they are old enough to vote (18 or over). | Forgetting to convert the input to an integer, causing a comparison error with a string; Using a single equals sign (=) for comparison instead of double equals (==) or >=  |
| **Developing** | Uses arrays/lists to store collections of data, writes programs with loops that process data structures, and begins to organise code into procedures or functions for clarity. | Write a program that stores 5 test scores in a list, calculates the average, and prints which scores are above the average. | Calculating the average by dividing by a hardcoded number (5) instead of using len(scores); Using a single loop to both calculate the total and compare to the average (the average is not yet known during the first loop) |
| **Secure** | Chooses appropriate data structures for different problems, writes modular programs using functions with parameters and return values, and debugs programs systematically. | Write a function called 'find_max' that takes a list of numbers as a parameter and returns the largest number, without using the built-in max() function. | Initialising 'largest' to 0 instead of the first element, which fails for lists of negative numbers; Not handling edge cases such as an empty list or a list with one element |
| **Mastery** | Designs programs using appropriate data structures (stacks, queues, dictionaries), writes well-structured modular code with clear documentation, and analyses the efficiency and robustness of their solutions. | Design a program for a library book-borrowing system. It should track which books are available, allow borrowing and returning, and use appropriate data structures. Justify your data structure choices. | Using a list instead of a dictionary, requiring linear search to find a specific book; Not including input validation (what if the ISBN does not exist? what if the book is already borrowed?) |

> **Model response (Emerging):** *age = int(input('Enter your age: '))
if age >= 18:
    print('You are old enough to vote.')
else:
    print('You are not old enough to vote yet.')*

> **Model response (Developing):** *scores = [72, 85, 63, 91, 78]
total = 0
for score in scores:
    total = total + score
average = total / len(scores)
print('Average:', average)
for score in scores:
    if score > average:
        print(score, 'is above average')*

> **Model response (Secure):** *def find_max(numbers):
    if len(numbers) == 0:
        return None
    largest = numbers[0]
    for number in numbers[1:]:
        if number > largest:
            largest = number
    return largest

# Test
print(find_max([3, 7, 2, 9, 5]))  # Should print 9
print(find_max([-5, -1, -8]))     # Should print -1
print(find_max([42]))             # Should print 42
print(find_max([]))               # Should print None*

> **Model response (Mastery):** *I would use a dictionary where each key is the book's ISBN and the value is another dictionary containing title, author and status (available/borrowed/borrower_name).

library = {}

def add_book(isbn, title, author):
    library[isbn] = {'title': title, 'author': author, 'status': 'available', 'borrower': None}

def borrow_book(isbn, borrower):
    if isbn not in library:
        return 'Book not found'
    if library[isbn]['status'] == 'borrowed':
        return f'Already borrowed by {library[isbn]["borrower"]}'
    library[isbn]['status'] = 'borrowed'
    library[isbn]['borrower'] = borrower
    return f'{library[isbn]["title"]} borrowed by {borrower}'

def return_book(isbn):
    if isbn not in library or library[isbn]['status'] == 'available':
        return 'Error: book not currently borrowed'
    library[isbn]['status'] = 'available'
    library[isbn]['borrower'] = None
    return f'{library[isbn]["title"]} returned'

Justification: A dictionary provides O(1) average lookup by ISBN — essential for a system that may contain thousands of books. Using a list would require O(n) linear search. The nested dictionary for each book groups related data logically. Functions are modular: each handles one operation with input validation and clear return messages.*

### Secondary concept: Algorithms: Sorting, Searching and Complexity (CO-KS34-C001)

**Type:** Knowledge | **Teaching weight:** 3/6

Classic algorithms for sorting (bubble sort, merge sort, quick sort) and searching (linear search, binary search) represent fundamental computational problems with well-understood solutions of different efficiencies. Algorithm complexity - how the time or space required by an algorithm grows as the input size grows - is expressed using Big O notation (O(n), O(n log n), O(n^2)). Understanding that different algorithms solving the same problem have different performance characteristics, and that the choice of algorithm matters at scale, is a key insight of computer science. At KS3, pupils study these algorithms, understand how they work and begin to compare their relative efficiency.

#### Differentiation

| Level | What success looks like | Common errors |
|-------|------------------------|---------------|
| **Emerging** | Understands that algorithms are step-by-step instructions for solving a problem, and can trace through a simple algorithm with small inputs, but cannot compare algorithms or explain efficiency. | Not comparing adjacent pairs systematically, skipping some comparisons; Stopping after one pass and declaring the list sorted when it is not |
| **Developing** | Can explain how several sorting and searching algorithms work, and recognises that different algorithms solve the same problem with different efficiency, though cannot yet quantify this using Big O notation. | Forgetting to mention that binary search requires a sorted list as a precondition; Saying binary search 'splits the list in two' without explaining which half is discarded and why |
| **Secure** | Implements sorting and searching algorithms in code, uses Big O notation to describe algorithmic complexity, and selects appropriate algorithms for given problem constraints. | Stating the Big O complexity without explaining what it means in practical terms; Not mentioning the space complexity trade-off (merge sort uses more memory than bubble sort) |
| **Mastery** | Analyses algorithmic trade-offs in real-world contexts, understands that no single algorithm is optimal for all situations, and evaluates algorithm choice based on input characteristics, constraints and requirements. | Recommending a single algorithm without considering the different types of queries the system needs to support; Not recognising that real-world systems combine multiple algorithms and data structures |

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
**Computational concepts:** data structure, abstraction, decomposition
**Abstraction level:** Symbolic
**Themes:** data structures, modular programming, software design

---

## Why this study matters

After learning basic programming, pupils need to organise data and code. Data structures (lists/arrays, dictionaries, records) teach that choosing how to store data affects how easily it can be processed. Modular programming (functions and procedures) teaches that code should be organised into reusable, testable blocks. A project like a student database or quiz system naturally requires both data structures and modular code, making the need for these concepts genuine rather than manufactured.

---

## Pitfalls to avoid

1. Teaching data structures in isolation from a project -- pupils need a reason to store data in a list, not just an exercise
2. Functions taught as 'mini-programs' without explaining parameters and return values -- these are the interface
3. Not testing modular code independently -- teach that each function should be tested separately before integration

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
| list | |
| array | |
| dictionary | |
| record | |
| index | |
| function | |
| procedure | |
| parameter | |
| return value | |
| scope | |
| local variable | |
| global variable | |
| modular | |
| Big O | *(from concept key vocabulary)* |
| algorithm | *(from concept key vocabulary)* |
| binary search | *(from concept key vocabulary)* |
| bubble sort | *(from concept key vocabulary)* |
| comparison | *(from concept key vocabulary)* |
| complexity | *(from concept key vocabulary)* |
| data structure | *(from concept key vocabulary)* |
| efficiency | *(from concept key vocabulary)* |
| encapsulate | *(from concept key vocabulary)* |
| iteration | *(from concept key vocabulary)* |

## Prior knowledge (retrieval plan)

Pupils should already know the following from earlier units:

| Prior knowledge needed | For concept | Description |
|----------------------|-------------|-------------|
| Algorithms | Algorithms: Sorting, Searching and Complexity | An algorithm is a precise, unambiguous sequence of instructions for solving a problem or accompli... |
| Programming: Sequence, Selection and Repetition | Data Structures and Modular Programming | All programs are built from three fundamental control structures: sequence (instructions executed... |

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
- list
- array
- dictionary
- record
- index
- function
- procedure
- parameter
- return value
- scope
- local variable
- global variable
- modular

**Core facts (expected standard):**
- **Data Structures and Modular Programming**: Chooses appropriate data structures for different problems, writes modular programs using functions with parameters and return values, and debugs programs systematically.

---

## Graph context

**Node type:** `ComputingTopicSuggestion` | **Study ID:** `TS-CO-KS3-005`

**Concept IDs:**
- `CO-KS34-C003`: Data Structures and Modular Programming (primary)
- `CO-KS34-C001`: Algorithms: Sorting, Searching and Complexity

**Cypher query:**
```cypher
MATCH (ts:ComputingTopicSuggestion {suggestion_id: 'TS-CO-KS3-005'})
  -[:DELIVERS_VIA]->(c:Concept)
  -[:HAS_DIFFICULTY_LEVEL]->(dl)
RETURN c.name, dl.label, dl.description
```

---

*Generated from the UK Curriculum Knowledge Graph — zero LLM generation.*
