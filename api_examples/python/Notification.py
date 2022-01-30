#
#  Copyright (C) BlueWave Studio - All Rights Reserved
#

import threading
import common.Api_pb2 as oap_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._notification_channel_id = None
        self._timer = None

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, oap version: {}.{}, api version: {}.{}"
            .format(message.result, message.oap_version.major,
                    message.oap_version.minor, message.api_version.major,
                    message.api_version.minor))

        register_notification_channel_request = oap_api.RegisterNotificationChannelRequest(
        )
        register_notification_channel_request.name = "Example Notification Channel"
        register_notification_channel_request.description = "Notification channel from API example"

        client.send(oap_api.MESSAGE_REGISTER_NOTIFICATION_CHANNEL_REQUEST, 0,
                    register_notification_channel_request.SerializeToString())

    def on_register_notification_channel_response(self, client, message):
        print(
            "register notification channel response, result: {}, icon id: {}".
            format(message.result, message.id))
        self._notification_channel_id = message.id

        if message.result == oap_api.RegisterNotificationChannelResponse.REGISTER_NOTIFICATION_CHANNEL_RESULT_OK:
            print("notification channel successfully registered")
            self.show_notification(client)

    def show_notification(self, client):
        show_notification = oap_api.ShowNotification()
        show_notification.channel_id = self._notification_channel_id
        show_notification.title = "Hello World"
        show_notification.description = "This is description of the notification"
        show_notification.single_line = "Hello World - This is an example"

        with open("assets/notification_icon.svg", 'rb') as icon_file:
            show_notification.icon = icon_file.read()

        with open("assets/notification_sound.wav", 'rb') as sound_file:
            show_notification.sound_pcm = sound_file.read()

        client.send(oap_api.MESSAGE_SHOW_NOTIFICATION, 0,
                    show_notification.SerializeToString())

        self._timer = threading.Timer(30, self.show_notification, [client])
        self._timer.start()

    def get_notification_channel_id(self):
        return self._notification_channel_id

    def get_timer(self):
        return self._timer


def main():
    client = Client("notification example")
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

    if event_handler.get_notification_channel_id() is not None:
        unregister_notification_channel = oap_api.UnregisterNotificationChannel(
        )
        unregister_notification_channel.id = event_handler.get_notification_channel_id(
        )
        client.send(oap_api.MESSAGE_UNREGISTER_NOTIFICATION_CHANNEL, 0,
                    unregister_notification_channel.SerializeToString())

    client.disconnect()


if __name__ == "__main__":
    main()
