import json
import threading
import time
from typing import Any

from colorama import Fore

from base import Device


class ADCControllerServer(Device):
    __WATER_TIME: int = 5
    __DELAY: int = 20

    def __init__(
            self,
            client_name: str = 'soil_moisture_server',
            telemetry_topic: str = 'soil_moisture_sensor/telemetry',
            command_topic: str = 'soil_moisture_sensor/commands',
            broker_url: str = 'test.mosquitto.org',
            soil_moisture_threshold: int = 100
    ) -> None:
        super().__init__(client_name, telemetry_topic, command_topic, broker_url)
        self.soil_moisture_threshold = soil_moisture_threshold

    def run_device_loop(self) -> None:
        """Server runs and listens for telemetry."""
        print(f"Server is running...")
        self.mqtt_controller.subscribe(self.telemetry_topic, self.handle_message)

    def __control_relay(self, state: bool) -> None:
        """Turns the relay on or off based on state."""
        self.mqtt_controller.unsubscribe(self.telemetry_topic)
        self.mqtt_controller.publish(
            self.command_topic, json.dumps(
                {'relay_on': state}
            )
        )
        print(Fore.RED, "Awaiting water time")
        time.sleep(self.__WATER_TIME)
        self.mqtt_controller.publish(
            self.command_topic, json.dumps(
                {'relay_on': not state}
            )
        )
        print(Fore.GREEN, "Watering complete")
        time.sleep(self.__DELAY)
        self.mqtt_controller.subscribe(self.telemetry_topic, self.handle_message)

    def handle_message(self, client: Any, userdata: Any, message: Any) -> None:
        """Handles telemetry and sends commands based on values."""
        try:
            payload = json.loads(message.payload.decode())
            print(Fore.MAGENTA, f"Received payload: {payload}")
            soil_moisture = payload.get('soil_moisture')
            if soil_moisture is not None:
                state = soil_moisture > self.soil_moisture_threshold
                if state:
                    threading.Thread(target=self.__control_relay, args=(state,)).start()
            else:
                print("Telemetry has no correct value.")
        except json.JSONDecodeError:
            print("Failed to decode telemetry message.")
