"""
F2 — Preprocessing Pipeline
Resize, normalize, denoise; output standardized tensors for the model.
"""
from dataclasses import dataclass
from typing import Optional

import cv2
import numpy as np
import torch


@dataclass
class PreprocessConfig:
    """Preprocessing configuration."""
    width: int = 640
    height: int = 480
    mean: tuple = (0.485, 0.456, 0.406)
    std: tuple = (0.229, 0.224, 0.225)
    denoise: bool = True


class PreprocessPipeline:
    """Image preprocessing: resize, normalize, denoise, tensor conversion."""

    def __init__(self, config: Optional[PreprocessConfig] = None):
        self.config = config or PreprocessConfig()

    def __call__(self, image: np.ndarray) -> torch.Tensor:
        """Run full pipeline and return tensor."""
        img = image.copy()
        if self.config.denoise:
            img = cv2.fastNlMeansDenoisingColored(img, None, 6, 6, 7, 21)
        img = cv2.resize(img, (self.config.width, self.config.height))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0
        img = (img - np.array(self.config.mean)) / np.array(self.config.std)
        img = np.transpose(img, (2, 0, 1))
        tensor = torch.from_numpy(img).float().unsqueeze(0)
        return tensor

    def for_yolo(self, image: np.ndarray) -> np.ndarray:
        """Return preprocessed image suitable for YOLOv8 (numpy, BGR)."""
        img = image.copy()
        if self.config.denoise:
            img = cv2.fastNlMeansDenoisingColored(img, None, 6, 6, 7, 21)
        return cv2.resize(img, (self.config.width, self.config.height))
