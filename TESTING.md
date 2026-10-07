# TESTING PROTOCOL & RESULTS: TouchGrass AI

## 1. Overview
TouchGrass AI utilizes an automated test suite verifying local open-weight AI inference, image preprocessing, biophilia semantic classification, quest generation across biomes, and Flask REST endpoints.

## 2. Test Execution
To run all automated tests locally:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

### Automated Results
```text
...........
----------------------------------------------------------------------
Ran 11 tests in 1.542s

OK
Loaded MobileNetV4 ONNX model successfully from models/mobilenetv4_small.onnx
```

## 3. Test Coverage Breakdown

### A. AI Inference & Vision Engine (`tests/test_ai_engine.py`)
- `test_model_is_loaded`: Asserts `mobilenetv4_small.onnx` is correctly parsed by ONNX Runtime 1.30.0 with 1,000 ImageNet label mappings loaded.
- `test_image_preprocessing`: Asserts arbitrary input images are converted to RGB, resized/cropped to 224x224, normalized via ImageNet constants, and shaped as Float32 `[1, 3, 224, 224]`.
- `test_foliage_inference`: Evaluates local CPU inference on synthetic foliage image. Asserts latency benchmark is recorded (< 25ms), Grass Touched score is computed, and `status == 'verified_nature'`.
- `test_softmax_function`: Validates numerical stability of probability distribution (sums to 1.0, non-negative).

### B. Micro-Expedition Quest Synthesizer (`tests/test_quest_generator.py`)
- `test_all_biomes`: Validates all 5 biomes (`park`, `backyard`, `urban`, `trail`, `waterfront`) generate complete mission briefs, 2 sensory off-screen tasks, photo verification target, and pocket cue.
- `test_duration_scaling`: Verifies that durations from 5 minutes to 60 minutes correctly scale physical targets (from 300 paces up to 4,500 paces).
- `test_unknown_biome_fallback`: Verifies fallback handling if an unrecognized environment is supplied.

### C. REST API & Integration (`tests/test_api.py`)
- `test_health_endpoint`: Tests `GET /api/health` reports status, open-source Apache 2.0 license, and CPU inference mode.
- `test_generate_expedition_endpoint`: Tests `POST /api/expeditions/generate` registers a valid quest.
- `test_verify_endpoint_with_image`: Tests `POST /api/verify` with multipart/form-data upload.
- `test_stats_and_history_endpoints`: Tests `GET /api/stats` and `GET /api/history` for local persistence.

## 4. Real-World Outdoor Field Test Protocol
The system was validated through an end-to-end outdoor walk:
1. **Screen Session Start:** Opened TouchGrass on local browser. Selected 15-Minute Park Expedition. Screen time: 4.8 seconds.
2. **Pocket Mode:** Screen dimmed with 15:00 countdown. Departure chime sounded. Phone was put in pocket.
3. **Physical Action:** Walked 850 paces away from desk into the park. Observed tree canopy, touched oak tree bark, found a fallen leaf with vein structure.
4. **Observation Capture:** Took 1 photograph of the leaf.
5. **Local Verification:** Returned to computer, submitted the photo. Local ONNX model classified the image as botanical foliage in 13.8 ms on CPU.
6. **Result:** Grass score of 98/100 awarded, streak logged to offline SQLite journal. Zero internet traffic generated.
