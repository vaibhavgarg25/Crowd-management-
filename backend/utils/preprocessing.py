from __future__ import annotations

import io
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torchvision import transforms


CSRNET_TRANSFORM = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def preprocess_csrnet_image(image_bytes: bytes, device: torch.device) -> torch.Tensor:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = CSRNET_TRANSFORM(image).unsqueeze(0)
    return tensor.to(device)


@dataclass
class SequenceNormalizer:
    method: str = "identity"
    mean: float = 0.0
    std: float = 1.0
    min_value: float = 0.0
    max_value: float = 1.0

    def normalize(self, values: np.ndarray) -> np.ndarray:
        if self.method == "zscore":
            denom = self.std if self.std != 0 else 1.0
            return (values - self.mean) / denom
        if self.method == "minmax":
            denom = self.max_value - self.min_value
            denom = denom if denom != 0 else 1.0
            return (values - self.min_value) / denom
        return values

    def denormalize(self, values: np.ndarray) -> np.ndarray:
        if self.method == "zscore":
            return values * self.std + self.mean
        if self.method == "minmax":
            return values * (self.max_value - self.min_value) + self.min_value
        return values


def load_scaler_from_json(path: Path) -> SequenceNormalizer | None:
    if not path.exists():
        return None

    payload = json.loads(path.read_text(encoding="utf-8"))
    method = payload.get("method", "identity").lower()

    if method == "zscore":
        return SequenceNormalizer(
            method="zscore",
            mean=float(payload["mean"]),
            std=float(payload["std"]),
        )

    if method == "minmax":
        return SequenceNormalizer(
            method="minmax",
            min_value=float(payload["min"]),
            max_value=float(payload["max"]),
        )

    return SequenceNormalizer(method="identity")


def preprocess_lstm_sequence(
    values: list[float],
    sequence_length: int,
    normalizer: SequenceNormalizer,
    device: torch.device,
) -> torch.Tensor:
    raw = np.asarray(values, dtype=np.float32)
    if len(raw) < sequence_length:
        raise ValueError(
            f"past_counts must contain at least {sequence_length} values for this model."
        )

    clipped = raw[-sequence_length:]
    normalized = normalizer.normalize(clipped)
    tensor = torch.tensor(normalized, dtype=torch.float32).view(1, sequence_length, 1)
    return tensor.to(device)
