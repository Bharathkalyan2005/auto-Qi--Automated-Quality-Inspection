"""Tests for image capture module."""
import pytest
import numpy as np

from src.capture import CameraCapture, CaptureConfig, Frame


def test_capture_config():
    cfg = CaptureConfig(camera_index=0, fps=10)
    assert cfg.fps == 10
    assert cfg.camera_index == 0


def test_frame_creation():
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    f = Frame(image=img, timestamp=1.0, frame_id=1)
    assert f.frame_id == 1
    assert f.image.shape == (480, 640, 3)


def test_camera_capture_connect_disconnect():
    cap = CameraCapture(CaptureConfig(camera_index=999))  # non-existent
    # May or may not connect; disconnect should not raise
    cap.disconnect()
