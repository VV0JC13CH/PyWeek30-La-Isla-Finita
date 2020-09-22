import arcade
# to be cross-platform:
from pathlib import Path

UI_SCALING = 0.5
BG_SCALING = 1


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

# BUSH

bush1 = arcade.Sprite(path_to_string('gfx', 'bg_bush1.png'), BG_SCALING)
bush2 = arcade.Sprite(path_to_string('gfx', 'bg_bush2.png'), BG_SCALING)
bush3 = arcade.Sprite(path_to_string('gfx', 'bg_bush3.png'), BG_SCALING)
bush4 = arcade.Sprite(path_to_string('gfx', 'bg_bush4.png'), BG_SCALING)
bush5 = arcade.Sprite(path_to_string('gfx', 'bg_bush5.png'), BG_SCALING)
bush6 = arcade.Sprite(path_to_string('gfx', 'bg_bush6.png'), BG_SCALING)

# ISLAND

island1 = arcade.Sprite(path_to_string('gfx', 'bg_island1.png'), BG_SCALING)
island2 = arcade.Sprite(path_to_string('gfx', 'bg_island2.png'), BG_SCALING)
island3 = arcade.Sprite(path_to_string('gfx', 'bg_island3.png'), BG_SCALING)
island4 = arcade.Sprite(path_to_string('gfx', 'bg_island4.png'), BG_SCALING)
island5 = arcade.Sprite(path_to_string('gfx', 'bg_island5.png'), BG_SCALING)
island6 = arcade.Sprite(path_to_string('gfx', 'bg_island6.png'), BG_SCALING)

# LEAFS of BIGGEST PALMA

leafs1 = arcade.Sprite(path_to_string('gfx', 'bg_bg_leafs1.png'), BG_SCALING)
leafs2 = arcade.Sprite(path_to_string('gfx', 'bg_bg_leafs2.png'), BG_SCALING)
leafs3 = arcade.Sprite(path_to_string('gfx', 'bg_bg_leafs3.png'), BG_SCALING)
leafs4 = arcade.Sprite(path_to_string('gfx', 'bg_bg_leafs4.png'), BG_SCALING)
leafs5 = arcade.Sprite(path_to_string('gfx', 'bg_bg_leafs5.png'), BG_SCALING)
leafs6 = arcade.Sprite(path_to_string('gfx', 'bg_bg_leafs6.png'), BG_SCALING)

# TREE PALMA

tree1 = arcade.Sprite(path_to_string('gfx', 'bg_tree1.png'), BG_SCALING)
tree2 = arcade.Sprite(path_to_string('gfx', 'bg_tree2.png'), BG_SCALING)
tree3 = arcade.Sprite(path_to_string('gfx', 'bg_tree3.png'), BG_SCALING)
tree4 = arcade.Sprite(path_to_string('gfx', 'bg_tree4.png'), BG_SCALING)
tree5 = arcade.Sprite(path_to_string('gfx', 'bg_tree5.png'), BG_SCALING)
tree6 = arcade.Sprite(path_to_string('gfx', 'bg_tree6.png'), BG_SCALING)

# SEA

sea = arcade.Sprite(path_to_string('gfx', 'bg_see.png'), BG_SCALING)

# SEA

sea_effects1 = arcade.Sprite(path_to_string('gfx', 'bg_see_effects1.png'), BG_SCALING)
sea_effects2 = arcade.Sprite(path_to_string('gfx', 'bg_see_effects2.png'), BG_SCALING)
sea_effects3 = arcade.Sprite(path_to_string('gfx', 'bg_see_effects3.png'), BG_SCALING)
sea_effects4 = arcade.Sprite(path_to_string('gfx', 'bg_see_effects4.png'), BG_SCALING)
sea_effects5 = arcade.Sprite(path_to_string('gfx', 'bg_see_effects5.png'), BG_SCALING)
sea_effects6 = arcade.Sprite(path_to_string('gfx', 'bg_see_effects6.png'), BG_SCALING)





# GAME
game_sky = arcade.load_texture(path_to_string('gfx', 'game_sky.png'))

# SFX

# MUSIC
track01 = path_to_string('music', 'track01.mp3')
track02 = path_to_string('music', 'track02.mp3')
songs_list = [track01, track02]
