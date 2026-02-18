"""
F7 — MQTT Integration
Subscribe to trigger topic, publish results; compatible with SCADA/MES.
"""
import json
from typing import Callable, Optional

try:
    import paho.mqtt.client as mqtt
    HAS_MQTT = True
except ImportError:
    HAS_MQTT = False


class MQTTIntegration:
    """MQTT client for trigger subscribe and result publish."""

    def __init__(
        self,
        broker: str = "localhost",
        port: int = 1883,
        trigger_topic: str = "/factory/line1/trigger",
        result_topic: str = "/factory/line1/result",
    ):
        self.broker = broker
        self.port = port
        self.trigger_topic = trigger_topic
        self.result_topic = result_topic
        self._client: Optional["mqtt.Client"] = None
        self._on_trigger: Optional[Callable[[dict], None]] = None

    def connect(self) -> bool:
        if not HAS_MQTT:
            return False
        self._client = mqtt.Client()
        try:
            self._client.connect(self.broker, self.port)
            self._client.on_message = self._handle_message
            self._client.subscribe(self.trigger_topic)
            self._client.loop_start()
            return True
        except Exception:
            return False

    def _handle_message(self, _client, _userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            if self._on_trigger:
                self._on_trigger(payload)
        except Exception:
            pass

    def on_trigger(self, callback: Callable[[dict], None]) -> None:
        """Register callback for trigger messages."""
        self._on_trigger = callback

    def publish_result(self, result: dict) -> bool:
        """Publish inspection result to result topic."""
        if not HAS_MQTT or not self._client:
            return False
        try:
            self._client.publish(
                self.result_topic,
                json.dumps(result),
                qos=1,
            )
            return True
        except Exception:
            return False

    def disconnect(self) -> None:
        if self._client:
            self._client.loop_stop()
            self._client.disconnect()
            self._client = None
