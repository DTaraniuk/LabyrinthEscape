from .le_surface import*


class PathSurface(LeSurface):
    def __init__(self, surface: pygame.Surface, is_rendered=False):
        super().__init__(surface, is_rendered)
        self._type = SurfaceType.PATH

    def update(self, upd_data: SurfaceUpdateData):
        path = upd_data.path
        path_surface = self._surface
        if len(path) == 0:
            return False
        cell_width = constants.WIDTH / constants.ROWS
        points: list[tuple[int, int]] = []
        for cell in path:
            points.append((cell.index_in_row * cell_width + cell_width / 2, cell.index_in_col * cell_width + cell_width / 2))
        pygame.draw.lines(path_surface, upd_data.path_color, closed=False, points=points, width=constants.WALL_WIDTH)
