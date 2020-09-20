import arcade
import os
import timeit

import entities
import settings
import sandbox

settings = settings.settings_load()

# INIT DATA
SET_TITLE = settings['GAME']['TITLE']
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
    def on_show(self):
        arcade.set_background_color(DEFAULT_BG)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Menu Screen",  self.window.width/2, self.window.height/2,
                         DEFAULT_FONT, font_size=50, anchor_x="center")
        arcade.draw_text("Once again!",  self.window.width/2, self.window.height/2-75,
                         DEFAULT_FONT, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(DEFAULT_BG)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Instructions Screen",  self.window.width/2, self.window.height/2,
                         DEFAULT_FONT, font_size=50, anchor_x="center")
        arcade.draw_text("I dare you!",  self.window.width/2, self.window.height/2-75,
                         DEFAULT_FONT, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.time_taken = 0

        # Entities (lists of sprites)
        self.cursor = entities.Cursor()

        # Developer mode
        self.processing_time = 0
        self.draw_time = 0
        self.frame_count = 0
        self.fps_start_timer = None
        self.fps = None

    def on_show(self):
        arcade.set_background_color(DEFAULT_BG)

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

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

        # Draw all the sprites.
        self.cursor.draw()

        # Below code has to be at the end of rendering
        self.draw_time = timeit.default_timer() - draw_start_time

    def on_update(self, delta_time):
        self.time_taken += delta_time

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.cursor.update()

    def on_mouse_motion(self, x, y, _dx, _dy):
        """
        Called whenever the mouse moves.
        """
        self.cursor.get_position(x, y)

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(DEFAULT_BG)

    def on_draw(self):
        arcade.start_render()

        # Draw player, for effect, on pause screen.
        # The previous View (GameView) was passed in
        # and saved in self.game_view.
        arcade.draw_text("PAUSED", self.window.width/2, self.window.height/2+50,
                         DEFAULT_FONT, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Press Esc. to return",
                         self.window.width/2,
                         self.window.height/2,
                         DEFAULT_FONT,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Press Enter to reset",
                         self.window.width / 2,
                         self.window.height / 2 - 30,
                         DEFAULT_FONT,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:  # reset game
            game = GameView()
            self.window.show_view(game)


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

        # Start viewport
        self.start_view = IntroView()
        self.show_view(self.start_view)

        # Start Resources Managers
        self.music_mng = entities.MusicManager(SET_MUSIC_VOLUME)

    def setup(self):
        self.music_mng.setup()

    def on_update(self, delta_time: float):
        self.music_mng.on_update(delta_time)

    def update_resolution(self):
        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)

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


def main():
    game = Island()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()