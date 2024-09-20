import threading
import uuid

from counterfit_connection import CounterFitConnection

from temperature_controller.temperature_sensor import TemperatureSensorDevice
from temperature_controller.temperature_server import TemperatureControllerServer


def main():
    CounterFitConnection.init('127.0.0.1', 5000)
    device_id = uuid.uuid4().hex
    telemetry_topic = f'{device_id}/telemetry'
    broker_url = 'test.mosquitto.org'

    device = TemperatureSensorDevice(
        client_name=f'{device_id}_client',
        telemetry_topic=telemetry_topic,
        broker_url=broker_url,
        pin=48,
    )

    controller_server = TemperatureControllerServer(
        client_name=f'{device_id}_server',
        telemetry_topic=telemetry_topic,
        broker_url=broker_url,
    )

    threading.Thread(target=controller_server.start).start()
    threading.Thread(target=device.start).start()


if __name__ == '__main__':
    main()
