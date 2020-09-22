import arcade
import os
import timeit

import entities
import settings

settings = settings.settings_load()

# INIT DATA A LOT OFF SETINGS
SCENES = ['INTRO', 'MAIN', 'OPTIONS', 'PAUSE', 'GAME_OVER', 'VICTORY', 'INTRODUCTION', 'LOAD', 'SCORES']
SET_TITLE = settings['GAME']['TITLE']
SET_SAVE_SLOTS = int(settings['DEFAULTS']['SAVE_SLOTS'])
DEFAULT_BG = arcade.color.WHITE
DEFAULT_FONT = arcade.color.BLACK
SET_MUSIC_VOLUME = settings['AUDIO']['MUSIC_VOL']
SET_SOUND_VOLUME = settings['AUDIO']['SOUND_VOL']
if int(settings['VIDEO']['FULL_RESOLUTION']) == 1:
    SET_FULL = True
    SET_WIDTH = int(settings['DEFAULTS']['WINDOW_WIDTH'])
    SET_HEIGHT = int(settings['DEFAULTS']['WINDOW_HEIGHT'])
    UI_SCALING = float(settings['DEFAULTS']['UI_SCALING'])
else:
    SET_FULL = False
    SET_WIDTH = int(settings['VIDEO']['WINDOW_WIDTH'])
    SET_HEIGHT = int(settings['VIDEO']['WINDOW_HEIGHT'])
    UI_SCALING = float(settings['VIDEO']['UI_SCALING'])
# DEVELOPER MODE
if int(settings['DEFAULTS']['SKIP_INTRO']) == 1:
    SET_SKIP_INTRO = 1
    CURRENT_SCENE = SCENES[1]
else:
    SET_SKIP_INTRO = 0
    CURRENT_SCENE = SCENES[0]

SET_DEVELOPER = int(settings['DEFAULTS']['DEVELOPER_MODE'])


class IntroView(arcade.View):
    def __init__(self):
        super().__init__()
        self.wait_sec = 0

    def on_show(self):
        arcade.set_background_color(DEFAULT_BG)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(self.window.width/2-entities.intro_team.width/4,
                                            self.window.height/2-entities.intro_team.height/4,
                                            entities.intro_team.width/2, entities.intro_team.height/2, entities.intro_team)
        if self.wait_sec >= 1:
            arcade.draw_text("PRESENTS", self.window.width/2,
                             self.window.height/2-entities.intro_team.height/4-60,
                             DEFAULT_FONT, font_size=20, anchor_x="center")
        if self.wait_sec >= 2:
            arcade.draw_text("PyWeek 30 Entry", self.window.width/2,
                             self.window.height/2-entities.intro_team.height/4-150,
                             DEFAULT_FONT, font_size=30, anchor_x="center")
        if self.wait_sec >= 5:
            arcade.draw_text("Click to continue...", 0,
                             0, DEFAULT_FONT, font_size=20, anchor_x="left")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        menu_view = MenuView()
        self.window.show_view(menu_view)

    def update(self, delta_time):
        self.wait_sec += delta_time


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.button_start = entities.Button(x=self.window.width/2, y=self.window.height*2/6,
                                            width=200, height=50,
                                            texture_idle=entities.button_textures['start'],
                                            texture_hover=entities.button_textures['start_hover'])
        self.button_exit = entities.Button(x=self.window.width / 2, y=self.window.height*1/6,
                                           width=200, height=50,
                                           texture_idle=entities.button_textures['exit'],
                                           texture_hover=entities.button_textures['exit_hover'])
        self.background = entities.DynamicBackground(x=self.window.width/2, y=self.window.height/2,
                                                     res_width=self.window.width,
                                                     res_height=self.window.height)

    def on_show(self):
        arcade.set_background_color(DEFAULT_BG)

    def on_update(self, delta_time: float):
        self.background.on_update()
        self.button_start.detect_mouse(self.window.cursor)
        self.button_exit.detect_mouse(self.window.cursor)

    def on_draw(self):
        arcade.start_render()
        self.background.on_draw()
        self.button_start.draw()
        self.button_exit.draw()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        if self.button_start.current_state == 'hover':
            start_game_view = StartGame(background = self.background)
            self.window.show_view(start_game_view)
        if self.button_exit.current_state == 'hover':
            self.window.close()


class StartGame(arcade.View):
    def __init__(self, background):
        super().__init__()
        self.background = background
        self.slot_buttons = []
        self.slot_buttons_restart = []
        self.margin = self.window.width/4

        for slot in range(1, SET_SAVE_SLOTS+1):
            _slot_button = entities.Button(x=self.margin*slot, y=self.window.height/3,
                                           width=150, height=35,
                                           texture_idle=entities.button_textures['slot'+str(slot)],
                                           texture_hover=entities.button_textures['slot'+str(slot)+'_hover'])
            _slot_restart_button = entities.Button(x=self.margin*slot, y=self.window.height/4,
                                                   width=150, height=35,
                                                   texture_idle=entities.button_textures['restart'+str(slot)],
                                                   texture_hover=entities.button_textures['restart'+str(slot)+'_hover'])
            self.slot_buttons.append(_slot_button)
            self.slot_buttons_restart.append(_slot_restart_button)

    def on_show(self):
        arcade.set_background_color(DEFAULT_BG)

    def on_update(self, delta_time: float):
        self.background.on_update()
        for button in self.slot_buttons:
            button.detect_mouse(self.window.cursor)
        for button in self.slot_buttons_restart:
            button.detect_mouse(self.window.cursor)

    def on_draw(self):
        arcade.start_render()
        self.background.on_draw()
        for button in self.slot_buttons:
            button.draw()
        for button in self.slot_buttons_restart:
            button.draw()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        for button in self.slot_buttons:
            if button.current_state == 'hover':
                game_view = GameView(background=self.background)
                self.window.show_view(game_view)
        for button in self.slot_buttons_restart:
            if button.current_state == 'hover':
                game_view = GameView()
                self.window.show_view(game_view)


class GameView(arcade.View):
    def __init__(self, background):
        super().__init__()
        self.background = background
        self.time_taken = 0

        # Developer mode
        self.processing_time = 0
        self.draw_time = 0
        self.frame_count = 0
        self.fps_start_timer = None
        self.fps = None

    def on_draw(self):
        # Start timing how long this takes
        draw_start_time = timeit.default_timer()
        if self.frame_count % 60 == 0:
            if self.fps_start_timer is not None:
                total_time = timeit.default_timer() - self.fps_start_timer
                self.fps = 60 / total_time
            self.fps_start_timer = timeit.default_timer()
        self.frame_count += 1
        arcade.start_render()
        self.background.on_draw()
        # Display timings
        output = f"Processing time: {self.processing_time:.3f}"
        arcade.draw_text(output, 20, self.window.height - 20, arcade.color.BLACK, 16)

        output = f"Drawing time: {self.draw_time:.3f}"
        arcade.draw_text(output, 20, self.window.height - 40, arcade.color.BLACK, 16)

        # Calculate time
        minutes = int(self.time_taken) // 60
        seconds = int(self.time_taken) % 60
        time_output = f"Time: {minutes:02d}:{seconds:02d}"

        # Output the timer text.
        arcade.draw_text(time_output, 20, self.window.height - 60, arcade.color.BLACK, 16)

        if self.fps is not None:
            output = f"FPS: {self.fps:.0f}"
            arcade.draw_text(output, 20, self.window.height - 80, arcade.color.BLACK, 16)

        # Below code has to be at the end of rendering
        self.draw_time = timeit.default_timer() - draw_start_time

    def on_update(self, delta_time):
        self.time_taken += delta_time
        self.background.on_update()

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = PauseView(paused_game_state=self, background=self.background)
            self.window.show_view(pause)


class PauseView(arcade.View):
    def __init__(self, paused_game_state, background):
        super().__init__()
        self.background = background
        self.paused_game_state = paused_game_state
        self.button_resume = entities.Button(x=self.window.width/2, y=self.window.height*3/6,
                                             width=200, height=50,
                                             texture_idle=entities.button_textures['resume'],
                                             texture_hover=entities.button_textures['resume_hover'])
        self.button_menu = entities.Button(x=self.window.width/2, y=self.window.height*2/6,
                                           width=200, height=50,
                                           texture_idle=entities.button_textures['menu'],
                                           texture_hover=entities.button_textures['menu_hover'])
        self.button_exit = entities.Button(x=self.window.width / 2, y=self.window.height*1/6,
                                           width=200, height=50,
                                           texture_idle=entities.button_textures['exit'],
                                           texture_hover=entities.button_textures['exit_hover'])

    def on_show(self):
        arcade.set_background_color(DEFAULT_BG)

    def on_update(self, delta_time: float):
        self.button_resume.detect_mouse(self.window.cursor)
        self.button_exit.detect_mouse(self.window.cursor)
        self.button_menu.detect_mouse(self.window.cursor)

    def on_draw(self):
        arcade.start_render()
        self.background.on_draw()
        self.button_resume.draw()
        self.button_exit.draw()
        self.button_menu.draw()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        if self.button_resume.current_state == 'hover':
            self.window.show_view(self.paused_game_state)
        if self.button_menu.current_state == 'hover':
            menu_view = MenuView()
            self.window.show_view(menu_view)
        if self.button_exit.current_state == 'hover':
            self.window.close()


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show(self):
        arcade.set_background_color(DEFAULT_FONT)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text("Game Over", 240, 400, DEFAULT_FONT, 54)
        arcade.draw_text("Click to restart", 310, 300, DEFAULT_FONT, 24)

        time_taken_formatted = f"{round(self.time_taken, 2)} seconds"
        arcade.draw_text(f"Time taken: {time_taken_formatted}",
                         self.window.width / 2,
                         200,
                         DEFAULT_FONT,
                         font_size=15,
                         anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


class Island(arcade.Window):
    def __init__(self):
        super().__init__(width=SET_WIDTH, height=SET_HEIGHT, title=SET_TITLE, fullscreen=SET_FULL)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Entities (lists of sprites)
        self.cursor = entities.Cursor()

        # Start viewport
        if SET_SKIP_INTRO == 1:
            self.start_view = MenuView()
        if SET_SKIP_INTRO == 0:
            self.start_view = IntroView()

        self.show_view(self.start_view)

        # Start Resources Managers
        self.music_mng = entities.MusicManager(SET_MUSIC_VOLUME)

    def setup(self):
        self.music_mng.setup()

    def on_update(self, delta_time: float):
        self.music_mng.on_update(delta_time)

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.cursor.update()

    def update_resolution(self):
        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)

    def on_mouse_motion(self, x, y, _dx, _dy):
        """
        Called whenever the mouse moves.
        """
        self.cursor.get_position(x, y)

    def on_show(self):
        arcade.set_background_color(DEFAULT_BG)

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.F:
            # User hits f. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Get the window coordinates. Match viewport to window coordinates
            # so there is a one-to-one mapping.
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)

        if key == arcade.key.S:
            # User hits s. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Instead of a one-to-one mapping, stretch/squash window to match the
            # constants. This does NOT respect aspect ratio. You'd need to
            # do a bit of math for that.
            self.set_viewport(0, SET_WIDTH, 0, SET_HEIGHT)

    def on_draw(self):
        # Draw all the sprites.
        self.cursor.draw()


def main():
    game = Island()
    # Initial all global managers:
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()