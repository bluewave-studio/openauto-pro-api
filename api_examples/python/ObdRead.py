#
#  Copyright (C) BlueWave Studio - All Rights Reserved
#

import common.Api_pb2 as oap_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._gauge_index = 4
        self._subscribed = False
        self._min_value = None
        self._max_value = None
        self._limit = None
        self._label = None
        self._precision = None

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, oap version: {}.{}, api version: {}.{}"
            .format(message.result, message.oap_version.major,
                    message.oap_version.minor, message.api_version.major,
                    message.api_version.minor))

        set_status_subscriptions = oap_api.SetStatusSubscriptions()
        set_status_subscriptions.subscriptions.append(
            oap_api.SetStatusSubscriptions.Subscription.OBD)
        client.send(oap_api.MESSAGE_SET_STATUS_SUBSCRIPTIONS, 0,
                    set_status_subscriptions.SerializeToString())

        subscribe_obd_gauge_change_request = oap_api.SubscribeObdGaugeChangeRequest(
        )
        subscribe_obd_gauge_change_request.gauge_index = self._gauge_index
        client.send(oap_api.MESSAGE_SUBSCRIBE_OBD_GAUGE_CHANGE_REQUEST, 0,
                    subscribe_obd_gauge_change_request.SerializeToString())

    def on_subscribe_obd_gauge_change_response(self, client, message):
        self._min_value = message.min_value
        self._max_value = message.max_value
        self._limit = message.limit
        self._label = message.label
        self._precision = message.precision

        print(
            "subscribe obd gauge change response, gauge index: {}, min value: {}, max value: {}, limit: {}, label: {}, precision: {}"
            .format(message.gauge_index, self._min_value, self._max_value,
                    self._limit, self._label, self._precision))

        if message.result == oap_api.SubscribeObdGaugeChangeResponse.SUBSCRIBE_OBD_GAUGE_CHANGE_RESULT_OK:
            self._subscribed = True

    def unsubscribe(self, client):
        if self._subscribed:
            unsubscribe_obd_gauge_change = oap_api.UnsubscribeObdGaugeChange()
            unsubscribe_obd_gauge_change.gauge_index = self._gauge_index
            client.send(oap_api.MESSAGE_UNSUBSCRIBE_OBD_GAUGE_CHANGE, 0,
                        unsubscribe_obd_gauge_change.SerializeToString())
            self._subscribed = False
            self._min_value = None
            self._max_value = None
            self._limit = None
            self._label = None
            self._precision = None

    def on_obd_gauge_value_changed(self, client, message):
        print("{0:.{1}f} {2}".format(message.value, self._precision,
                                     self._label))

    def on_obd_connection_status(self, client, message):
        print("obd connection status, state: {}".format(message.state))


def main():
    client = Client("obd read example")
    event_handler = EventHandler()
    client.set_event_handler(event_handler)
    client.connect('127.0.0.1', 44405)

    active = True
    while active:
        try:
            active = client.wait_for_message()
        except KeyboardInterrupt:
            break

    event_handler.unsubscribe(client)
    client.disconnect()


if __name__ == "__main__":
    main()
