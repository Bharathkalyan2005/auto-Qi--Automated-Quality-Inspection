"""
F1 — Image Capture Module
Connect to USB / IP industrial camera, configurable FPS, trigger via sensor or MQTT.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Generator, Optional

import cv2
import numpy as np


@dataclass
class CaptureConfig:
    """Camera capture configuration."""
    camera_index: int = 0
    camera_ip: Optional[str] = None
    fps: int = 10
    width: int = 640
    height: int = 480


@dataclass
class Frame:
    """Captured frame with metadata."""
    image: np.ndarray
    timestamp: float
    frame_id: int
    source: str = "camera"


class CameraCapture:
    """Handles USB and IP camera capture with configurable FPS and trigger support."""

    def __init__(self, config: Optional[CaptureConfig] = None):
        self.config = config or CaptureConfig()
        self._cap: Optional[cv2.VideoCapture] = None
        self._frame_id = 0

    def connect(self) -> bool:
        """Connect to camera (USB by index or IP)."""
        if self.config.camera_ip:
            self._cap = cv2.VideoCapture(self.config.camera_ip)
        else:
            self._cap = cv2.VideoCapture(self.config.camera_index)

        if not self._cap.isOpened():
            return False

        self._cap.set(cv2.CAP_PROP_FPS, self.config.fps)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.height)
        return True

    def disconnect(self) -> None:
        """Release camera resource."""
        if self._cap:
            self._cap.release()
            self._cap = None

    def capture_one(self) -> Optional[Frame]:
        """Capture a single frame."""
        import time
        if not self._cap or not self._cap.isOpened():
            if not self.connect():
                return None
        ret, img = self._cap.read()
        if not ret or img is None:
            return None
        self._frame_id += 1
        return Frame(
            image=img,
            timestamp=time.time(),
            frame_id=self._frame_id,
            source="camera",
        )

    def stream(
        self,
        callback: Optional[Callable[[Frame], None]] = None,
        stop_condition: Optional[Callable[[], bool]] = None,
    ) -> Generator[Frame, None, None]:
        """Stream frames at configured FPS; optional callback and stop condition."""
        import time
        if not self.connect():
            return
        try:
            frame_interval = 1.0 / self.config.fps
            last_capture = 0
            while True:
                if stop_condition and stop_condition():
                    break
                now = time.time()
                if now - last_capture >= frame_interval:
                    frame = self.capture_one()
                    if frame:
                        if callback:
                            callback(frame)
                        yield frame
                    last_capture = now
                time.sleep(0.01)
        finally:
            self.disconnect()

    def save_frame(self, frame: Frame, path: Path) -> bool:
        """Save frame to disk."""
        path.parent.mkdir(parents=True, exist_ok=True)
        return cv2.imwrite(str(path), frame.image)
