from .le_surface import*
from graphics.drawer import draw_cell


class CellSurface(LeSurface):
    def __init__(self, surface: pygame.Surface, is_rendered=False):
        super().__init__(surface, is_rendered)
        self._type = SurfaceType.CELL

    def update(self, upd_data: SurfaceUpdateData):
        for cell in upd_data.cells_to_update:
            draw_cell(cell, self._surface)
