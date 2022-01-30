#
#  Copyright (C) BlueWave Studio - All Rights Reserved
#

import threading
import common.Api_pb2 as oap_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._day = False
        self._timer = None

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, oap version: {}.{}, api version: {}.{}"
            .format(message.result, message.oap_version.major,
                    message.oap_version.minor, message.api_version.major,
                    message.api_version.minor))

        self.toggle_day_night(client)

    def toggle_day_night(self, client):
        self._day = not self._day

        set_day_night = oap_api.SetDayNight()
        set_day_night.android_auto_night_mode = self._day
        set_day_night.oap_night_mode = self._day
        client.send(oap_api.MESSAGE_SET_DAY_NIGHT, 0,
                    set_day_night.SerializeToString())

        self._timer = threading.Timer(10, self.toggle_day_night, [client])
        self._timer.start()

    def get_timer(self):
        return self._timer


def main():
    client = Client("day night example")
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
