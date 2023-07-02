import socket
from threading import Thread, Lock
from .sock_message import SockMessage, MsgType, recv_sock_msg, send_sock_msg
from typing import Optional


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected: bool = False

        self.messages: list[SockMessage] = []
        self.messages_lock: Lock = Lock()

        self.listen_thread: Thread = Thread(target=self.__listen_and_record, daemon=True)

    def try_connect(self, ip, port=7777) -> bool:
        try:
            self.client.connect((ip, port))
            connection_confirmation = recv_sock_msg(self.client)
            if connection_confirmation.msg_type == MsgType.CONN:
                self.connected = True
                self.listen_thread.start()
                return True
        except socket.error:
            pass
        return False

    def send_message(self, msg_type: MsgType, msg_contents):
        send_sock_msg(self.client, msg_type, msg_contents)

    def __listen_and_record(self):
        while self.connected:
            msg = recv_sock_msg(self.client)
            with self.messages_lock:
                self.messages.append(msg)

    def fetch_messages(self) -> list[SockMessage]:
        res = list()
        with self.messages_lock:
            if len(self.messages) > 0:
                res.extend(self.messages)
                self.messages.clear()
        return res
