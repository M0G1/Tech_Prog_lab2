# -*- coding: utf-8 -*-

import json
import parametr

END_CHARACTER = "\0"
MESSAGE_PATTERN = "{username}>{message}"
TARGET_ENCODING = "utf-8"


class Message(object):

    def __init__(self, **kwargs):
        self.username = None
        self.message = None
        self.is_game_data = None  # or is it a chat data
        self.is_win = None
        self.rocket_pos = None
        self.Lagrange_pos = None
        self.rocket_speed = None
        self.quit = False
        self.__dict__.update(kwargs)

    def get_speed_list_XYR(self) -> tuple:
        return tuple([self.rocket_speed[param] for param in parametr.XYR])

    def __str__(self):
        return MESSAGE_PATTERN.format(**self.__dict__)

    def marshal(self):
        return (json.dumps(self.__dict__) + END_CHARACTER).encode(TARGET_ENCODING)
