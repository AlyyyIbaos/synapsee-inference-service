import numpy as np
import tensorflow as tf

MODEL_PATH = "model/synapsee_cnnlstm_30k.keras"


def load_model():
    """
    Load the trained CNN-LSTM TensorFlow model.
    """
    model = tf.keras.models.load_model(MODEL_PATH)
    return model


def predict_from_features(model, payload: dict):
    """
    Run prediction on a sequence of features.
    Expected input shape: (60, 12) or (1, 60, 12)
    """

    if "sequence" not in payload:
        return {"error": "Missing 'sequence' in request body"}

    # Convert input to numpy array
    seq = np.array(payload["sequence"], dtype=np.float32)

    # Accept (60,12) or (1,60,12)
    if seq.ndim == 2:
        seq = np.expand_dims(seq, axis=0)

    if seq.ndim != 3:
        return {
            "error": f"Invalid shape {seq.shape}. Expected (60,12) or (1,60,12)"
        }

    if seq.shape[1] != 60 or seq.shape[2] != 12:
        return {
            "error": f"Wrong shape {seq.shape}. Expected (1,60,12)"
        }

    # Run inference
    preds = model.predict(seq, verbose=0)

    score = float(preds[0][0])
    label = "cheating" if score >= 0.5 else "normal"

    return {
        "cheating_score": score,
        "label": label
    }
