#
#  Copyright (C) BlueWave Studio - All Rights Reserved
#

import random
import threading
import time
import common.Api_pb2 as oap_api
from common.Client import Client, ClientEventHandler

injecting_active = True


def inject_obd_gauge_formula_value(client):
    obd_inject_gauge_formula_value = oap_api.ObdInjectGaugeFormulaValue()

    while injecting_active:

        for formula, min_value, max_value in [("getPidValue(1)", -40, 215),
                                              ("getPidValue(0)", 0, 100),
                                              ("getPidValue(4)", 0, 8000),
                                              ("getPidValue(5)", 0, 255)]:
            obd_inject_gauge_formula_value.formula = formula
            obd_inject_gauge_formula_value.value = random.randint(
                min_value, max_value)
            client.send(oap_api.MESSAGE_OBD_INJECT_GAUGE_FORMULA_VALUE, 0,
                        obd_inject_gauge_formula_value.SerializeToString())

        time.sleep(0.1)


class EventHandler(ClientEventHandler):

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, oap version: {}.{}, api version: {}.{}"
            .format(message.result, message.oap_version.major,
                    message.oap_version.minor, message.api_version.major,
                    message.api_version.minor))

        threading.Thread(target=inject_obd_gauge_formula_value,
                         args=(client, )).start()


def main():
    client = Client("obd inject example")
    event_handler = EventHandler()
    client.set_event_handler(event_handler)
    client.connect('127.0.0.1', 44405)

    active = True
    while active:
        try:
            active = client.wait_for_message()
        except KeyboardInterrupt:
            break

    global injecting_active
    injecting_active = False

    client.disconnect()


if __name__ == "__main__":
    main()
