import pygame
import socket
import time
import sys
import os
import copy
import threading
proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(proj_dir)
from common import helper, constants
from graphics import Renderer
from game_logic import GameState, GameStateChange, CoordPair
from threading import Thread
from sock_message import SockMessage, MsgType


class Client:
    def __init__(self, ip, port=7777):
        self.win = pygame.display.set_mode((constants.WIDTH, constants.WIDTH))  # Create window with 800x800 resolution
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))

        self._receive_player_id()
        self.server_gs: GameState = None
        # self.own_gs: GameState = None
        self.renderer = Renderer(self.win, self.player_id)

        self.move_thread: threading.Thread = Thread(target=self.send_movement, daemon=True)
        self.render_thread: threading.Thread = Thread(target=self.render_game, daemon=True)
        self.update_thread: threading.Thread = Thread(target=self.update_game_state, daemon=True)

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
        while True:
            try:
                msg: SockMessage = helper.recv_message(self.client)
                if msg.msg_type == MsgType.GSC:
                    game_state_change: GameStateChange = msg.msg_content
                    self.server_gs.apply_change(game_state_change)
                elif msg.msg_type == MsgType.MOVE:
                    player_name, new_direction = msg.msg_content
                    self.server_gs.update_player_direction(player_name, new_direction)

            except Exception as e:
                print(f"Error: {e}")
                break

    def send_movement(self):
        prev_vec = CoordPair()
        while True:
            player_move_vector = helper.input_movement()
            if not player_move_vector.equals(prev_vec):
                helper.send_message(self.client, player_move_vector)
                prev_vec = player_move_vector

            time.sleep(1.0 / constants.FPS)

    def render_game(self):
        clock = pygame.time.Clock()

        while True:
            try:
                # self.own_gs.advance_timeline(1)
                # self.renderer.render(self.own_gs)
                self.renderer.render(self.server_gs)
            except Exception as e:
                print(f"Error: {e}")
                break

            clock.tick(constants.FPS)

    # endregion
    def run(self):
        # Wait for "start" message from server
        start_message = helper.recv_message(self.client)
        if start_message != constants.START:
            print("Did not receive 'start' message from server.")
            self.client.close()
            return

        # receive initial game state from server
        self._receive_initial_game_state()
        # self.own_gs = copy.deepcopy(self.server_gs)
        self.move_thread.start()
        self.update_thread.start()
        self.render_thread.start()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.client.close()
                    return


pygame.init()
if __name__ == "__main__":
    HAMACHI_IP = input("Enter the HAMACHI IP of the host (Dimas)")
    client = Client(HAMACHI_IP)
    client.run()
