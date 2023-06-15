import pygame
import socket
from common import helper, constants
import time
from graphics import Renderer
from game_logic import GameState, GameStateChange, CoordPair
from threading import Thread
from queue import Queue


class Client:
    def __init__(self, ip, port=7777):
        self.win = pygame.display.set_mode((constants.WIDTH, constants.WIDTH))  # Create window with 800x800 resolution
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))
        self.queue = Queue()

        self._receive_player_id()
        self.gs = self._receive_initial_game_state()
        self.renderer = Renderer(self.win, self.player_id)

        self.move_thread = Thread(target=self.send_movement, daemon=True)

    def _receive_player_id(self):
        received_data = self.client.recv(4)
        self.player_id = int.from_bytes(received_data, byteorder='big')

    def _receive_initial_game_state(self):
        gs = helper.recv_message(self.client)
        if not isinstance(gs, GameState):
            print("failed to get initial gs")
            self.client.close()
            exit(1)
        return gs

    def send_movement(self):
        prev_vec = CoordPair()
        while True:
            player_move_vector = helper.input_movement()
            if not player_move_vector.equals(prev_vec):
                helper.send_message(self.client, player_move_vector)
                prev_vec = player_move_vector

            time.sleep(1.0 / constants.FPS)

    def run(self):
        # Wait for "start" message from server
        start_message = helper.recv_message(self.client)
        if start_message != constants.START:
            print("Did not receive 'start' message from server.")
            self.client.close()
            return

        self.move_thread.start()
        # receive initial game state from server
        self.gs = helper.recv_message(self.client)

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.client.close()
                    return

            try:
                game_state_change: GameStateChange = helper.recv_message(self.client)
                self.gs.apply_change(game_state_change)

                self.renderer.render(self.gs)
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
