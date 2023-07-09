from .le_surface import*
from graphics.drawer import draw_wall


class WallSurface(LeSurface):
    def __init__(self, surface: pygame.Surface, is_rendered=False):
        super().__init__(surface, is_rendered)
        self._type = SurfaceType.CELL

    def update(self, upd_data: SurfaceUpdateData):
        for wall in upd_data.walls_to_update:
            draw_wall(self._surface, wall)
