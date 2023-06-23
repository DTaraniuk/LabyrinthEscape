import pygame
from common.constants import *
from .surfaces import *


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
        self._main_surface = MainSurface(main_s, True)
        self._surfaces: dict[SurfaceType, LeSurface] = {}
        self._init_surfaces()

    def _init_surfaces(self):
        scr_size = (WIDTH, WIDTH)
        self._surfaces = {key: cls(pygame.Surface(scr_size, pygame.SRCALPHA), False) for key, cls in surface_classes.items()}
        essentials = [SurfaceType.MAZE,
                      SurfaceType.PLAY]
        self.show_surfaces(essentials)

    def get_surface(self, surface_type: SurfaceType) -> LeSurface:
        return self._surfaces.get(surface_type, None)

    def clear_surface(self, surface_type: SurfaceType):
        surface_ = self._surfaces.get(surface_type, None)
        if surface_ is not None:
            surface_.clear()

    def render(self, rect_list: list[pygame.Rect] = None):
        self._main_surface.update(None)  # just refresh it
        if rect_list is not None:
            for surface_type, surface in self._surfaces.items():
                if not surface.is_rendered:
                    continue
                for rect in rect_list:
                    self._main_surface.blit(surface, rect, area=rect)
        else:
            for surface_type, surface in self._surfaces.items():
                if not surface.is_rendered:
                    continue
                dest = (0, 0)
                self._main_surface.blit(surface, dest)

        pygame.display.flip()

    def update_surface(self, upd_data: SurfaceUpdateData, surface_type: SurfaceType):
        surface = self._surfaces.get(surface_type)
        if surface:
            surface.update(upd_data)

    def update_surfaces(self, upd_data: SurfaceUpdateData, surface_types: list[SurfaceType] = None):
        if not surface_types:
            surface_types = list(SurfaceType)
        for surface_type in surface_types:
            self._surfaces[surface_type].update(upd_data)

    def show_surface(self, surface_type: SurfaceType):
        self._surfaces[surface_type].is_rendered = True

    def hide_surface(self, surface_type: SurfaceType):
        self._surfaces[surface_type].is_rendered = False

    def show_surfaces(self, surface_types: list[SurfaceType] = None):
        if not surface_types:
            surface_types = list(SurfaceType)
        for surface_type in surface_types:
            self._surfaces[surface_type].is_rendered = True

    def hide_surfaces(self, surface_types: list[SurfaceType] = None):
        if not surface_types:
            surface_types = list(SurfaceType)
        for surface_type in surface_types:
            self._surfaces[surface_type].is_rendered = False
