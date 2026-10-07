"""
Integration tests for TouchGrass AI Flask API endpoints.
Verifies /api/health, /api/expeditions/generate, /api/verify, /api/stats, and /api/history.
"""

import unittest
import io
from PIL import Image
from app import app
import database


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        database.init_db()

    def test_health_endpoint(self):
        """Verifies health check returns healthy status and ONNX model details."""
        res = self.client.get('/api/health')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['model_license'], 'Apache 2.0 (Open Source & Open Weight)')
        self.assertTrue(data['model_loaded'])

    def test_generate_expedition_endpoint(self):
        """Verifies expedition generation via API."""
        payload = {
            'duration_mins': 20,
            'biome': 'park'
        }
        res = self.client.post('/api/expeditions/generate', json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('quest', data)
        self.assertEqual(data['quest']['biome'], 'park')

    def test_verify_endpoint_with_image(self):
        """Verifies observation verification with uploaded image file."""
        # 1. Generate an expedition first
        gen_res = self.client.post('/api/expeditions/generate', json={'duration_mins': 15, 'biome': 'backyard'})
        quest_id = gen_res.get_json()['quest']['quest_id']

        # 2. Create in-memory synthetic image
        img = Image.new('RGB', (120, 120), color=(50, 160, 50))
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)

        # 3. Post multipart form to /api/verify
        res = self.client.post(
            '/api/verify',
            data={
                'expedition_id': quest_id,
                'actual_duration_mins': 15,
                'image': (img_bytes, 'leaf_photo.jpg')
            },
            content_type='multipart/form-data'
        )

        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('verification', data)
        self.assertIn('grass_score', data['verification'])

    def test_stats_and_history_endpoints(self):
        """Verifies /api/stats and /api/history endpoints return successfully."""
        res_stats = self.client.get('/api/stats')
        self.assertEqual(res_stats.status_code, 200)
        self.assertTrue(res_stats.get_json()['success'])

        res_hist = self.client.get('/api/history')
        self.assertEqual(res_hist.status_code, 200)
        self.assertTrue(res_hist.get_json()['success'])


if __name__ == '__main__':
    unittest.main()
