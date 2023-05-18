import pygame
import socket
import pickle
import helper
from threading import Thread
from renderer import Renderer

pygame.init()
win = pygame.display.set_mode((800, 800))  # Create window with 800x800 resolution

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


def handle_server_data(client_):
    while True:
        try:
            print("Waiting for data from server...")
            # Receive data from the server
            game_state = helper.recv_message(client_)
            print("Received data from server.")
            print("Data loaded successfully.")

            # Pass the game_state to the renderer
            renderer.update_surfaces(game_state)
            renderer.render(game_state)

        except Exception as e:
            print(f"Error: {e}")
            break


# Create the renderer with the player
renderer = Renderer(win, player_id)

# Start the thread to handle data from the server
Thread(target=handle_server_data, args=(client,), daemon=True).start()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # Handle key press events for player movement
        player_move_vector = helper.input_movement()

        print("Sending player move vector to server...")
        helper.send_message(client, player_move_vector)
        print("Player move vector sent.")
