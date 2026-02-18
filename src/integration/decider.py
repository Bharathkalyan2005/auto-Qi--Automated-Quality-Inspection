"""
F4 — Accept/Reject Decision Logic
Configurable confidence threshold, pass/fail decision, log with timestamp + image.
"""
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional

import cv2
import numpy as np

from src.inference.engine import DetectionResult


class Decision(str, Enum):
    PASS = "pass"
    FAIL = "fail"


@dataclass
class InspectionResult:
    """Full inspection result."""
    decision: Decision
    confidence_threshold: float
    detections: List[DetectionResult]
    inference_ms: float
    timestamp: datetime
    image_path: Optional[str] = None


class DecisionLogic:
    """Apply confidence threshold, decide pass/fail, log results."""

    def __init__(
        self,
        confidence_threshold: float = 0.85,
        log_dir: str = "logs/inspections",
    ):
        self.confidence_threshold = confidence_threshold
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def decide(
        self,
        detections: List[DetectionResult],
        inference_ms: float = 0.0,
        image: Optional[np.ndarray] = None,
    ) -> InspectionResult:
        """Determine pass/fail based on any defect above threshold."""
        above_threshold = [
            d for d in detections
            if d.confidence >= self.confidence_threshold
        ]
        decision = Decision.FAIL if above_threshold else Decision.PASS
        ts = datetime.utcnow()
        result = InspectionResult(
            decision=decision,
            confidence_threshold=self.confidence_threshold,
            detections=above_threshold,
            inference_ms=inference_ms,
            timestamp=ts,
        )
        if image is not None:
            result.image_path = self._log(result, image)
        return result

    def _log(self, result: InspectionResult, image: np.ndarray) -> str:
        """Save image and metadata to log dir."""
        ts = result.timestamp.strftime("%Y%m%d_%H%M%S")
        name = f"{ts}_{result.decision.value}"
        img_path = self.log_dir / f"{name}.jpg"
        meta_path = self.log_dir / f"{name}.json"
        cv2.imwrite(str(img_path), image)
        meta = {
            "decision": result.decision.value,
            "timestamp": result.timestamp.isoformat(),
            "detections": [
                {
                    "defect_class": d.defect_class,
                    "confidence": d.confidence,
                    "bbox": {
                        "x1": d.bbox.x1, "y1": d.bbox.y1,
                        "x2": d.bbox.x2, "y2": d.bbox.y2,
                    },
                }
                for d in result.detections
            ],
            "inference_ms": result.inference_ms,
        }
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)
        return str(img_path)
