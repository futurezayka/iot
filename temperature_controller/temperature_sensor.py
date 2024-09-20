import time
from datetime import datetime
from typing import Any

from counterfit_shims_seeed_python_dht import DHT

from base.device_abc import Device


class TemperatureSensorDevice(Device):
    def __init__(
            self,
            client_name: str = 'temperature_sensor_client',
            telemetry_topic: str = 'temperature_sensor/telemetry',
            broker_url: str = 'test.mosquitto.org',
            pin: int = 1,
    ) -> None:
        super().__init__(client_name, telemetry_topic, broker_url)
        self.dht_sensor = DHT('11', pin)

    def run_device_loop(self) -> None:
        """Main loop for the light sensor. Reads sensor data and publishes telemetry."""

        while True:
            _, temp = self.dht_sensor.read()
            timestamp = datetime.now().astimezone().replace(microsecond=0).isoformat()
            telemetry = {
                'time': timestamp,
                'temperature': temp
            }
            self.publish_telemetry(telemetry)
            time.sleep(1)

    def handle_message(self, client: Any, userdata: Any, message: Any) -> None:
        pass
