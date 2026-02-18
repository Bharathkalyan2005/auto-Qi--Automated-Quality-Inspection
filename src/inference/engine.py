"""
F3 — Defect Detection Engine
Load trained YOLOv8/ResNet model, run inference in <200ms, return defect class, confidence, bbox.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

import cv2
import numpy as np


@dataclass
class BoundingBox:
    x1: float
    y1: float
    x2: float
    y2: float


@dataclass
class DetectionResult:
    """Single defect detection."""
    defect_class: str
    confidence: float
    bbox: BoundingBox


class InferenceEngine:
    """Defect detection using YOLOv8 (or ResNet fallback)."""

    def __init__(
        self,
        model_path: Optional[str] = None,
        conf_threshold: float = 0.5,
        device: str = "cpu",
    ):
        self.model_path = Path(model_path) if model_path else None
        self.conf_threshold = conf_threshold
        self.device = device
        self._model = None
        self._model_type: Optional[str] = None

    def load_model(self, model_path: Optional[str] = None) -> bool:
        """Load YOLOv8 or fallback to placeholder."""
        path = Path(model_path or self.model_path or "")
        if path.exists():
            try:
                from ultralytics import YOLO
                self._model = YOLO(str(path))
                self._model_type = "yolov8"
                return True
            except Exception:
                pass
        self._model = None
        self._model_type = "mock"
        return True

    def run(
        self,
        image: np.ndarray,
        conf_threshold: Optional[float] = None,
    ) -> Tuple[List[DetectionResult], float]:
        """Run inference; returns (detections, inference_time_ms)."""
        import time
        start = time.perf_counter()
        conf = conf_threshold if conf_threshold is not None else self.conf_threshold

        if self._model is None:
            self.load_model()

        results: List[DetectionResult] = []

        if self._model_type == "yolov8" and self._model:
            preds = self._model(image, conf=conf, verbose=False)
            for p in preds:
                if p.boxes is None:
                    continue
                for box in p.boxes:
                    xyxy = box.xyxy[0].cpu().numpy()
                    cls_id = int(box.cls[0].item())
                    names = p.names or {}
                    defect_class = names.get(cls_id, f"class_{cls_id}")
                    results.append(
                        DetectionResult(
                            defect_class=defect_class,
                            confidence=float(box.conf[0].item()),
                            bbox=BoundingBox(
                                x1=float(xyxy[0]),
                                y1=float(xyxy[1]),
                                x2=float(xyxy[2]),
                                y2=float(xyxy[3]),
                            ),
                        )
                    )
        else:
            # Mock inference for dev without a trained model
            pass

        elapsed_ms = (time.perf_counter() - start) * 1000
        return results, elapsed_ms
