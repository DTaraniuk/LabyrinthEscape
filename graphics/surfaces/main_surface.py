from .le_surface import *


class MainSurface(LeSurface):
    def __init__(self, surface: pygame.Surface, is_rendered=False):
        super().__init__(surface, is_rendered)  # main surface is always rendered
        self._type = SurfaceType.MAIN

    def update(self, upd_data: SurfaceUpdateData):
        self._surface.fill(constants.GREY)
