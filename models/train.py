"""
Model training for YOLOv8 defect detection.
"""
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
LABELED = DATA_DIR / "labeled"
SAVED = Path(__file__).resolve().parent / "saved"


def train(
    data_yaml: Path | None = None,
    epochs: int = 50,
    imgsz: int = 640,
    batch: int = 16,
) -> str:
    """Train YOLOv8 on labeled defect data. Returns path to best model."""
    try:
        from ultralytics import YOLO
    except ImportError:
        raise RuntimeError("ultralytics not installed; pip install ultralytics")

    yaml = data_yaml or LABELED / "data.yaml"
    if not yaml.exists():
        (LABELED / "images").mkdir(parents=True, exist_ok=True)
        (LABELED / "labels").mkdir(parents=True, exist_ok=True)
        yaml_content = f"""path: {LABELED.absolute()}
train: images
val: images
names:
  0: defect
"""
        with open(yaml, "w") as f:
            f.write(yaml_content)

    model = YOLO("yolov8n.pt")
    results = model.train(
        data=str(yaml),
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        project=str(SAVED),
        name="run",
    )
    best = Path(results.save_dir) / "weights" / "best.pt"
    if best.exists():
        dest = SAVED / "yolov8_defect.pt"
        dest.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy(best, dest)
        return str(dest)
    return str(results.save_dir)


if __name__ == "__main__":
    train()
