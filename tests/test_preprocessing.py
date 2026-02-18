"""Tests for preprocessing pipeline."""
import numpy as np
import torch

from src.preprocessing import PreprocessPipeline, PreprocessConfig


def test_preprocess_output_shape():
    pipe = PreprocessPipeline(PreprocessConfig(width=224, height=224))
    img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    out = pipe(img)
    assert isinstance(out, torch.Tensor)
    assert out.shape == (1, 3, 224, 224)


def test_preprocess_for_yolo():
    pipe = PreprocessPipeline()
    img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    out = pipe.for_yolo(img)
    assert out.shape == (480, 640, 3)
