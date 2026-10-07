# AI STACK: TouchGrass AI

## 1. Selected Model Specification

| Attribute | Value |
|---|---|
| **Model Name** | MobileNetV4 Conv Small (`mobilenetv4_conv_small.e1200_r224_in1k`) |
| **Model Version** | ONNX Release 1.0 (ImageNet-1k trained) |
| **Model License** | **Apache 2.0** (Open-source, commercial-friendly, open-weight) |
| **Model Source / Repo** | [Hugging Face: onnx-community/mobilenetv4_conv_small.e1200_r224_in1k](https://huggingface.co/onnx-community/mobilenetv4_conv_small.e1200_r224_in1k) |
| **Framework / Runtime** | **ONNX Runtime 1.30.0** (Linux Foundation open runtime) |
| **Hardware Requirements** | Standard x86_64 or ARM64 CPU (No GPU or VRAM required; < 50MB RAM footprint) |
| **Model File Size** | 15.08 MB (`models/mobilenetv4_small.onnx`) |
| **Execution Mode** | **100% Local Inference** on device CPU |
| **Internet Required?** | **No** (Fully operational offline once local ONNX model file is present) |
| **Model Swappability** | Fully swappable with any standard ONNX vision classifier (ResNet, SqueezeNet, EfficientNet, ViT) |

## 2. Why This Model Was Selected
1. **Lightweight & Fast:** Executes inference in **~12 milliseconds** on an average CPU. No GPU hardware or CUDA drivers are needed.
2. **True Open Source:** Released under the permissive **Apache 2.0 license**, guaranteeing open weight inspection, redistribution, and freedom from proprietary lock-in.
3. **Broad Botanical & Nature Taxonomy:** Pre-trained on 1,000 ImageNet categories covering extensive flora (trees, flowers, mushrooms, acorns, leaves), fauna (songbirds, insects, mammals, amphibians), geological formations (valleys, cliffs, seashores), and contrasting indoor objects (monitors, keyboards, cell phones, desks).
4. **Offline Resilience:** Enables outdoor operation on battery power without cellular signal.

## 3. Input & Output Formats

### Input
- **Format:** Image tensor (RGB normalized)
- **Dimensions:** `[1, 3, 224, 224]` (Batch size 1, 3 channels, 224x224 pixels)
- **Tensor Type:** Float32
- **Preprocessing Pipeline:**
  1. Pillow loads JPEG/PNG/WebP.
  2. Bilinear resize and center crop to 224x224.
  3. Channel rescaling to `[0.0, 1.0]`.
  4. Standard ImageNet normalization: Mean `[0.485, 0.456, 0.406]`, Std `[0.229, 0.224, 0.225]`.
  5. Dimension transpose to `(C, H, W)`.

### Output
- **Raw Logits:** Tensor shape `[1, 1000]` Float32.
- **Post-processing:**
  1. Softmax probability conversion.
  2. Top-5 candidate class extraction with confidence scores.
  3. **Biophilia Semantic Mapping:** Classification into high-level categories:
     - `FLORA` (Plants, leaves, trees, flowers, lichen, fungus)
     - `FAUNA` (Birds, insects, wildlife, pollinators)
     - `OUTDOOR_LANDSCAPE` (Geology, paths, water, skies, park structures)
     - `INDOOR_NON_NATURE` (Computer screens, desks, keyboards, appliances)
  4. Decision rule: If indoor non-nature dominates, flag with `grass_touched: false` and reject with friendly prompt to step away from the screen.

## 4. Latency & Resource Benchmarks
- **CPU Inference Time:** 11–16 ms on Intel/AMD x86_64 CPU.
- **Memory Consumption:** ~38 MB peak RSS.
- **Disk Footprint:** 15.08 MB (model) + 120 KB (taxonomy config).

## 5. Known Limitations & Mitigation
- **Extreme Macro Close-ups:** Very blurry or low-light close-ups may exhibit lower confidence. Handled gracefully with fallback confidence scoring and soft thresholding.
- **Indoor Houseplants:** May register as flora. The verification prompt explicitly nudges users to outdoor biomes, and the app pairs verification with elapsed outdoor timer logs.
