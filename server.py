import socket
import pickle
import helper
from threading import Thread
from game_state import GameState
from maze import Maze
from player import Player
from minotaur import Minotaur
from coordpair import CoordPair
from constants import *


class GameServer:
    def __init__(self, host='localhost', port=7777):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        self.clients = []

        self.maze = Maze(ROWS, WIDTH)
        self.maze.generate_labyrinth()
        self.gs = GameState(self.maze)

        self.running = True

    def handle_client(self, conn, player):
        while self.running:
            try:
                print("Waiting for move direction from player...")
                move_direction = helper.recv_message(conn)
                print("Received move direction.")
                print("Move direction loaded successfully.")
                player.move_direction = move_direction
                self.gs.advance_timeline(1)
                print("Sending game state to player...")
                helper.send_message(conn, self.gs)
                print("Game state sent.")
            except Exception as e:
                print(f"Error {e} occurred. Removing client.")
                self.clients.remove(conn)
                self.gs.players.remove(player)
                if self.gs.minotaur == player:
                    self.gs.minotaur = None
                conn.close()
                break

    def start(self):
        print("Server started, waiting for connections...")
        while self.running:
            conn, addr = self.server.accept()
            if len(self.clients) == 0:  # minotaur
                mino_start = self.maze.get_random_edge_cell().get_pos()
                player = Minotaur(mino_start, (self.maze.cell_width, self.maze.cell_width), MINOTAUR_IMG, is_player_controlled=True)
            else:
                center = (ROWS // 2 + 0.5) * self.maze.cell_width
                player_start = CoordPair(center, center)
                player = Player(player_start, (self.maze.cell_width/2, self.maze.cell_width/2), PLAYER_IMG)
            self.gs.add_player(player)

            player_id = len(self.clients)
            print("Sending player ID to client...")
            conn.send(player_id.to_bytes(4, byteorder='big'))
            print("Player ID sent.")
            self.clients.append(conn)
            print(f"Player connected: {addr}")

            thread = Thread(target=self.handle_client, args=(conn, player), daemon=True)
            thread.start()
            print("Started thread to handle client.")


if __name__ == "__main__":
    server = GameServer()
    try:
        server.start()
    finally:
        server.server.close()
