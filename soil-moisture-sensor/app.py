import threading
import uuid

from counterfit_connection import CounterFitConnection

from sensor import ADCSensorDevice
from server import ADCControllerServer


def main():
    CounterFitConnection.init('127.0.0.1', 5000)
    device_id = uuid.uuid4().hex
    telemetry_topic = f'{device_id}/telemetry'
    command_topic = f'{device_id}/command'
    broker_url = 'test.mosquitto.org'

    device = ADCSensorDevice(
        client_name=f'{device_id}_client',
        telemetry_topic=telemetry_topic,
        command_topic=command_topic,
        broker_url=broker_url,
        pin_adc=48,
        pin_relay=49,
    )

    controller_server = ADCControllerServer(
        client_name=f'{device_id}_server',
        telemetry_topic=telemetry_topic,
        command_topic=command_topic,
        broker_url=broker_url,
        soil_moisture_threshold=683,
    )

    threading.Thread(target=controller_server.start).start()
    threading.Thread(target=device.start).start()


if __name__ == '__main__':
    main()
