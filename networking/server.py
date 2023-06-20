import pygame
import socket
import threading
import time
from common import constants, helper
from game_logic import Player, GameState, Maze, Minotaur, CoordPair
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from sock_message import SockMessage, MsgType
from network_constants import *
from datetime import datetime
from live_clock import LiveClock


class GameServer:
    def __init__(self, host='localhost', port=7777):
        self.player_input_threads: dict[str, threading.Thread] = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        self.players: dict[str, Player] = {}
        self.clients: dict[str, socket.socket] = {}
        self.player_keys: list[str] = []

        self.maze = Maze(constants.ROWS, constants.WIDTH)
        self.maze.generate_labyrinth()
        self.gs = GameState(self.maze)

        self.connecting = True
        self.running = False

    def listen_for_start_command(self):
        while True:
            start_command = input("Enter 'start' to begin the game: ")
            if start_command.lower() == "start":
                self.connecting = False
                self.running = True
                break

    def input_movement(self, name: str):
        while self.running:
            try:
                conn = self.clients[name]
                player = self.players[name]
                if conn and player:
                    move_direction = helper.recv_message(conn)
                    player.move_direction = move_direction
                    msg = SockMessage(MsgType.MOVE, (name, move_direction, self.gs.step))
                    self.broadcast_message(msg)
                else:
                    print(f"WARN: Failed to input movement for player {name} on time {self.gs.step}.")
            except Exception as e:
                print(f"ERR: Error {e} occurred during movement input for player {name}. Removing")
                self.player_keys.remove(name)
                return

    def broadcast_message(self, msg: SockMessage):
        with ThreadPoolExecutor() as executor:
            for name in self.player_keys:
                executor.submit(self.send_message_to_client, name, msg)

    def send_message_to_client(self, name, msg: SockMessage):
        try:
            conn = self.clients[name]
            if conn:
                helper.send_message(conn, msg)
        except Exception as e:
            print(f"ERR: Error {e} occurred during broadcast to player {name}. Removing")
            self.player_keys.remove(name)

    def advance_and_broadcast(self):
        clock = LiveClock()
        while self.running:
            curr_time = datetime.now()
            change = self.gs.advance_timeline(1)
            # print(f"server advance on time {self.gs.time}")

            if self.gs.step % GSC_CHANGE_RATE == 0:
                msg = SockMessage(MsgType.GSC, change)
                self.broadcast_message(msg)
                # print(f"Sent gs update to clients on time {change.step} at {datetime.now().time()}")

            # print(f"Time before tick : {datetime.now()}")
            clock.tick(constants.FPS)
            # print(f"{(datetime.now() - curr_time).total_seconds()}\t{datetime.now().time()}")
            # print(f"Time after tick : {datetime.now()}")

    def listen_for_connections(self):
        while True:
            conn, addr = self.server.accept()
            if not self.connecting:
                break

            player_id = len(self.player_keys)
            if player_id == 0:  # minotaur
                mino_start = self.maze.get_random_edge_cell().get_pos()
                player = Minotaur(mino_start, (self.maze.cell_width, self.maze.cell_width), is_player_controlled=True)
            else:
                center = (constants.ROWS // 2 + 0.5) * self.maze.cell_width
                player_start = CoordPair(center, center)
                player = Player(player_start, (self.maze.cell_width / 2, self.maze.cell_width / 2),
                                name=f"Player{player_id}")
            self.gs.add_player(player)

            # send ID to client
            conn.send(player_id.to_bytes(4, byteorder='big'))
            self.player_keys.append(player.name)
            self.players[player.name] = player
            self.clients[player.name] = conn
            print(f"Player connected: {addr} with id {player_id}")

            thread = Thread(target=self.input_movement, args=(player.name,), daemon=True)
            self.player_input_threads[player.name] = thread

    def start(self):
        print("Server started, waiting for connections...")

        # Listen for game start (console)
        Thread(target=self.listen_for_start_command, daemon=True).start()

        # Listen for connections (hamachi VPN)
        Thread(target=self.listen_for_connections, daemon=True).start()

        while self.connecting:  # This will just keep the main thread from progressing until 'start' command is given
            time.sleep(0.1)

        print(f"Starting the game with {len(self.player_keys)} players")
        # Send "start" message to all clients
        for name in self.player_keys:
            conn = self.clients[name]
            if conn:
                helper.send_message(conn, constants.START)

        # Start reading player input and send them initial game state
        for name, thread in self.player_input_threads.items():
            helper.send_message(self.clients[name], self.gs)
            thread.start()

        # Start a separate thread that advances the game state and broadcasts it to all clients
        broadcast_thread = Thread(target=self.advance_and_broadcast, daemon=True)
        broadcast_thread.start()


HAMACHI_IP = input("Enter the HAMACHI IP of the host (Dimas)")

if __name__ == "__main__":
    server = GameServer(host=HAMACHI_IP)
    try:
        server.start()
        while server.connecting or server.running:  # Keep main thread alive while server is running
            time.sleep(1)
    finally:
        server.server.close()
