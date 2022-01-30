#
#  Copyright (C) BlueWave Studio - All Rights Reserved
#

import random
import threading
import common.Api_pb2 as oap_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._timer = None

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, oap version: {}.{}, api version: {}.{}"
            .format(message.result, message.oap_version.major,
                    message.oap_version.minor, message.api_version.major,
                    message.api_version.minor))

        self.inject_temperature_value(client)

    def inject_temperature_value(self, client):
        inject_temperature_sensor_value = oap_api.InjectTemperatureSensorValue(
        )
        inject_temperature_sensor_value.value = random.randint(-40, 40)
        client.send(oap_api.MESSAGE_INJECT_TEMPERATURE_SENSOR_VALUE, 0,
                    inject_temperature_sensor_value.SerializeToString())

        self._timer = threading.Timer(15, self.inject_temperature_value,
                                      [client])
        self._timer.start()

    def get_timer(self):
        return self._timer


def main():
    client = Client("inject temperature example")
    event_handler = EventHandler()
    client.set_event_handler(event_handler)
    client.connect('127.0.0.1', 44405)

    active = True
    while active:
        try:
            active = client.wait_for_message()
        except KeyboardInterrupt:
            break

    if event_handler.get_timer() is not None:
        event_handler.get_timer().cancel()

    client.disconnect()


if __name__ == "__main__":
    main()
