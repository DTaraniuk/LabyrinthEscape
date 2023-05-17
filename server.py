import socket
import pickle
import pygame
from threading import Thread
from game_state import GameState
from maze import Maze
from player import Player
from minotaur import Minotaur
from coordpair import CoordPair
from constants import *

# The server's hostname or IP address
HOST = 'localhost'
# The port used by the server
PORT = 12345


def handle_client(conn, player, gs):
    while True:
        # Receive player move vector from client
        data = conn.recv(1024)
        player_move_vector = pickle.loads(data)

        # Update player's move direction based on received move vector
        player.move_direction = player_move_vector

        # Advance game state
        gs.advance_timeline(1)

        # Send updated game state to client
        data = pickle.dumps(gs)
        conn.sendall(data)


def main():
    maze = Maze(ROWS, WIDTH)
    maze.generate_labyrinth()

    center = (ROWS // 2 + 0.5) * maze.cell_width
    player_start = CoordPair(center, center)
    player_img = pygame.image.load(f"{IMG_FOLDER}\\{PLAYER_IMG}")
    player = Player(player_start, (maze.cell_width/2, maze.cell_width/2), player_img)

    mino_start = maze.get_random_edge_cell().get_pos()
    minotaur_img = pygame.image.load(f"{IMG_FOLDER}\\{MINOTAUR_IMG}")
    minotaur = Minotaur(mino_start, (maze.cell_width, maze.cell_width), minotaur_img)

    gs = GameState(minotaur, maze)
    gs.add_player(player)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            Thread(target=handle_client, args=(conn, player, gs)).start()

main()
