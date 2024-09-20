import json
from abc import ABC, abstractmethod
from typing import Any

from .mqtt_base import MQTTController


class Device(ABC):
    def __init__(
            self,
            client_name: str = 'device_client',
            telemetry_topic: str = 'device/telemetry',
            command_topic: str = 'device/commands',
            broker_url: str = 'test.mosquitto.org'
    ) -> None:
        """
        Initializes a generic device.

        :param client_name: Name of the MQTT client
        :param telemetry_topic: Topic to publish telemetry data
        :param command_topic: Topic to receive commands
        :param broker_url: URL of the MQTT broker
        """
        self.client_name = client_name
        self.telemetry_topic = telemetry_topic
        self.command_topic = command_topic
        self.broker_url = broker_url
        self.mqtt_controller = MQTTController(self.client_name, self.broker_url)
        self.mqtt_controller.connect()

    def start(self) -> None:
        """Initializes the device and starts sending telemetry."""
        try:
            self.run_device_loop()
        except Exception as e:
            print(f"Error in device loop: {e}")

    def publish_telemetry(self, telemetry_data: dict[str, Any]) -> None:
        """Publishes telemetry data to the MQTT broker.

        :param telemetry_data: Data to be sent as telemetry
        """

        try:
            message = json.dumps(telemetry_data)
        except json.JSONDecodeError:
            print("Failed to encode telemetry data.")
            message = '{}'

        self.mqtt_controller.publish(self.telemetry_topic, message)

    @abstractmethod
    def run_device_loop(self) -> None:
        """Main loop for the device's functionality. Must be implemented by each device."""
        raise NotImplementedError

    @abstractmethod
    def handle_message(self, client: Any, userdata: Any, message: Any) -> None:
        """Handles incoming messages. Must be implemented by each device."""
        raise NotImplementedError
