#
#  Copyright (C) BlueWave Studio - All Rights Reserved
#

import threading
import common.Api_pb2 as oap_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._id = 0
        self._duck = False
        self._timer = None

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, oap version: {}.{}, api version: {}.{}"
            .format(message.result, message.oap_version.major,
                    message.oap_version.minor, message.api_version.major,
                    message.api_version.minor))

        register_audio_focus_receiver_request = oap_api.RegisterAudioFocusReceiverRequest(
        )
        register_audio_focus_receiver_request.name = "audio focus example"
        register_audio_focus_receiver_request.category = oap_api.RegisterAudioFocusReceiverRequest.AUDIO_STREAM_CATEGORY_ENTERTAINMENT
        client.send(oap_api.MESSAGE_REGISTER_AUDIO_FOCUS_RECEIVER_REQUEST, 0,
                    register_audio_focus_receiver_request.SerializeToString())

    def on_register_audio_focus_receiver_response(self, client, message):
        print("register audio focus receiver response, result: {}, id: {}".
              format(message.result, message.id))
        self._id = message.id
        self.toggle_duck(client)

    def on_audio_focus_change_response(self, client, message):
        print("audio focus change response, result: {}, id: {}".format(
            message.result, message.id))

    def toggle_duck(self, client):
        self._duck = not self._duck

        audio_focus_change_request = oap_api.AudioFocusChangeRequest()
        audio_focus_change_request.id = self._id

        if self._duck:
            audio_focus_change_request.type = oap_api.AudioFocusChangeRequest.AUDIO_FOCUS_TYPE_DUCK
        else:
            audio_focus_change_request.type = oap_api.AudioFocusChangeRequest.AUDIO_FOCUS_TYPE_RELEASE

        client.send(oap_api.MESSAGE_AUDIO_FOCUS_CHANGE_REQUEST, 0,
                    audio_focus_change_request.SerializeToString())

        self._timer = threading.Timer(5, self.toggle_duck, [client])
        self._timer.start()

    def get_audio_focus_receiver_id(self):
        return self._id

    def get_timer(self):
        return self._timer


def main():
    client = Client("audio focus duck")
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

    if event_handler.get_audio_focus_receiver_id() is not None:
        unregister_audio_focus_receiver = oap_api.UnregisterAudioFocusReceiver(
        )
        unregister_audio_focus_receiver.id = event_handler.get_audio_focus_receiver_id(
        )
        client.send(oap_api.MESSAGE_UNREGISTER_AUDIO_FOCUS_RECEIVER, 0,
                    unregister_audio_focus_receiver.SerializeToString())

    client.disconnect()


if __name__ == "__main__":
    main()
