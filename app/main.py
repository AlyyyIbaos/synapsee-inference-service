from fastapi import FastAPI
from app.model_loader import load_model, predict_from_features

app = FastAPI()
_model = None

@app.on_event("startup")
def startup_event():
    global _model
    _model = load_model()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: dict):
    return predict_from_features(_model, payload)
