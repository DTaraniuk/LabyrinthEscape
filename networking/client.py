import pygame
import socket
import sys
import os
import time
import threading
proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(proj_dir)
sys.path.append(proj_dir)
from common import helper, constants
from graphics import Renderer
from game_logic import GameState, GameStateChange, CoordPair
from threading import Thread
from sock_message import SockMessage, MsgType
from datetime import datetime, timedelta
from network_constants import *
from live_clock import LiveClock


class Client:
    def __init__(self, ip, port=7777):
        self.win = pygame.display.set_mode((constants.WIDTH, constants.WIDTH))  # Create window with 800x800 resolution
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))

        self._receive_player_name()
        self.client_gs: GameState = None
        self.renderer = Renderer(self.win, self.player_name)
        self.game_state_lock: threading.Lock = threading.Lock()

        self.move_thread: threading.Thread = Thread(target=self.send_movement, daemon=True)
        self.render_thread: threading.Thread = Thread(target=self.render_game, daemon=True)
        self.update_thread: threading.Thread = Thread(target=self.update_game_state, daemon=True)

    # region init
    def _receive_player_name(self):
        self.player_name: str = helper.recv_message(self.client)

    def _receive_initial_game_state(self):
        gs = helper.recv_message(self.client)
        if not isinstance(gs, GameState):
            print("failed to get initial gs")
            self.client.close()
            exit(1)
        self.client_gs = gs

    # endregion

    # region run
    def update_game_state(self):
        while True:
            try:
                msg: SockMessage = helper.recv_message(self.client)
                with self.game_state_lock:
                    if msg.msg_type == MsgType.GSC:
                        game_state_change: GameStateChange = msg.msg_content
                        self.client_gs.apply_change(game_state_change)
                        # print(f"recv update on time\t{self.client_gs.step} at {datetime.now().time()}")
                    elif msg.msg_type == MsgType.MOVE:
                        player_name, new_direction, time = msg.msg_content
                        self.client_gs.update_player_direction(player_name, new_direction, time)
            except Exception as e:
                print(f"Error: {e}")
                break

    def send_movement(self):
        prev_vec = CoordPair()
        while True:
            player_move_vector = helper.input_movement()
            if not player_move_vector.equals(prev_vec):
                # print(f"sent move on time {self.client_gs.step}")
                helper.send_message(self.client, player_move_vector)
                prev_vec = player_move_vector

            time.sleep(1.0 / constants.FPS)

    def render_game(self):
        clock = LiveClock()
        while True:
            print(self.client_gs.step)
            curr_time = datetime.now()
            try:
                print(f"__ advance render {(datetime.now() - curr_time).total_seconds()}")
                with self.game_state_lock:
                    self.client_gs.advance_timeline(1)
                print(f"advance __ render {(datetime.now() - curr_time).total_seconds()}")
                self.renderer.render(self.client_gs)
                print(f"advance render __ {(datetime.now() - curr_time).total_seconds()}")
            except Exception as e:
                print(f"Error: {e}")
                break

            # print(f"Time before tick : {datetime.now()}")
            clock.tick(constants.FPS)
            # print(f"{(datetime.now() - curr_time).total_seconds()}\t{datetime.now().time()}")
            # print(f"Time after tick : {datetime.now()}")

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
