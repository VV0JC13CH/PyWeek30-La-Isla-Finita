import arcade
import assets
# time for sounds purposes:
import time

# Textures
intro_team = assets.intro_authors

# Music
music_list = [assets.track01,
              assets.track02]

button_textures = {"start": assets.button_start_idle,
                   "start_hover": assets.button_start_hover,
                   "exit": assets.button_exit_idle,
                   "exit_hover": assets.button_exit_hover,
                   "resume": assets.button_resume_idle,
                   "resume_hover": assets.button_resume_hover,
                   "restart": assets.button_restart_idle,
                   "restart_hover": assets.button_restart_hover,
                   "slot1": assets.button_slot1_idle,
                   "slot1_hover": assets.button_slot1_hover,
                   "restart1": assets.button_restart1_idle,
                   "restart1_hover": assets.button_restart1_hover,
                   "slot2": assets.button_slot2_idle,
                   "slot2_hover": assets.button_slot2_hover,
                   "restart2": assets.button_restart2_idle,
                   "restart2_hover": assets.button_restart2_hover,
                   "slot3": assets.button_slot3_idle,
                   "slot3_hover": assets.button_slot3_hover,
                   "restart3": assets.button_restart3_idle,
                   "restart3_hover": assets.button_restart3_hover,
                   "menu": assets.button_menu_idle,
                   "menu_hover": assets.button_menu_hover
}


class Entity(arcade.SpriteList):
    def __init__(self):
        super().__init__()


class Cursor(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.idle = assets.player_cursor_idle
        self.hover = assets.player_cursor_hover
        self.select = assets.player_cursor_select
        self.current_state = 'idle'
        self.append(self.idle)

    def get_position(self, dx, dy):
        for sprite in self:
            sprite.center_x = dx
            sprite.center_y = dy

    def change_state(self, state):
        if state == 'hover':
            self.sprite_list.clear()
            self.append(self.hover)
        elif state == 'select':
            self.sprite_list.clear()
            self.append(self.select)
        else:
            self.sprite_list.clear()
            self.append(self.idle)


class DynamicBackground(Entity):
    # DOES NOTHING MEANS EVERYTHING
    def __init__(self, res_width, res_height, width=800, height=600, x=400, y=300):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.res_width = res_width
        self.res_height = res_height
        self.sky = assets.dynamic_background_sky_by_hour
        self.sea = assets.sea
        self.frames_of_bg = assets.dynamic_background_frames
        self.frame = 0
        self.previous_delta = 0
        self.game_hour = 14
        self.current_frame = 0
        self.speed_of_Frames = 0.09
        self.append(self.frames_of_bg[0])
        for sprite in self.frames_of_bg:
            sprite.center_x = self.x
            sprite.center_y = self.y
            sprite.width = self.width
            sprite.height = self.height

    def draw_sea_and_sky(self):
        arcade.draw_lrwh_rectangle_textured(0, self.res_height/2, self.res_width, self.res_height,
                                            self.sky[int(self.game_hour)])
        arcade.draw_lrwh_rectangle_textured(0, 0, self.res_width, self.res_height/2, self.sea)

    def on_draw(self):
        self.draw_sea_and_sky()
        self.draw()

    def change_frame(self, frame):
        self.sprite_list.clear()
        self.append(self.frames_of_bg[frame])

    def on_update(self, delta_time: float = 1/60):
        if self.current_frame < 5.9:
            self.frame += self.speed_of_Frames
            self.current_frame += self.speed_of_Frames
            self.change_frame(int(self.frame))
        elif int(self.current_frame) in range(5,11):
            self.current_frame += self.speed_of_Frames
            self.frame -= self.speed_of_Frames
            self.change_frame(int(self.frame))
        else:
            self.current_frame = 0
            self.frame = 0

    def update_hour(self, minute_of_game):
        self.game_hour = int(minute_of_game) % 24
        print(minute_of_game, self.game_hour)


class Button(Entity):
    # EVERYTHING IS FREAKING BUTTON IN THIS GAME
    def __init__(self, width=200, height=200, x=200, y=200,
                 texture_idle=assets.button_idle, texture_hover=assets.button_hover, action='change_scene'):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.idle = texture_idle
        self.hover = texture_hover
        self.all_sprites = [self.idle, self.hover]
        self.current_state = 'idle'
        self.append(self.idle)
        for sprite in self.all_sprites:
            sprite.center_x = self.x
            sprite.center_y = self.y
            sprite.width = self.width
            sprite.height = self.height

    def change_state(self, state):
        self.current_state = state
        if state == 'hover':
            self.sprite_list.clear()
            self.append(self.hover)
        else:
            self.sprite_list.clear()
            self.append(self.idle)

    def detect_mouse(self, mouse_instance):
        if arcade.check_for_collision_with_list(self[0], mouse_instance):
            self.change_state(state='hover')
        else:
            self.change_state(state='idle')


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

        if position == 0.0:
            self.advance_song()
            self.play_song()


