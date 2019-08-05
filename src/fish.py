import pyglet


class Fish(pyglet.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, batch, batch_group, vel_max_x=1.25, vel_max_y=1.0, scale=None):
        super().__init__(image, batch=batch, group=batch_group)

        if scale is not None:
            self.scale = scale

        self.pos_x_inicial = pos_x
        self.pos_y_inicial = pos_y
        self.x = pos_x
        self.y = pos_y
        self._vel_max_x = vel_max_x * self.width
        self._vel_max_y = vel_max_y * self.height
        self.vel_atual_x = 0.0
        self.vel_atual_y = 0.0

        self.dead = False

        self.going_up = False
        self._going_right = False
        self.going_down = False
        self._going_left = False

    def stop(self):
        self.going_up = False
        self.going_right = False
        self.going_down = False
        self.going_left = False

    def re_center(self):
        self.position = (self.pos_x_inicial, self.pos_y_inicial)

    @property
    def vel_max_y(self):
        return self._vel_max_y

    @vel_max_y.setter
    def vel_max_y(self, vel):
        self._vel_max_y = vel * self.height

    @property
    def vel_max_x(self):
        return self._vel_max_x

    @vel_max_x.setter
    def vel_max_x(self, vel):
        self._vel_max_x = vel * self.width

    @property
    def going_right(self):
        return self._going_right

    @going_right.setter
    def going_right(self, going_right):
        if going_right != self._going_right:
            if going_right:
                self.x += self.width
            else:
                self.x -= self.width
            self.scale_x *= -1
        self._going_right = going_right

    @property
    def going_left(self):
        return self._going_left

    @going_left.setter
    def going_left(self, going_left):
        self._going_left = going_left

    def update(self, dt):
        if self.going_right:
            self.x += (self._vel_max_x * dt)
        elif self.going_left:
            self.x += (-self._vel_max_x * dt)
        self.y += (self._vel_max_y * dt) if self.going_up else (-self._vel_max_y * dt) if self.going_down else 0

    def collide(self, other_fish):
        if not other_fish.is_dead() and not self.is_dead():
            if other_fish.scale <= self.scale:
                self.multiply_scale(1.05)
            else:
                self.color = (255, 0, 0)
                self.kill()

    def multiply_scale(self, scale):
        """
        Multiplica a escala atual do peixe pela recebida, recomendasse o uso de frações invertidas
        para aumentar ou diminuir.

        Ex: 1,25 para aumentar e 0,8 para diminuir (5/4 e 4/5)
        ou  1,11 para aumentar e 0,9 para diminuir (10/9 e 9/10)"""
        self.scale *= scale

    def kill(self):
        self.stop()
        self.dead = True

    def is_dead(self):
        return self.dead

    def go_up(self):
        if not self.dead:
            self.going_up = True

    def go_down(self):
        if not self.dead:
            self.going_down = True

    def go_left(self):
        if not self.dead:
            self.going_left = True

    def go_right(self):
        if not self.dead:
            self.going_right = True

    def stop_going_up(self):
        if not self.dead:
            self.going_up = False

    def stop_going_down(self):
        if not self.dead:
            self.going_down = False

    def stop_going_left(self):
        if not self.dead:
            self.going_left = False

    def stop_going_right(self):
        if not self.dead:
            self.going_right = False
