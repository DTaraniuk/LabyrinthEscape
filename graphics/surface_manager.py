import pygame
import enum
from common.constants import *
from .surfaces import *


class SurfaceType(enum.Enum):
    MAIN = 'main'
    MAZE = 'maze'
    GRID = 'grid'
    PATH = 'path'
    TEXT = 'text'
    PLAY = 'play'
    OPAQ = 'opaque'


# The order is crucial
surface_classes = {
            SurfaceType.MAZE: MazeSurface,
            SurfaceType.GRID: GridSurface,
            SurfaceType.PATH: PathSurface,
            SurfaceType.PLAY: PlaySurface,
            SurfaceType.OPAQ: OpaqueSurface,
            SurfaceType.TEXT: TextSurface
        }


class SurfaceManager:
    def __init__(self, main_s: pygame.Surface):
        self._surfaces: dict[SurfaceType, LeSurface] = {SurfaceType.MAIN: MainSurface(main_s)}
        self._init_surfaces()

    def _init_surfaces(self):
        scr_size = (WIDTH, WIDTH)
        self._surfaces = {key: cls(pygame.Surface(scr_size, pygame.SRCALPHA)) for key, cls in surface_classes.items()}

    # def create_surface(self, surface_type: SurfaceType, size: Tuple[int, int]):
    #     self._surfaces[surface_type] = surface_classes[surface_type](pygame.Surface(size, pygame.SRCALPHA))

    def get_surface(self, surface_type: SurfaceType) -> LeSurface:
        return self._surfaces.get(surface_type, None)

    def clear_surface(self, surface_type: SurfaceType):
        surface_ = self._surfaces.get(surface_type, None)
        if surface_ is not None:
            surface_.clear()

    def render(self, rect_list: list[pygame.Rect] = None):
        main_s: LeSurface = self._surfaces[SurfaceType.MAIN]

        if rect_list is not None:
            for surface_type, surface in self._surfaces.items():
                if not surface.is_rendered:
                    continue
                for rect in rect_list:
                    main_s.blit(surface, rect, area=rect)
        else:
            for surface_type, surface in self._surfaces.items():
                if not surface.is_rendered:
                    continue
                dest = (0, 0)
                main_s.blit(surface, dest)

        pygame.display.flip()

    def show_surface(self, surface_type: SurfaceType):
        self._surfaces[surface_type].is_rendered = True

    def hide_surface(self, surface_type: SurfaceType):
        self._surfaces[surface_type].is_rendered = False
