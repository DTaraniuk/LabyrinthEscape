import pygame
import socket
import helper
from renderer import Renderer
import constants

pygame.init()
win = pygame.display.set_mode((constants.WIDTH, constants.WIDTH))  # Create window with 800x800 resolution

SERVER = "127.0.0.1"  # The IP of the server
PORT = 7777  # The port of the server
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
print("Connecting to the server...")
client.connect(ADDR)
print("Connected to the server.")

# Receive player ID from the server
print("Receiving player ID...")
received_data = client.recv(4)
player_id = int.from_bytes(received_data, byteorder='big')
print(f"Received player ID: {player_id}")


# Start the thread to handle data from the server
# Thread(target=handle_server_data, args=(client,), daemon=True).start()


clock = pygame.time.Clock()
# Create the renderer with the player
renderer = Renderer(win, player_id)
# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            client.close()
            break

    try:
        # Handle key press events for player movement
        player_move_vector = helper.input_movement()

        print("Sending player move vector to server...")
        helper.send_message(client, player_move_vector)
        print("Player move vector sent.")
        print("Waiting for data from server...")
        # Receive data from the server
        game_state = helper.recv_message(client)
        print("Received data from server.")
        print("Data loaded successfully.")

        # Pass the game_state to the renderer
        clock.tick(constants.FPS)
        renderer.render(game_state)
        # win.fill(constants.LIGHT_BLUE)

    except Exception as e:
        print(f"Error: {e}")
        break

client.close()
