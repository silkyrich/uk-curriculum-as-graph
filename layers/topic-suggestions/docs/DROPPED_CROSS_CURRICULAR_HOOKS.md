# Dropped Cross-Curricular Hooks

Documents all cross-curricular hooks that were dropped during the cleanup from `cross_curricular_hooks` (JSON blobs with free-text strings or `{subject, hook, strength}` dicts) to `cross_curricular_links` (proper relationship targets with a specific `target_id` pointing to an existing study/unit/enquiry node in the graph).

## Summary

| Metric | Count |
|--------|-------|
| Total hooks processed | 463 |
| Matched (became `cross_curricular_links`) | 183 |
| **Dropped (documented below)** | **280** |
| Data files processed | 18 |

### Drop reasons at a glance

| Reason | Count |
|--------|-------|
| No study nodes for Mathematics | ~72 |
| No study nodes for PSHE | ~35 |
| No KS1 Science enquiry nodes | ~28 |
| No KS3 English unit nodes | ~16 |
| No RS/RE study nodes at matching specificity | ~13 |
| No KS3 Art/DT/Music study nodes | ~6 |
| No study nodes for Drama | 5 |
| No study nodes for Physical Education | 3 |
| No study nodes for Languages | 2 |
| No KS2 Citizenship study nodes | 1 |
| Too vague / no matching target node | ~99 |

---

## 1. No study nodes for target subject

### 1a. Mathematics (~72 hooks)

Maths has only reference nodes in the graph (MathsManipulative, MathsRepresentation, MathsContext, ReasoningPromptType) -- not study/unit nodes. All hooks targeting Maths were dropped because there is no `target_id` to point to.

| Source ID | Source Name | Hook Text |
|-----------|------------|-----------|
| HS-KS2-002 | Roman Britain | Roman numerals; measuring distances along Roman roads |
| HS-KS2-004 | Vikings and Anglo-Saxon England | Viking navigation and measurement; trading calculations |
| HS-KS2-005 | Local History Study | Census data analysis: population change, occupations, household sizes |
| HS-KS2-007 | Ancient Sumer | Sumerian base-60 number system: why we have 60 seconds and 360 degrees |
| HS-KS2-008 | The Indus Valley Civilisation | Standardised weights and measures used across the entire civilisation; grid planning |
| HS-KS2-009 | Ancient Egypt | Egyptian numerals; geometry in pyramid construction |
| HS-KS2-011 | Ancient Greece | Greek contributions to geometry and mathematical reasoning |
| HS-KS2-012 | Early Islamic Civilisation | Algebra (from Arabic 'al-jabr'); the development of the number system we use today |
| HS-KS2-013 | Mayan Civilisation | Mayan base-20 number system; the concept of zero developed independently |
| HS-KS3-001 | Medieval Britain 1066-1509 | Domesday Book data: analysing medieval statistics about land, population and resources |
| HS-KS3-008 | Pre-Columbian Americas Depth Study | Inca quipu as a recording system; Aztec calendar mathematics |
| HS-KS3-010 | Early Modern European History | The Scientific Revolution and the mathematical foundations of modern science |
| GS-GE-KS1-001 | Our Local Area | Simple data collection -- counting types of buildings, shops, or vehicles |
| GS-GE-KS1-005 | Hot and Cold Places | Recording weather data on simple charts and pictograms |
| GS-GE-KS2-001 | UK Regional Study | Using grid references and scale on OS maps of the region |
| GS-GE-KS2-003 | Americas Regional Study | Comparing scale -- distances, areas, and population sizes across continents |
| GS-GE-KS2-004 | Rivers and the Water Cycle | Measuring rainfall, calculating river flow rates, reading scales |
| GS-GE-KS2-005 | Climate Zones, Biomes and Vegetation Belts | Reading climate graphs -- temperature and rainfall data for different zones |
| GS-GE-KS2-006 | Trade, Economic Geography and Fairtrade | Calculating prices, profits, and shares along a supply chain; reading trade data |
| GS-GE-KS2-007 | Geographical Skills and Fieldwork | Grid references as coordinates, scale calculations, compass bearings, data presentation |
| GS-GE-KS3-001 | Haiti 2010 Earthquake | Interpreting statistical data on development indicators (HDI, GDP) |
| GS-GE-KS3-002 | Japan 2011 Earthquake and Tsunami | Comparing statistical data across two events (magnitude, deaths, GDP) |
| GS-GE-KS3-003 | Climate Change | Interpreting line graphs, scatter plots, and trend data from climate records |
| GS-GE-KS3-004 | Development and Global Inequality: Nigeria | Calculating and comparing development indicators (GDP per capita, HDI, literacy rates) |
| GS-GE-KS3-005 | Urbanisation: Lagos and London | Interpreting population growth curves and percentage calculations |
| GS-GE-KS3-006 | Resource Management: UK Water | Data handling with water consumption statistics, surplus/deficit calculations |
| GS-GE-KS3-007 | Africa: Place Depth Study | Comparing development data across African nations using multiple indicators |
| GS-GE-KS3-008 | Asia: Place Depth Study | Population data analysis using very large numbers and growth rate calculations |
| GS-GE-KS3-009 | Geographical Fieldwork Investigation | Sampling methods, data presentation (graphs, charts), calculating averages and percentages |
| SE-KS2-001 | Friction Investigation | Measuring in centimetres, recording in tables, drawing bar charts |
| SE-KS2-002 | Plant Growth Enquiry | Measuring height in centimetres, plotting line graphs to show change over time |
| SE-KS2-004 | Sound Investigation | Measuring and ordering, recognising patterns in data |
| SE-KS2-005 | Electrical Circuits Investigation | Drawing circuit diagrams using standard symbols accurately |
| SE-KS2-006 | States of Matter and the Water Cycle | Measuring volume in millilitres, reading thermometers, plotting results |
| SE-KS2-007 | Light and Shadows Investigation | Measuring shadow lengths, plotting line graphs, identifying proportional relationships |
| SE-KS2-008 | Human Body: Digestion and Teeth | Interpreting data about tooth decay from the egg shell experiment |
| SE-KS2-010 | Separating Mixtures | Measuring volumes accurately, recording data in tables |
| SE-KS3-001 | Cell Structure and Microscopy | Calculating magnification using the formula: magnification = image size / actual size |
| SE-KS3-001 | Cell Structure and Microscopy | Working with very small numbers and unit conversions (mm to micrometres) |
| SE-KS3-002 | Acids, Alkalis and Neutralisation | Reading scales accurately (pH scale, measuring cylinders), plotting graphs of pH vs volume |
| SE-KS3-003 | Forces and Motion Investigation | Calculating speed from distance-time data, plotting and interpreting graphs, using formulae |
| SE-KS3-003 | Forces and Motion Investigation | Gradient of a distance-time graph represents speed |
| SE-KS3-004 | Photosynthesis Rate Investigation | Plotting rate graphs, calculating means from repeat readings, understanding inverse square relationships |
| SE-KS3-005 | Particle Model and Changes of State | Plotting temperature-time graphs, reading scales, calculating gradients |
| SE-KS3-006 | Ecosystem Relationships and Fieldwork | Calculating means, using random number tables for sampling, estimating population size |
| SE-KS3-007 | Energy Transfers and Insulation Investigation | Calculating efficiency as a percentage, plotting cooling curves, reading thermometer scales |
| SE-KS3-008 | Chemical Reactions: Metals and Acids | Ranking data, comparing temperature changes quantitatively |
| EU-EN-KS1-001 | Traditional Tales: The Three Billy Goats Gruff | Counting and ordering (three goats, size comparison) |
| EU-EN-Y4-003 | Persuasive Writing: Save Our Park | Data collection and presentation to support arguments |
| TS-AD-KS1-001 | Colour Mixing | Sorting and comparing: which colours are warm? Which are cool? |
| TS-AD-KS1-005 | Printing with Found Objects | Repeating patterns: ABAB, ABCABC |
| TS-AD-KS1-006 | Mondrian Primary Colours | Right angles, parallel lines, rectangles, squares |
| TS-AD-KS1-007 | Kandinsky Circles | Circles, concentric shapes, symmetry |
| TS-AD-KS1-009 | Weaving and Textiles | Repeating patterns, counting threads |
| TS-AD-KS2-008 | Architectural Drawing | Symmetry, angles, parallel lines, measurement, scale |
| TS-AD-KS2-009 | Yayoi Kusama Dots and Infinity | Pattern, scale, covering surfaces |
| TS-AD-KS2-011 | Gaudi Architecture and Mosaic | Tessellation, shape, area coverage |
| TS-MU-KS1-004 | Round and Round | Repeating patterns in the ostinato |
| TS-MU-KS2-002 | Glockenspiel Stage 1 | Patterns in note sequences |
| TS-MU-KS2-005 | Composing with Structure: Rondo | Pattern: ABACADA as a mathematical sequence |
| TS-DT-KS1-001 | Moving Pictures (Sliders and Levers) | Measurement -- cutting strips to length |
| TS-DT-KS1-002 | Freestanding Structures | 3D shapes, measurement, comparison of height |
| TS-DT-KS1-003 | Wheeled Vehicles | Measurement, distance, comparing |
| TS-DT-KS2-001 | Cam Mechanisms: Moving Toys | Circles, rotation, measurement |
| TS-DT-KS2-002 | Shell Structures: Packaging | Nets of 3D shapes, measurement, area, surface area |
| TS-DT-KS2-003 | Textiles: Pencil Case | Measurement, area, pattern cutting |
| TS-DT-KS2-004 | Design a Torch | Measurement -- cutting housing to size, battery compartment dimensions |
| TS-DT-KS2-006 | Bridges: Beam, Arch and Truss | Measurement, weight, data collection and graphing |
| TS-DT-KS2-007 | Programmable Buggy | Measurement, angles, distance |
| TS-DT-KS2-008 | Savoury Pasta Bake | Measuring ingredients, scaling recipes |
| TS-DT-KS2-009 | Pulleys and Gears: Fairground Ride | Gear ratios, multiplication, division |
| TS-RS-KS2-001 | Why Do People Pray? | Five daily prayers, prayer times, compass directions |

### 1b. PSHE (~35 hooks)

No PSHE study nodes exist in the graph. PSHE is not a standalone subject in the UK National Curriculum. Hooks were pedagogically useful but reference a subject with no importable study nodes.

| Source ID | Source Name | Hook Text |
|-----------|------------|-----------|
| GS-GE-KS1-002 | The United Kingdom: Countries, Capitals and Seas | Identity -- which country do we live in? What does it mean to live in the UK? |
| GS-GE-KS1-004 | Contrasting Non-European Locality Study | Similarities in daily life, empathy, and understanding diverse communities |
| GS-GE-KS2-006 | Trade, Economic Geography and Fairtrade | Fairness, global citizenship, and making ethical consumer choices |
| GS-GE-KS3-001 | Haiti 2010 Earthquake | International aid, empathy, and understanding global inequality |
| SE-KS2-008 | Human Body: Digestion and Teeth | Healthy eating and dental hygiene |
| EU-EN-KS1-001 | Traditional Tales: The Three Billy Goats Gruff | Themes of bravery, problem-solving, and standing up to bullies |
| EU-EN-KS1-002 | Traditional Tales: Little Red Riding Hood | Stranger danger and personal safety |
| EU-EN-KS1-004 | Poetry: Nursery Rhymes and Rhyming Poems | Poems about feelings and emotions |
| EU-EN-KS1-006 | Narrative: Dogger | Feelings about loss and the kindness of siblings and others |
| EU-EN-KS1-009 | Traditional Tales: The Enormous Turnip | Teamwork and co-operation |
| EU-EN-KS1-010 | Recount: Diary of a Killer Cat | Seeing events from different points of view |
| EU-EN-Y3-003 | Adventure Narrative: The BFG | Friendship, bravery, and standing up for what is right |
| EU-EN-Y4-001 | Adventure Narrative: The Iron Man | Themes of fear, friendship, and acceptance of difference |
| EU-EN-Y4-003 | Persuasive Writing: Save Our Park | Community participation and civic responsibility |
| EU-EN-Y4-004 | Poetry: Performance and Form | Self-expression and confidence through performance |
| EU-EN-Y4-006 | Fairy Tales: Rewriting the Classics | Exploring themes of good and evil, justice, and morality in fairy tales |
| EU-EN-Y4-008 | Discussion and Debate: Should Animals Be Kept in Zoos? | Ethical decision-making and respecting different viewpoints |
| EU-EN-Y5-002 | Persuasion and Discussion: Balanced Argument | Current affairs and ethical issues |
| EU-EN-Y6-001 | Narrative: Literary Fiction | Themes of identity, growing up, and moral choice |
| EU-EN-Y6-002 | Non-Fiction: Formal Persuasion and Discussion | Topical ethical issues (environment, technology, rights) |
| EU-ELT-KS4-003 | A Christmas Carol: Redemption and Social Responsibility | Social responsibility, inequality, and wealth distribution |
| EU-ELT-KS4-004 | An Inspector Calls: Class, Responsibility, and Socialism | Social responsibility, community, and inequality |
| EU-ENL-KS4-003 | Transactional Writing: Speech | Ethical and social issues as speech topics |
| EU-ENL-KS4-004 | Transactional Writing: Article and Letter | Writing to real audiences about genuine issues |
| TS-AD-KS1-007 | Kandinsky Circles | Collaboration: contributing to a shared artwork |
| TS-AD-KS1-010 | Self-Portraits | Identity, uniqueness, belonging |
| TS-AD-KS2-009 | Yayoi Kusama Dots and Infinity | Mental health awareness: Kusama uses art therapeutically |
| TS-MU-KS1-001 | Hey You! | Expressing yourself, confidence |
| TS-MU-KS1-006 | Your Imagination | Imagination, creativity, expressing ideas |
| TS-MU-KS1-007 | Friendship Song | Friendship, kindness, belonging |
| TS-MU-KS2-001 | Three Little Birds | Optimism, resilience |
| TS-MU-KS2-003 | Lean on Me | Community, supporting each other, empathy |
| TS-MU-KS2-006 | Livin' on a Prayer | Perseverance and working together themes |
| TS-MU-KS2-008 | Happy | Wellbeing, positive emotions |
| TS-RS-KS2-002 | What Makes a Good Leader? | Leadership, qualities, role models |

### 1c. Drama (5 hooks)

No Drama study nodes exist in the graph. All from English KS2/KS4 units.

| Source ID | Source Name | Hook Text |
|-----------|------------|-----------|
| EU-EN-Y4-002 | Myths and Legends: Greek Myths | Dramatic retelling and performance of myths |
| EU-EN-Y4-006 | Fairy Tales: Rewriting the Classics | Performing fairy tales from different characters' perspectives |
| EU-EN-Y6-003 | Shakespeare: A Midsummer Night's Dream | Performance techniques and stagecraft |
| EU-ELT-KS4-001 | Macbeth: Ambition and Moral Decline | Performance interpretation of key scenes |
| EU-ELT-KS4-002 | Macbeth: Guilt and the Supernatural | Staging the witches -- how do directorial choices affect audience interpretation? |

### 1d. Physical Education (3 hooks)

No PE study nodes exist at the right key stage levels for matching.

| Source ID | Source Name | Hook Text |
|-----------|------------|-----------|
| HS-KS2-011 | Ancient Greece | The ancient Olympic Games compared with their modern counterpart |
| SE-KS3-003 | Forces and Motion Investigation | Measuring running speeds over different distances |
| EU-EN-KS1-003 | Instructions: How to Wash a Woolly Mammoth | Writing instructions for a simple game |

### 1e. Languages (2 hooks)

No Languages study nodes exist in the graph.

| Source ID | Source Name | Hook Text |
|-----------|------------|-----------|
| GS-GE-KS2-002 | European Regional Study | Connections to French, Spanish, or German language learning if the region aligns |
| EU-EN-Y4-007 | Spelling and Vocabulary: Word Detective | Comparing English spelling patterns with French and Spanish cognates |

---

## 2. No study nodes at the target key stage

### 2a. No KS1 Science enquiry nodes (~28 hooks)

Science enquiry nodes (ScienceEnquiry) only exist at KS2 and KS3. All KS1-sourced hooks targeting Science were dropped.

| Source ID | Source Name | Hook Text |
|-----------|------------|-----------|
| HS-KS1-001 | Changes Within Living Memory | Materials and technology: why do objects look and work differently now? |
| HS-KS1-002 | The Great Fire of London | Materials: why did the wooden buildings burn? What materials resist fire? |
| HS-KS1-004 | The Moon Landings | Space, Earth and the Moon; what is the Moon? How far away is it? |
| HS-KS1-005 | Florence Nightingale & Mary Seacole | Hygiene and handwashing: why did Nightingale insist on cleanliness? |
| HS-KS1-007 | Christopher Columbus & Neil Armstrong | Comparing the technology of a sailing ship with a spacecraft |
| GS-GE-KS1-001 | Our Local Area | Seasonal changes observed in the local environment |
| GS-GE-KS1-004 | Contrasting Non-European Locality Study | Comparing weather and seasons between the two localities |
| GS-GE-KS1-005 | Hot and Cold Places | Seasonal changes, temperature measurement, and simple weather recording |
| EU-EN-KS1-003 | Instructions: How to Wash a Woolly Mammoth | Writing up a simple investigation as instructions |
| EU-EN-KS1-007 | Information Text: All About Animals | Living things and their habitats -- animal classification, diet, habitat |
| EU-EN-KS1-008 | Poetry: Silly Poems and Tongue Twisters | Tongue twisters about science topics (slippery, slimy slugs) |
| EU-EN-KS1-009 | Traditional Tales: The Enormous Turnip | Plants and growing -- what do plants need to grow? |
| EU-EN-KS1-010 | Recount: Diary of a Killer Cat | Animals and their habitats -- writing a diary from an animal's perspective |
| TS-AD-KS1-001 | Colour Mixing | Colour in nature: why are leaves green? Why are flowers different colours? |
| TS-AD-KS1-002 | Drawing from Observation | Observing and recording: seasonal changes, plant growth |
| TS-AD-KS1-003 | Collage and Texture | Materials and their properties: rough, smooth, shiny, dull |
| TS-AD-KS1-004 | Clay Pinch Pots | Materials: clay as a malleable material that dries hard |
| TS-AD-KS1-005 | Printing with Found Objects | Leaves and natural forms as printing objects |
| TS-AD-KS1-008 | Andy Goldsworthy Nature Art | Seasonal changes, natural materials, living and non-living |
| TS-AD-KS1-010 | Self-Portraits | Human body: facial features, senses |
| TS-MU-KS1-005 | Zootime: Animal Sound Composition | Animal habitats, classification |
| TS-DT-KS1-001 | Moving Pictures (Sliders and Levers) | Forces -- push and pull, cause and effect |
| TS-DT-KS1-002 | Freestanding Structures | Materials and their properties, forces |
| TS-DT-KS1-003 | Wheeled Vehicles | Forces -- push and pull, friction, surfaces |
| TS-DT-KS1-005 | Fruit Salad | Healthy eating, food groups |
| TS-DT-KS1-006 | Sandwich Design Challenge | Food groups, healthy eating |
| TS-DT-KS1-007 | Windmill | Wind, forces, renewable energy |
| TS-RS-KS1-001 | Harvest and Thankfulness | Seasons, plant growth, food chains |

### 2b. No KS3 English unit nodes (~16 hooks)

English units (EnglishUnit) only exist at KS1, KS2, and KS4. All KS3 hooks targeting English were dropped.

| Source ID | Source Name | Hook Text |
|-----------|------------|-----------|
| HS-KS3-001 | Medieval Britain 1066-1509 | Medieval literature: Chaucer's Canterbury Tales as a source for medieval society |
| HS-KS3-002 | Development of Church, State and Society 1509-1745 | Milton's political writings; pamphlet culture and the origins of free speech |
| HS-KS3-003 | The Elizabethan Age | Shakespeare's plays as both literature and historical sources for Elizabethan society |
| HS-KS3-004 | Ideas, Power, Industry and Empire 1745-1901 | Dickens, the Brontes and Victorian social commentary literature as historical sources |
| HS-KS3-005 | Challenges 1901 to Present Day | War poetry and propaganda analysis; oral history and memoir as literary forms |
| HS-KS3-006 | The Holocaust | Anne Frank's diary and Primo Levi's testimony as both literature and historical source |
| HS-KS3-007 | A Study of an Aspect or Theme in World History | Literature and primary sources from the chosen society |
| HS-KS3-010 | Early Modern European History | Enlightenment texts and political pamphlets as sources and rhetorical models |
| GS-GE-KS3-003 | Climate Change | Evaluating persuasive writing and media coverage of climate issues |
| GS-GE-KS3-004 | Development and Global Inequality: Nigeria | Analysing different perspectives on development through contrasting written sources |
| GS-GE-KS3-009 | Geographical Fieldwork Investigation | Writing up fieldwork reports with clear structure and evidence-based conclusions |
| SE-KS3-001 | Cell Structure and Microscopy | Writing a method using precise scientific vocabulary and passive voice |
| SE-KS3-002 | Acids, Alkalis and Neutralisation | Writing a risk assessment using formal, precise language |
| SE-KS3-004 | Photosynthesis Rate Investigation | Writing a scientific explanation using causal language and the photosynthesis equation |
| SE-KS3-005 | Particle Model and Changes of State | Using the particle model to write a scientific explanation |
| SE-KS3-006 | Ecosystem Relationships and Fieldwork | Writing a discursive text about the impact of human activity on ecosystems |

### 2c. No KS3 Art/DT/Music study nodes (6 hooks)

Foundation subject study nodes (ArtTopicSuggestion, DTTopicSuggestion, MusicTopicSuggestion) only exist at KS1 and KS2.

| Source ID | Source Name | Target Subject | Hook Text |
|-----------|------------|----------------|-----------|
| HS-KS3-003 | The Elizabethan Age | Art & Design | The Armada Portrait and other Elizabethan portraiture as propaganda |
| HS-KS3-009 | An Islamic Civilisation | Art & Design | Mughal miniature painting or Ottoman tile work; the Taj Mahal as architecture |
| GS-GE-KS3-002 | Japan 2011 Earthquake and Tsunami | Design & Technology | Engineering for earthquake resistance |
| GS-GE-KS3-006 | Resource Management: UK Water | Design & Technology | Water filtration and purification systems |
| GS-GE-KS3-007 | Africa: Place Depth Study | Art | African art traditions, textile design, and contemporary African artists |
| SE-KS3-007 | Energy Transfers and Insulation Investigation | DT | Designing insulated containers or energy-efficient products |

### 2d. No KS2 Citizenship study nodes (1 hook)

Citizenship study nodes only exist at KS3-KS4.

| Source ID | Source Name | Hook Text |
|-----------|------------|-----------|
| EU-EN-Y6-002 | Non-Fiction: Formal Persuasion and Discussion | Democracy, rights, and responsibilities |

---

## 3. RS/RE hooks too thematic to match (~13 hooks)

RS study nodes exist but the hook text was too thematic (morality, guilt, free will, theological questions) to confidently match to a specific RS unit. These describe abstract moral/philosophical concepts rather than named curriculum studies.

| Source ID | Source Name | Hook Text |
|-----------|------------|-----------|
| HS-KS3-001 | Medieval Britain 1066-1509 | The power of the Church in medieval society: how faith shaped law, education and daily life |
| HS-KS3-002 | Development of Church, State and Society 1509-1745 | The Reformation: how did the break with Rome change English religion and society? |
| HS-KS3-006 | The Holocaust | The moral and theological questions raised by the Holocaust; responses of faith communities |
| HS-KS3-007 | A Study of an Aspect or Theme in World History | Religious and philosophical traditions of the chosen society |
| HS-KS3-009 | An Islamic Civilisation | Religious tolerance and conflict within Islamic empires; Akbar's religious policies |
| GS-GE-KS3-008 | Asia: Place Depth Study | Buddhism, Hinduism, Islam, and Sikhism in their geographical contexts |
| GS-GE-KS3-010 | Middle East: Place Depth Study | Islam in its geographical context; religious diversity in the region |
| EU-ELT-KS4-001 | Macbeth: Ambition and Moral Decline | Morality, guilt, the supernatural, free will versus fate |
| EU-ELT-KS4-002 | Macbeth: Guilt and the Supernatural | Concepts of sin, conscience, and divine judgement |
| EU-ELT-KS4-003 | A Christmas Carol: Redemption and Social Responsibility | Charity, compassion, redemption, and the Christian moral framework |
| EU-ELT-KS4-004 | An Inspector Calls: Class, Responsibility, and Socialism | Moral responsibility, socialism versus individualism |
| EU-ELT-KS4-005 | Jekyll and Hyde: Duality and Victorian Repression | Good and evil, free will, and moral responsibility |
| EU-ELT-KS4-006 | Poetry Anthology: Power and Conflict | Ethical dimensions of power and conflict |

---

## 4. Too vague / no matching target node (~99 hooks)

Hooks where the target subject has study nodes but the text was too generic, referenced historical technology, spanned multiple periods or regions, or described a pedagogical approach rather than matching a specific curriculum study node.

Key patterns in this category:
- **Ancient history science connections** (mummification, bronze casting, Mayan astronomy, irrigation) -- Science enquiry nodes cover experimental/observational topics, not historical technology
- **Medieval/early modern geography** (medieval settlement patterns, Irish plantations, European political geography) -- no matching geography study nodes for these historical periods
- **Generic art references** ("art from the chosen period", "illustrating own version of story") -- too unspecific to match a named art study
- **Generic literacy connections** ("descriptive vocabulary", "storytelling", "story structure") -- describe skills rather than matching a specific English unit
- **Ancient river geography** (Nile, Indus, Yellow River, Fertile Crescent) -- no ancient geography study nodes exist; geography studies cover contemporary places
- **Generic science connections** ("dreams and sleep", "the science of happiness", "waves and water") -- no matching science enquiry node at the right specificity

| Source ID | Source Name | Target Subject | Hook Text |
|-----------|------------|----------------|-----------|
| HS-KS1-001 | Changes Within Living Memory | Art & Design | Comparing art, design and fashion across decades |
| HS-KS2-001 | Stone Age to Iron Age Britain | Design & Technology | Tool-making: designing and evaluating Stone Age and Bronze Age tools |
| HS-KS2-004 | Vikings and Anglo-Saxon England | Design & Technology | Longship design: why was the design so effective for raiding and trading? |
| HS-KS2-006 | British History Beyond 1066 | Art & Design | Art from the chosen period as both source material and creative inspiration |
| HS-KS2-007 | Ancient Sumer | Geography | The Fertile Crescent: how geography enabled civilisation through irrigation |
| HS-KS2-008 | The Indus Valley Civilisation | Geography | The Indus River system: how geography enabled and constrained the civilisation |
| HS-KS2-008 | The Indus Valley Civilisation | Science | Water management and drainage systems: engineering solutions to urban sanitation |
| HS-KS2-009 | Ancient Egypt | Geography | The Nile: how river geography enabled agriculture, settlement and civilisation |
| HS-KS2-009 | Ancient Egypt | Science | Mummification as a scientific process; irrigation technology |
| HS-KS2-010 | The Shang Dynasty | Art & Design | Chinese calligraphy from oracle bone script to modern characters; bronze vessel design |
| HS-KS2-010 | The Shang Dynasty | Science | Bronze casting: how did the Shang achieve such sophisticated metalwork? |
| HS-KS2-010 | The Shang Dynasty | Geography | The Yellow River and its role in Chinese civilisation |
| HS-KS2-012 | Early Islamic Civilisation | Science | Islamic contributions to medicine, astronomy and optics |
| HS-KS2-013 | Mayan Civilisation | Science | Mayan astronomical observations and their calendar systems |
| HS-KS3-001 | Medieval Britain 1066-1509 | Geography | Medieval settlement patterns, town charters and the growth of urban centres |
| HS-KS3-002 | Development of Church, State and Society 1509-1745 | Geography | The plantation of Ireland and its lasting consequences |
| HS-KS3-003 | The Elizabethan Age | Geography | Early English exploration and colonisation: mapping the expansion of English knowledge of the world |
| HS-KS3-004 | Ideas, Power, Industry and Empire 1745-1901 | Science | Industrial technology: steam power, textile machinery, iron and steel production |
| HS-KS3-005 | Challenges 1901 to Present Day | Geography | Geopolitics of the World Wars; Cold War geography; decolonisation and the reshaping of the world map |
| HS-KS3-005 | Challenges 1901 to Present Day | Science | Technological developments driven by war: radar, nuclear weapons, computing, medicine |
| HS-KS3-008 | Pre-Columbian Americas Depth Study | Science | Aztec and Inca agriculture: chinampas (floating gardens) and terracing |
| HS-KS3-010 | Early Modern European History | Geography | European political geography and how it changed through warfare and revolution |
| GS-GE-KS1-002 | The United Kingdom: Countries, Capitals and Seas | History | The four countries of the UK and how they came to be united |
| GS-GE-KS2-001 | UK Regional Study | Science | Physical processes shaping the region -- river erosion, weathering, glaciation |
| GS-GE-KS2-001 | UK Regional Study | English | Travel writing and descriptive accounts of the region |
| GS-GE-KS2-007 | Geographical Skills and Fieldwork | Science | Scientific enquiry methods -- observation, measurement, recording, and conclusion |
| GS-GE-KS3-001 | Haiti 2010 Earthquake | Science | Seismic waves and the structure of the Earth |
| GS-GE-KS3-001 | Haiti 2010 Earthquake | History | Colonial history of Haiti and its long-term impact on development |
| GS-GE-KS3-002 | Japan 2011 Earthquake and Tsunami | Science | Seismic waves, subduction zones, and tsunami mechanics |
| GS-GE-KS3-002 | Japan 2011 Earthquake and Tsunami | Science | Nuclear energy and the Fukushima meltdown |
| GS-GE-KS3-003 | Climate Change | Science | The greenhouse effect, carbon cycle, and atmospheric chemistry |
| GS-GE-KS3-004 | Development and Global Inequality: Nigeria | Science | Oil extraction processes and environmental impacts |
| GS-GE-KS3-005 | Urbanisation: Lagos and London | Science | Urban heat island effect and pollution |
| GS-GE-KS3-008 | Asia: Place Depth Study | Science | Monsoon weather systems, Himalayan tectonics, and delta formation |
| GS-GE-KS3-009 | Geographical Fieldwork Investigation | Science | Scientific method -- hypothesis, variables, fair testing principles applied to geographical contexts |
| SE-KS2-002 | Plant Growth Enquiry | Geography | Discussing how climate and light availability affect plant growth globally |
| SE-KS2-003 | Rocks and Fossils Classification | History | How fossils changed scientific understanding of Earth's history |
| SE-KS2-004 | Sound Investigation | DT | Designing and building a simple musical instrument |
| SE-KS2-005 | Electrical Circuits Investigation | English | Writing instructions for building a circuit using imperative verbs |
| SE-KS2-007 | Light and Shadows Investigation | Art | Shadow puppetry and silhouette art |
| SE-KS2-007 | Light and Shadows Investigation | English | Descriptive writing using light and shadow imagery |
| SE-KS2-009 | Evolution and Adaptation | English | Writing a biography of a significant scientist (Darwin, Wallace, Mary Anning) |
| EU-EN-KS1-002 | Traditional Tales: Little Red Riding Hood | Art | Illustrating own version of the story |
| EU-EN-Y3-001 | Traditional Tales: Myths from Around the World | Geography | Where in the world do these myths come from? |
| EU-EN-Y3-003 | Adventure Narrative: The BFG | Science | Dreams and sleep -- the BFG's dream-catching links to understanding sleep |
| EU-EN-Y3-004 | Poetry: Shape Poems and Calligrams | Art | Visual poetry as art -- creating illustrated calligrams |
| EU-EN-Y3-004 | Poetry: Shape Poems and Calligrams | Science | Shape poems about natural phenomena (water, fire, animals) |
| EU-EN-Y4-001 | Adventure Narrative: The Iron Man | Art | Illustration and character design inspired by the text |
| EU-EN-Y4-004 | Poetry: Performance and Form | History | Narrative poetry as a way of retelling historical events |
| EU-EN-Y4-006 | Fairy Tales: Rewriting the Classics | Art | Illustrating traditional versus modern fairy tale scenes for contrast |
| EU-EN-Y4-007 | Spelling and Vocabulary: Word Detective | Science | Technical vocabulary with Latin and Greek roots |
| EU-EN-Y5-002 | Persuasion and Discussion: Balanced Argument | Science | Environmental issues (deforestation, plastic, climate change) |
| EU-EN-Y5-002 | Persuasion and Discussion: Balanced Argument | Geography | Global issues with local impact |
| EU-EN-Y5-003 | Poetry: Classic and Contemporary Comparison | Science | Nature poetry linked to environmental topics |
| EU-EN-Y5-003 | Poetry: Classic and Contemporary Comparison | History | Historical context of classic poems |
| EU-EN-Y6-001 | Narrative: Literary Fiction | History | Historical fiction drawing on KS2 history topics |
| EU-EN-Y6-002 | Non-Fiction: Formal Persuasion and Discussion | Science | Scientific debates (space exploration, genetic modification) |
| EU-EN-Y6-003 | Shakespeare: A Midsummer Night's Dream | Art | Set and costume design for a production |
| EU-ELT-KS4-005 | Jekyll and Hyde: Duality and Victorian Repression | Science | Darwinism, degeneration theory, and Victorian anxieties about human nature |
| EU-ELT-KS4-006 | Poetry Anthology: Power and Conflict | Geography | Nature and landscape poetry -- Ozymandias, Storm on the Island |
| EU-ENL-KS4-003 | Transactional Writing: Speech | Citizenship | Democratic debate and civic engagement |
| EU-ENL-KS4-004 | Transactional Writing: Article and Letter | Citizenship | Engaging with local and national debates through letter writing |
| EU-ENL-KS4-005 | Spoken Language Endorsement: Formal Presentation | All subjects | Presentation skills are transferable to every subject area |
| EU-ENL-KS4-005 | Spoken Language Endorsement: Formal Presentation | Citizenship | Public speaking and democratic participation |
| TS-AD-KS1-002 | Drawing from Observation | English | Descriptive vocabulary: what does it look like? Feel like? |
| TS-AD-KS1-003 | Collage and Texture | DT | Joining techniques: gluing, overlapping, layering |
| TS-AD-KS1-004 | Clay Pinch Pots | History | Ancient pottery: how did people make pots before machines? |
| TS-AD-KS1-006 | Mondrian Primary Colours | History | 1920s Europe, De Stijl movement |
| TS-AD-KS1-009 | Weaving and Textiles | History | Weaving across cultures: looms from ancient Egypt to modern mills |
| TS-AD-KS2-003 | Hokusai Wave Printing | Geography | Japan, Pacific Ocean, island nations |
| TS-AD-KS2-003 | Hokusai Wave Printing | History | Edo period Japan (1603-1868) |
| TS-AD-KS2-003 | Hokusai Wave Printing | Science | Waves and water |
| TS-AD-KS2-004 | Monet and Impressionism | History | 19th century France, Impressionist movement |
| TS-AD-KS2-007 | Barbara Hepworth Sculpture | History | 20th century British art, women in art |
| TS-AD-KS2-008 | Architectural Drawing | History | Architectural styles through different periods |
| TS-MU-KS1-002 | In the Groove | History | Historical context of Blues, Baroque |
| TS-MU-KS1-003 | Hands, Feet, Heart | History | South African culture and heritage |
| TS-MU-KS2-003 | Lean on Me | History | Soul music and the civil rights movement |
| TS-MU-KS2-004 | Djembe Drumming: West African Rhythms | Geography | West Africa, Ghana, Senegal |
| TS-MU-KS2-005 | Composing with Structure: Rondo | English | Story structure: recurring themes with variations |
| TS-MU-KS2-007 | The Planets: Mars and Jupiter | Science | The solar system, planets |
| TS-MU-KS2-007 | The Planets: Mars and Jupiter | History | Holst and early 20th century Britain, World War I context for Mars |
| TS-MU-KS2-008 | Happy | Science | The science of happiness (age-appropriate) |
| TS-MU-KS2-009 | Film Music Composition | Computing | Video editing, sequencing |
| TS-MU-KS2-010 | Music and History: Baroque to Modern | History | Historical periods: Baroque courts, French Revolution, Industrial Revolution, World Wars |
| TS-DT-KS1-001 | Moving Pictures (Sliders and Levers) | English | Storytelling -- the moving picture tells a story |
| TS-DT-KS1-004 | Puppets | English | Character creation, storytelling, puppet shows |
| TS-DT-KS1-004 | Puppets | Art | Design, decoration, facial features |
| TS-DT-KS2-002 | Shell Structures: Packaging | Science | Materials properties: why card not plastic? |
| TS-DT-KS2-003 | Textiles: Pencil Case | Art | Surface decoration, personal design |
| TS-DT-KS2-005 | Bread Making | Science | Yeast as a living organism, fermentation, carbon dioxide, chemical changes |
| TS-DT-KS2-005 | Bread Making | History | Bread across civilisations: ancient Egypt, medieval bakers, wartime rationing |
| TS-RS-KS1-002 | Special Books and Sacred Texts | English | Stories, books, characters, morals |
| TS-RS-KS1-002 | Special Books and Sacred Texts | History | Ancient books and scrolls |
| TS-RS-KS2-001 | Why Do People Pray? | Geography | Mecca, Jerusalem, Varanasi -- places of prayer |
| TS-RS-KS2-002 | What Makes a Good Leader? | History | Historical leaders, ancient civilisations |

---

## Notes

- This document is purely archival. The dropped hooks have no impact on the graph or import scripts.
- The hook text remains pedagogically useful as teaching guidance even though it could not be expressed as a graph relationship with a specific `target_id`.
- If future layers add study nodes for Mathematics, PSHE, Drama, PE, Languages, KS3 English, or KS1 Science, some of these hooks could be re-evaluated for matching.
- The original `cross_curricular_hooks` property was a JSON blob (either free-text strings with `[Subject]` prefix or `{subject, hook, strength}` dicts). The replacement `cross_curricular_links` property uses `{target_id, hook}` objects that resolve to actual graph nodes.
