from le_surface import*
from surface_update_data import SurfaceUpdateData
from graphics.drawer import draw_cell
from ..surface_manager import SurfaceType


class MazeSurface(LeSurface):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)
        self._type = SurfaceType.MAZE

    def update(self, upd_data: SurfaceUpdateData):
        for cell in upd_data.cells_to_update:
            draw_cell(cell, self._surface)
