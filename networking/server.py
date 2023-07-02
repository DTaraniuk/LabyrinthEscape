import pygame
import socket
import threading
import time
from common import constants, helper
from game_logic import LePlayer, GameState, Maze, LeMinotaur, CoordPair
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from networking.sock_message import SockMessage, MsgType, send_sock_msg, recv_sock_msg, send_message
from networking.network_constants import *
from datetime import datetime
from networking.live_clock import LiveClock
from typing import Callable, Any


class GameServer:
    def __init__(self, host='localhost', port=7777):
        self.client_listen_threads: dict[str, threading.Thread] = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        self.clients: dict[str, socket.socket] = {}
        self.player_names: list[str] = []

        self.maze = Maze(constants.ROWS, constants.WIDTH)
        self.maze.generate_labyrinth()
        self.gs = GameState(self.maze, write_changes=True)
        self.gs_lock: threading.Lock = threading.Lock()
        self.broadcast_advance_thread: threading.Thread = Thread(target=self.advance_and_broadcast, daemon=True)

        self.player_ready_map: dict[str, bool] = {}

        self.connecting = True
        self.running = False

    def listen_for_start_command(self):
        while True:
            start_command = input("Enter 'start' to begin the game: ")
            if start_command.lower() != 'start':
                continue

            if not all(self.player_ready_map.values()):
                print('Not all players are ready')
                continue

            self.connecting = False
            self.running = True
            break

    def listen_to_client(self, name: str):
        conn = self.clients.get(name)
        if not conn:
            print(f'Failed to get conn for player {name}.')
            return

        msg_action_map: dict[MsgType, Callable[[str, SockMessage], None]] = {
            MsgType.RDY: self.update_player_ready_map,
            MsgType.MOVE: self.update_player_movement
        }
        while self.running or self.connecting:
            try:  # TODO implement new listening
                msg = recv_sock_msg(conn)
                if not msg:
                    continue

                msg_action_map[msg.msg_type](name, msg)
            except Exception as e:
                print(f"ERR: Error {e} occurred while listening to player {name} on time {self.gs.step}. Removing")
                self.player_names.remove(name)
                return

    def update_player_ready_map(self, name: str, msg: SockMessage) -> None:
        self.player_ready_map.update({name: not self.player_ready_map[name]})
        msg = SockMessage(MsgType.RDY, name)
        self.broadcast_message(msg)

    def update_player_movement(self, name: str, msg: SockMessage):
        player = self.gs.players.get(name)
        move_direction = msg.msg_content
        if not player:
            print(f'Failed to get player {name}.')
        with self.gs_lock:
            player.move_direction = move_direction
        msg = SockMessage(MsgType.MOVE, (name, move_direction, self.gs.step))
        self.broadcast_message(msg)

    def broadcast_message(self, msg: SockMessage):
        with ThreadPoolExecutor() as executor:
            for name in self.player_names:
                executor.submit(self.send_message_to_client, name, msg)

    def send_message_to_client(self, name, msg: SockMessage):
        try:
            conn = self.clients[name]
            if conn:
                send_message(conn, msg)
        except Exception as e:
            print(f"ERR: Error {e} occurred during broadcast to player {name}. Removing")
            self.player_names.remove(name)

    def advance_and_broadcast(self):
        clock = LiveClock()
        while self.running:
            # curr_time = datetime.now()
            with self.gs_lock:
                self.gs.advance_timeline(1)
            # print(f"server advance on time {self.gs.time}")
            change = self.gs.get_aggregated_changes()

            if self.gs.step % GSC_CHANGE_RATE == 0:
                msg = SockMessage(MsgType.GS_UPD, change)
                self.broadcast_message(msg)
                # print(f"Sent gs update to clients on time {change.step} at {datetime.now().time()}")

            # print(f"Time before tick : {datetime.now()}")
            clock.tick(constants.FPS)
            # print(f"{(datetime.now() - curr_time).total_seconds()}\t{datetime.now().time()}")
            # print(f"Time after tick : {datetime.now()}")

    def listen_for_connections(self):
        while self.connecting:
            conn, addr = self.server.accept()
            send_sock_msg(conn, MsgType.CONN, None) # confirm connection

            init_msg: SockMessage = recv_sock_msg(conn)
            if init_msg.msg_type != MsgType.CONN:
                print(f'Error occurred while connecting')
                break
            player_name = init_msg.msg_content
            self.add_player(player_name, conn, addr)

    def add_player(self, player_name, conn, addr):
        player_id = len(self.player_names)
        if player_name in self.player_names:
            player_name = f'{player_name}_{player_id}'

        if player_id == 0:  # minotaur
            mino_start = self.maze.get_random_edge_cell().get_pos()
            player = LeMinotaur(pos=mino_start,
                                size=(self.maze.cell_width, self.maze.cell_width),
                                is_player_controlled=True,
                                name=player_name)
        else:
            center = (constants.ROWS // 2 + 0.5) * self.maze.cell_width
            player_start = CoordPair(center, center)
            player = LePlayer(player_start,
                              (self.maze.cell_width / 2, self.maze.cell_width / 2),
                              name=player_name)
        self.gs.add_player(player)

        # send current players, their ready status and final player name to the client
        welcome_msg = SockMessage(MsgType.LOBBY_INIT, (player_name, self.player_ready_map))
        send_message(conn, welcome_msg)

        # send player name to clients
        msg = SockMessage(MsgType.CONN, player_name)

        self.player_names.append(player_name)
        self.clients[player_name] = conn
        self.player_ready_map[player_name] = False
        self.broadcast_message(msg)
        print(f"Player connected: {addr} with name {player_name}")

        client_listen_thread = Thread(target=self.listen_to_client, args=(player_name,), daemon=True)
        self.client_listen_threads[player.name] = client_listen_thread
        client_listen_thread.start()

    def start(self):
        print("Server started, waiting for connections...")

        # Listen for game start (console)
        Thread(target=self.listen_for_start_command, daemon=True).start()

        # Listen for connections (hamachi VPN)
        Thread(target=self.listen_for_connections, daemon=True).start()

        while self.connecting:  # This will just keep the main thread from progressing until 'start' command is given
            time.sleep(0.1)

        print(f"Starting the game with {len(self.player_names)} players")
        # send initial game state and start the game
        self.broadcast_message(SockMessage(MsgType.START, self.gs))

        # Start a thread that advances the game state and broadcasts it to all clients
        self.broadcast_advance_thread.start()


if __name__ == "__main__":
    HAMACHI_IP = input("Enter the HAMACHI IP of the host (Dimas)")
    server = GameServer(host=HAMACHI_IP)
    try:
        server.start()
        while server.connecting or server.running:  # Keep main thread alive while server is running
            time.sleep(1)
    finally:
        server.server.close()
