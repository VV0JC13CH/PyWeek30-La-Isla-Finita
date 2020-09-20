import arcade
from pathlib import Path


def path_to_string(directory, file):
    return str(Path.cwd().joinpath(directory, file).resolve())


UI_SCALING = 0.5


# INTRO
intro_authors = arcade.load_texture(path_to_string('gfx', 'intro_team_white.png'))

# UI

player_cursor_idle = arcade.Sprite(path_to_string('gfx', 'cursor_idle.png'), UI_SCALING)
player_cursor_hover = arcade.Sprite(path_to_string('gfx', 'cursor_hover.png'), UI_SCALING)
player_cursor_select = arcade.Sprite(path_to_string('gfx', 'cursor_select.png'), UI_SCALING)

# STRINGS
# GAME
game_sky = arcade.load_texture(path_to_string('gfx', 'game_sky.png'))