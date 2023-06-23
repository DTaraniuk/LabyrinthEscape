from .le_surface import*
from ..drawer import draw_grid


class GridSurface(LeSurface):
    def __init__(self, surface: pygame.Surface, is_rendered=False):
        super().__init__(surface, is_rendered)
        self._type = SurfaceType.GRID

    def update(self, upd_data: SurfaceUpdateData):
        draw_grid(self._surface, constants.GREY)
