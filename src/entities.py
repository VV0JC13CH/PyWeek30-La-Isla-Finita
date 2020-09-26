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
game_title_orange = assets.game_title_orange
game_title_blue = assets.game_title_blue


def draw_title(color, window):
    if color == 'orange':
        arcade.draw_lrwh_rectangle_textured(window.width / 2 - game_title_orange.width / 2,
                                            window.height * 4 / 5,
                                            game_title_orange.width,
                                            game_title_orange.height,
                                            game_title_orange)
    else:
        arcade.draw_lrwh_rectangle_textured(window.width / 2 - game_title_blue.width / 2,
                                            window.height * 4 / 5,
                                            game_title_blue.width,
                                            game_title_blue.height,
                                            game_title_blue)


class Bird(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 0.5
        self.current_frame = 0
        self.texture = assets.white_bird[self.current_frame][0]
        self.speed_of_Frames = 0.25
        self.animated_textures = assets.white_bird
        self.facing_left = True

    def follow_hero(self, hero_sprite):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Random 1 in 100 chance that we'll change from our old direction and
        # then re-aim toward the player
        if random.randrange(100) == 0:
            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the bullet
            destination_x = hero_sprite.center_x
            destination_y = hero_sprite.center_y
            if hero_sprite.center_x < self.center_x:
                self.facing_left = True
            else:
                self.facing_left = False

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = destination_x - start_x
            y_diff = destination_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            self.change_x = math.cos(angle) * self.speed
            self.change_y = math.sin(angle) * self.speed

    def on_update(self):
        if self.facing_left:
            left = 0
        else:
            left = 1
        if self.current_frame <= 4:
            self.current_frame += self.speed_of_Frames
            self.texture = self.animated_textures[int(self.current_frame)][left]
        else:
            self.current_frame = 0
            self.texture = self.animated_textures[0][left]


def spawn_birds(wave, bird_list, screen_width, screen_height):
    if len(bird_list) <= wave:
        for i in range(wave+1):
            bird = Bird()
            # Position the bird
            bird.center_x = random.randrange(-screen_width, screen_width*2)
            bird.center_y = random.randrange(screen_height, screen_height*2)

            # Add the coin to the lists
            bird_list.append(bird)


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
        self.hero_bottom_build = assets.hero_bottom_build
        self.hero_top_idle = assets.hero_top_idle
        self.hero_top_run = assets.hero_top_run
        self.hero_top_throw = assets.hero_top_throw
        self.hero_top_build = assets.hero_top_build
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
        self.dying = False
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
        # Keys
        self.key_left_pressed = False
        self.key_right_pressed = False
        self.key_up_pressed = False
        self.key_down_pressed = False

        # Position/Motion:
        self.center_x = start_x
        self.center_y = start_y
        self.history_x = start_x
        self.history_y = start_y
        self.history_has_coco_left = False
        self.history_has_coco_right = False
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

    def _change_position(self, dx, dy):
        if not self.dying:
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

    def change_position(self, island_width, island_height):
        self.change_x = 0
        if not self.dying and not self.current_state == 'build':
            if island_width * 0.30 < self.sprite_list[0].center_x and self.key_left_pressed and not self.key_right_pressed:
                self.change_x = -self.movement_speed
                self.change_state('run')
            elif self.sprite_list[0].center_x < island_width * 0.84 and self.key_right_pressed and not self.key_left_pressed:
                self.change_x = self.movement_speed
                self.change_state('run')
            elif self.key_down_pressed and not self.key_up_pressed:
                self.change_state('build')
                self.history_x = self.sprite_list[0].center_x
                self.history_y = self.sprite_list[0].center_y
                self.history_has_coco_left = self.has_coco_left
                self.history_has_coco_right = self.has_coco_right
                self.has_coco_left = False
                self.has_coco_right = False
                for sprite in self:
                    sprite.change_x = 0
                    sprite.change_y = 0
                    sprite.center_x = island_width / 2
                    sprite.center_y = island_height * 0.7
            elif not self.key_left_pressed and not self.key_right_pressed:
                self.change_x = 0
                self.change_state(state='idle')
        elif self.key_up_pressed and not self.key_down_pressed and self.current_state == 'build':
            self.change_state('idle')
            self.has_coco_left = self.history_has_coco_left
            self.has_coco_right = self.history_has_coco_right
            for sprite in self:
                sprite.center_x = self.history_x
                sprite.center_y = self.history_y
            self.center_x = self.history_x
            self.center_y = self.history_y
            self.sprite_top_coco_left.center_x = self.history_x
            self.sprite_top_coco_left.center_y = self.history_y
            self.sprite_top_coco_right.center_x = self.history_x
            self.sprite_top_coco_right.center_y = self.history_y

        self._change_position(self.change_x, self.change_y)

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
        if self.current_state == 'die':
            self.dying = True
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
        elif self.current_state == 'build':
            self.sprite_top.texture = self.hero_top_build[0][left]
            self.sprite_bottom.texture = self.hero_bottom_build[0][left]
        elif self.current_state == 'run':
            if not self.dying:
                self.current_frame_run += 1
                if self.current_frame_run >= 4 * self.updates_per_frame_run:
                    self.current_frame_run = 0
                self.sprite_top.texture = self.hero_top_run[self.current_frame_run // self.updates_per_frame_run][left]
                self.sprite_bottom.texture = self.hero_bottom_run[self.current_frame_run // self.updates_per_frame_run][left]
        elif self.current_state == 'throw':
            if not self.dying:
                self.current_frame_throw += 1
                if self.current_frame_throw >= 3 * self.updates_per_frame_throw:
                    self.has_coco = False
                    self.current_frame_throw = 0
                self.sprite_top.texture = self.hero_top_throw[self.current_frame_throw // self.updates_per_frame_throw][left]
                self.sprite_bottom.texture = self.hero_bottom_throw[self.current_frame_throw // self.updates_per_frame_throw][left]
        elif self.current_state == 'idle':
            if not self.dying:
                self.current_frame_idle += 1
                if self.current_frame_idle >= 2 * self.updates_per_frame_idle:
                    self.current_frame_idle = 0
                self.sprite_top.texture = self.hero_top_idle[self.current_frame_idle // self.updates_per_frame_idle][left]
                self.sprite_bottom.texture = self.hero_bottom_idle[self.current_frame_idle // self.updates_per_frame_idle][left]

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
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.key_left_pressed = True
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.key_right_pressed = True
        elif key == arcade.key.W or key == arcade.key.UP:
            self.key_up_pressed = True
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.key_down_pressed = True

    def on_key_release(self, key):
        """
        Called when the user releases a key.
        """
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.key_left_pressed = False
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.key_right_pressed = False
        elif key == arcade.key.W or key == arcade.key.UP:
            self.key_up_pressed = False
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.key_down_pressed = False


class Coco(arcade.Sprite):
    def __init__(self, filename, pymunk_shape):
        super().__init__(filename, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2
        self.pymunk_shape = pymunk_shape


class FireCoco(arcade.Sprite):
    def __init__(self, filename, pymunk_shape):
        super().__init__(filename, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2
        self.pymunk_shape = pymunk_shape


class CocoSystem:
    def __init__(self, screen_width, screen_height, coco_x, coco_y):
        self.obstacle_list = arcade.SpriteList()
        self.coco_list: arcade.SpriteList[Coco] = arcade.SpriteList()
        self.fire_coco_list: arcade.SpriteList[FireCoco] = arcade.SpriteList()

        self.shoot_one_cocos = False
        self.shoot_two_cocos = False

        # -- Pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)

        self.isle_borders = []
        self.ticks_to_next_coco = 10

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
        self.isle_borders.append(shape)

        # Flat side of island
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, [screen_width/2-195, screen_height/2-95],
                               [screen_width/2+195, screen_height/2-95], 0.0)
        shape.friction = 10
        self.space.add(shape)
        self.isle_borders.append(shape)

        # Right side of island
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, [screen_width/2+190, screen_height/2-100], [screen_width/2+270, screen_height/2-190], 0.0)
        shape.friction = 10
        self.space.add(shape)
        self.isle_borders.append(shape)

    def on_draw(self):
        self.coco_list.draw()
        self.fire_coco_list.draw()

    def on_update(self, player_list):
        player = player_list
        # Getting cocos from tree:
        self.ticks_to_next_coco -= 1
        if self.ticks_to_next_coco <= 0:
            self.ticks_to_next_coco = 100
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
        for coco in self.fire_coco_list:
            if coco.pymunk_shape.body.position.y < self.screen_height/2-180:
                self.space.remove(coco.pymunk_shape, coco.pymunk_shape.body)
                coco.remove_from_sprite_lists()
            elif coco.pymunk_shape.body.position.x > self.screen_width+10:
                self.space.remove(coco.pymunk_shape, coco.pymunk_shape.body)
                coco.remove_from_sprite_lists()
            elif coco.pymunk_shape.body.position.x < -10:
                self.space.remove(coco.pymunk_shape, coco.pymunk_shape.body)
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

        if self.shoot_two_cocos:
            mass = 200
            radius = 15
            moment = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, moment)
            # Lets make a coco fall from tree:
            x = player.sprite_list[0].center_x
            y = player.sprite_list[0].center_y + 24
            body.position = x, y
            shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
            shape.friction = 0.3
            self.space.add(body, shape)
            power = 450
            body.apply_impulse_at_local_point(power*pymunk.Vec2d(player.throw_at_x-player.center_x,
                                                                 player.throw_at_y-player.center_y))
            sprite = Coco(filename=assets.coco_filename, pymunk_shape=shape)
            self.fire_coco_list.append(sprite)

            body = pymunk.Body(mass, moment)
            # Lets make a coco fall from tree:
            x = player.sprite_list[0].center_x
            y = player.sprite_list[0].center_y - 24
            body.position = x, y
            shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
            shape.friction = 0.3
            self.space.add(body, shape)
            power = 450
            body.apply_impulse_at_local_point(power*pymunk.Vec2d(player.throw_at_x-player.center_x,
                                                                 player.throw_at_y-player.center_y))
            sprite = Coco(filename=assets.coco_filename, pymunk_shape=shape)
            self.fire_coco_list.append(sprite)
            self.shoot_two_cocos = False

        elif self.shoot_one_cocos:
            mass = 200
            radius = 15
            moment = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, moment)
            # Lets make a coco fall from tree:
            x = player.sprite_list[0].center_x
            y = player.sprite_list[0].center_y+24
            body.position = x, y
            shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
            shape.friction = 0.3
            self.space.add(body, shape)
            power = 900
            body.apply_impulse_at_local_point(power*pymunk.Vec2d(player.throw_at_x-player.center_x,
                                                                 player.throw_at_y-player.center_y))
            sprite = Coco(filename=assets.coco_filename, pymunk_shape=shape)
            self.fire_coco_list.append(sprite)
            self.shoot_one_cocos = False

        # Move sprites to where physics objects are
        for coco in self.fire_coco_list:
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
    def __init__(self, res_width, res_height, width=800, height=600, x=400, y=300, game_hour=14):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.res_width = res_width
        self.res_height = res_height
        self.raft_completion = 0.0
        self.is_static = True
        self.sky = assets.dynamic_background_sky_by_hour
        self.sea = assets.sea
        self.frames_of_bg = assets.dynamic_background_frames
        self.frames_of_bg_leafs = assets.dynamic_background_leafs
        self.frames_of_bg_raft = assets.dynamic_background_raft
        self.raft = arcade.Sprite(center_x=width/2, center_y=height/2)
        self.raft.texture = self.frames_of_bg_raft[0]
        self.raft.center_x = self.x
        self.raft.center_y = self.y
        self.raft.width = self.width
        self.raft.height = self.height
        self.leafs = arcade.Sprite(center_x=width/2, center_y=height/2)
        self.leafs.texture = self.frames_of_bg_leafs[0]
        self.leafs_frame = 0
        self.leafs.center_x = self.x
        self.leafs.center_y = self.y
        self.leafs.width = self.width
        self.leafs.height = self.height
        self.frame = 0
        self.previous_delta = 0
        self.game_hour = game_hour
        self.victory = False
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

    def building_raft(self, current_state, speed):
        if self.raft_completion >= 1:
            self.victory = True
        elif current_state == 'build' and self.raft_completion < 1.0:
            self.raft_completion += speed

    def draw_raft(self):
        if self.raft_completion > 0.05:
            self.raft.draw()
        if self.raft_completion >= 1:
            self.raft.texture = self.frames_of_bg_raft[5]
        elif self.raft_completion >= 0.85:
            self.raft.texture = self.frames_of_bg_raft[4]
        elif self.raft_completion >= 0.70:
            self.raft.texture = self.frames_of_bg_raft[3]
        elif self.raft_completion >= 0.55:
            self.raft.texture = self.frames_of_bg_raft[2]
        elif self.raft_completion >= 0.40:
            self.raft.texture = self.frames_of_bg_raft[1]
        else:
            self.raft.texture = self.frames_of_bg_raft[0]

    def update_raft(self):
        if self.raft_completion >= 1:
            self.raft.change_x = -1
            self.raft.change_y = -1

    def on_draw(self):
        self.draw_sea_and_sky()
        self.draw()
        self.draw_leafs()
        self.draw_raft()

    def change_frame(self, frame):
        self.sprite_list.clear()
        self.append(self.frames_of_bg[frame])
        self.leafs.texture = self.frames_of_bg_leafs[frame]

    def on_update(self, delta_time: float = 1/60):
        self.update_raft()
        self.raft.update()
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
                 texture_idle=assets.button_idle, texture_hover=assets.button_hover, slot=0):
        super().__init__()
        self.slot = slot
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

    def play_song(self):
        """ Play the song. """
        # Stop what is currently playing.
        if self.music:
            self.music.stop()

        # Play the next song
        self.music = arcade.Sound(self.music_list[self.current_song], streaming=True)
        self.music.play(self.volume)
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


