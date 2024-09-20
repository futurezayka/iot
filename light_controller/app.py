import threading
import uuid

from counterfit_connection import CounterFitConnection

from light_sensor import LightSensorDevice
from light_server import LightControllerServer


def main():
    CounterFitConnection.init('127.0.0.1', 5000)
    device_id = uuid.uuid4().hex
    telemetry_topic = f'{device_id}/telemetry'
    command_topic = f'{device_id}/commands'
    broker_url = 'test.mosquitto.org'

    device = LightSensorDevice(
        client_name=f'{device_id}_client',
        telemetry_topic=telemetry_topic,
        command_topic=command_topic,
        broker_url=broker_url,
        light_pin=48,
        led_pin=49
    )

    controller_server = LightControllerServer(
        client_name=f'{device_id}_server',
        telemetry_topic=telemetry_topic,
        command_topic=command_topic,
        broker_url=broker_url,
        light_threshold=480
    )

    threading.Thread(target=controller_server.start).start()
    threading.Thread(target=device.start).start()


if __name__ == '__main__':
    main()
