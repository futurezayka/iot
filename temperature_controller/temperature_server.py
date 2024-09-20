import json
import threading
from typing import Any

from base import Device
from base.csv_handler import CSVMixin


class TemperatureControllerServer(Device, CSVMixin):
    def __init__(
            self,
            client_name: str = 'temperature_server',
            telemetry_topic: str = 'temperature_sensor/telemetry',
            broker_url: str = 'test.mosquitto.org',
            csv_file_path: str = 'temperature_data.csv'
    ) -> None:

        Device.__init__(self, client_name, telemetry_topic, broker_url)
        CSVMixin.__init__(self, csv_file_path)

    def run_device_loop(self) -> None:
        """Server runs and listens for telemetry."""
        print(f"Server is running and subscribing to {self.telemetry_topic}")
        self.mqtt_controller.subscribe(self.telemetry_topic, self.handle_message)

    def handle_message(self, client: Any, userdata: Any, message: Any) -> None:
        """Handles telemetry messages from the sensor."""
        headers = ('time', 'temperature')
        try:
            payload = json.loads(message.payload.decode())
            if isinstance(payload, dict) and all(key in headers for key in payload.keys()):
                threading.Thread(target=self.append_to_csv, args=(payload,)).start()
        except json.JSONDecodeError:
            print("Failed to decode telemetry message.")
