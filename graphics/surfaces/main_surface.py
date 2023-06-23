from ..surface_manager import SurfaceType
from le_surface import *
from surface_update_data import SurfaceUpdateData


class MainSurface(LeSurface):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)
        self._type = SurfaceType.MAIN

    def update(self, upd_data: SurfaceUpdateData):
        self._surface.fill(constants.GREY)
