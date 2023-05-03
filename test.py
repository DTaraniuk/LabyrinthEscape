import pygame

pygame.init()
pygame.display.set_mode((800, 600))

# Load a font and set its size
font = pygame.font.Font(None, 36)

# Render a text string
text = "Hello, Pygame!"
text_surface = font.render(text, True, (255, 255, 255))

# Get the dimensions of the rendered text surface
width, height = text_surface.get_size()

print(f"Text surface width: {width}, height: {height}")
