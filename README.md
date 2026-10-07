# TouchGrass AI 🌱

> **The Screen Ends Here. Your Expedition Begins.**  
> An open-source AI micro-expedition engine designed to get people off the screen and into the real world. Powered by local **MobileNetV4 ONNX** running on CPU in ~12 milliseconds.

---

## Problem
Modern developers, engineers, and desk workers spend 8–12 hours daily staring at glowing screens. During short 15-minute breaks, cognitive fatigue and decision paralysis drive users right back into screen dopamine loops and doomscrolling. Traditional navigation and fitness apps make the problem worse: they require constant screen-gazing, route tracking, and cloud data harvesting.

## Solution
**TouchGrass AI** operates on a non-negotiable principle: **The screen should be the shortest part of the experience.**
- **Screen Time < 30 seconds:** Select time budget (5m, 15m, 30m, 60m) and immediate biome (Park, Backyard, Urban, Trail, Waterfront).
- **Sensory Micro-Quest:** AI synthesizes an actionable outdoor mission with physical, off-screen sensory objectives (feeling tree bark, counting birdsong, escaping asphalt).
- **Pocket Mode:** Screen dims to an ambient timer, plays a calming departure chime, and instructs you to pocket the phone and step outside.
- **Physical Outdoor Action:** Walk, observe nature, disconnect from digital noise, and capture exactly one field photo.
- **Local AI Biophilia Verification:** Local open-source computer vision classifies the finding in 12ms, awards a Grass Touched score, logs outdoor minutes to a private SQLite journal, and flags indoor computer monitors or keyboards.

---

## Demo
- **Demo Script & Video Plan:** See [DEMO_SCRIPT.md](file:///d:/hactoberfest/week1/DEMO_SCRIPT.md) for scene-by-scene timing.
- **Quick Local Demo:** Run `python app.py` and open `http://127.0.0.1:5000`.

---

## Features
- **Ultra-Fast Dispatch:** Dispatches missions in under 5 seconds with zero unnecessary forms.
- **Biophilia Sensory Engine:** Grounded sensory tasks tailored to 5 distinct biomes.
- **Ambient Pocket Mode:** High-contrast, battery-friendly outdoor timer with Web Audio synthesized departure and return chimes.
- **100% Local Open-Source AI:** MobileNetV4 Small ONNX model runs on CPU in ~12ms. Zero cloud API calls.
- **Indoor Tech Rejection:** Rejects desktop computer screens, keyboards, and office furniture with gentle nudges to step outside.
- **Private Offline Journal:** Tracks outdoor minutes, expeditions, and daily streaks locally via SQLite.

---

## How It Works
```text
USER PROBLEM (Screen fatigue / desk lock-in)
       ↓
SHORT SCREEN INTERACTION (< 30 seconds)
       ↓
AI-POWERED DECISION (Synthesizes sensory outdoor quest)
       ↓
POCKET MODE (Screen dims, audio chime, phone goes into pocket)
       ↓
REAL-WORLD ACTION (15 min outdoor walk, sensory immersion)
       ↓
REAL-WORLD RESULT (Observation captured: leaf, flower, bird, tree)
       ↓
LOCAL AI VERIFICATION (MobileNetV4 ONNX runs on CPU in 12ms)
       ↓
PRIVATE JOURNAL LOG (Outdoor minutes and streaks recorded locally)
```

---

## Open-Source AI
- **Model Name:** `mobilenetv4_conv_small.e1200_r224_in1k`
- **Model License:** **Apache 2.0 (Permissive Open Source & Open Weight)**
- **Runtime:** **ONNX Runtime 1.30.0 (Linux Foundation AI & Data)**
- **Hardware Requirement:** Standard CPU (No GPU or CUDA required; < 40MB RAM)
- **Model Size:** 15.08 MB (`models/mobilenetv4_small.onnx`)
- **Latency:** ~12ms per inference on standard CPU

For detailed specifications, see [AI_STACK.md](file:///d:/hactoberfest/week1/AI_STACK.md).

---

## Why Open AI?
1. **Total Privacy:** Field photos of personal gardens, neighborhoods, and backyards are never uploaded to commercial third-party cloud servers.
2. **Offline Resilience:** Functions in remote state parks, hiking trails, or zones with zero cellular connectivity.
3. **Zero Recurring Cost:** Completely free from API subscriptions, per-token billing, or proprietary rate limits.
4. **Instant 12ms Latency:** Local CPU inference is 20x faster than cloud multimodal API round-trips.

---

## Architecture
```text
Frontend (HTML5 / CSS3 / Vanilla JS / Web Audio API)
   ↓
REST API (Python 3.14 / Flask 3.0)
   ↓
Quest Engine (quest_generator.py)
   ↓
Local ONNX Runtime 1.30 (ai_engine.py)
   ↓
MobileNetV4 Small ONNX (15MB local weights)
   ↓
Local SQLite Storage (data/expeditions.db)
```
For detailed architecture flow and component diagrams, see [ARCHITECTURE.md](file:///d:/hactoberfest/week1/ARCHITECTURE.md).

---

## Tech Stack
- **AI Core:** ONNX Runtime, NumPy, Pillow, MobileNetV4 ONNX
- **Backend:** Python 3.14, Flask, Flask-CORS, SQLite3
- **Frontend:** HTML5, CSS3, ES6 JavaScript, Web Audio API
- **Testing:** Python `unittest` framework

---

## Local Setup

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Git

### 2. Clone Repository
```bash
git clone https://github.com/your-username/touchgrass-ai.git
cd touchgrass-ai
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify / Download Model Weights
The repository automatically includes or downloads the open-weight model:
```bash
python download_models.py
```

### 5. Run the Application
```bash
python app.py
```
Open your browser at `http://127.0.0.1:5000`.

---

## Environment Variables
Copy `.env.example` to `.env`:
```env
FLASK_ENV=production
FLASK_PORT=5000
FLASK_HOST=127.0.0.1
MODEL_PATH=models/mobilenetv4_small.onnx
CONFIG_PATH=models/config.json
DB_PATH=data/expeditions.db
```
*Note: No proprietary third-party API keys are needed.*

---

## Running the AI Model
You can test the AI vision classifier directly from the command line:
```bash
python -c "
from PIL import Image
from ai_engine import classifier
img = Image.new('RGB', (224, 224), color=(34, 139, 34))
res = classifier.classify_image(img)
print(res)
"
```

---

## Testing
Run the automated test suite:
```bash
python -m unittest discover -s tests -p "test_*.py"
```
See [TESTING.md](file:///d:/hactoberfest/week1/TESTING.md) for full coverage and real-world outdoor validation details.

---

## Privacy
- All images are processed strictly in-memory on your local CPU.
- No telemetry, analytics, or cloud trackers.
- Database records remain 100% on your local disk (`data/expeditions.db`).

---

## Limitations
- Model is optimized for macroscopic flora, fauna, and scenery. Extreme low-light close-ups may have reduced confidence.
- Indoor houseplants may trigger flora recognition; pairing with elapsed outdoor timer logs mitigates false claims.

---

## Future Improvements
- Audio birdsong spectrogram classifier using local ONNX audio model.
- PWA (Progressive Web App) manifest for one-tap home screen installation on mobile.
- Bluetooth Low Energy (BLE) integration with smart pedometers for step verification.

---

## License
- Application Code: **MIT License**
- Model Weights: **Apache 2.0 License** (MobileNetV4 ONNX)
