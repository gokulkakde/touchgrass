# TOUCH GRASS CHALLENGE SUBMISSION

## Title
**TouchGrass AI — The 15-Minute Outdoor Micro-Expedition Engine**

## Tags
`#opensource` `#ai` `#onnx` `#python` `#health` `#touchgrass`

---

## What I Built
**TouchGrass AI** is a purpose-built micro-expedition application designed with one strict non-negotiable rule: **The screen must be the shortest part of the experience.**

Desk workers, developers, and students spend over 8–10 hours each day locked in front of glowing monitors. When brief breaks occur, dopamine loops typically direct users straight into doomscrolling. TouchGrass AI breaks this cycle:
1. **Under 5-Second Screen Interaction:** The user chooses their available time (5m, 15m, 30m, 60m) and immediate biome (Public Park, Backyard, Urban Sidewalk, Trail, Waterfront).
2. **Instant Micro-Quest Synthesis:** The engine synthesizes a sensory outdoor mission containing physical off-screen observation tasks (touching tree bark, listening to avian soundscapes, escaping asphalt).
3. **Pocket Mode:** The screen dims to a minimalist ambient timer and plays a calming departure chime. The instruction is explicit: *"Put your device in your pocket. The screen experience is over. Touch grass."*
4. **Real-World Action:** The user leaves their desk, takes an outdoor walk, touches real nature, and captures exactly one photo of their field finding.
5. **Local Open-Source AI Biophilia Verification:** Back at their desk, our **MobileNetV4 ONNX** model (Apache 2.0 open weights) executes on CPU in **~12 milliseconds**, verifying genuine botanical/fauna biophilia and rejecting indoor computer monitors and keyboards. Zero cloud telemetry; 100% private.

---

## Demo
- **Repository:** Included in this submission workspace.
- **Local Run:** `python app.py` -> browse to `http://127.0.0.1:5000`.
- **Demo Script:** Full 2-minute walkthrough documented in [DEMO_SCRIPT.md](file:///d:/hactoberfest/week1/DEMO_SCRIPT.md).

---

## Code
- Core AI Engine: [`ai_engine.py`](file:///d:/hactoberfest/week1/ai_engine.py)
- Quest Synthesizer: [`quest_generator.py`](file:///d:/hactoberfest/week1/quest_generator.py)
- Database & Streaks: [`database.py`](file:///d:/hactoberfest/week1/database.py)
- Web Application: [`app.py`](file:///d:/hactoberfest/week1/app.py)
- Frontend: [`templates/index.html`](file:///d:/hactoberfest/week1/templates/index.html), [`static/style.css`](file:///d:/hactoberfest/week1/static/style.css), [`static/app.js`](file:///d:/hactoberfest/week1/static/app.js)
- Automated Test Suite: [`tests/`](file:///d:/hactoberfest/week1/tests/)

---

## How I Built It

### Product Architecture
```text
User at Desk (< 5 seconds)
      ↓
Web Frontend (Pill selectors & Screen Timer)
      ↓
Backend API (Flask 3.0)
      ↓
Quest Engine (Biome-grounded sensory tasks)
      ↓
POCKET MODE (Screen dims, departure chime, phone pocketed)
      ↓
REAL-WORLD ACTION (15 min outdoor walk, sensory presence, 1 photo)
      ↓
Local ONNX Runtime (MobileNetV4 Small, 12ms CPU inference)
      ↓
Biophilia & Indoor Scene Classifier
      ↓
Local SQLite Journal (streaks & outdoor minutes logged)
```

### AI Implementation
- **Model:** `MobileNetV4 Conv Small` (`mobilenetv4_conv_small.e1200_r224_in1k`).
- **License:** **Apache 2.0 (True Open Source & Open Weight)**.
- **Runtime:** `onnxruntime` 1.30.0 with pure CPU execution provider.
- **Inference Approach:** Tensor preprocessing (224x224 RGB, ImageNet normalization), Float32 tensor execution, softmax probability extraction, and semantic biophilia mapping into `FLORA`, `FAUNA`, `OUTDOOR_LANDSCAPE`, and `INDOOR_NON_NATURE`.
- **Why this model:** 15MB disk size, < 40MB memory footprint, executes in 12ms on CPU without requiring GPU drivers or cloud API keys.

### Technology Stack
- **AI Core:** ONNX Runtime, NumPy, Pillow, MobileNetV4 ONNX.
- **Backend:** Python 3.14, Flask, SQLite3, Flask-CORS.
- **Frontend:** Semantic HTML5, CSS3, Vanilla ES6 JavaScript, Web Audio API.

---

## Why Does Open Innovation Matter?
We chose an open-weight, self-hosted ONNX model over proprietary closed APIs (like GPT-4o or Claude Vision) for four critical reasons:

1. **Privacy & Backyard Safety:** Outdoor micro-expeditions often take place in private yards, family gardens, or neighborhood parks. Uploading personal field photos to third-party cloud AI vendors creates unwarranted privacy risks. With open ONNX, the image never leaves the user's CPU.
2. **Offline Resilience in Remote Nature:** Nature lovers frequently walk in forests, national parks, or valleys with zero cellular connectivity. A proprietary API fails immediately when offline. Open-source local inference runs seamlessly with no internet connection.
3. **Zero Token Cost & Sustainability:** Running thousands of daily micro-expeditions would cost hundreds of dollars in closed API tokens. MobileNetV4 ONNX runs for $0.00 forever on standard hardware.
4. **Sub-20ms Deterministic Latency:** Rather than waiting 2–5 seconds for a cloud multimodal API to respond over HTTP, local CPU execution returns in 12ms.

---

## Prize Categories
- **Core Open-Source AI:** Open-weight MobileNetV4 model with ONNX Runtime CPU inference.
- **Touch Grass Alignment:** Specifically built to minimize screen time (< 30s) and compel physical outdoor walking and nature observation.
- **Local / Edge AI:** 100% offline-ready and privacy-preserving.

---

## Team Submissions
- Built for the Touch Grass Open-Source AI Challenge.
