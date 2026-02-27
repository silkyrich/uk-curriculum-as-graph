# Design and Technology | Teacher Planner: Electronic Systems: Night Light with Microcontroller
*[TS-DT-KS3-003]*

**Subject:** Design and Technology | **Key Stage:** KS3 | **Year group:** Y8, Y9
**Statutory reference:** understand and use electrical and electronic systems in their products | **Source document:** Design and Technology (KS3) - National Curriculum Programme of Study
**Estimated duration:** 10 lessons | **Status:** Convention

**Planner coverage:** 8/10 expected capabilities surfaced

**Available now:** Curriculum anchor, Concept model, Differentiation data, Thinking lens, Lesson structure, Cross-curricular links, Prior knowledge links, Learner scaffolding
**Still thin/missing:** Vocabulary definitions, Success criteria

---

## Concepts

This study delivers **1 primary concept** and **3 secondary concepts**.

### Primary concept: Embedded Computing and Product Intelligence (DT-KS3-C003)

**Type:** Knowledge | **Teaching weight:** 3/6

Embedded computing refers to the integration of programmable microcontrollers and electronic components into physical products, enabling them to sense their environment, process information and control physical outputs. This creates intelligent, responsive products that adapt their behaviour to conditions and user inputs. At KS3, pupils learn to design and build products with embedded computing, applying programming knowledge from computing to create sensors, input devices, output actuators and control logic within designed products.

**Teaching guidance:** Use accessible microcontroller platforms (micro:bit, Arduino, Raspberry Pi) for embedded computing projects. Design tasks that require products to respond to sensor inputs (temperature, light, sound, proximity, touch) and control physical outputs (motors, LEDs, speakers, displays). Teach pupils to specify the input-process-output logic of their product's intelligence before programming. Connect to the wider world: how is embedded computing used in everyday products (washing machines, smartphones, cars, medical devices)? Evaluate how well the program meets the product's design specification.

**Key vocabulary:** embedded, microcontroller, sensor, actuator, input, output, program, control, logic, condition, feedback, responsive, automation, interface, prototype

**Common misconceptions:** Pupils may see electronics and programming as separate from 'proper' DT making. Framing embedded computing as a component of product design, like any other mechanical or material element, integrates it appropriately. Pupils may find it difficult to specify product behaviour before programming; teaching input-process-output planning as a design step addresses this. The debugging of electronic and software systems can be frustrating; systematic fault-finding strategies build resilience.

#### Differentiation

| Level | What success looks like | Example task | Common errors |
|-------|------------------------|-------------|---------------|
| **Emerging** | Knows that computers can be put inside products and that sensors can detect things like light and temperature, but cannot explain how these components work together. | Name two everyday products that contain a small computer (microcontroller) inside them. | Naming products with screens (like laptops) rather than products with embedded computing; Not explaining what the microcontroller actually does inside the product |
| **Developing** | Can describe the input-process-output model of embedded systems and identify appropriate sensors and actuators for a given design brief. | Design a simple automatic plant watering system. Describe the input, process and output stages. | Confusing input sensors with output actuators; Not explaining the processing logic (the decision the microcontroller makes) |
| **Secure** | Programs microcontrollers to read sensor data and control outputs using conditional logic, and integrates electronic components into physical product designs with appropriate consideration of power, housing and user interface. | Write pseudocode for a night light that turns on automatically when it is dark AND when motion is detected, then turns off after 30 seconds of no motion. | Using OR instead of AND (the light would activate in daylight whenever motion is detected); Not including a timer reset mechanism, causing the light to turn off while someone is still in the room |
| **Mastery** | Designs embedded systems with multiple sensor inputs and feedback loops, evaluates the broader implications of intelligent products, and connects product intelligence to real-world applications such as IoT and automation. | A 'smart' school building could use embedded computing to reduce energy waste. Design a system, explain how it uses feedback, and evaluate one ethical concern. | Describing a simple on/off control rather than a feedback loop with continuous adjustment; Not identifying the privacy implications of occupancy monitoring in schools |

> **Model response (Emerging):** *A washing machine contains a microcontroller that controls the water temperature, drum speed and cycle timing. A microwave oven contains a microcontroller that controls the power level and cooking time based on the buttons you press.*

> **Model response (Developing):** *Input: A soil moisture sensor detects how wet or dry the soil is and sends a signal to the microcontroller. Process: The microcontroller compares the moisture reading to a threshold value. If the soil moisture is below the threshold (too dry), it triggers the output. Output: A small water pump is activated, pumping water from a reservoir to the plant pot. When the moisture sensor detects the soil is wet enough, the microcontroller turns off the pump.*

> **Model response (Secure):** *LOOP FOREVER:
  lightLevel = READ light sensor
  motion = READ PIR motion sensor
  IF lightLevel < 200 AND motion == TRUE THEN
    TURN ON LED
    SET timer = 30 seconds
    WHILE timer > 0:
      motion = READ PIR motion sensor
      IF motion == TRUE THEN
        RESET timer = 30 seconds
      END IF
      WAIT 1 second
      timer = timer - 1
    END WHILE
    TURN OFF LED
  END IF
END LOOP

This uses an AND condition so the light only activates in darkness with motion present. The timer resets each time new motion is detected, keeping the light on while someone is moving in the room.*

> **Model response (Mastery):** *The system would use occupancy sensors (PIR) in each room, temperature sensors, light sensors, and CO2 sensors, all connected to a central microcontroller network. Feedback loop 1 (heating): temperature sensors feed current room temperature to the controller, which compares it to a setpoint. If the room is unoccupied (PIR detects no motion for 10 minutes), the setpoint drops to 15 degrees C to save energy. When occupancy is detected, the setpoint returns to 21 degrees C. The controller adjusts radiator valves continuously — this is a negative feedback loop that maintains the target temperature. Feedback loop 2 (lighting): light sensors measure ambient daylight and adjust artificial lighting to maintain a constant illumination level, dimming when sunlight is strong and brightening when it is dim. CO2 sensors trigger ventilation when levels indicate poor air quality, overriding energy-saving modes because health takes priority. Ethical concern: occupancy data reveals patterns about when and where specific people are in the building. If linked to individual identifiers (through timetabling or ID cards), this becomes surveillance data that could be used to monitor staff productivity or student attendance without their informed consent. The system should be designed to detect occupancy without identifying individuals — using anonymous motion detection rather than personal tracking.*

### Secondary concept: User-Centred Design (DT-KS3-C001)

**Type:** Process | **Teaching weight:** 3/6

User-centred design is a design philosophy and process that places the needs, capabilities, preferences and context of intended users at the centre of every design decision. It involves deep empathy with users, structured research methods (interviews, observation, surveys, prototyping), iterative testing with real users, and continuous refinement based on user feedback. At KS3, pupils develop understanding of user-centred design as a distinct and powerful approach that produces solutions better suited to genuine human needs than solutions derived purely from technical or aesthetic assumptions.

#### Differentiation

| Level | What success looks like | Common errors |
|-------|------------------------|---------------|
| **Emerging** | Recognises that designers should think about who will use a product, but relies on personal assumptions rather than structured research to identify user needs. | Listing features they personally want rather than questions about user needs; Focusing only on appearance rather than functional requirements |
| **Developing** | Can describe user-centred design methods such as interviews and observation, and begins to use them to create a basic design specification, though research may be shallow. | Writing leading questions that assume a solution (e.g., 'Would you like a bigger handle?'); Not explaining how the information gathered would inform specific design decisions |
| **Secure** | Conducts structured user research, develops user personas, translates findings into measurable design criteria, and uses iterative prototyping to test ideas with real users. | Skipping the observation and interview stages and jumping straight to designing based on assumptions; Creating a prototype but not testing it with actual users in the real context of use |
| **Mastery** | Critically evaluates competing user needs and design trade-offs, applies professional design thinking frameworks, and justifies design decisions with reference to user research evidence. | Simply choosing one user group over the other rather than seeking an inclusive solution; Not referencing real-world examples of inclusive design that resolve similar tensions |

### Secondary concept: Materials Science and Properties (DT-KS3-C002)

**Type:** Knowledge | **Teaching weight:** 3/6

Materials science is the study of the properties of materials - physical, mechanical, thermal, electrical, chemical and aesthetic - and how these properties determine the suitability of materials for specific applications. At KS3, pupils develop systematic understanding of the properties of a range of materials including metals, polymers, wood-based materials, ceramics, composites and smart materials. Understanding properties enables pupils to make informed material selection decisions and to understand why materials behave as they do under different conditions and manufacturing processes.

#### Differentiation

| Level | What success looks like | Common errors |
|-------|------------------------|---------------|
| **Emerging** | Can name some materials (wood, metal, plastic) and describe basic properties such as hard, soft or flexible, but struggles to explain why a specific material is chosen for a specific purpose. | Saying 'because metal gets hot' without explaining the concept of thermal conductivity; Not recognising that the choice relates to material properties, not just tradition |
| **Developing** | Understands categories of materials and their general properties, and can select appropriate materials for simple products by matching properties to requirements. | Choosing a material based on personal preference rather than comparing properties against requirements; Not considering that different users might have different protection priorities |
| **Secure** | Systematically evaluates materials against multiple criteria including functional performance, aesthetics, cost, environmental impact and manufacturing compatibility, using a selection matrix approach. | Including only one or two criteria rather than considering multiple requirements simultaneously; Not acknowledging that different weightings of criteria could change the recommendation |
| **Mastery** | Applies advanced materials knowledge including smart materials and composites, evaluates how material properties interact with manufacturing processes, and considers the full lifecycle of material choices. | Focusing only on performance improvements without considering manufacturing constraints and environmental costs; Not recognising that the recyclability difference between metals and composites is a significant sustainability issue |

### Secondary concept: Specialist Making Processes and CAM (DT-KS3-C005)

**Type:** Skill | **Teaching weight:** 3/6

At KS3, making extends beyond hand tool skills to encompass specialist processes — including laser cutting, CNC routing, 3D printing, vacuum forming, heat bending, laminating and computer-aided manufacture (CAM) — that are used in professional design and manufacturing contexts. Understanding which processes are appropriate for specific materials and design outcomes, and developing competence in executing them precisely, is the central challenge of the make domain at KS3. Pupils also develop understanding that making is not a one-pass process but an iterative one: encountering problems during making often requires returning to the design to adapt it.

#### Differentiation

| Level | What success looks like | Common errors |
|-------|------------------------|---------------|
| **Emerging** | Can use basic hand tools safely with guidance and follows step-by-step making instructions, but does not independently select tools or processes for a given task. | Suggesting a wood saw, which would crack the acrylic due to inappropriate tooth pattern; Not mentioning clamping or securing the workpiece before cutting |
| **Developing** | Can select appropriate tools and processes for different materials, understands the link between CAD files and CAM output, and works with reasonable precision. | Using a raster image format (JPEG, PNG) instead of a vector format; Not checking that the design is at actual size (1:1 scale) before sending to the machine |
| **Secure** | Selects and uses specialist tools and CAM processes competently, adapts making approaches when problems arise, and applies quality control checks throughout the making process. | Trying to fix the gap with adhesive rather than diagnosing and correcting the root cause; Not testing the correction on scrap material before committing to a full re-cut |
| **Mastery** | Combines hand and digital manufacturing processes strategically, understands industrial manufacturing contexts, and evaluates when CAM offers genuine advantages over hand making. | Recommending only CNC or only hand making without considering a hybrid approach; Not considering the setup time and cost investment required for CNC production |

---

## Thinking lens: Perspective and Interpretation (primary)

**Key question:** Whose perspective is this, what shapes it, and what might be missing?

**Why this lens fits:** User-centred design is built on the systematic practice of adopting the user's perspective — empathy mapping, user journey analysis and prototype testing with real users all require pupils to interpret the design problem through someone else's lived experience.

**Question stems for KS3:**
- What contextual factors shaped this perspective?
- How does the author's position affect the reliability of this account?
- Whose perspective is missing from this record, and why does that matter?
- How have interpretations of this event changed over time, and what drove those changes?

**Secondary lens:** Structure and Function — Selecting the right material for a complex product and the right specialist process to work it (laser cutting sheet acrylic, CNC routing MDF) requires reasoning about how the material's structure enables or constrains the chosen manufacturing process and the product's eventual function.

---

## Session structure: Design, Make, Evaluate

### Design, Make, Evaluate
The core Design & Technology cycle. Pupils investigate existing products and user needs, design a solution with clear specifications, plan the making process, construct using appropriate materials and techniques, test against the design brief, and evaluate the outcome with suggestions for improvement.

`investigate` → `design` → `plan` → `make` → `test` → `evaluate`

**Assessment:** Design portfolio including investigation findings, annotated design with specifications, making log, test results, and evaluative conclusion comparing outcome to original brief.

**Teacher note:** Use the DESIGN, MAKE AND EVALUATE template: investigate the context, users, and existing solutions before designing. Expect detailed design development with annotation explaining choices of material, construction, and finish. Guide making with attention to precision, quality of finish, and safe use of tools. Demand evaluation against the specification that identifies strengths, weaknesses, and potential improvements.

**KS3 question stems:**
- How have you used your investigation of existing products to inform your design?
- What are the strengths of your chosen materials and construction methods?
- How does the quality of your making compare with your design intentions?
- How would you improve your product based on testing and evaluation?

---

## Design and Technology: Electronic Systems

**Design brief:** Design and make a night light that switches on automatically when the room gets dark. Use a microcontroller, an LDR sensor, and LEDs. The housing must be attractive and functional. Optional: add colour-changing or brightness-adjustment features.

**Materials:** Arduino Nano or micro:bit, breadboard, LDR sensor, LEDs (standard and RGB), resistors (330Ω, 10kΩ), jumper wires, battery pack or USB power, card, acrylic or 3D-printed housing
**Tools:** computer for programming, soldering iron (teacher supervised, optional), wire strippers, pliers, multimeter
**Techniques:** breadboard prototyping, reading sensor values via serial monitor, programming conditional logic (if sensor < threshold, turn on LED), soldering (optional, for permanent circuit), housing design and manufacture
**Safety notes:** Low voltage only (5V max via USB or battery pack). Soldering iron: teacher-supervised, well-ventilated area, safety glasses, soldering station. Never solder battery terminals. Check circuit connections before powering on. LEDs can be bright at close range -- do not look directly into high-brightness LEDs.

**Evaluation criteria:**
- Does the light switch on automatically in darkness?
- Does the threshold level work appropriately?
- Is the housing well-designed and finished?
- Is the code efficient and well-commented?

---

## Why this study matters

A night light that responds to ambient light levels (using an LDR sensor and microcontroller) is the simplest embedded computing project and the natural progression from KS2 simple circuits. Pupils learn that products can sense their environment and respond intelligently -- the core principle of embedded computing. Programming the microcontroller (Arduino or micro:bit) to read sensor input and control LED output teaches input-process-output in a physical context.

---

## Pitfalls to avoid

1. LDR readings fluctuating -- teach threshold values and hysteresis (a dead zone between on and off)
2. LEDs wired without current-limiting resistors -- teach why resistors are essential to prevent burnout
3. Code uploaded but nothing happens -- check wiring before debugging code; hardware faults are more common than software faults

---

## Cross-curricular opportunities

| Link | Subject | Connection | Strength |
|------|---------|------------|----------|
| Energy Transfers and Insulation Investigation | Science | Energy transfers, electrical circuits, light and sensors | Moderate |

---

## Vocabulary word mat

| Term | Meaning |
|------|---------|
| microcontroller | |
| sensor | |
| LDR (light-dependent resistor) | |
| LED | |
| resistor | |
| threshold | |
| input | |
| process | |
| output | |
| embedded system | |
| 3D printing | *(from concept key vocabulary)* |
| CAM | *(from concept key vocabulary)* |
| CNC | *(from concept key vocabulary)* |
| accessibility | *(from concept key vocabulary)* |
| actuator | *(from concept key vocabulary)* |
| adapt | *(from concept key vocabulary)* |
| alloy | *(from concept key vocabulary)* |
| automation | *(from concept key vocabulary)* |
| ceramic | *(from concept key vocabulary)* |
| composite | *(from concept key vocabulary)* |

## Prior knowledge (retrieval plan)

Pupils should already know the following from earlier units:

| Prior knowledge needed | For concept | Description |
|----------------------|-------------|-------------|
| Research-Informed Design | User-Centred Design | At KS2, effective design is grounded in research that identifies the needs, preferences and const... |
| Electrical Systems and Series Circuits | Embedded Computing and Product Intelligence | Electrical systems use the flow of electrical current through components to produce light, sound,... |
| Accurate Making and Material Processing | Specialist Making Processes and CAM | Accurate making refers to the ability to execute practical tasks — measuring, marking out, cuttin... |

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
- microcontroller
- sensor
- LDR (light-dependent resistor)
- LED
- resistor
- threshold
- input
- process
- output
- embedded system

**Core facts (expected standard):**
- **Embedded Computing and Product Intelligence**: Programs microcontrollers to read sensor data and control outputs using conditional logic, and integrates electronic components into physical product designs with appropriate consideration of power, housing and user interface.

---

## Graph context

**Node type:** `DTTopicSuggestion` | **Study ID:** `TS-DT-KS3-003`

**Concept IDs:**
- `DT-KS3-C003`: Embedded Computing and Product Intelligence (primary)
- `DT-KS3-C001`: User-Centred Design
- `DT-KS3-C002`: Materials Science and Properties
- `DT-KS3-C005`: Specialist Making Processes and CAM

**Cypher query:**
```cypher
MATCH (ts:DTTopicSuggestion {suggestion_id: 'TS-DT-KS3-003'})
  -[:DELIVERS_VIA]->(c:Concept)
  -[:HAS_DIFFICULTY_LEVEL]->(dl)
RETURN c.name, dl.label, dl.description
```

---

*Generated from the UK Curriculum Knowledge Graph — zero LLM generation.*
