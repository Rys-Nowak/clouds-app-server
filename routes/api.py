from flask import Blueprint, request, jsonify
import base64
import cv2
import numpy as np
import matplotlib.pyplot as plt

from utils.validation import validate_base64_image
from utils.classification import predict_cloud_type

api = Blueprint('/api', __name__)

@api.route('/predict', methods = ['POST'])
def predict():
    try:
        data = request.get_json()
        if 'input' not in data:
            return jsonify({'error': 'No input image provided'}), 400

        input = data['input']
        if not validate_base64_image(input):
            return jsonify({'error': 'Invalid input image'}), 400

        input_bytes = base64.b64decode(input.split(',')[1])
        input_vector = np.frombuffer(input_bytes, dtype=np.uint8)
        input_img = cv2.imdecode(input_vector, cv2.IMREAD_COLOR) # BGR
        if input_img is None:
            return jsonify({'error': 'Failed to decode image'}), 400

        return {
            "Ac": 0.5,
            "Cc": 0.7,
            "Sc": 0.1,
            "Cu": 0.1,
            "St": 0.1,
            "As": 0.1,
            "Cs": 0.1,
            "Ns": 0.2,
            "Cb": 0.1,
            "Ci": 0.1,
            "Ct": 0.1,
        }
        return jsonify(predict_cloud_type(input_img)), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
