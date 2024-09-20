from typing import Any

import paho.mqtt.client as mqtt
from colorama import Fore
from paho.mqtt.enums import CallbackAPIVersion


class MQTTController:
    def __init__(
            self,
            client_name: str,
            broker_url: str = 'test.mosquitto.org'
    ) -> None:
        """
        Initializes the MQTT client.

        :param client_name: MQTT client name
        :param broker_url: URL of the MQTT broker
        """
        self.client = mqtt.Client(
            client_id=client_name,
            callback_api_version=CallbackAPIVersion.VERSION2
        )
        self.broker_url = broker_url
        print(Fore.LIGHTGREEN_EX, f"Initialized MQTT client: {client_name}")

    def connect(self) -> None:
        """Connects the MQTT client to the broker."""
        try:
            self.client.connect(self.broker_url)
            self.client.loop_start()
        except mqtt.MQTTException as e:
            print(f"Failed to connect to MQTT broker: {e}")

    def unsubscribe(self, topic: str) -> None:
        """Unsubscribes from an MQTT topic.

        :param topic: MQTT topic to unsubscribe from
        """
        try:
            self.client.unsubscribe(topic)
            print(Fore.LIGHTCYAN_EX, f"Unsubscribed to {topic}")
        except mqtt.MQTTException as e:
            print(f"Failed to unsubscribe from {topic}: {e}")

    def subscribe(self, topic: str, on_message_callback: Any) -> None:
        """Subscribes to a topic with a message handler.

        :param topic: MQTT topic to subscribe to
        :param on_message_callback: Function to handle incoming messages
        """
        try:
            self.client.subscribe(topic)
            self.client.on_message = on_message_callback
            print(Fore.LIGHTCYAN_EX, f"Subscribed to {topic}")
        except mqtt.MQTTException as e:
            print(f"Failed to subscribe to {topic}: {e}")

    def publish(self, topic: str, message: str) -> None:
        """Publishes a message to the specified MQTT topic.

        :param topic: MQTT topic to publish to
        :param message: Message to send
        """
        try:
            self.client.publish(topic, message)
            print(Fore.BLUE, f"Published to {topic}: {message}")
        except mqtt.MQTTException as e:
            print(f"Failed to publish to {topic}: {e}")

    def stop(self) -> None:
        """Stops the MQTT client."""
        try:
            self.client.loop_stop()
        except mqtt.MQTTException as e:
            print(f"Failed to stop MQTT client: {e}")
        finally:
            self.client.disconnect()
            print("Disconnected from MQTT broker")
