# PRODUCT SPECIFICATION: TouchGrass AI

## 1. Problem Statement
Modern knowledge workers, developers, and students spend upwards of 8–12 hours a day trapped behind screens. This causes digital eye strain, attention fatigue, and "nature deficit disorder." When individuals do find 10–30 minutes of downtime, decision paralysis and dopamine loops lead them straight back to scrolling social media or staring at notifications. Existing fitness and trail apps often compound this problem: they demand constant interaction, turn-by-turn screen gazing, social feed consumption, or paid cloud subscriptions.

## 2. Target Users
- **Software Engineers & Remote Workers:** Suffer from screen lock-in and desk stiffness between meetings or coding sprints.
- **Students & Writers:** Experience mental fatigue and need brief, structured grounding breaks.
- **Everyday Nature Seekers:** Want quick, purposeful motivation to step outside without spending 20 minutes planning an elaborate hike.

## 3. Current Behavior vs. TouchGrass AI

| Aspect | Current Behavior | TouchGrass AI |
|---|---|---|
| Screen Time | 10–30 minutes browsing feeds or planning routes | **< 30 seconds** to generate quest and enter Pocket Mode |
| Outdoor Presence | Glancing at screens for GPS, maps, or messages | Phone goes into pocket; sensory observation takes over |
| AI Interaction | Chatting back-and-forth with cloud chatbots | Instant local generation + offline sensory mission |
| Verification | Manual check-ins or fitness tracker telemetry | **Local Open-Source Vision AI** verifies organic field findings in 12ms |
| Privacy | Location traces and photos uploaded to cloud servers | **100% Local Inference** on device; zero cloud telemetry |

## 4. Product Solution
TouchGrass AI is a micro-expedition dispatch engine designed under a strict non-negotiable principle: **The screen should be the shortest part of the experience.**

The user experience follows a 5-step loop:
1. **Quick Dispatch (5 seconds):** Select available time (5m, 15m, 30m, 60m) and immediate environment (Park, Backyard, City Street, Trail, Waterfront).
2. **Sensory Quest Synthesizer (Instant):** Generates a structured micro-quest containing one clear mission brief, two sensory focus tasks (listening, texture, pacing), and one outdoor observation target to spot.
3. **Pocket Mode (Lock Screen):** The screen dims to a minimalist, ambient high-contrast timer. An audible prompt reminds the user: *"Screen off. Step outside. Touch grass."*
4. **Real-World Action:** The user walks outside, engages their physical senses, disconnects from digital noise, and snaps exactly one field photo of a natural element.
5. **Local AI Biophilia Verification:** Back at their desk (or upon returning), the local open-source vision model runs on CPU in ~12ms. It verifies real flora/fauna/landscape vs. indoor office clutter, records outdoor minutes, and logs the field discovery to a local private journal.

## 5. AI Role
- **Core Open Model:** MobileNetV4 Small (Apache 2.0 license) executed via ONNX Runtime on CPU.
- **Inference Objective:** Semantic scene understanding and organic classification. Distinguishes natural organic matter (flora, fungi, wildlife, sky, geological formations, foliage) from indoor screen environments (monitors, keyboards, desks, phones).
- **Quest Dispatcher:** Deterministic, context-grounded micro-expedition synthesizer that maps time constraints and biomes into actionable, safe sensory tasks.

## 6. Open-Source Role
Open-source AI is non-negotiable for TouchGrass:
- **Zero API Dependency / Offline First:** Works deep in wilderness, parks, or low-connectivity zones without requiring cell service.
- **Total Privacy:** Field photos of private backyards, neighborhood spots, or personal spaces are never transmitted over the internet.
- **Zero Ongoing Cost:** No tokens, subscriptions, or vendor lock-in.

## 7. Touch Grass Mechanism
- Screen interaction limit: UI emphasizes closing or pocketing the phone immediately.
- Sensory tasks require physical presence (touching tree bark, listening to wind/birds, counting steps away from asphalt).
- Rejection of indoor photos: Taking a picture of your computer monitor or keyboard returns an indoor warning with zero points awarded.

## 8. Success Metrics
- **Disconnect Ratio:** Minutes spent outdoors vs. seconds spent on screen (target: > 30:1).
- **Expeditions Completed:** Real-world walks finished and verified.
- **Biophilia Encounters:** Unique flora, fauna, and outdoor textures identified locally.
- **Outdoor Minutes Logged:** Cumulative time spent touching grass.
