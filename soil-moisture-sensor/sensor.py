import json
import time
from typing import Any

from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay

from base import Device


class ADCSensorDevice(Device):
    def __init__(
            self,
            client_name: str = 'soil_moisture_sensor_client',
            telemetry_topic: str = 'soil_moisture_sensor/telemetry',
            command_topic: str = 'soil_moisture_sensor/command',
            broker_url: str = 'test.mosquitto.org',
            pin_adc: int = 1,
            pin_relay: int = 2,
    ) -> None:
        super().__init__(client_name, telemetry_topic, command_topic, broker_url)
        self.pin_adc = pin_adc
        self.adc_sensor = ADC()
        self.relay = GroveRelay(pin_relay)

    def run_device_loop(self) -> None:
        """Main loop for the sensor. Reads sensor data and publishes telemetry."""
        print(f"Client is running...")
        self.mqtt_controller.subscribe(self.command_topic, self.handle_message)
        while True:
            soil_moisture = self.adc_sensor.read(self.pin_adc)
            telemetry = {
                'soil_moisture': soil_moisture,
            }
            self.publish_telemetry(telemetry)
            time.sleep(10)

    def handle_message(self, client: Any, userdata: Any, message: Any) -> None:
        payload = json.loads(message.payload.decode())
        relay_on = payload.get('relay_on')
        if relay_on is not None:
            self.relay.on() if relay_on else self.relay.off()
        else:
            print("Not a valid command.")
