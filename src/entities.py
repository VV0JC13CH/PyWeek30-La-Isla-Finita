import arcade
import assets


class Entity(arcade.SpriteList):
    def __init__(self):
        super().__init__()


class Cursor(Entity):
    def __init__(self):
        super().__init__()
        self.center_x = 50
        self.center_y = 50
        self.state = 'idle'
        self.idle = assets.player_cursor_idle
        self.hover = assets.player_cursor_hover
        self.select = assets.player_cursor_select
        self.append(self.idle)
        self.append(self.hover)
        self.append(self.select)

    def get_position(self, dx, dy):
        for sprite in self:
            sprite.center_x = dx
            sprite.center_y = dy
