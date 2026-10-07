"""
Model Download & Setup Script for TouchGrass AI.
Downloads the open-weight MobileNetV4 Small ONNX model (Apache 2.0 license)
from the open Hugging Face repository into models/ directory.
"""

import os
import requests

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
CONFIG_URL = 'https://huggingface.co/onnx-community/mobilenetv4_conv_small.e1200_r224_in1k/raw/main/config.json'
MODEL_URL = 'https://huggingface.co/onnx-community/mobilenetv4_conv_small.e1200_r224_in1k/resolve/main/onnx/model.onnx'

CONFIG_PATH = os.path.join(MODEL_DIR, 'config.json')
MODEL_PATH = os.path.join(MODEL_DIR, 'mobilenetv4_small.onnx')


def setup_models():
    os.makedirs(MODEL_DIR, exist_ok=True)

    if not os.path.exists(CONFIG_PATH):
        print(f"Downloading model config and taxonomy from {CONFIG_URL}...")
        r = requests.get(CONFIG_URL, timeout=30)
        r.raise_for_status()
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            f.write(r.text)
        print("Taxonomy config saved.")
    else:
        print(f"Taxonomy config already present at {CONFIG_PATH}")

    if not os.path.exists(MODEL_PATH):
        print(f"Downloading open-weight MobileNetV4 ONNX (~15MB) from {MODEL_URL}...")
        r = requests.get(MODEL_URL, stream=True, timeout=60)
        r.raise_for_status()
        with open(MODEL_PATH, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
        print(f"Model saved successfully to {MODEL_PATH} ({os.path.getsize(MODEL_PATH)} bytes)")
    else:
        print(f"Model already present at {MODEL_PATH} ({os.path.getsize(MODEL_PATH)} bytes)")


if __name__ == '__main__':
    setup_models()
