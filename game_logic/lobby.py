import socket
from .player import Player


class Lobby:
    def __init__(self, host_name: str, host: socket.socket):
        self._clients: dict = {host_name: host}
        self._clients_ready: dict = {host_name: False}

    def toggle_ready(self, name):
        self._clients_ready[name] = not self._clients_ready[name]

    def add_client(self, name, sock):
        self._clients[name] = sock

    def get_clients(self):
        return self._clients.copy()
