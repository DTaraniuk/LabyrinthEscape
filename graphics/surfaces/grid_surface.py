from le_surface import*
from surface_update_data import SurfaceUpdateData
from graphics import draw_grid
from ..surface_manager import SurfaceType


class GridSurface(LeSurface):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)
        self._type = SurfaceType.GRID

    def update(self, upd_data: SurfaceUpdateData):
        draw_grid(self._surface, constants.GREY)
