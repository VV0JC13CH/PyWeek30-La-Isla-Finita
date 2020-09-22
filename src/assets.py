import arcade
# to be cross-platform:
from pathlib import Path

UI_SCALING = 0.5
BG_SCALING = 1
SKY_SCALING = 1


def path_to_string(directory, file):
    return str(Path.cwd().joinpath(directory, file).resolve())


# INTRO
intro_authors = arcade.load_texture(path_to_string('gfx', 'intro_team_white.png'))

# UI
player_cursor_idle = arcade.Sprite(path_to_string('gfx', 'cursor_idle.png'), UI_SCALING)
player_cursor_hover = arcade.Sprite(path_to_string('gfx', 'cursor_hover.png'), UI_SCALING)
player_cursor_select = arcade.Sprite(path_to_string('gfx', 'cursor_select.png'), UI_SCALING)

# UI BUTTONS
button_idle = arcade.Sprite(path_to_string('gfx', 'ui_button.png'), UI_SCALING)
button_hover = arcade.Sprite(path_to_string('gfx', 'ui_button_hover.png'), UI_SCALING)
button_start_idle = arcade.Sprite(path_to_string('gfx', 'ui_button_start.png'), UI_SCALING)
button_start_hover = arcade.Sprite(path_to_string('gfx', 'ui_button_start_hover.png'), UI_SCALING)
button_exit_idle = arcade.Sprite(path_to_string('gfx', 'ui_button_exit.png'), UI_SCALING)
button_exit_hover = arcade.Sprite(path_to_string('gfx', 'ui_button_exit_hover.png'), UI_SCALING)
button_resume_idle = arcade.Sprite(path_to_string('gfx', 'ui_button_resume.png'), UI_SCALING)
button_resume_hover = arcade.Sprite(path_to_string('gfx', 'ui_button_resume_hover.png'), UI_SCALING)
button_restart_idle = arcade.Sprite(path_to_string('gfx', 'ui_button_restart.png'), UI_SCALING)
button_restart_hover = arcade.Sprite(path_to_string('gfx', 'ui_button_restart_hover.png'), UI_SCALING)
button_restart1_idle = arcade.Sprite(path_to_string('gfx', 'ui_button_restart.png'), UI_SCALING)
button_restart1_hover = arcade.Sprite(path_to_string('gfx', 'ui_button_restart_hover.png'), UI_SCALING)
button_restart2_idle = arcade.Sprite(path_to_string('gfx', 'ui_button_restart.png'), UI_SCALING)
button_restart2_hover = arcade.Sprite(path_to_string('gfx', 'ui_button_restart_hover.png'), UI_SCALING)
button_restart3_idle = arcade.Sprite(path_to_string('gfx', 'ui_button_restart.png'), UI_SCALING)
button_restart3_hover = arcade.Sprite(path_to_string('gfx', 'ui_button_restart_hover.png'), UI_SCALING)
button_slot1_idle = arcade.Sprite(path_to_string('gfx', 'ui_button_slot1.png'), UI_SCALING)
button_slot1_hover = arcade.Sprite(path_to_string('gfx', 'ui_button_slot1_hover.png'), UI_SCALING)
button_slot2_idle = arcade.Sprite(path_to_string('gfx', 'ui_button_slot2.png'), UI_SCALING)
button_slot2_hover = arcade.Sprite(path_to_string('gfx', 'ui_button_slot2_hover.png'), UI_SCALING)
button_slot3_idle = arcade.Sprite(path_to_string('gfx', 'ui_button_slot3.png'), UI_SCALING)
button_slot3_hover = arcade.Sprite(path_to_string('gfx', 'ui_button_slot3_hover.png'), UI_SCALING)
button_menu_idle = arcade.Sprite(path_to_string('gfx', 'ui_button_menu.png'), UI_SCALING)
button_menu_hover = arcade.Sprite(path_to_string('gfx', 'ui_button_menu_hover.png'), UI_SCALING)

# BACKGROUND
dynamic_background_frames = []


for x in range(1,7,1):
    background = arcade.Sprite(path_to_string('gfx', 'bg_full_island'+str(x)+'.png'), BG_SCALING)
    dynamic_background_frames.append(background)

# SEA

sea = arcade.Sprite(path_to_string('gfx', 'bg_see.png'), BG_SCALING)


# SKY
game_sky = arcade.Sprite(path_to_string('gfx', 'game_sky.png'), SKY_SCALING)

# SFX

# MUSIC
track01 = path_to_string('music', 'track01.mp3')
track02 = path_to_string('music', 'track02.mp3')
songs_list = [track01, track02]
