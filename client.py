import pygame
import socket
import helper
from renderer import Renderer
from game_state import GameState, GameStateChange
import constants
from threading import Thread
from queue import Queue
from coordpair import CoordPair
pygame.init()


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
        self.move_thread.start()

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
        prev_vec = CoordPair(0, 0)
        while True:
            player_move_vector = helper.input_movement()
            if player_move_vector != prev_vec:
                helper.send_message(self.client, player_move_vector)
                prev_vec = player_move_vector

    def run(self):
        # Wait for "start" message from server
        start_message = helper.recv_message(self.client)
        if start_message != constants.START:
            print("Did not receive 'start' message from server.")
            self.client.close()
            return

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


if __name__ == "__main__":
    HAMACHI_IP = input("Enter the HAMACHI IP of the host (Dimas)")
    client = Client(HAMACHI_IP)
    client.run()
