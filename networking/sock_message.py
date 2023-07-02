import pickle
import struct
from enum import Enum
from typing import Optional


class MsgType(Enum):
    CONN = 'conn'
    RDY = 'rdy'
    START = 'start'
    GS_UPD = 'gs_upd'
    MOVE = 'move'
    LOBBY_INIT = 'lobby_init'


class SockMessage:
    def __init__(self, msg_type: MsgType, msg_content):
        self.msg_type: MsgType = msg_type
        self.msg_content = msg_content


def recv_sock_msg(sock) -> Optional[SockMessage]:
    msg = recv_message(sock)
    if not isinstance(msg, SockMessage):
        return None
    return msg


def send_sock_msg(sock, msg_type: MsgType, msg_content) -> None:
    msg = SockMessage(msg_type, msg_content)
    send_message(sock, msg)


def send_message(sock, message):
    # Prefix each message with a 4-byte length (network byte order)
    data = pickle.dumps(message)
    message_length = len(data)
    sock.sendall(struct.pack('>I', message_length) + data)


def recv_message(sock):
    # Read message length and unpack it into an integer
    raw_message_length = recv_all(sock, 4)
    if not raw_message_length:
        return None
    message_length = struct.unpack('>I', raw_message_length)[0]
    # Read the message data
    data = recv_all(sock, message_length)
    return pickle.loads(data)


def recv_all(sock, length):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data