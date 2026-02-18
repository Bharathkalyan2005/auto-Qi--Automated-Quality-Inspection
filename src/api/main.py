"""
F5 — REST API (FastAPI)
POST /inspect, GET /results, GET /stats, POST /retrain
"""
import os
from pathlib import Path

# Load .env so ANTHROPIC_API_KEY is available
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass
from datetime import datetime
from typing import List, Optional

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.inference.engine import DetectionResult, InferenceEngine
from src.integration.decider import Decision, DecisionLogic, InspectionResult
from src.preprocessing.pipeline import PreprocessPipeline

# Config from env
MODEL_PATH = os.getenv("MODEL_PATH", "models/saved/yolov8_defect.pt")
CONF_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.85"))
LOG_DIR = Path(os.getenv("LOG_DIR", "logs/inspections"))

app = FastAPI(title="AutoQI API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Singletons
engine = InferenceEngine(model_path=MODEL_PATH, conf_threshold=CONF_THRESHOLD)
decider = DecisionLogic(confidence_threshold=CONF_THRESHOLD, log_dir=str(LOG_DIR))
preprocess = PreprocessPipeline()

# In-memory store (replace with DB in prod)
_inspection_history: List[dict] = []
_stats = {"total": 0, "pass": 0, "fail": 0}


def _ndarray_from_upload(file: UploadFile) -> np.ndarray:
    content = file.file.read()
    arr = np.frombuffer(content, dtype=np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


class InspectResponse(BaseModel):
    decision: str
    detections: List[dict]  # may include ai_description when ANTHROPIC_API_KEY is set
    inference_ms: float
    timestamp: str


class StatsResponse(BaseModel):
    total: int
    pass_count: int
    fail_count: int
    pass_rate: float
    fail_rate: float


class RetrainResponse(BaseModel):
    status: str
    job_id: Optional[str] = None
    message: str


@app.post("/inspect", response_model=InspectResponse)
async def inspect(file: UploadFile = File(...), ai_insights: bool = True):
    """Submit image, get defect inspection result. Optionally add AI-generated descriptions."""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400, "Expected image file")
    img = _ndarray_from_upload(file)
    if img is None:
        raise HTTPException(400, "Invalid image")
    preprocessed = preprocess.for_yolo(img)
    detections, inference_ms = engine.run(preprocessed)
    result = decider.decide(detections, inference_ms=inference_ms, image=img)

    detections_data = [
        {"defect_class": d.defect_class, "confidence": d.confidence}
        for d in result.detections
    ]
    if ai_insights and detections_data:
        from src.api.anthropic_ai import generate_defect_description
        for d in detections_data:
            d["ai_description"] = generate_defect_description(
                d["defect_class"], d["confidence"]
            )

    _inspection_history.append({
        "decision": result.decision.value,
        "detections": detections_data,
        "inference_ms": result.inference_ms,
        "timestamp": result.timestamp.isoformat(),
    })
    _stats["total"] += 1
    if result.decision == Decision.PASS:
        _stats["pass"] += 1
    else:
        _stats["fail"] += 1
    return InspectResponse(
        decision=result.decision.value,
        detections=detections_data,
        inference_ms=result.inference_ms,
        timestamp=result.timestamp.isoformat(),
    )


@app.get("/results")
async def results(skip: int = 0, limit: int = 50):
    """Paginated inspection history."""
    return {
        "items": _inspection_history[skip : skip + limit],
        "total": len(_inspection_history),
    }


@app.get("/stats", response_model=StatsResponse)
async def stats():
    """Defect rates and accuracy metrics."""
    t = _stats["total"] or 1
    return StatsResponse(
        total=_stats["total"],
        pass_count=_stats["pass"],
        fail_count=_stats["fail"],
        pass_rate=round(_stats["pass"] / t, 4),
        fail_rate=round(_stats["fail"] / t, 4),
    )


@app.post("/retrain", response_model=RetrainResponse)
async def retrain():
    """Trigger model retraining job (async)."""
    from src.integration.retrain import queue_retrain
    job_id = queue_retrain()
    return RetrainResponse(
        status="queued",
        job_id=job_id,
        message="Retraining job queued. Check /retrain/status for progress.",
    )


@app.get("/retrain/status/{job_id}")
async def retrain_status(job_id: str):
    """Get retraining job status."""
    from src.integration.retrain import get_retrain_status
    status = get_retrain_status(job_id)
    if status is None:
        raise HTTPException(404, "Job not found")
    return status


@app.get("/analyze")
async def analyze():
    """Claude analysis of quality report and suggested actions."""
    from src.api.anthropic_ai import analyze_defect_report
    s = {k: v for k, v in _stats.items()}
    return {"analysis": analyze_defect_report(s), "stats": s}


@app.get("/analyze/retrain-suggestion")
async def retrain_suggestion():
    """Claude suggests whether to retrain based on defect trends."""
    from src.api.anthropic_ai import suggest_retrain
    t = _stats["total"] or 1
    fail_rate = _stats["fail"] / t
    return {"suggestion": suggest_retrain(_stats.copy(), fail_rate)}


@app.get("/config")
async def config_status():
    """Check if Anthropic API key is configured (no key value exposed)."""
    key = os.getenv("ANTHROPIC_API_KEY", "")
    configured = bool(key.strip() and not key.strip().startswith("sk-ant-your"))
    return {"anthropic_configured": configured}
