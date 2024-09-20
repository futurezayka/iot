import json
import time
from typing import Any

from counterfit_shims_grove.grove_led import GroveLed
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor

from base.device_abc import Device


class LightSensorDevice(Device):
    def __init__(
            self,
            client_name: str = 'light_sensor_client',
            telemetry_topic: str = 'light_sensor/telemetry',
            command_topic: str = 'light_sensor/commands',
            broker_url: str = 'test.mosquitto.org',
            light_pin: int = 1,
            led_pin: int = 2
    ) -> None:
        super().__init__(client_name, telemetry_topic, command_topic, broker_url)
        self.light_sensor = GroveLightSensor(light_pin)
        self.led = GroveLed(led_pin)

    def run_device_loop(self) -> None:
        """Main loop for the light sensor. Reads sensor data and publishes telemetry."""
        print(f"Device subscribing to command topic: {self.command_topic}")
        self.mqtt_controller.subscribe(self.command_topic, self.handle_message)

        while True:
            light_value = self.light_sensor.light
            telemetry = {'light': light_value}
            self.publish_telemetry(telemetry)
            time.sleep(5)

    def handle_message(self, client: Any, userdata: Any, message: Any) -> None:
        """Handles incoming commands to control the LED."""
        payload = json.loads(message.payload.decode())
        led_on = payload.get('led_on')
        if led_on is not None:
            self.led.on() if led_on else self.led.off()
        else:
            print("No 'led_on' in received command.")
