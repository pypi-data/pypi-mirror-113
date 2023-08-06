import pygame
import pkg_resources


# Mixins
from pystage.core._events import _Events
from pystage.core._motion import _Motion
from pystage.core._sensing import _Sensing, _SensingSprite
from pystage.core._looks import _LooksSprite
from pystage.core._pen import _Pen
from pystage.core._variables import _Variables
from pystage.core._operators import _Operators
from pystage.core._control import _ControlSprite
from pystage.core._sound import _Sound


class CoreSprite(_Motion, _Events, _LooksSprite, _Sound, _Sensing, _SensingSprite, _ControlSprite, _Operators, _Variables, _Pen):

    def __init__(self, stage, costume="default"):
        self.stage = stage
        # Above attributes need to be set first so that mixins can access them properly
        super().__init__()
        default_file = pkg_resources.resource_filename("pystage", "images/zombie_idle.png")
        self.image = pygame.image.load(default_file)
        self.rect = self.image.get_rect()
        if costume:
            self.pystage_addcostume(costume)
        # The facade is the translated API
        self.facade = None


    def update(self, dt):
        self.code_manager._update(dt)
        self.costume_manager.update_sprite_image()
        self._update_pen()


    def _pg_pos(self):
        return pygame.Vector2(self.x + self.stage.center_x, 
                -self.y + self.stage.center_y)


    def _update_pos_from_rect(self):
        pos = self.rect.topleft + self.costume_manager.get_offset()
        self.x = pos.x - self.stage.center_x
        self.y = -pos.y + self.stage.center_y

    def __str__(self):
        return self.costume_manager.get_costume().name
