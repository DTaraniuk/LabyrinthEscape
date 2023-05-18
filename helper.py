from pathfinding import*
from typing import Callable
from maze import Maze
from coordpair import CoordPair
import struct
import pygame
import pickle
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from renderer import Renderer


def wait_for_input():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            elif e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return


def read_endpoints(maze: Maze) -> Tuple[Cell, Cell]:
    click_num = 0
    width = WIDTH/ROWS
    start: Cell = None
    end: Cell = None
    while click_num < 2:
        click = pygame.event.wait()
        if click.type != pygame.MOUSEBUTTONDOWN:
            continue
        x, y = tuple(int(value // width) for value in click.pos)
        if click_num == 0:
            start = maze[x, y]
        else:
            end = maze[x, y]
        click_num += 1
    return start, end


def handle_pathfinding_call(renderer: 'Renderer', maze, algo: Callable[[Cell, Cell], PathfindingRes], path_color: tuple[int, int, int]):
    start, end = read_endpoints(maze)
    pathfinding_res = algo(start, end)
    # for cell in pathfinding_res.affected_nodes:
    #     cell.color = cell_color
    #     cell.request_update()
    renderer.render_path(pathfinding_res.path, path_color)


def input_movement() -> CoordPair:
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
    return player_move_vector


def send_message(sock, message):
    # Prefix each message with a 4-byte length (network byte order)
    data = pickle.dumps(message)
    message_length = len(data)
    sock.sendall(struct.pack('>I', message_length) + data)


def recv_message(sock):
    # Read message length and unpack it into an integer
    raw_message_length = recv_all(sock, 4)
    if not raw_message_length:
        return None
    message_length = struct.unpack('>I', raw_message_length)[0]
    # Read the message data
    return pickle.loads(recv_all(sock, message_length))


def recv_all(sock, length):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data
