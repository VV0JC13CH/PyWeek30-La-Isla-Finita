import arcade
import assets
# time for sounds purposes:
import time
# Damns...those UIs:
from arcade.gui import UIFlatButton, UIGhostFlatButton, UIManager
from arcade.gui.ui_style import UIStyle

# Textures
intro_team = assets.intro_authors

# Music
music_list = [assets.track01,
              assets.track02]


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

    def get_position(self, dx, dy):
        for sprite in self:
            sprite.center_x = dx
            sprite.center_y = dy


class MusicManager:
    def __init__(self, init_volume=0.8):
        self.volume = float(init_volume)
        self.music_list = []
        self.current_song = 0
        self.music = None

    def advance_song(self):
        """ Advance our pointer to the next song. This does NOT start the song. """
        self.current_song += 1
        if self.current_song >= len(self.music_list):
            self.current_song = 0
        print(f"Advancing song to {self.current_song}.")

    def play_song(self):
        """ Play the song. """
        # Stop what is currently playing.
        if self.music:
            self.music.stop()

        # Play the next song
        print(f"Playing {self.music_list[self.current_song]}")
        self.music = arcade.Sound(self.music_list[self.current_song], streaming=True)
        self.music.play(self.volume)
        # This is a quick delay. If we don't do this, our elapsed time is 0.0
        # and on_update will think the music is over and advance us to the next
        # song before starting this one.
        time.sleep(0.03)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # List of music
        self.music_list = assets.songs_list
        # Array index of what to play
        self.current_song = 0
        # Play the song
        self.play_song()

    def on_draw(self, screen_height):
        """ Render the screen. """
        position = self.music.get_stream_position()
        length = self.music.get_length()
        text_position = f"{int(position) // 60}:{int(position) % 60:02} of {int(length) // 60}:{int(length) % 60:02}"
        text_song = f"Currently playing: {self.music_list[self.current_song]}"

    def on_update(self, dt):

        position = self.music.get_stream_position()

        # The position pointer is reset to 0 right after we finish the song.
        # This makes it very difficult to figure out if we just started playing
        # or if we are doing playing.
        if position == 0.0:
            self.advance_song()
            self.play_song()


class UiManager:
    def __init__(self, viewport_width, viewport_height):
        self.ui_manager = UIManager()
        self.window_width = viewport_width
        self.window_height = viewport_height

    def setup_main(self):
        """ Setup the view """
        self.ui_manager.purge_ui_elements()
        flat = UIFlatButton('Hello world', center_x=200, center_y=self.window_height // 2, width=200, height=40)
        flat.set_style_attrs(
            font_color=arcade.color.WHITE,
            font_color_hover=arcade.color.WHITE,
            font_color_press=arcade.color.WHITE,
            bg_color=(51, 139, 57),
            bg_color_hover=(51, 139, 57),
            bg_color_press=(28, 71, 32),
            border_color=(51, 139, 57),
            border_color_hover=arcade.color.WHITE,
            border_color_press=arcade.color.WHITE
        )
        self.ui_manager.add_ui_element(flat)

        # creates a new class, which will match the id
        UIStyle.default_style().set_class_attrs(
            'right_button',
            font_color=arcade.color.WHITE,
            font_color_hover=arcade.color.WHITE,
            font_color_press=arcade.color.WHITE,
            bg_color=(135, 21, 25),
            bg_color_hover=(135, 21, 25),
            bg_color_press=(122, 21, 24),
            border_color=(135, 21, 25),
            border_color_hover=arcade.color.WHITE,
            border_color_press=arcade.color.WHITE
        )
        self.ui_manager.add_ui_element(UIGhostFlatButton(
            'Hello world',
            center_x=600,
            center_y=self.window_height // 2,
            width=200,
            height=40,
            id='right_button'
        ))

    def on_show_view_main(self):
        self.setup_main()
