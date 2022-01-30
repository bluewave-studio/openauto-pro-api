#
#  Copyright (C) BlueWave Studio - All Rights Reserved
#

import threading
import common.Api_pb2 as oap_api
from common.Client import Client, ClientEventHandler


class EventHandler(ClientEventHandler):

    def __init__(self):
        self._id = 0

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

        audio_focus_change_request = oap_api.AudioFocusChangeRequest()
        audio_focus_change_request.id = self._id
        audio_focus_change_request.type = oap_api.AudioFocusChangeRequest.AUDIO_FOCUS_TYPE_GAIN

        client.send(oap_api.MESSAGE_AUDIO_FOCUS_CHANGE_REQUEST, 0,
                    audio_focus_change_request.SerializeToString())

    def on_audio_focus_change_response(self, client, message):
        print("audio focus change response, result: {}, id: {}".format(
            message.result, message.id))

    def on_audio_focus_action(self, client, message):
        action = message.action

        if action == oap_api.AudioFocusAction.AUDIO_FOCUS_ACTION_TYPE_SUSPEND:
            print("suspend audio stream")
        elif action == oap_api.AudioFocusAction.AUDIO_FOCUS_ACTION_TYPE_RESTORE:
            print("resume audio stream")
        elif action == oap_api.AudioFocusAction.AUDIO_FOCUS_ACTION_TYPE_LOSS:
            print("stop audio stream, lost focus type: {}".format(
                message.lost_type))
        elif action == oap_api.AudioFocusAction.AUDIO_FOCUS_ACTION_TYPE_DUCK_START:
            print("decrease stream volume")
        elif action == oap_api.AudioFocusAction.AUDIO_FOCUS_ACTION_TYPE_DUCK_END:
            print("restore stream volume")

    def on_audio_focus_media_key(self, client, message):
        event_type = message.event_type
        key_type = message.key_type

        if key_type == oap_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_TYPE_PLAY:
            if event_type == oap_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_PRESS:
                print("play pressed")
            elif event_type == oap_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_RELEASE:
                print("play released")
        elif key_type == oap_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_TYPE_PAUSE:
            if event_type == oap_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_PRESS:
                print("pause pressed")
            elif event_type == oap_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_RELEASE:
                print("pause released")
        elif key_type == oap_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_TYPE_PREVIOUS:
            if event_type == oap_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_PRESS:
                print("previous pressed")
            elif event_type == oap_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_RELEASE:
                print("previous released")
        elif key_type == oap_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_TYPE_NEXT:
            if event_type == oap_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_PRESS:
                print("next pressed")
            elif event_type == oap_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_RELEASE:
                print("next released")
        elif key_type == oap_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_TYPE_TOGGLE_PLAY:
            if event_type == oap_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_PRESS:
                print("toggle play pressed")
            elif event_type == oap_api.AudioFocusMediaKey.AUDIO_FOCUS_MEDIA_KEY_EVENT_TYPE_RELEASE:
                print("toggle play released")

    def get_audio_focus_receiver_id(self):
        return self._id


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
