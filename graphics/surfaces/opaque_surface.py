from .le_surface import*


class OpaqueSurface(LeSurface):
    def __init__(self, surface: pygame.Surface, is_rendered=False):
        super().__init__(surface, is_rendered)
        self._type = SurfaceType.OPAQ

    def update(self, upd_data: SurfaceUpdateData):
        shade_color = upd_data.shade_color if upd_data.shade_color else constants.GREY
        self._surface.fill(shade_color + (255 * (1 - upd_data.opacity),))
