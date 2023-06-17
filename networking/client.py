import pygame
import socket
import time
import sys
import os
import copy
import threading
proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(proj_dir)
os.chdir(proj_dir)
from common import helper, constants
from graphics import Renderer
from game_logic import GameState, GameStateChange, CoordPair
from threading import Thread
from datetime import datetime


class Client:
    def __init__(self, ip, port=7777):
        self.win = pygame.display.set_mode((constants.WIDTH, constants.WIDTH))  # Create window with 800x800 resolution
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))
        self.game_state_lock = threading.Lock()

        self._receive_player_id()
        self.server_gs: GameState = None
        # self.own_gs: GameState = None
        self.renderer = Renderer(self.win, self.player_id)

        self.move_thread: threading.Thread = Thread(target=self.send_movement, daemon=True)
        self.update_thread: threading.Thread = None

    # region init
    def _receive_player_id(self):
        received_data = self.client.recv(4)
        self.player_id = int.from_bytes(received_data, byteorder='big')

    def _receive_initial_game_state(self):
        gs = helper.recv_message(self.client)
        if not isinstance(gs, GameState):
            print("failed to get initial gs")
            self.client.close()
            exit(1)
        self.server_gs = gs

    # endregion

    # region run
    def update_game_state(self):
        clock = pygame.time.Clock()
        while True:
            try:
                game_state_change: GameStateChange = helper.recv_message(self.client)
                with self.game_state_lock:
                    self.server_gs.apply_change(game_state_change)
                    # self.own_gs.populate(self.server_gs)
            except Exception as e:
                print(f"Error: {e}")
                break

            now = datetime.now().time()

            print(f"Current time: {now}, game time: {self.server_gs.time}")
            clock.tick(constants.FPS)

    def send_movement(self):
        prev_vec = CoordPair()
        while True:
            player_move_vector = helper.input_movement()
            if not player_move_vector.equals(prev_vec):
                helper.send_message(self.client, player_move_vector)
                prev_vec = player_move_vector

            time.sleep(1.0 / constants.FPS)

    # endregion
    def run(self):
        # Wait for "start" message from server
        start_message = helper.recv_message(self.client)
        if start_message != constants.START:
            print("Did not receive 'start' message from server.")
            self.client.close()
            return

        while True:
            msg = helper.recv_message(self.client)
            print(f"Received message from server: {msg}. Sending back:")
            reply = input("Enter the reply")
            helper.send_message(self.client, reply)

        # receive initial game state from server
        self._receive_initial_game_state()
        # self.own_gs = copy.deepcopy(self.server_gs)

        self.update_thread = Thread(target=self.update_game_state, daemon=True)
        self.move_thread.start()
        self.update_thread.start()

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.client.close()
                    return

            try:
                with self.game_state_lock:
                    # self.own_gs.advance_timeline(1)
                    # self.renderer.render(self.own_gs)

                    self.renderer.render(self.server_gs)
                clock.tick(constants.FPS)

            except Exception as e:
                print(f"Error: {e}")
                break

        self.client.close()


pygame.init()
if __name__ == "__main__":
    HAMACHI_IP = input("Enter the HAMACHI IP of the host (Dimas)")
    client = Client(HAMACHI_IP)
    client.run()
