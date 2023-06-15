import socket
import threading

import constants
import helper
from threading import Thread
import time
from game_state import GameState
from maze import Maze
from player import Player
from minotaur import Minotaur
from coordpair import CoordPair
from constants import *


class GameServer:
    def __init__(self, host='localhost', port=7777):
        self.player_input_threads: dict[Player, threading.Thread] = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        self.clients: dict[Player, socket.socket] = {}

        self.maze = Maze(ROWS, WIDTH)
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

    def input_movement(self, conn, player):
        while self.running:
            try:
                # print("Waiting for move direction from player...")
                move_direction = helper.recv_message(conn)
                # print("Received move direction.")
                # print("Move direction loaded successfully.")
                player.move_direction = move_direction
            except Exception as e:
                print(f"Error {e} occurred during movement input.")

    def advance_and_broadcast(self):
        advance_cnt = 0
        while self.running:
            time.sleep(1.0 / FPS)
            change = self.gs.advance_timeline(1)
            advance_cnt += 1

            if advance_cnt % 1000 == 0:
                print(f"Advanced game state timeline {advance_cnt} times.")

            for conn in self.clients.values():
                try:
                    # print("Sending game state change to player...")
                    helper.send_message(conn, change)
                    # print("Game state change sent.")
                except Exception as e:
                    print(f"Error {e} occurred during broadcast.")

    def listen_for_connections(self):
        while True:
            conn, addr = self.server.accept()
            if not self.connecting:
                break
            if len(self.clients) == 0:  # minotaur
                mino_start = self.maze.get_random_edge_cell().get_pos()
                player = Minotaur(mino_start, (self.maze.cell_width, self.maze.cell_width), MINOTAUR_IMG, is_player_controlled=True)
            else:
                center = (ROWS // 2 + 0.5) * self.maze.cell_width
                player_start = CoordPair(center, center)
                player = Player(player_start, (self.maze.cell_width / 2, self.maze.cell_width / 2), PLAYER_IMG)
            self.gs.add_player(player)

            player_id = len(self.clients)
            print("Sending player ID to client...")
            conn.send(player_id.to_bytes(4, byteorder='big'))
            print("Player ID sent.")
            helper.send_message(conn, self.gs)
            self.clients[player] = conn
            print(f"Player connected: {addr}")

            thread = Thread(target=self.input_movement, args=(conn, player), daemon=True)
            self.player_input_threads[player] = thread
            print("Started thread to handle client.")

    def start(self):
        print("Server started, waiting for connections...")

        # Listen for game start (console)
        Thread(target=self.listen_for_start_command, daemon=True).start()

        # Listen for connections (hamachi VPN)
        Thread(target=self.listen_for_connections, daemon=True).start()

        while self.connecting:  # This will just keep the main thread from progressing until 'start' command is given
            time.sleep(0.1)

        print(f"Starting the game with {len(self.clients)} players")
        # Send "start" message to all clients
        for conn in self.clients.values():
            helper.send_message(conn, constants.START)

        # Start reading player input and send them initial game state
        for player, thread in self.player_input_threads.items():
            helper.send_message(self.clients[player], self.gs)
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
