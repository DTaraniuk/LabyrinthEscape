import pygame
import socket
import pickle
from coordpair import CoordPair
from renderer import Renderer
from surface_manager import SurfaceManager
from main import init_surfaces
from constants import *
import event_handler

# The server's hostname or IP address
HOST = 'localhost'
# The port used by the server
PORT = 12345


def main(win: pygame.Surface) -> None:
    pygame.init()
    surface_manager = init_surfaces(win)

    clock = pygame.time.Clock()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Initially receive the game state from the server
        data = s.recv(1024)
        gs = pickle.loads(data)
        player = gs.get_player("player_name")  # replace "player_name" with actual player name
        player_renderer = Renderer(surface_manager, player)

        run = True
        event_handler.user_message(surface_manager, "Privet. Click to start", FONT_SIZE)
        surface_manager.render()
        while run:
            for event_ in pygame.event.get():
                if event_.type == pygame.QUIT:
                    run = False
                    break
            # move player
            keys = pygame.key.get_pressed()
            player_move_vector = CoordPair()
            if keys[pygame.K_UP]:
                player_move_vector += CoordPair(0, -1)
            if keys[pygame.K_DOWN]:
                player_move_vector += CoordPair(0, 1)
            if keys[pygame.K_LEFT]:
                player_move_vector += CoordPair(-1, 0)
            if keys[pygame.K_RIGHT]:
                player_move_vector += CoordPair(1, 0)

            # Send player move vector to server
            data = pickle.dumps(player_move_vector)
            s.sendall(data)

            # Receive updated game state from server
            data = s.recv(1024)
            gs = pickle.loads(data)

            clock.tick(FPS)
            player_renderer.render(gs)

    pygame.quit()


WIN = pygame.display.set_mode((WIDTH, WIDTH))
main(WIN)
