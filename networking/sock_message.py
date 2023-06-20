from enum import Enum


class MsgType(Enum):
    GSC = 'gsc'
    MOVE = 'move'


class SockMessage:
    def __init__(self, msg_type: MsgType, msg_content):
        self.msg_type: MsgType = msg_type
        self.msg_content = msg_content
