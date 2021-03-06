#
#  Copyright (C) BlueWave Studio - All Rights Reserved
#

import threading
import common.Api_pb2 as oap_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._reverse_gear_engaged = False
        self._timer = None

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, oap version: {}.{}, api version: {}.{}"
            .format(message.result, message.oap_version.major,
                    message.oap_version.minor, message.api_version.major,
                    message.api_version.minor))

        self.toggle_reverse_gear_status(client)

    def toggle_reverse_gear_status(self, client):
        self._reverse_gear_engaged = not self._reverse_gear_engaged

        set_reverse_gear_status = oap_api.SetReverseGearStatus()
        set_reverse_gear_status.engaged = self._reverse_gear_engaged
        client.send(oap_api.MESSAGE_SET_REVERSE_GEAR_STATUS, 0,
                    set_reverse_gear_status.SerializeToString())

        self._timer = threading.Timer(15, self.toggle_reverse_gear_status,
                                      [client])
        self._timer.start()

    def get_timer(self):
        return self._timer


def main():
    client = Client("reverse gear status example")
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
