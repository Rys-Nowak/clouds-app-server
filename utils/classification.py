from typing import *
import numpy as np
import cv2
from utils.horizon_detection import trim_horizon

from flask import current_app


def preprocess(input_img: np.ndarray, trim_horizon_flag: bool=False):
    out_img = input_img
    if trim_horizon_flag:
        out_img = trim_horizon(out_img)

    out_img = cv2.resize(out_img, (224, 224))
    return out_img

def predict_cloud_type(input_img: np.ndarray, trim_horizon_flag: bool=False) -> Dict[str, float]:
    cls = current_app.config['cls']
    img = preprocess(input_img, trim_horizon_flag)
    pred = cls.predict(img)
    result = {}
    for i, val in enumerate(pred):
        result.update({cls.get_label(i): str(val)})

    return result
