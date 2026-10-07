"""
Local Open-Source AI Inference Engine for TouchGrass AI.
Runs MobileNetV4 Small ONNX model completely offline via ONNX Runtime.
Performs semantic scene classification and biophilia detection.
"""

import os
import json
import time
import numpy as np
from PIL import Image

TECH_INDOOR_KEYWORDS = [
    'monitor', 'screen', 'keyboard', 'laptop', 'mouse', 'television', 'desk', 
    'table', 'chair', 'sofa', 'couch', 'cabinet', 'refrigerator', 'microwave', 
    'modem', 'printer', 'cell', 'cellular', 'phone', 'ipod', 'remote control',
    'cassette', 'hard disc', 'loudspeaker', 'toaster', 'espresso', 'projector',
    'notebook, notebook computer', 'desktop computer'
]

FLORA_KEYWORDS = [
    'plant', 'tree', 'leaf', 'flower', 'grass', 'moss', 'lichen', 'fern', 'acorn',
    'mushroom', 'agaric', 'bolete', 'earthstar', 'fungus', 'pine', 'conifer',
    'daisy', 'yellow lady\'s slipper', 'sunflower', 'dandelion', 'rose', 'orchid',
    'lotus', 'foliage', 'branch', 'wood', 'bark', 'bush', 'shrub', 'vine', 'seed',
    'pot, flowerpot', 'head cabbage', 'broccoli', 'cauliflower', 'zucchini',
    'cucumber', 'artichoke', 'bell pepper', 'hay', 'straw', 'corn'
]

LANDSCAPE_KEYWORDS = [
    'cliff', 'drop, drop-off', 'valley', 'vale', 'alp', 'volcano', 'promontory',
    'headland', 'seashore', 'coast', 'sandbar', 'sand bar', 'lakeside', 'lakeshore',
    'geyser', 'park bench', 'fountain', 'stone wall', 'dam', 'breakwater',
    'trail', 'path', 'forest', 'meadow'
]


class BiophiliaClassifier:
    def __init__(self, model_path='models/mobilenetv4_small.onnx', config_path='models/config.json'):
        self.model_path = model_path
        self.config_path = config_path
        self.session = None
        self.id2label = {}
        self.is_loaded = False
        self.input_name = None
        self.load_model()

    def load_model(self):
        """Loads the ONNX model and ImageNet label mappings."""
        if not os.path.exists(self.model_path):
            print(f"Warning: ONNX model not found at {self.model_path}")
            return False

        try:
            import onnxruntime as ort
            # Initialize ONNX Runtime session with CPU provider
            self.session = ort.InferenceSession(self.model_path, providers=['CPUExecutionProvider'])
            self.input_name = self.session.get_inputs()[0].name

            # Load labels if available
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
                    self.id2label = cfg.get('id2label', {})
            else:
                self.id2label = {str(i): f"class_{i}" for i in range(1000)}

            self.is_loaded = True
            print(f"Loaded MobileNetV4 ONNX model successfully from {self.model_path}")
            return True
        except Exception as e:
            print(f"Error loading ONNX model: {e}")
            self.is_loaded = False
            return False

    def preprocess(self, pil_image):
        """
        Preprocesses a PIL Image to the required Float32 tensor [1, 3, 224, 224].
        Normalizes with standard ImageNet mean and std.
        """
        # Ensure RGB
        img = pil_image.convert('RGB')
        # Resize maintaining aspect ratio then center crop to 224x224
        img = img.resize((256, 256), Image.Resampling.BILINEAR)
        left = (256 - 224) // 2
        top = (256 - 224) // 2
        img = img.crop((left, top, left + 224, top + 224))

        # Convert to numpy array in [0, 1]
        arr = np.array(img, dtype=np.float32) / 255.0

        # Standard ImageNet normalization
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        arr = (arr - mean) / std

        # Transpose from (H, W, C) to (C, H, W)
        arr = np.transpose(arr, (2, 0, 1))

        # Add batch dimension -> [1, 3, 224, 224]
        return np.expand_dims(arr, axis=0)

    def _softmax(self, x):
        """Numerically stable softmax."""
        e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e_x / np.sum(e_x, axis=-1, keepdims=True)

    def _categorize_label(self, idx, label_text):
        """Categorizes an ImageNet label into a Biophilia domain using index ranges and keywords."""
        idx = int(idx)
        lower = label_text.lower()
        
        # Check indoor/tech keywords first
        for kw in TECH_INDOOR_KEYWORDS:
            if kw in lower:
                return 'INDOOR_NON_NATURE'
                
        # ImageNet 0-397: Animals, Birds, Insects, Marine Life (Fauna)
        if 0 <= idx <= 397:
            return 'FAUNA'
            
        # Botanical and fungi classes
        if 984 <= idx <= 998 or any(k in lower for k in FLORA_KEYWORDS):
            return 'FLORA'
            
        # Natural geological formations and outdoor park elements
        if any(k in lower for k in LANDSCAPE_KEYWORDS):
            return 'OUTDOOR_LANDSCAPE'
            
        return 'ORGANIC_GENERAL'

    def classify_image(self, pil_image):
        """
        Runs local inference on an image and returns structured biophilia metrics.
        """
        if not self.is_loaded:
            # Attempt reloading
            if not self.load_model():
                return {
                    'success': False,
                    'error': 'ONNX model is not loaded.',
                    'latency_ms': 0
                }

        t_start = time.perf_counter()
        tensor = self.preprocess(pil_image)

        # Execute ONNX session
        outputs = self.session.run(None, {self.input_name: tensor})
        logits = outputs[0][0]
        probs = self._softmax(logits)

        latency_ms = round((time.perf_counter() - t_start) * 1000, 2)

        # Get top-5 predictions
        top5_indices = np.argsort(probs)[-5:][::-1]
        top_predictions = []
        for idx in top5_indices:
            label = self.id2label.get(str(idx), f"class_{idx}")
            prob = float(probs[idx])
            cat = self._categorize_label(idx, label)
            top_predictions.append({
                'class_id': int(idx),
                'label': label,
                'probability': round(prob, 4),
                'category': cat
            })

        top = top_predictions[0]
        top_cat = top['category']

        # Determine nature verification status
        is_nature = top_cat in {'FLORA', 'FAUNA', 'OUTDOOR_LANDSCAPE', 'ORGANIC_GENERAL'}
        is_indoor = top_cat == 'INDOOR_NON_NATURE'

        # Calculate Grass Touched Score (0 to 100)
        if is_indoor:
            grass_score = max(0, int(15 - (top['probability'] * 15)))
            feedback = f"Indoor environment detected ({top['label'].split(',')[0]}). No grass detected! Leave your desk and step outside."
            status = "rejected_indoor"
        else:
            # Score based on confidence and natural categorization
            base_score = 75
            if top_cat == 'FLORA':
                base_score = 90
            elif top_cat == 'FAUNA':
                base_score = 95
            elif top_cat == 'OUTDOOR_LANDSCAPE':
                base_score = 85
            grass_score = min(100, int(base_score + (top['probability'] * 10)))
            clean_label = top['label'].split(',')[0].title()
            feedback = f"Natural element identified: {clean_label} ({top_cat.replace('_', ' ').title()}). Touch grass verified!"
            status = "verified_nature"

        return {
            'success': True,
            'status': status,
            'is_nature': is_nature,
            'grass_score': grass_score,
            'biophilia_category': top_cat,
            'primary_identification': top['label'].split(',')[0].strip(),
            'confidence': round(top['probability'] * 100, 1),
            'top_predictions': top_predictions,
            'feedback': feedback,
            'latency_ms': latency_ms,
            'model_name': 'MobileNetV4 Conv Small (ONNX Local)',
            'inference_mode': '100% Local CPU'
        }


# Singleton classifier instance
classifier = BiophiliaClassifier()
