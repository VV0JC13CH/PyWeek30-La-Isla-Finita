import arcade

UI_SCALING = 0.5

# INTRO
intro_authors = arcade.load_texture("gfx/intro_team_white.png")

# UI

player_cursor_idle = arcade.Sprite("gfx/cursor_idle.png", UI_SCALING)
player_cursor_hover = arcade.Sprite("gfx/cursor_hover.png", UI_SCALING)
player_cursor_select = arcade.Sprite("gfx/cursor_select.png", UI_SCALING)

# STRINGS

# GAME
game_sky = arcade.load_texture("gfx/game_sky.png")