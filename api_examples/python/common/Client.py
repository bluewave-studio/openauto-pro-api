#
#  Copyright (C) BlueWave Studio - All Rights Reserved
#

import socket
import struct
import threading
import common.Api_pb2 as oap_api
from common.Message import Message


class ClientEventHandler:

    def on_hello_response(self, client, message):
        pass

    def on_register_status_icon_response(self, client, message):
        pass

    def on_register_notification_channel_response(self, client, message):
        pass

    def on_phone_connection_status(self, client, message):
        pass

    def on_phone_levels_status(self, client, message):
        pass

    def on_phone_voice_call_status(self, client, message):
        pass

    def on_navigation_status(self, client, message):
        pass

    def on_navigation_maneuver_details(self, client, message):
        pass

    def on_navigation_maneuver_distance(self, client, message):
        pass

    def on_register_audio_focus_receiver_response(self, client, message):
        pass

    def on_audio_focus_change_response(self, client, message):
        pass

    def on_audio_focus_action(self, client, message):
        pass

    def on_audio_focus_media_key(self, client, message):
        pass

    def on_media_status(self, client, message):
        pass

    def on_media_metadata(self, client, message):
        pass

    def on_projection_status(self, client, message):
        pass

    def on_subscribe_obd_gauge_change_response(self, client, message):
        pass

    def on_obd_gauge_value_changed(self, client, message):
        pass

    def on_obd_connection_status(self, client, message):
        pass

    def on_temperature_status(self, client, message):
        pass


class Client:

    def __init__(self, name):
        self._connected = False
        self._event_handler = None
        self._name = name
        self._send_lock = threading.Lock()
        self._receive_lock = threading.Lock()

    def set_event_handler(self, event_handler):
        self._event_handler = event_handler

    def connect(self, hostname, port):
        if self._connected:
            self._socket.close()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((hostname, port))
        self._connected = True
        self._send_hello(self._name)

    def disconnect(self):
        if self._connected:
            self.send(oap_api.MESSAGE_BYEBYE, 0, bytes())

            self._socket.close()
            self._connected = False

    def receive(self) -> Message:
        with self._receive_lock:
            header_size = 12
            header_data = self._socket.recv(header_size)
            (payload_size, id,
             flags) = struct.unpack('<III', header_data[:header_size])
            payload = self._socket.recv(payload_size)
            return Message(id, flags, payload)

    def send(self, id, flags, payload):
        with self._send_lock:
            header_data = struct.pack('<III', len(payload), id, flags)
            self._socket.sendall(header_data)
            self._socket.sendall(payload)

    def _send_hello(self, name):
        hello_request = oap_api.HelloRequest()
        hello_request.name = name
        hello_request.api_version.major = oap_api.API_MAJOR_VERSION
        hello_request.api_version.minor = oap_api.API_MINOR_VERSION

        self.send(oap_api.MESSAGE_HELLO_REQUEST, 0,
                  hello_request.SerializeToString())

    def wait_for_message(self):
        can_continue = True

        message = self.receive()

        if message.id == oap_api.MESSAGE_PING:
            self.send(oap_api.MESSAGE_PONG, 0, bytes())
        elif message.id == oap_api.MESSAGE_BYEBYE:
            can_continue = False

        if self._event_handler is not None:
            if message.id == oap_api.MESSAGE_HELLO_RESPONSE:
                hello_response = oap_api.HelloResponse()
                hello_response.ParseFromString(message.payload)
                self._event_handler.on_hello_response(self, hello_response)
            elif message.id == oap_api.MESSAGE_REGISTER_STATUS_ICON_RESPONSE:
                register_status_icon_response = oap_api.RegisterStatusIconResponse(
                )
                register_status_icon_response.ParseFromString(message.payload)
                self._event_handler.on_register_status_icon_response(
                    self, register_status_icon_response)
            elif message.id == oap_api.MESSAGE_REGISTER_NOTIFICATION_CHANNEL_RESPONSE:
                register_notification_channel_response = oap_api.RegisterNotificationChannelResponse(
                )
                register_notification_channel_response.ParseFromString(
                    message.payload)
                self._event_handler.on_register_notification_channel_response(
                    self, register_notification_channel_response)
            elif message.id == oap_api.MESSAGE_PHONE_CONNECTION_STATUS:
                phone_connection_status = oap_api.PhoneConnectionStatus()
                phone_connection_status.ParseFromString(message.payload)
                self._event_handler.on_phone_connection_status(
                    self, phone_connection_status)
            elif message.id == oap_api.MESSAGE_PHONE_LEVELS_STATUS:
                phone_levels_status = oap_api.PhoneLevelsStatus()
                phone_levels_status.ParseFromString(message.payload)
                self._event_handler.on_phone_levels_status(
                    self, phone_levels_status)
            elif message.id == oap_api.MESSAGE_PHONE_VOICE_CALL_STATUS:
                phone_voice_call_status = oap_api.PhoneVoiceCallStatus()
                phone_voice_call_status.ParseFromString(message.payload)
                self._event_handler.on_phone_voice_call_status(
                    self, phone_voice_call_status)
            elif message.id == oap_api.MESSAGE_NAVIGATION_STATUS:
                navigation_status = oap_api.NavigationStatus()
                navigation_status.ParseFromString(message.payload)
                self._event_handler.on_navigation_status(
                    self, navigation_status)
            elif message.id == oap_api.MESSAGE_NAVIGATION_MANEUVER_DETAILS:
                navigation_maneuver_details = oap_api.NavigationManeuverDetails(
                )
                navigation_maneuver_details.ParseFromString(message.payload)
                self._event_handler.on_navigation_maneuver_details(
                    self, navigation_maneuver_details)
            elif message.id == oap_api.MESSAGE_NAVIGATION_MANEUVER_DISTANCE:
                navigation_maneuver_distance = oap_api.NavigationManeuverDistance(
                )
                navigation_maneuver_distance.ParseFromString(message.payload)
                self._event_handler.on_navigation_maneuver_distance(
                    self, navigation_maneuver_distance)
            elif message.id == oap_api.MESSAGE_REGISTER_AUDIO_FOCUS_RECEIVER_RESPONSE:
                register_audio_focus_receiver_response = oap_api.RegisterAudioFocusReceiverResponse(
                )
                register_audio_focus_receiver_response.ParseFromString(
                    message.payload)
                self._event_handler.on_register_audio_focus_receiver_response(
                    self, register_audio_focus_receiver_response)
            elif message.id == oap_api.MESSAGE_AUDIO_FOCUS_CHANGE_RESPONSE:
                audio_focus_change_response = oap_api.AudioFocusChangeResponse(
                )
                audio_focus_change_response.ParseFromString(message.payload)
                self._event_handler.on_audio_focus_change_response(
                    self, audio_focus_change_response)
            elif message.id == oap_api.MESSAGE_AUDIO_FOCUS_ACTION:
                audio_focus_action = oap_api.AudioFocusAction()
                audio_focus_action.ParseFromString(message.payload)
                self._event_handler.on_audio_focus_action(
                    self, audio_focus_action)
            elif message.id == oap_api.MESSAGE_AUDIO_FOCUS_MEDIA_KEY:
                audio_focus_media_key = oap_api.AudioFocusMediaKey()
                audio_focus_media_key.ParseFromString(message.payload)
                self._event_handler.on_audio_focus_media_key(
                    self, audio_focus_media_key)
            elif message.id == oap_api.MESSAGE_MEDIA_STATUS:
                media_status = oap_api.MediaStatus()
                media_status.ParseFromString(message.payload)
                self._event_handler.on_media_status(self, media_status)
            elif message.id == oap_api.MESSAGE_MEDIA_METADATA:
                media_metadata = oap_api.MediaMetadata()
                media_metadata.ParseFromString(message.payload)
                self._event_handler.on_media_metadata(self, media_metadata)
            elif message.id == oap_api.MESSAGE_PROJECTION_STATUS:
                projection_status = oap_api.ProjectionStatus()
                projection_status.ParseFromString(message.payload)
                self._event_handler.on_projection_status(
                    self, projection_status)
            elif message.id == oap_api.MESSAGE_SUBSCRIBE_OBD_GAUGE_CHANGE_RESPONSE:
                subscribe_obd_gauge_change_response = oap_api.SubscribeObdGaugeChangeResponse(
                )
                subscribe_obd_gauge_change_response.ParseFromString(
                    message.payload)
                self._event_handler.on_subscribe_obd_gauge_change_response(
                    self, subscribe_obd_gauge_change_response)
            elif message.id == oap_api.MESSAGE_OBD_GAUGE_VALUE_CHANGED:
                obd_gauge_value_changed = oap_api.ObdGaugeValueChanged()
                obd_gauge_value_changed.ParseFromString(message.payload)
                self._event_handler.on_obd_gauge_value_changed(
                    self, obd_gauge_value_changed)
            elif message.id == oap_api.MESSAGE_OBD_CONNECTION_STATUS:
                obd_connection_status = oap_api.ObdConnectionStatus()
                obd_connection_status.ParseFromString(message.payload)
                self._event_handler.on_obd_connection_status(
                    self, obd_connection_status)
            elif message.id == oap_api.MESSAGE_TEMPERATURE_STATUS:
                temperature_status = oap_api.TemperatureStatus()
                temperature_status.ParseFromString(message.payload)
                self._event_handler.on_temperature_status(
                    self, temperature_status)

        return can_continue
