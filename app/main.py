from fastapi import FastAPI, HTTPException
from app.model_loader import load_model, predict_from_features

app = FastAPI()

_model = None


@app.on_event("startup")
def startup_event():
    """
    Load the CNN-LSTM model once when the service starts.
    """
    global _model
    try:
        _model = load_model()
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Failed to load model: {e}")
        _model = None


@app.get("/health")
def health():
    """
    Health check endpoint.
    """
    return {
        "status": "ok",
        "model_loaded": _model is not None
    }


@app.post("/predict")
def predict(payload: dict):
    """
    Run inference using the loaded CNN-LSTM model.
    """
    if _model is None:
        # Safety check for cold start or load failure
        raise HTTPException(
            status_code=503,
            detail="Model not loaded yet. Please try again later."
        )

    return predict_from_features(_model, payload)
