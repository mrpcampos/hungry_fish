import pyglet
from src.fish import Fish


class MyWindow(pyglet.window.Window):
    def __init__(self, hungry_fish, icon_image, background_image, game, frame_rate=1 / 60.0, caption="Título da Janela", *args,
                 **kwargs):

        self.hungry_fish = hungry_fish
        self.game_batch = pyglet.graphics.Batch()
        self.background_batch_group = pyglet.graphics.OrderedGroup(0)
        self.brainless_batch_group = pyglet.graphics.OrderedGroup(1)
        self.player_batch_group = pyglet.graphics.OrderedGroup(2)
        self.labels_batch_group = pyglet.graphics.OrderedGroup(3)

        self.background = pyglet.sprite.Sprite(background_image,
                                               batch=self.game_batch,
                                               group=self.background_batch_group)
        super().__init__(width=self.background.width, height=self.background.height, caption=caption, *args, **kwargs)

        self.set_minimum_size(self.width, self.height)
        self.set_icon(icon_image)

        self.game = game

        self.player = None

        self.frame_rate = frame_rate
        self.fps_display = pyglet.window.FPSDisplay(self)
        self.fps_display.label.color = (255, 255, 255, 255)

    def new_sprite(self, image, x=0, y=0, scale=None):
        if scale is not None:
            return Fish(image, x, y, batch=self.game_batch, batch_group=self.brainless_batch_group, scale=scale)
        else:
            return Fish(image, x, y, batch=self.game_batch, batch_group=self.brainless_batch_group)

    def new_player_sprite(self, image, x, y, scale=None):
        return Fish(image, x, y, batch=self.game_batch, batch_group=self.player_batch_group, scale=scale)

    def set_player(self, player):
        self.player = player

    def on_draw(self):
        self.clear()
        self.game_batch.draw()
        self.fps_display.draw()

    def on_deactivate(self):
        self.game.pause_game()

    def on_activate(self):
        self.game.resume_game()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            self.player.go_up()
        elif symbol == pyglet.window.key.RIGHT:
            self.player.go_right()
        elif symbol == pyglet.window.key.DOWN:
            self.player.go_down()
        elif symbol == pyglet.window.key.LEFT:
            self.player.go_left()
        elif symbol == pyglet.window.key.S:
            self.player.stop()
        elif symbol == pyglet.window.key.C:
            self.player.re_center()
        elif symbol == pyglet.window.key.ENTER:
            self.hungry_fish.respaw()

    def on_text_motion(self, motion):
        if motion == pyglet.window.key.MOTION_UP:
            self.player.go_up()
        elif motion == pyglet.window.key.MOTION_RIGHT:
            self.player.go_right()
        elif motion == pyglet.window.key.MOTION_DOWN:
            self.player.go_down()
        elif motion == pyglet.window.key.MOTION_LEFT:
            self.player.go_left()

    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            self.player.stop_going_up()
        elif symbol == pyglet.window.key.RIGHT:
            self.player.stop_going_right()
        elif symbol == pyglet.window.key.DOWN:
            self.player.stop_going_down()
        elif symbol == pyglet.window.key.LEFT:
            self.player.stop_going_left()

    def on_mouse_press(self, x, y, button, modifiers, **kwargs):
        '''Começa o jogo quando pressionar com o mouse
        '''
        self.hungry_fish.start_game()
