from le_surface import*
from surface_update_data import SurfaceUpdateData
from common.helper import create_text_frame
from ..surface_manager import SurfaceType


class TextSurface(LeSurface):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)
        self._type = SurfaceType.TEXT

    def update(self, upd_data: SurfaceUpdateData):
        text = upd_data.text
        font = upd_data.font
        text_frame = create_text_frame(text,
                                       font,
                                       text_color=constants.PINK,
                                       frame_color=constants.BLACK,
                                       padding=int(font.get_height() / 2),
                                       aspect_ratio=(3, 2))
        width = text_frame.get_rect().width
        height = text_frame.get_rect().height
        x = (constants.WIDTH - width) / 2
        y = (constants.WIDTH - height) / 2
        self._surface.blit(text_frame, (x, y))
