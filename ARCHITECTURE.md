# ARCHITECTURE: TouchGrass AI

## 1. System Overview

TouchGrass AI is designed with a lightweight, decoupled architecture prioritizing zero screen time, low latency, and offline independence.

```mermaid
flowchart TD
    User([User at Screen]) -->|Selects Time & Biome <5s| UI[Web Frontend: Responsive UI]
    UI -->|POST /api/expeditions/generate| BE[Backend API: Flask Service]
    BE -->|Synthesize Grounded Micro-Quest| QuestGen[Quest Generator Engine]
    QuestGen -->|Structured Quest JSON| UI
    
    UI -->|Activates Pocket Mode| Pocket[Pocket Mode: Screen Dims / Minimal Timer]
    Pocket -->|User Steps Away from Desk| RealWorld[Real-World Physical Expedition]
    
    RealWorld -->|Walks 15-30m, Touches Grass, Takes 1 Photo| FieldPhoto[Field Photo Captured]
    FieldPhoto -->|Upload Photo| BE
    
    BE -->|Preprocessing 224x224 RGB| Preproc[Image Pipeline: Pillow + NumPy]
    Preproc -->|Float32 Tensor [1, 3, 224, 224]| ORT[ONNX Runtime 1.30 Local CPU Engine]
    ORT -->|Execute Open Weights| Model[(MobileNetV4 Small ONNX 15MB)]
    Model -->|1000 Class Logits in 12ms| BioClassifier[Biophilia & Scene Classifier]
    
    BioClassifier -->|Check Nature vs. Indoor Screen| Verdict{Nature Detected?}
    Verdict -->|Yes: Flora / Fauna / Landscape| Verified[Verified Grass Touched + Score Awarded]
    Verdict -->|No: Monitor / Keyboard / Desk| Rejected[Rejection: 'Step Outside!']
    
    Verified -->|Update Offline Journal| DB[(Local SQLite DB: expeditions.db)]
    Verified -->|Show Result & Prompt to Disconnect| UI
```

## 2. Layer Breakdown

### A. Frontend Layer
- **Tech:** Clean semantic HTML5, modern CSS3 (high-contrast, responsive, dark/light outdoor readable mode), vanilla JavaScript ES6.
- **Responsiveness:** Optimized for both mobile devices (phones carried outside) and desktop workstations (where knowledge workers initiate their break).
- **Audio Feedback:** Web Audio API native synthesizer for calming nature chimes and departure bells without heavy external audio asset downloads.
- **Pocket Mode:** Minimal ambient display showing elapsed outdoor time, screen-off recommendations, and high-visibility controls.

### B. Backend Layer
- **Tech:** Python 3.14 + Flask 3.0 + Flask-CORS.
- **Endpoints:**
  - `GET /` — Serves main responsive application.
  - `POST /api/expeditions/generate` — Dispatches customized micro-quests based on duration and biome.
  - `POST /api/verify` — Processes uploaded field photos, runs local ONNX inference, and returns biophilia analysis.
  - `GET /api/history` — Returns recent completed expeditions.
  - `GET /api/stats` — Returns total minutes touched, streak count, and biophilia diversity breakdown.
  - `GET /api/health` — Reports model availability, ONNX runtime status, and hardware latency.

### C. Open-Source AI Inference Layer
- **Runtime:** `onnxruntime` CPU provider.
- **Model:** `mobilenetv4_small.onnx` (15.08 MB).
- **Taxonomy Engine:** Maps 1,000 ImageNet categories into biological and environment buckets:
  - `FLORA`: Wildflowers, trees, mushrooms, grasses, leaves, foliage, lichens.
  - `FAUNA`: Birds, bees, butterflies, small mammals, reptiles, insects.
  - `OUTDOOR_LANDSCAPE`: Hills, lakes, seashores, cliffs, public parks, footpaths.
  - `INDOOR_NON_NATURE`: Desktop computers, displays, television screens, keyboards, desks.
- **Latency:** ~12ms per execution.

### D. Data Storage Layer
- **Database:** Local SQLite (`data/expeditions.db`).
- **Schema:**
  - `expeditions`: Stores `id`, `created_at`, `duration_target`, `duration_actual`, `biome`, `mission_title`, `status` (`pending`, `completed`, `rejected`).
  - `verifications`: Stores `id`, `expedition_id`, `top_label`, `confidence`, `biophilia_category`, `grass_score`, `verified_at`.
- **Zero Cloud Storage:** All data stays on the local filesystem.

## 3. Data Flow & Security
1. No telemetry or tracking scripts.
2. No third-party API credentials needed or stored.
3. Completely safe to operate in air-gapped or offline outdoor scenarios.
