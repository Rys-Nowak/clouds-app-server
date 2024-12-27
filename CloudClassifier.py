import keras
import tensorflow as tf
import numpy as np


@keras.saving.register_keras_serializable("Custom")
class AugmentationLayer(keras.layers.Layer):
    def __init__(self, tranforms=None, **kwargs):
        super(AugmentationLayer, self).__init__(**kwargs)

    def get_config(self):
        config = super(AugmentationLayer, self).get_config()
        return config

    def call(self, inputs, training=None):
        if training:
            # Irrelevant during prediction
            pass

        return inputs

class CloudClassifier:
    model_path: str = 'keras_models/classifier.keras'
    class_to_label = {
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

    def __init__(self):
        self.model = None

    def load_model(self):
        print("Loading model...")
        self.model = keras.saving.load_model(self.model_path)
        self.model.summary()
        print("Loading completed")

    def clear_model(self):
        self.model = None

    def predict(self, img: np.ndarray):
        if self.model is None:
            raise ValueError("Model is not loaded")

        return self.model.predict(tf.convert_to_tensor(img[np.newaxis, :]))[0]

    def get_label(self, class_num: int):
        return self.class_to_label.get(class_num)
