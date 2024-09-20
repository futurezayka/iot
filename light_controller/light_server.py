import json
from typing import Any

from base.device_abc import Device


class LightControllerServer(Device):
    def __init__(
            self,
            client_name: str = 'light_server',
            telemetry_topic: str = 'light_sensor/telemetry',
            command_topic: str = 'light_sensor/commands',
            broker_url: str = 'test.mosquitto.org',
            light_threshold: int = 480
    ) -> None:
        super().__init__(client_name, telemetry_topic, command_topic, broker_url)

        self.light_threshold = light_threshold

    def run_device_loop(self) -> None:
        """Server runs and listens for telemetry."""
        print(f"Server is running and subscribing to {self.telemetry_topic}")
        self.mqtt_controller.subscribe(self.telemetry_topic, self.handle_message)

    def handle_message(self, client: Any, userdata: Any, message: Any) -> None:
        """Handles telemetry and sends commands based on light values."""
        try:
            payload = json.loads(message.payload.decode())
            light_value = payload.get('light')
            if light_value is not None:
                self.mqtt_controller.publish(
                    self.command_topic, json.dumps(
                        {'led_on': light_value < self.light_threshold}
                    )
                )
            else:
                print("Telemetry has no 'light' value.")
        except json.JSONDecodeError:
            print("Failed to decode telemetry message.")
