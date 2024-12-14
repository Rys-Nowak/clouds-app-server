from flask import Blueprint

api = Blueprint('/api', __name__)

@api.route('/predict')
def predict():
    return {
        "Ac": 0.5,
        "Cc": 0.5
    }
