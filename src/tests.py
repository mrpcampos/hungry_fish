from src.window import MyWindow
from src.hungry_fish import HungryFish
from src import Collision_calculator
import pyglet
from pyglet import resource
from ctypes import *


class tests:
    def __init__(self):
        resource.path = ['resources']

        self.window = MyWindow(self, background_image=resource.animation('oyster.gif'),
                               frame_rate=1 / 60,
                               icon_image=HungryFish.preload_image('icon_photo.jpg'),
                               game=self, resizable=False)

        player_fish_image = HungryFish.preload_image('orange-skin_fish.png')
        # player_fish_image = HungryFish.preload_image('aaa.png')
        player_posx = self.window.width // 2
        player_posy = self.window.height // 2
        self.player = self.window.new_player_sprite(player_fish_image, x=player_posx, y=player_posy, scale=1)
        self.window.set_player(self.player)
        # self.player.vel_max_x = 10
        # self.player.vel_max_y = 10

        self.fishes_images = []
        self.yellow_fish_image = HungryFish.preload_image('yellow_fish.png')
        self.blue_fish_image = HungryFish.preload_image('blue_fish.png')
        self.pink_fish_image = HungryFish.preload_image('pink_fish.png')
        self.fishes_images.append(self.yellow_fish_image)
        self.fishes_images.append(self.blue_fish_image)
        self.fishes_images.append(self.pink_fish_image)

        self.collision_calculator = Collision_calculator.Collision_calculator()

        self.collision_calculator.cache_image(player_fish_image)
        [self.collision_calculator.cache_image(fish_image) for fish_image in self.fishes_images]

        self.brainless_fishes = []
        self.start_population()

        pyglet.app.run()

    def start_population(self):
        fish1 = self.generate_fish(pos_y=self.window.height // 2 + 80, pos_x=self.window.width // 2 + 100,
                                   going_right=False, vel=0, scale=1,
                                   fish_image=self.blue_fish_image)

        fish2 = self.generate_fish(pos_y=self.window.height // 2 - 80, pos_x=self.window.width // 2 + 100,
                                   going_right=False, vel=0, scale=1,
                                   fish_image=self.blue_fish_image)
        fish2.scale_y *= -1

        fish3 = self.generate_fish(pos_y=self.window.height // 2 - 80, pos_x=self.window.width // 2 - 100,
                                   going_right=False, vel=0, scale=1,
                                   fish_image=self.yellow_fish_image)
        fish3.scale_y *= -1
        fish3.scale_x *= -1

        fish4 = self.generate_fish(pos_y=self.window.height // 2 + 80, pos_x=self.window.width // 2 - 100,
                                   going_right=False, vel=0, scale=1,
                                   fish_image=self.pink_fish_image)
        fish4.scale_x *= -1

        self.brainless_fishes.append(fish1)
        self.brainless_fishes.append(fish2)
        self.brainless_fishes.append(fish3)
        self.brainless_fishes.append(fish4)

    def generate_fish(self, pos_y, pos_x, going_right, vel, fish_image, scale=1.0):
        fish = self.window.new_sprite(fish_image, x=pos_x, y=pos_y, scale=scale)
        fish.vel_max_x = vel
        if going_right:
            fish.going_right = going_right
        else:
            fish.going_left = True
        return fish

    def pause_game(self):
        pyglet.clock.unschedule(self.update)
        self.player.stop()

    def resume_game(self):
        pyglet.clock.schedule_interval(self.update, self.window.frame_rate)

    def update(self, dt):
        self.player.update(dt)
        for fish in self.brainless_fishes:
            fish.update(dt, )
            fish.color = (255, 255, 255)
        self.check_and_handle_collisions()
        self.remove_dead_bodies()

    def check_and_handle_collisions(self):
        for fish in self.brainless_fishes:
            if self.collision_calculator.is_colliding(self.player, fish):
                fish.color = (255, 0, 0)

    def remove_dead_bodies(self):
        for fish in self.brainless_fishes:
            if fish.is_dead():
                self.exclude_fish(fish)

    def exclude_fish(self, fish):
        self.brainless_fishes.remove(fish)
        fish.batch = None


if __name__ == "__main__":
    tests()
