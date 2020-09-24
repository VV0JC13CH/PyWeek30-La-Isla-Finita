import arcade
# to be cross-platform:
from pathlib import Path

UI_SCALING = 0.5
BG_SCALING = 1
SKY_SCALING = 1
UNIT_SCALING = 1




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

button_textures = {"start": button_start_idle,
                   "start_hover": button_start_hover,
                   "exit": button_exit_idle,
                   "exit_hover": button_exit_hover,
                   "resume": button_resume_idle,
                   "resume_hover": button_resume_hover,
                   "restart": button_restart_idle,
                   "restart_hover": button_restart_hover,
                   "slot1": button_slot1_idle,
                   "slot1_hover": button_slot1_hover,
                   "restart1": button_restart1_idle,
                   "restart1_hover": button_restart1_hover,
                   "slot2": button_slot2_idle,
                   "slot2_hover": button_slot2_hover,
                   "restart2": button_restart2_idle,
                   "restart2_hover": button_restart2_hover,
                   "slot3": button_slot3_idle,
                   "slot3_hover": button_slot3_hover,
                   "restart3": button_restart3_idle,
                   "restart3_hover": button_restart3_hover,
                   "menu": button_menu_idle,
                   "menu_hover": button_menu_hover
}

# BACKGROUND
dynamic_background_frames = []
dynamic_background_sky_by_hour = []

for x in range(1,7,1):
    background = arcade.Sprite(path_to_string('gfx', 'bg_full_island'+str(x)+'.png'), BG_SCALING)
    dynamic_background_frames.append(background)
for x in range(1,25,1):
    sky = arcade.load_texture(path_to_string('gfx', 'sky'+str(x)+'.png'))
    dynamic_background_sky_by_hour.append(sky)


# SEA
sea = arcade.load_texture(path_to_string('gfx', 'bg_see.png'))

# Hero
hero_bottom_idle = []
hero_bottom_run = []
hero_bottom_throw = []
hero_top_idle = []
hero_top_run = []
hero_top_throw = []
hero_die = []
hero_top = (hero_top_idle, hero_top_run, hero_top_throw)
hero_bottom = (hero_bottom_idle, hero_bottom_run, hero_bottom_throw)

# Idle 2 frames
for x in range(1,3,1):
    _hero_bottom_idle = arcade.Sprite(path_to_string('gfx', 'hero_bottom_idle'+str(x)+'.png'), UNIT_SCALING)
    hero_bottom_idle.append(_hero_bottom_idle)
    _hero_top_idle = arcade.Sprite(path_to_string('gfx', 'hero_top_idle'+str(x)+'.png'), UNIT_SCALING)
    hero_top_idle.append(_hero_top_idle)

# Run 4 frames
for x in range(1,5,1):
    _hero_bottom_run = arcade.Sprite(path_to_string('gfx', 'hero_bottom_run'+str(x)+'.png'), UNIT_SCALING)
    hero_bottom_run.append(_hero_bottom_run)
    _hero_top_run = arcade.Sprite(path_to_string('gfx', 'hero_top_run'+str(x)+'.png'), UNIT_SCALING)
    hero_top_run.append(_hero_top_run)

# Throw 3 frames
for x in range(1,4,1):
    _hero_bottom_throw = arcade.Sprite(path_to_string('gfx', 'hero_bottom_throw'+str(x)+'.png'), UNIT_SCALING)
    hero_bottom_throw.append(_hero_bottom_throw)
    _hero_top_throw = arcade.Sprite(path_to_string('gfx', 'hero_top_throw'+str(x)+'.png'), UNIT_SCALING)
    hero_top_throw.append(_hero_top_throw)

# DIE 6 frames
for x in range(1,4,1):
    _hero_die = arcade.Sprite(path_to_string('gfx', 'hero_die'+str(x)+'.png'), UNIT_SCALING)
    hero_die.append(_hero_die)

# MUSIC
track01 = path_to_string('music', 'track01.mp3')
track02 = path_to_string('music', 'track02.mp3')
songs_list = [track01, track02]
