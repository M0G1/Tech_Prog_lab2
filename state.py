import json
import parametr

END_CHARACTER = "\0"
MESSAGE_PATTERN = "{username}>{message}"
TARGET_ENCODING = "utf-8"


class State(object):

    def __init__(self, **kwargs):
        self.change_of_speed = None
        self.speed = None
        self.rocket_pos = None
        self.L1 = None
        self.__dict__.update(kwargs)

    def __str__(self):
        return MESSAGE_PATTERN.format(**self.__dict__)

    def marshal(self):
        return (json.dumps(self.__dict__) + END_CHARACTER).encode(TARGET_ENCODING)

