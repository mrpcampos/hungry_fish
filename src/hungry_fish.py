from src.window import MyWindow
from pyglet import resource
from src import Collision_calculator
import random
import pyglet


class HungryFish:
    def __init__(self):
        resource.path = ['resources']

        self.window = MyWindow(self, background_image=resource.animation('crab.gif'),
                               icon_image=self.preload_image('icon_photo.jpg'),
                               game=self, resizable=False)

        self.player_fish_image = self.preload_image('orange-skin_fish.png')
        player_posx = self.window.width // 2
        player_posy = self.window.height // 2
        self.player = self.window.new_player_sprite(self.player_fish_image, x=player_posx, y=player_posy, scale=0.7)

        self.fishes_images = []
        self.yellow_fish_image = self.preload_image('yellow_fish.png')
        self.blue_fish_image = self.preload_image('blue_fish.png')
        self.pink_fish_image = self.preload_image('pink_fish.png')
        self.fishes_images.append(self.yellow_fish_image)
        self.fishes_images.append(self.blue_fish_image)
        self.fishes_images.append(self.pink_fish_image)

        Collision_calculator.cache_image(self.player_fish_image)
        [Collision_calculator.cache_image(fish_image) for fish_image in self.fishes_images]

        self.world_seed = None
        self.brainless_fishes = []

        self.music = resource.media('secunda.wav', streaming=False)

        pyglet.app.run()

    @staticmethod
    def preload_image(path=None):
        if path is not None:
            return resource.image(path)
        else:
            return None

    def start_game(self):
        self.window.set_player(self.player)

        if self.world_seed is None:
            random.seed()
        else:
            random.seed(self.world_seed)

        self.music.play()

        self.start_population()

    def respaw(self):
        self.exclude_player()
        self.player = self.window.new_player_sprite(self.player_fish_image, x=self.window.width // 2, y=self.window.height // 2, scale=0.7)
        self.window.set_player(self.player)

    def start_population(self):
        order = random.randint(0, 2)

        yellow_posx_inicial = self.window.width + random.randint(0,
                                                                 self.window.width // 4) + self.yellow_fish_image.width
        yellow_posy_inicial = ((order * (self.window.height // 3)) + random.randint(0, self.window.height // 3))
        yellow_fish = self.window.new_sprite(self.yellow_fish_image, x=yellow_posx_inicial, y=yellow_posy_inicial)
        yellow_fish.vel_max_x = random.randint(80, 175) / 100
        yellow_fish.going_left = True

        blue_posx_inicial = self.window.width + random.randint(0, self.window.width // 3) + (
                self.blue_fish_image.width // 2)
        blue_posy_inicial = ((order + 1) * (self.window.height // 3) +
                             random.randint(0, self.window.height // 3)) % self.window.height
        blue_fish = self.window.new_sprite(self.blue_fish_image, x=blue_posx_inicial, y=blue_posy_inicial)
        blue_fish.vel_max_x = random.randint(80, 175) / 100
        blue_fish.going_left = True

        pink_posx_inicial = self.window.width + random.randint(0, self.window.width // 3) + (
                self.pink_fish_image.width // 2)
        pink_posy_inicial = ((order + 2) * (self.window.height // 3) +
                             random.randint(0, self.window.height // 3)) % self.window.height
        pink_fish = self.window.new_sprite(self.pink_fish_image, x=pink_posx_inicial, y=pink_posy_inicial)
        pink_fish.vel_max_x = random.randint(80, 175) / 100
        pink_fish.going_left = True

        self.brainless_fishes.extend([yellow_fish, blue_fish, pink_fish])
        for i in range(0, 3):
            self.brainless_fishes.append(self.add_random_generated_fish())

    def control_population(self, dt):
        for fish in self.brainless_fishes:
            if fish.is_dead() or (fish.going_right and fish.x > self.window.width + fish.width) or (
                    (not fish.going_right) and fish.x < -fish.width):
                self.exclude_brainless_fish(fish)
                self.add_random_generated_fish()

    def generate_fish(self, pos_y, going_right, vel, fish_image, x_variation=0, scale=1):
        pos_x = (
            - fish_image.width // 2 - x_variation if going_right else self.window.width + fish_image.width + x_variation)
        fish = self.window.new_sprite(fish_image, x=pos_x, y=pos_y, scale=scale)
        fish.vel_max_x = vel
        if going_right:
            fish.going_right = going_right
            # fish.multiply_scale_x(-1)
        else:
            fish.going_left = True
        return fish

    def add_random_generated_fish(self):
        going_right = random.choice((True, False))
        fish_image = random.choice(self.fishes_images)
        fish = self.generate_fish(random.randint(0, self.window.height), going_right,
                                  random.randint(80, 175) / 100, fish_image,
                                  random.randint(0, self.window.width // 3),
                                  scale=round(random.uniform(0.5, 1.6), ndigits=2))
        self.brainless_fishes.append(fish)
        return fish

    def pause_game(self):
        pyglet.clock.unschedule(self.update)
        self.player.stop()

    def resume_game(self):
        pyglet.clock.schedule_interval(self.update, self.window.frame_rate)

    def update(self, dt):
        self.player.update(dt)
        [fish.update(dt) for fish in self.brainless_fishes]
        self.control_population(dt)
        self.check_and_handle_collisions()
        self.recicle_dead_bodies()

    def check_and_handle_collisions(self):
        for fish in self.brainless_fishes:
            if Collision_calculator.is_colliding(self.player, fish):
                self.player.collide(fish)
                fish.collide(self.player)

    def recicle_dead_bodies(self):
        for fish in self.brainless_fishes:
            if fish.is_dead():
                self.exclude_brainless_fish(fish)
                self.add_random_generated_fish()

    def exclude_brainless_fish(self, fish):
        self.brainless_fishes.remove(fish)
        fish.batch = None

    def exclude_player(self):
        self.player.batch = None
        self.player = None

if __name__ == "__main__":
    HungryFish()
