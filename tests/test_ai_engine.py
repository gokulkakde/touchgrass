"""
Unit tests for TouchGrass AI Inference Engine.
Verifies ONNX loading, preprocessing, classification, and latency.
"""

import unittest
import numpy as np
from PIL import Image
from ai_engine import classifier, BiophiliaClassifier


class TestAIEngine(unittest.TestCase):

    def setUp(self):
        self.classifier = classifier

    def test_model_is_loaded(self):
        """Verifies that the local MobileNetV4 ONNX model is loaded."""
        self.assertTrue(self.classifier.is_loaded, "ONNX model should be successfully loaded")
        self.assertIsNotNone(self.classifier.session, "InferenceSession should not be None")
        self.assertGreater(len(self.classifier.id2label), 0, "Labels mapping should not be empty")

    def test_image_preprocessing(self):
        """Verifies image preprocessing creates [1, 3, 224, 224] Float32 tensor."""
        test_img = Image.new('RGB', (400, 300), color=(120, 200, 80))
        tensor = self.classifier.preprocess(test_img)
        self.assertEqual(tensor.shape, (1, 3, 224, 224))
        self.assertEqual(tensor.dtype, np.float32)

    def test_foliage_inference(self):
        """Tests inference on synthetic foliage image."""
        # Create a deep green synthetic image
        img = Image.new('RGB', (224, 224), color=(34, 139, 34))
        result = self.classifier.classify_image(img)

        self.assertTrue(result['success'])
        self.assertIn('status', result)
        self.assertIn('grass_score', result)
        self.assertGreaterEqual(result['grass_score'], 0)
        self.assertLessEqual(result['grass_score'], 100)
        self.assertIn('latency_ms', result)
        self.assertGreater(result['latency_ms'], 0)
        self.assertEqual(result['inference_mode'], '100% Local CPU')

    def test_softmax_function(self):
        """Verifies numerically stable softmax sums to 1.0."""
        dummy_logits = np.array([2.0, 1.0, 0.1, -1.0])
        probs = self.classifier._softmax(dummy_logits)
        self.assertAlmostEqual(np.sum(probs), 1.0, places=5)
        self.assertTrue(np.all(probs >= 0.0))


if __name__ == '__main__':
    unittest.main()
