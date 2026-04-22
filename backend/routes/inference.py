from __future__ import annotations

import numpy as np
import torch
from fastapi import APIRouter, File, HTTPException, UploadFile

from utils.model_registry import registry
from utils.preprocessing import preprocess_csrnet_image, preprocess_lstm_sequence
from utils.risk import evaluate_risk
from utils.schemas import (
    PredictCountResponse,
    PredictFutureRequest,
    PredictFutureResponse,
    RiskRequest,
    RiskResponse,
)


router = APIRouter(tags=["inference"])


@router.post("/predict-count", response_model=PredictCountResponse)
async def predict_count(image: UploadFile = File(...)) -> PredictCountResponse:
    if registry.csrnet is None:
        raise HTTPException(status_code=503, detail="CSRNet model is not loaded.")

    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded image is empty.")

    try:
        tensor = preprocess_csrnet_image(image_bytes, registry.device)
        with torch.no_grad():
            output = registry.csrnet(tensor)

        # CSRNet usually returns a density map; summing gives total crowd count.
        if isinstance(output, (tuple, list)):
            output = output[0]

        if not isinstance(output, torch.Tensor):
            raise ValueError("CSRNet output must be a torch.Tensor.")

        predicted_count = float(torch.sum(output).item())
        if predicted_count < 0:
            predicted_count = 0.0

        return PredictCountResponse(predicted_count=round(predicted_count, 2))
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to run crowd counting: {exc}") from exc


@router.post("/predict-future", response_model=PredictFutureResponse)
def predict_future(payload: PredictFutureRequest) -> PredictFutureResponse:
    if registry.lstm is None:
        raise HTTPException(status_code=503, detail="LSTM model is not loaded.")

    try:
        sequence = preprocess_lstm_sequence(
            payload.past_counts,
            sequence_length=registry.lstm_seq_len,
            normalizer=registry.normalizer,
            device=registry.device,
        )

        with torch.no_grad():
            prediction = registry.lstm(sequence)

        if isinstance(prediction, (tuple, list)):
            prediction = prediction[0]

        if not isinstance(prediction, torch.Tensor):
            raise ValueError("LSTM output must be a torch.Tensor.")

        predicted_value = float(prediction.squeeze().item())
        denorm = registry.normalizer.denormalize(np.asarray([predicted_value], dtype=np.float32))
        predicted_next_count = float(max(0.0, denorm[0]))

        return PredictFutureResponse(predicted_next_count=round(predicted_next_count, 2))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to run future prediction: {exc}") from exc


@router.post("/risk", response_model=RiskResponse)
def compute_risk(payload: RiskRequest) -> RiskResponse:
    risk_score, level = evaluate_risk(
        current=payload.current_count,
        predicted=payload.predicted_count,
        previous=payload.previous_count,
    )

    return RiskResponse(risk_score=round(risk_score, 2), level=level)


@router.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "device": str(registry.device),
        "csrnet_loaded": registry.csrnet is not None,
        "lstm_loaded": registry.lstm is not None,
        "lstm_sequence_length": registry.lstm_seq_len,
        "normalization_method": registry.normalizer.method,
    }
