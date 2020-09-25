import arcade
import assets
# time for sounds purposes:
import time
# math for hero angle
import numpy
# cocos
import pymunk
import random
import math

intro_team = assets.intro_authors


class Entity(arcade.SpriteList):
    def __init__(self):
        super().__init__()


class Hero(arcade.SpriteList):
    def __init__(self, start_x, start_y):
        super().__init__()
        # Sprites lists, last zero means = right, one means left, two coco, 3 left coco
        self.hero_bottom_idle = assets.hero_bottom_idle
        self.hero_bottom_run = assets.hero_bottom_run
        self.hero_bottom_throw = assets.hero_bottom_throw
        self.hero_top_idle = assets.hero_top_idle
        self.hero_top_run = assets.hero_top_run
        self.hero_top_throw = assets.hero_top_throw
        self.hero_die = assets.hero_die
        self.hero_all = assets.hero_all
        self.hero_top_textures = assets.hero_top
        self.hero_bottom_textures = assets.hero_bottom
        # Starting sprites
        # Idle[0], run[1] throw[2]
        self.sprite_top = arcade.Sprite()
        self.sprite_top_coco_left = arcade.Sprite()
        self.sprite_top_coco_right = arcade.Sprite()
        self.sprite_bottom = arcade.Sprite()
        self.sprite_top.texture = self.hero_top_idle[0][0]
        self.sprite_top_coco_left.texture = self.hero_top_idle[0][2]
        self.sprite_top_coco_right.texture = self.hero_top_idle[0][3]
        self.sprite_bottom.texture = self.hero_top_idle[0][0]
        self.append(self.sprite_top)
        self.append(self.sprite_bottom)
        # Actions
        self.died = False
        self.current_state = 'idle'
        self.has_coco = False
        self.has_coco_left = False
        self.has_coco_left_took = False
        self.has_coco_right = False
        self.has_coco_right_took = False
        self.sprite_list_coco_left = arcade.SpriteList()
        self.sprite_list_coco_right = arcade.SpriteList()
        self.sprite_list_coco_left.append(self.sprite_top_coco_left)
        self.sprite_list_coco_right.append(self.sprite_top_coco_right)
        self.is_throwing = False
        # Frames
        self.current_frame_run = 0
        self.current_frame_idle = 0
        self.current_frame_throw = 0
        self.current_frame_die = 0
        self.updates_per_frame_run = 8
        self.updates_per_frame_idle = 40
        self.updates_per_frame_throw = 16
        self.updates_per_frame_die = 14
        # Position/Motion:
        self.center_x = start_x
        self.center_y = start_y
        for sprite in self.sprite_list:
            sprite.center_x = self.center_x
            sprite.center_y = self.center_y
        for sprite in self.sprite_list_coco_left:
            sprite.center_x = self.center_x
            sprite.center_y = self.center_y
        for sprite in self.sprite_list_coco_right:
            sprite.center_x = self.center_x
            sprite.center_y = self.center_y
        self.change_x = 0
        self.change_y = 0
        self.movement_speed = 1.2
        self.facing_left = False

        # Mouse interaction
        self.throw_at_x = 0
        self.throw_at_y = 0
        self.angle = 0

    def change_position(self, dx, dy):
        if not self.died:
            for sprite in self:
                sprite.change_x = dx*self.movement_speed
                sprite.change_y = dy*self.movement_speed
            self.sprite_top_coco_left.change_x = dx * self.movement_speed
            self.sprite_top_coco_left.change_y = dy * self.movement_speed
            self.sprite_top_coco_right.change_x = dx * self.movement_speed
            self.sprite_top_coco_right.change_y = dy * self.movement_speed
        else:
            for sprite in self:
                sprite.change_x = 0
                sprite.change_y = 0
            self.sprite_top_coco_left.change_x = 0
            self.sprite_top_coco_left.change_y = 0
            self.sprite_top_coco_right.change_x = 0
            self.sprite_top_coco_right.change_y = 0

    def on_draw_cocos(self):
        if self.has_coco_left_took:
            self.has_coco_left = True
            self.has_coco_left_took = False
        elif self.has_coco_left:
            if self.current_state != 'throw':
                if self.current_state != 'die':
                    self.sprite_list_coco_left.draw()
            elif self.current_state == 'throw':
                self.has_coco_left = False
                self.has_coco_right = False
        if self.has_coco_right_took:
            self.has_coco_right = True
            self.has_coco_right_took = False
        elif self.has_coco_right:
            if self.current_state != 'throw':
                if self.current_state != 'die':
                    self.sprite_list_coco_right.draw()
            elif self.current_state == 'throw':
                self.has_coco_left = False
                self.has_coco_right = False

    # Giving parameters to next sprites
    def change_state(self, state):
        self.current_state = state

    def update_animation(self, delta_time: float = 1/60):
        if self.facing_left:
            left = 1
        else:
            left = 0
        if self.current_state == 'run':
            self.current_frame_run += 1
            if self.current_frame_run >= 4 * self.updates_per_frame_run:
                self.current_frame_run = 0
            self.sprite_top.texture = self.hero_top_run[self.current_frame_run // self.updates_per_frame_run][left]
            self.sprite_bottom.texture = self.hero_bottom_run[self.current_frame_run // self.updates_per_frame_run][left]
        elif self.current_state == 'throw':
            self.current_frame_throw += 1
            if self.current_frame_throw >= 3 * self.updates_per_frame_throw:
                self.has_coco = False
                self.current_frame_throw = 0
            self.sprite_top.texture = self.hero_top_throw[self.current_frame_throw // self.updates_per_frame_throw][left]
            self.sprite_bottom.texture = self.hero_bottom_throw[self.current_frame_throw // self.updates_per_frame_throw][left]
        elif self.current_state == 'idle':
            self.current_frame_idle += 1
            if self.current_frame_idle >= 2 * self.updates_per_frame_idle:
                self.current_frame_idle = 0
            self.sprite_top.texture = self.hero_top_idle[self.current_frame_idle // self.updates_per_frame_idle][left]
            self.sprite_bottom.texture = self.hero_bottom_idle[self.current_frame_idle // self.updates_per_frame_idle][left]
        elif self.current_state == 'die':
            if not self.died:
                self.current_frame_die += 1
                self.sprite_bottom.angle -= 1
                if self.current_frame_die >= 6 * self.updates_per_frame_die:
                    self.current_frame_die = 0
                    self.died = True
                self.sprite_top.remove_from_sprite_lists()
                self.sprite_bottom.texture = self.hero_die[self.current_frame_die // self.updates_per_frame_die]
            else:
                self.sprite_bottom.texture = self.hero_die[5]

    def flip_horizontaly(self, mouse_x):
        if mouse_x < self.center_x:
            self.facing_left = True
        else:
            self.facing_left = False

    def get_angle(self, mouse_x, mouse_y):
        self.throw_at_x = mouse_x
        self.throw_at_y = mouse_y
        p0 = [mouse_x, mouse_y]
        p1 = [self.center_x, self.center_y]
        p2 = [mouse_x, self.center_y]
        v0 = numpy.array(p0) - numpy.array(p1)
        v1 = numpy.array(p2) - numpy.array(p1)
        self.angle = numpy.degrees(numpy.math.atan2(numpy.linalg.det([v0, v1]), numpy.dot(v0, v1)))
        return self.angle

    def update_hero_angle(self, mouse_x, mouse_y):
        angle = self.get_angle(mouse_x, mouse_y)
        if int(abs(angle)) in range(0,10):
            self.sprite_top.angle = -float(angle)
            self.sprite_top_coco_left.angle = -float(angle)
            self.sprite_top_coco_right.angle = -float(angle)

    def on_key_press(self, key):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.W:
            self.change_y = self.movement_speed
        elif key == arcade.key.S:
            self.change_y = -self.movement_speed
        elif key == arcade.key.A:
            self.change_x = -self.movement_speed
        elif key == arcade.key.D:
            self.change_x = self.movement_speed
        self.change_state('run')
        self.change_position(self.change_x, self.change_y)

    def on_key_release(self, key):
        """
        Called when the user releases a key.
        """
        if key == arcade.key.W or key == arcade.key.S:
            self.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.change_x = 0
        self.change_state(state='idle')
        self.change_position(self.change_x, self.change_y)


class Coco(arcade.Sprite):
    def __init__(self, filename, pymunk_shape):
        super().__init__(filename, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2
        self.pymunk_shape = pymunk_shape


class CocoSystem:
    def __init__(self, screen_width, screen_height, coco_x, coco_y):
        self.obstacle_list = arcade.SpriteList()
        self.coco_list: arcade.SpriteList[Coco] = arcade.SpriteList()
        # -- Pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)
        self.static_lines = []
        self.ticks_to_next_ball = 10

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.coco_x = coco_x
        self.coco_y = coco_y

        # Left side of island
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, [screen_width/2-260, screen_height/2-180],
                               [screen_width/2-190, screen_height/2-100], 0.0)
        shape.friction = 10
        self.space.add(shape)
        self.static_lines.append(shape)

        # Flat side of island
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, [screen_width/2-195, screen_height/2-95],
                               [screen_width/2+195, screen_height/2-95], 0.0)
        shape.friction = 10
        self.space.add(shape)
        self.static_lines.append(shape)

        # Right side of island
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, [screen_width/2+190, screen_height/2-100], [screen_width/2+270, screen_height/2-190], 0.0)
        shape.friction = 10
        self.space.add(shape)
        self.static_lines.append(shape)

    def on_draw(self):
        self.coco_list.draw()

    def on_update(self, player_list):
        player = player_list
        self.ticks_to_next_ball -= 1
        if self.ticks_to_next_ball <= 0:
            self.ticks_to_next_ball = 100
            mass = 3.0
            radius = 15
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            # Lets make a coco fall from tree:
            x = random.randint(self.screen_width/2-100, self.screen_width/2)
            y = self.screen_height/2+100
            body.position = x, y
            shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
            shape.friction = 0.3
            self.space.add(body, shape)
            sprite = Coco(filename=assets.coco_filename, pymunk_shape=shape)
            self.coco_list.append(sprite)

        # Check for cocos that fall into water
        for coco in self.coco_list:
            if coco.pymunk_shape.body.position.y < self.screen_height/2-180:
                # Remove balls from physics space
                self.space.remove(coco.pymunk_shape, coco.pymunk_shape.body)
                # Remove balls from physics list
                coco.remove_from_sprite_lists()

        # Grab cocos by player:
        for coco in self.coco_list:
            if arcade.check_for_collision_with_list(coco, player):
                # Remove balls from physics space
                if not player.has_coco_left:
                    self.space.remove(coco.pymunk_shape, coco.pymunk_shape.body)
                # Remove balls from physics list
                    coco.remove_from_sprite_lists()
                    player.has_coco_left_took = True
                elif not player.has_coco_right:
                    self.space.remove(coco.pymunk_shape, coco.pymunk_shape.body)
                    # Remove balls from physics list
                    coco.remove_from_sprite_lists()
                    player.has_coco_right_took = True

        self.space.step(1 / 60.0)

        # Move sprites to where physics objects are
        for coco in self.coco_list:
            coco.center_x = coco.pymunk_shape.body.position.x
            coco.center_y = coco.pymunk_shape.body.position.y
            coco.angle = math.degrees(coco.pymunk_shape.body.angle)


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
        self.is_static = True
        self.sky = assets.dynamic_background_sky_by_hour
        self.sea = assets.sea
        self.frames_of_bg = assets.dynamic_background_frames
        self.frames_of_bg_leafs = assets.dynamic_background_leafs
        self.leafs = arcade.Sprite(center_x=width/2, center_y=height/2)
        self.leafs.texture = self.frames_of_bg_leafs[0]
        self.leafs_frame = 0
        self.leafs.center_x = self.x
        self.leafs.center_y = self.y
        self.leafs.width = self.width
        self.leafs.height = self.height
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
        arcade.draw_lrwh_rectangle_textured(0, self.res_height / 2, self.res_width, self.res_height,
                                            self.sky[int(self.game_hour)])
        arcade.draw_lrwh_rectangle_textured(0, 0, self.res_width, self.res_height/2, self.sea)

    def draw_leafs(self):
        self.leafs.draw()

    def on_draw(self):
        self.draw_sea_and_sky()
        self.draw()
        self.draw_leafs()

    def change_frame(self, frame):
        self.sprite_list.clear()
        self.append(self.frames_of_bg[frame])
        self.leafs.texture = self.frames_of_bg_leafs[frame]

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


class Button(Entity):
    # EVERYTHING IS FREAKING BUTTON IN THIS GAME
    def __init__(self, width=200, height=200, x=200, y=200,
                 texture_idle=assets.button_idle, texture_hover=assets.button_hover):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.textures = assets.button_textures
        self.idle = self.textures[texture_idle]
        self.hover = self.textures[texture_hover]

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


