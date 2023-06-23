from le_surface import*
from surface_update_data import SurfaceUpdateData
from graphics import draw_player
from game_logic import Player, Cell
from ..surface_manager import SurfaceType


class PlaySurface(LeSurface):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)
        self._type = SurfaceType.PLAY

    def update(self, upd_data: SurfaceUpdateData):
        self._surface.fill(constants.TRANSPARENT)

        players = upd_data.players_with_images

        if not players:
            return

        if upd_data.cells_to_update:
            players_to_draw = [p for p in players if is_player_in_cells(p[0], upd_data.cells_to_update)]
        else:
            players_to_draw = players
        for player, image in players_to_draw:
            draw_player(player, image, self._surface)


def is_player_in_cells(player: Player, cells: list[Cell]) -> bool:
    for cell in cells:
        c_x, c_y = cell.get_x(), cell.get_y()
        p_x, p_y = player.get_x(), player.get_y()
        if (c_x <= p_x < c_x + cell.width) and (c_y <= p_y < c_y + cell.width):
            return True
    return False
