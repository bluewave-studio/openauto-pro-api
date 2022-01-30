#
#  Copyright (C) BlueWave Studio - All Rights Reserved
#

import threading
import common.Api_pb2 as oap_api
from common.Client import Client, ClientEventHandler


def listen_for_key_events(client):
    while True:
        key_type = None
        entered_key_type = input(
            "Enter key type (type break to exit): ").upper()

        if entered_key_type == "UP":
            key_type = oap_api.KeyEvent.KEY_TYPE_UP
        elif entered_key_type == "DOWN":
            key_type = oap_api.KeyEvent.KEY_TYPE_DOWN
        elif entered_key_type == "LEFT":
            key_type = oap_api.KeyEvent.KEY_TYPE_LEFT
        elif entered_key_type == "RIGHT":
            key_type = oap_api.KeyEvent.KEY_TYPE_RIGHT
        elif entered_key_type == "SCROLL_LEFT":
            key_type = oap_api.KeyEvent.KEY_TYPE_SCROLL_LEFT
        elif entered_key_type == "SCROLL_RIGHT":
            key_type = oap_api.KeyEvent.KEY_TYPE_SCROLL_RIGHT
        elif entered_key_type == "ENTER":
            key_type = oap_api.KeyEvent.KEY_TYPE_ENTER
        elif entered_key_type == "BACK":
            key_type = oap_api.KeyEvent.KEY_TYPE_BACK
        elif entered_key_type == "HOME":
            key_type = oap_api.KeyEvent.KEY_TYPE_HOME
        elif entered_key_type == "ANSWER_CALL":
            key_type = oap_api.KeyEvent.KEY_TYPE_ANSWER_CALL
        elif entered_key_type == "PHONE_MENU":
            key_type = oap_api.KeyEvent.KEY_TYPE_PHONE_MENU
        elif entered_key_type == "HANGUP_CALL":
            key_type = oap_api.KeyEvent.KEY_TYPE_HANGUP_CALL
        elif entered_key_type == "PLAY":
            key_type = oap_api.KeyEvent.KEY_TYPE_PLAY
        elif entered_key_type == "TOGGLE_PLAY":
            key_type = oap_api.KeyEvent.KEY_TYPE_TOGGLE_PLAY
        elif entered_key_type == "PAUSE":
            key_type = oap_api.KeyEvent.KEY_TYPE_PAUSE
        elif entered_key_type == "STOP":
            key_type = oap_api.KeyEvent.KEY_TYPE_STOP
        elif entered_key_type == "PREVIOUS_TRACK":
            key_type = oap_api.KeyEvent.KEY_TYPE_PREVIOUS_TRACK
        elif entered_key_type == "NEXT_TRACK":
            key_type = oap_api.KeyEvent.KEY_TYPE_NEXT_TRACK
        elif entered_key_type == "MEDIA_MENU":
            key_type = oap_api.KeyEvent.KEY_TYPE_MEDIA_MENU
        elif entered_key_type == "NAVIGATION_MENU":
            key_type = oap_api.KeyEvent.KEY_TYPE_NAVIGATION_MENU
        elif entered_key_type == "VOICE_COMMAND":
            key_type = oap_api.KeyEvent.KEY_TYPE_VOICE_COMMAND
        elif entered_key_type == "MODE":
            key_type = oap_api.KeyEvent.KEY_TYPE_MODE
        elif entered_key_type == "TOGGLE_NIGHT_MODE":
            key_type = oap_api.KeyEvent.KEY_TYPE_TOGGLE_NIGHT_MODE
        elif entered_key_type == "TOGGLE_TOPBAR":
            key_type = oap_api.KeyEvent.KEY_TYPE_TOGGLE_TOPBAR
        elif entered_key_type == "TOGGLE_MUTE":
            key_type = oap_api.KeyEvent.KEY_TYPE_TOGGLE_MUTE
        elif entered_key_type == "VOLUME_UP":
            key_type = oap_api.KeyEvent.KEY_TYPE_VOLUME_UP
        elif entered_key_type == "VOLUME_DOWN":
            key_type = oap_api.KeyEvent.KEY_TYPE_VOLUME_DOWN
        elif entered_key_type == "BRIGHTNESS_UP":
            key_type = oap_api.KeyEvent.KEY_TYPE_BRIGHTNESS_UP
        elif entered_key_type == "BRIGHTNESS_DOWN":
            key_type = oap_api.KeyEvent.KEY_TYPE_BRIGHTNESS_DOWN
        elif entered_key_type == "BRING_TO_FRONT":
            key_type = oap_api.KeyEvent.KEY_TYPE_BRING_TO_FRONT
        elif entered_key_type == "BREAK":
            print("Press Ctrl+C to exit...")
            return
        else:
            print("Invalid key")

        if key_type is not None:
            key_event = oap_api.KeyEvent()
            key_event.key_type = key_type

            key_event.event_type = oap_api.KeyEvent.EVENT_TYPE_PRESS
            client.send(oap_api.MESSAGE_KEY_EVENT, 0,
                        key_event.SerializeToString())

            key_event.event_type = oap_api.KeyEvent.EVENT_TYPE_RELEASE
            client.send(oap_api.MESSAGE_KEY_EVENT, 0,
                        key_event.SerializeToString())


class EventHandler(ClientEventHandler):

    def on_hello_response(self, client, message):
        print(
            "received hello response, result: {}, oap version: {}.{}, api version: {}.{}"
            .format(message.result, message.oap_version.major,
                    message.oap_version.minor, message.api_version.major,
                    message.api_version.minor))

        threading.Thread(target=listen_for_key_events, args=(client, )).start()


def main():
    client = Client("media data example")
    event_handler = EventHandler()
    client.set_event_handler(event_handler)
    client.connect('127.0.0.1', 44405)

    active = True
    while active:
        try:
            active = client.wait_for_message()
        except KeyboardInterrupt:
            break

    client.disconnect()


if __name__ == "__main__":
    main()
