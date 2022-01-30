#
#  Copyright (C) BlueWave Studio - All Rights Reserved
#


class Message:

    def __init__(self, id, flags, payload):
        self.id = id
        self.flags = flags
        self.payload = payload
