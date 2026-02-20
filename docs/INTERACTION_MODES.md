# Creative Interaction Modes: Beyond Typing

**Principle**: The app is NOT a chatbot. It's a multimodal learning environment that uses the best interaction method for each pedagogical goal.

---

## Mode 1: Blackboard Presenter (Khan Academy Style)

**Best for**: Worked examples, step-by-step explanations, visual derivations

### Technical Implementation

**Canvas**: Infinite blackboard (pan and zoom like Khan videos)
**Interaction**: AI "writes" in real-time (handwriting animation)
**Child role**: Watches, then tries their own version

### Example: Long Multiplication (Y4)

**AI explains**: 23 × 14

*[Blackboard appears, AI "hand" writes:]*

```
    23
  × 14
  ----
```

**AI voice** (synchronized with writing):
> "First, let's do 4 times 23..."

*[Writes]:*

```
    23
  × 14
  ----
    92  ← 4 × 23
```

*[Zooms in on the 92]:*

> "See that? 4 times 3 is 12, write the 2, carry the 1..."

*[Highlights the carried 1 in a different color]:*

```
    ¹23   ← carried 1 appears
  ×  14
  ----
    92
```

**Then AI zooms out, continues**:

```
    ¹23
  ×  14
  ----
    92  ← 4 × 23
   230  ← 10 × 23 (shifted left)
  ----
   322
```

**Now child's turn**: Same problem appears blank. Child can:
- Draw with finger/stylus on touchscreen
- See AI's working (button: "Show me again")
- Get hints (button: "I'm stuck")

**Data collected**:
- How many times child viewed explanation
- Where child made errors in their working
- Whether child used hint system

---

## Mode 2: Video Generation (AI-Created Visuals)

**Best for**: Bringing abstract concepts to life, memorable imagery

### Example 1: Fractions (Y5)

**Concept**: Equivalent fractions (1/2 = 2/4 = 3/6)

**AI generates** (using Stable Diffusion / DALL-E):
- A pizza being cut into 2 slices
- Same pizza being cut into 4 slices
- Same pizza being cut into 6 slices

*[Video shows transformation: pizza morphs from 2→4→6 slices]*

**AI voice**:
> "Watch the pizza. It's the same pizza, but we're cutting it into smaller and smaller pieces."

*[Highlights half the pizza across all three versions — 1/2, 2/4, 3/6 — showing they're the same amount]*

**Child interaction**:
- Tap to freeze frame
- Drag slider to control the slicing speed
- Request different scenarios: "Show me with a cake" / "Show me with a chocolate bar"

---

### Example 2: Onomatopoeia (Y3 English)

**Concept**: Words that sound like what they mean

**AI voice**: "Let's make a lion roar. What sound does a lion make?"

*[Child speaks: "ROAR!"]*

**AI generates video**:
- A cartoon lion wearing a pink hat (whimsical, memorable)
- Lion opens mouth, "ROAR" appears as wobbly text
- Text shakes and vibrates with the roar sound

**AI**: "That's an onomatopoeia — a word that sounds like the thing!"

**More examples generated**:
- SPLASH (child jumps in puddle)
- BUZZ (bee flying)
- CRUNCH (child eating apple)

Each generated with child-requested details:
- "Make the bee wear sunglasses"
- "Make it a rainbow puddle"

**Data collected**:
- Which examples child requested
- Which examples child remembered 3 days later (retrieval test)

---

## Mode 3: Paper-and-Pen Interface (Digital Notebook)

**Best for**: Free-form problem solving, planning, drafting

### Example: Story Planning (Y5 English)

**Task**: Plan a story with a clear beginning, middle, end

**Interface**: Digital notebook with handwriting recognition

**AI sets up structure**:
*[Three boxes appear: BEGINNING | MIDDLE | END]*

**AI voice**: "Draw or write your ideas in each box. Don't worry about spelling."

**Child draws/writes**:
- BEGINNING: Dragon finds treasure (child draws crude dragon + gold coins)
- MIDDLE: Knight tries to steal it (child writes "nite trise to steel it")
- END: Dragon shares with village (child draws stick figures + treasure)

**AI response** (after child finishes):
> "I can see your story! A dragon finds treasure, a knight tries to steal it, but the dragon shares. That's kind!"
>
> *[Corrects spelling on screen]: "knight tries to steal"*
>
> "Now — how does the dragon FEEL when the knight tries to steal? Angry? Scared? Confused?"

**Child writes**: "angree" [angry]

**AI**: "Good! Let's add that to your middle section."

*[Inserts "The dragon felt ANGRY" into the middle box]*

---

## Mode 4: Manipulatives (Draggable Objects)

**Best for**: Concrete understanding before abstract symbols

### Example: Place Value (Y2)

**Interface**: Thousands of draggable blocks

**AI voice**: "Show me 342 using these blocks."

*[Child sees]:*
- Big cubes (hundreds)
- Flat squares (tens)
- Small cubes (ones)

*[Child drags]:*
- 3 big cubes (300)
- 4 flat squares (40)
- 2 small cubes (2)

**AI**: "Yes! 3 hundreds, 4 tens, 2 ones makes 342."

*[Blocks magically rearrange into the number 342]*

**Now challenge**: "What if we take away one hundred?"

*[Child drags away one big cube]*

**AI**: "What number is left?"

*[Child can count remaining blocks OR type/speak answer]*

---

## Mode 5: Animation Scrubbing (Video Timeline Control)

**Best for**: Understanding processes, cause-effect, sequences

### Example: Plant Growth (Y2 Science)

**Interface**: Video scrubber (like video editing software)

**Video shows**: Bean seed growing into plant (timelapse, 20 seconds)

**AI voice**: "Drag the timeline to see what happens."

*[Child drags scrubber left/right, video plays forward/backward]*

**Questions appear as child scrubs**:

- **At 0s (seed in soil)**: "What does the seed need to start growing?"
  - Child can tap: WATER | LIGHT | WARMTH

- **At 5s (root appears)**: "What grew first — the root or the leaves?"
  - *[Child scrubs back and forth to check]*
  - Child answers: "Root!"

- **At 10s (shoot breaks surface)**: "Why does the shoot grow up?"
  - *[AI generates side-by-side videos: one with light above, one with light sideways]*
  - *[Shoot grows toward light in both]*
  - Child: "It grows toward light!"

**Data collected**:
- How many times child scrubbed to compare stages
- Whether child noticed root-before-leaves without prompting
- Self-correction (initial wrong answer, then scrubbed to check)

---

## Mode 6: Spatial Exploration (3D Environment)

**Best for**: Geography, 3D shapes, spatial reasoning

### Example: Map Skills (Y3 Geography)

**Interface**: 3D virtual classroom (simple, low-poly, fast rendering)

**AI voice**: "You're standing at the door. Walk to the teacher's desk."

*[Child uses arrow keys / swipes to move avatar]*

**AI**: "Good! Now — if I draw a map of this room from above, what shape would the teacher's desk be?"

*[Switches to top-down 2D view]*

*[Child draws]: Rectangle

**AI**: "Yes! Now mark where YOU are on the map."

*[Child taps location]*

**AI**: "Right! Now here's the tricky bit. Which direction is the window from where you're standing?"

*[Switches back to 3D view]*

*[Child sees window to their left]*

*[Switches to map view]*

**Compass appears**: *[Child rotates it or taps: WEST]*

**AI**: "Exactly — WEST!"

---

## Mode 7: Physical Movement (Camera + Pose Detection)

**Best for**: PE, phonics (articulation), kinesthetic learning

### Example: Phonics Articulation (Y1)

**Interface**: Device camera shows child's face with overlay

**AI voice**: "Let's practice the /i/ sound. Watch my mouth."

*[Animated character shows exaggerated /i/ mouth shape]*

**AI**: "Now you try! Say 'ih' like in 'sit.'"

*[Camera activates, shows child's face]*

*[Overlay shows target mouth shape in green, child's mouth in real-time]*

*[As child says "ih", their mouth shape is compared to target]*

**AI**: "Great! Your mouth was almost closed — that's the /i/ sound!"

---

### Example: Symmetry (Y3 Maths)

**Interface**: Full-body camera (tablet propped up)

**AI voice**: "Make a symmetrical shape with your arms."

*[Child spreads arms wide, mirror image style]*

**AI**: "Yes! Both arms the same. Now try an asymmetrical shape."

*[Child raises one arm up, one arm down]*

**AI**: "That's asymmetrical — different on each side!"

*[On-screen: line of symmetry drawn through child's body, showing both sides match/don't match]*

---

## Mode 8: Audio Recording + Playback (Voice Reflection)

**Best for**: Speaking practice, self-assessment, explanation tasks

### Example: Explain Your Method (Y4 Maths)

**AI**: "You worked out 47 + 38 = 85. That's correct! Now press record and explain HOW you did it."

*[Child presses big red button]*

*[Child explains]: "Um... I did 40 + 30 is 70, then 7 + 8 is 15, then 70 + 15 is 85."

*[Recording stops]*

**AI plays it back with visual transcript**:
> "I did 40 + 30 is 70, then 7 + 8 is 15, then 70 + 15 is 85."

**AI**: "Perfect! You split the numbers into tens and ones. That's called partitioning."

*[Saves recording to portfolio, parent can listen in dashboard]*

---

## Mode 9: Collaborative Whiteboard (AI + Child Co-Create)

**Best for**: Planning, concept mapping, collaborative problem-solving

### Example: Story Structure (Y5 English)

**AI starts**: "Let's plan a mystery story together."

*[AI draws a circle in the center]: "THE MYSTERY"*

**AI**: "What's the mystery? Draw or write your idea."

*[Child draws]: "Missing cat"

**AI draws arrows from center**:
- CLUES (blank)
- SUSPECTS (blank)
- SOLUTION (blank)

**AI**: "Now — what clues might the detective find?"

*[Child writes]: "Paw prints"

*[AI adds]: "Cat hair on sofa"

**AI**: "Good! More clues?"

*[Child writes]: "Half-eaten tuna"

**AI**: "Ooh! That's suspicious. Who might have taken the cat?"

*[Child writes under SUSPECTS]: "Neighbor"

*[AI adds]: "Cat's best friend (another cat?)"

**Together they build the story structure visually.**

*[At end, AI generates]: "Want me to turn this into a story starter?"*

*[AI writes opening paragraph based on their plan]*

---

## Mode 10: Augmented Reality (AR Overlay)

**Best for**: Measurement, real-world connections, spatial tasks

### Example: Measuring Length (Y2 Maths)

**Interface**: Camera + AR overlay

**AI**: "Point your camera at something shorter than 30cm."

*[Child points at pencil]*

*[AR ruler appears overlaid on pencil: 18cm]*

**AI**: "Good! That's 18cm — shorter than 30cm."

**AI**: "Now find something longer than 50cm."

*[Child points at table]*

*[AR ruler extends: 120cm]*

**AI**: "Yes! That's way longer — 120cm!"

---

## Implementation Summary

| Mode | Best For | Tech Required | Age Range |
|---|---|---|---|
| **Blackboard** | Worked examples, derivations | Canvas API, handwriting animation | Y3+ |
| **Video generation** | Visual concepts, memorable imagery | DALL-E API, video synthesis | Y1+ |
| **Paper-and-pen** | Planning, drafting, free-form | Handwriting recognition, OCR | Y3+ |
| **Manipulables** | Concrete understanding | Drag-and-drop, physics engine | Y1-Y4 |
| **Animation scrubbing** | Processes, sequences | Video player API | Y2+ |
| **3D exploration** | Spatial reasoning, geography | WebGL, simple 3D engine | Y3+ |
| **Physical movement** | Pose detection, kinesthetic learning | MediaPipe, TensorFlow Lite | Y1-Y3 |
| **Audio recording** | Explanation, self-assessment | Speech-to-text, audio playback | Y3+ |
| **Collaborative whiteboard** | Co-creation, planning | Real-time canvas sync | Y4+ |
| **AR overlay** | Real-world measurement, connections | ARKit/ARCore | Y2+ |

---

## Privacy Considerations

**Camera/microphone use**:
- ✅ Parent explicit consent required
- ✅ Local processing (MediaPipe, TensorFlow Lite run on-device)
- ❌ Video never uploaded to cloud (only pose/mouth shape data)
- ❌ No facial recognition, no biometric storage

**Generated content** (DALL-E, Stable Diffusion):
- Child's prompt stored: "lion wearing pink hat"
- Generated image stored: Yes (part of learning session)
- Image used for training: NO (opt-out from all generative AI training datasets)

---

## Data Structures for Multimodal Interactions

```json
{
  "session_id": "sess_2026_02_20_001",
  "child_id": "child_amelie_y2",
  "interactions": [
    {
      "timestamp": "2026-02-20T10:15:32Z",
      "mode": "blackboard",
      "concept_id": "MA-Y4-MULT-003",
      "interaction_data": {
        "ai_explanation_views": 2,
        "child_attempt_strokes": [/* SVG path data */],
        "errors_detected": ["carried 1 incorrectly"],
        "hints_requested": 1
      }
    },
    {
      "timestamp": "2026-02-20T10:18:15Z",
      "mode": "video_generation",
      "concept_id": "MA-Y5-FRAC-002",
      "interaction_data": {
        "prompt": "pizza cut into slices",
        "video_generated": "stable_diffusion_output_uuid",
        "child_interactions": {
          "paused_at_frames": [120, 240],
          "scrubbed_back_count": 3,
          "requested_replay": true
        }
      }
    },
    {
      "timestamp": "2026-02-20T10:22:40Z",
      "mode": "voice_recording",
      "concept_id": "MA-Y4-MULT-003",
      "interaction_data": {
        "recording_duration_ms": 8200,
        "transcript": "I did 40 + 30 is 70, then 7 + 8 is 15, then 70 + 15 is 85",
        "explanation_quality": "complete_with_method",
        "vocabulary_used": ["partitioning", "tens", "ones"]
      }
    }
  ]
}
```

---

## Conclusion

**The app is a multimedia learning studio**, not a text chat. Each concept uses the BEST interaction mode for that pedagogical goal:

- Want to show worked examples? → Blackboard
- Want memorable imagery? → Video generation
- Want to develop explanation skills? → Voice recording
- Want concrete understanding? → Manipulatives
- Want spatial reasoning? → 3D exploration / AR

**The child never gets bored typing** because they're rarely typing. They're drawing, speaking, dragging, watching, exploring.

**Every mode is data-rich**: We collect how child interacts (scrubs video, requests replays, draws attempt, speaks explanation) and use that to optimize learning.

**Privacy-first**: Camera/mic use requires consent, processing is local, no biometric data stored.
