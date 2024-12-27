from flask import Blueprint, request, jsonify
import base64
import cv2
import numpy as np

from flask import current_app

from utils.validation import validate_base64_image
from utils.classification import predict_cloud_type


api = Blueprint('/api', __name__)

@api.route('/predict', methods = ['POST'])
def predict():
    try:
        data = request.get_json()
        if 'input' not in data:
            return jsonify({'error': 'No input image provided'}), 400
        
        trim_horizon_flag = True
        if data.get('horizon') == False:
            trim_horizon_flag = False

        input = data['input']
        if not validate_base64_image(input):
            return jsonify({'error': 'Invalid input image'}), 400

        input_bytes = base64.b64decode(input.split(',')[1])
        input_vector = np.frombuffer(input_bytes, dtype=np.uint8)
        input_img_bgr = cv2.imdecode(input_vector, cv2.IMREAD_COLOR)
        if input_img_bgr is None:
            return jsonify({'error': 'Failed to decode image'}), 400

        input_img = cv2.cvtColor(input_img_bgr, cv2.COLOR_BGR2RGB)
        try:
            return jsonify(predict_cloud_type(input_img, trim_horizon_flag)), 200
        except Exception as e:
            return jsonify({'error': 'Prediction failed: '+str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@api.route('/reload', methods = ['POST'])
def reload_model():
    try:
        current_app.config['cls'].load_model()
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/clear', methods = ['POST'])
def clear_model():
    current_app.config['cls'].clear_model()
    return jsonify(), 204
