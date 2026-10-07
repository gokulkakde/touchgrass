"""
TouchGrass AI - Flask Server & REST API.
Dispatches outdoor micro-expeditions and verifies natural field observations via local ONNX inference.
"""

import os
import io
import time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from PIL import Image

from ai_engine import classifier
from quest_generator import generate_quest
import database

app = Flask(__name__)
CORS(app)

# Ensure database is initialized
database.init_db()


@app.route('/')
def index():
    """Serves the main single-page application."""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Returns AI model status, runtime architecture, and open-source license information."""
    return jsonify({
        'status': 'healthy',
        'app_name': 'TouchGrass AI',
        'model_name': 'MobileNetV4 Conv Small (ONNX)',
        'model_license': 'Apache 2.0 (Open Source & Open Weight)',
        'runtime': 'ONNX Runtime 1.30.0 (CPU Local)',
        'model_loaded': classifier.is_loaded,
        'inference_target': '100% Local Device CPU (Offline Ready)',
        'timestamp': time.time()
    })


@app.route('/api/expeditions/generate', methods=['POST'])
def api_generate_expedition():
    """
    Synthesizes and registers an outdoor micro-expedition based on time and biome.
    Screen interaction designed to complete in < 5 seconds.
    """
    data = request.get_json(silent=True) or {}
    duration = int(data.get('duration_mins', 15))
    biome = data.get('biome', 'park')

    quest = generate_quest(duration_mins=duration, biome=biome)
    database.save_expedition(quest)

    return jsonify({
        'success': True,
        'quest': quest
    }), 201


@app.route('/api/verify', methods=['POST'])
def api_verify_observation():
    """
    Receives an outdoor field photograph, runs local ONNX vision inference,
    evaluates organic biophilia vs. indoor screen, and updates the local journal.
    """
    expedition_id = request.form.get('expedition_id')
    duration_str = request.form.get('actual_duration_mins')
    actual_duration = int(duration_str) if duration_str and duration_str.isdigit() else 15

    if not expedition_id:
        return jsonify({
            'success': False,
            'error': 'Missing required expedition_id parameter.'
        }), 400

    if 'image' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No image file uploaded in field "image".'
        }), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'Uploaded file is empty.'
        }), 400

    try:
        # Open and validate image with Pillow
        image_bytes = file.read()
        pil_img = Image.open(io.BytesIO(image_bytes))

        # Run local ONNX inference
        result = classifier.classify_image(pil_img)

        # Record to local SQLite database
        database.record_verification(expedition_id, result, actual_duration)

        return jsonify({
            'success': True,
            'verification': result
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to process image: {str(e)}'
        }), 500


@app.route('/api/history', methods=['GET'])
def api_history():
    """Returns recent micro-expedition logs."""
    history = database.get_history(limit=20)
    return jsonify({
        'success': True,
        'history': history
    })


@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Returns cumulative outdoor disconnect metrics and streak information."""
    stats = database.get_stats()
    return jsonify({
        'success': True,
        'stats': stats
    })


if __name__ == '__main__':
    # Running locally on port 5000
    app.run(host='127.0.0.1', port=5000, debug=False)
