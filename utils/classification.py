from typing import *
import numpy as np
import keras


MODEL_PATH = 'keras/classifier.keras'
CLASS_TO_LABEL = {
    0: 'Ac',
    1: 'As',
    2: 'Cb',
    3: 'Cc',
    4: 'Ci',
    5: 'Cs',
    6: 'Ct',
    7: 'Cu',
    8: 'Ns',
    9: 'Sc',
    10: 'St'
}

def predict_cloud_type(input_img: np.ndarray) -> Dict[str, float]:
    cls = keras.saving.load_model(MODEL_PATH)
    pred = cls.predict(np.array([input_img]))
    result = {}
    for label, val in zip(CLASS_TO_LABEL.values(), pred[0]):
        result.update({label: str(val)})

    return result
