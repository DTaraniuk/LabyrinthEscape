import pygame
from common import constants
from game_logic import LePlayer


class ImageStorage:
    def __init__(self):
        self.images: dict[str, pygame.Surface] = {}

    def _load_image(self, image_name, size) -> pygame.Surface:
        if image_name not in self.images:
            raw_image = pygame.image.load(f"{constants.IMG_FOLDER}\\{image_name}")
            converted_image = raw_image.convert_alpha()
            scaled_image = pygame.transform.scale(converted_image, size)
            self.images[image_name] = scaled_image
        return self.images[image_name]

    def get_or_add(self, player: LePlayer) -> pygame.Surface:
        image_name = player.get_image()
        if image_name:
            result_image = self._load_image(image_name, player.size)
        else:
            result_image = pygame.Surface(player.size, pygame.SRCALPHA)
            result_image.fill(constants.LIGHT_BLUE)
        return result_image
