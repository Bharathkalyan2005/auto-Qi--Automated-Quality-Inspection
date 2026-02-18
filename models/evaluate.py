"""
Model evaluation for defect detection.
"""
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
LABELED = DATA_DIR / "labeled"


def evaluate(model_path: str, data_yaml: Path | None = None) -> dict:
    """Run validation and return metrics."""
    try:
        from ultralytics import YOLO
    except ImportError:
        return {"error": "ultralytics not installed"}

    yaml = data_yaml or LABELED / "data.yaml"
    if not yaml.exists():
        return {"error": "data.yaml not found"}

    model = YOLO(model_path)
    results = model.val(data=str(yaml))
    return {
        "mAP50": float(getattr(results, "metrics", None) and getattr(results.metrics, "map50", 0) or 0),
        "mAP50-95": float(getattr(results, "metrics", None) and getattr(results.metrics, "map", 0) or 0),
    }
