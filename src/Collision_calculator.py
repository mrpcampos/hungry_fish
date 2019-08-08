from pyglet.gl import *
from ctypes import *


class Retangle:
    '''Cria estruturas retângulares para calculo de colisões'''

    def __init__(self, x1, y1, x2, y2):
        '''Cria um retângulo com o ponto minimo e máximo

        O canto inferior esquerdo é dado pelo x1 e y1
        o canto superior direito é dado por x2 e y2'''
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

    def retangle_from_intersected_area(self, r):
        '''Gera um retângulo a partir da área de intercecção do retângulo recebido e do da classe

        ATENÇÃO só chamar esse método se souber que os retângulos se cruzam!
        Esse método não verifica isso!'''
        n = Retangle(max(self.x1, r.x1), max(self.y1, r.y1), min(self.x2, r.x2), min(self.y2, r.y2))
        return n

    def check_if_intersects(self, r):
        '''Verifica se os retângulos se encostam'''
        if self.x2 < r.x1 or self.y2 < r.y1 or self.x1 > r.x2 or self.y1 > r.y2:
            return False
        return True

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    def __repr__(self):
        return '[%d %d %d %d]' % (self.x1, self.y1, self.x2, self.y2)

    @staticmethod
    def from_sprite(sprite):
        '''Cria um retângulo a partir de um sprite'''
        i = (sprite._texture if not sprite._animation else sprite._animation.frames[sprite._frame_index].image)
        x = int(sprite.x - i.anchor_x)
        y = int(sprite.y - i.anchor_y)
        if sprite.scale_x < 0:
            if sprite.scale_y < 0:
                return Retangle(x - sprite.width, y - sprite.height, x, y)
            else:
                return Retangle(x - sprite.width, y, x, y + sprite.height)
        else:
            if sprite.scale_y < 0:
                return Retangle(x, y - sprite.height, x + sprite.width, y)
            else:
                return Retangle(x, y, x + sprite.width, y + sprite.height)


class Collision_calculator:
    image_data_cache = {}

    def cache_image(self, image):
        if image not in self.image_data_cache:
            image_data = image.get_image_data().get_data('A', image.width)
            self.image_data_cache[image] = image_data

    def is_colliding(self, game_object1, game_object2):
        '''Informa se dois sprites se encostam.
        Dois sprites estão se encostando se dois pixeis não vazios ocuparem o mesmo local'''

        # Broad fase: Ver se os retangulos dos sprites se encontram
        retangulo1, retangulo2 = Retangle.from_sprite(game_object1), Retangle.from_sprite(game_object2)
        if retangulo1.check_if_intersects(retangulo2):
            # Gera um retângulo para a área sobreposta pelos dois
            intersection_retangle = retangulo1.retangle_from_intersected_area(retangulo2)

            # Ve em que ponto das imagens esse novo retangulo começa
            offx1, offy1, o1x, o1y = self.get_intersection_offsets(intersection_retangle, retangulo1, game_object1)
            offx2, offy2, o2x, o2y = self.get_intersection_offsets(intersection_retangle, retangulo2, game_object2)

            # Pega as informações dos pixels da imagem
            d1, d2 = self.get_image(game_object1), self.get_image(game_object2)

            # converte em um tipo mais facil de trabalhar (inicialmente vem como String)
            p1 = cast(d1[0], POINTER(c_ubyte))
            p2 = cast(d2[0], POINTER(c_ubyte))

            # Pra cada 'pixel' do retângulo de sobreposição vemos se há colição
            for i in range(0, intersection_retangle.width):
                for j in range(0, intersection_retangle.height):
                    c1 = p1[(offx1 + i * o1x) + (offy1 + j * o1y) * d1[1]]
                    c2 = p2[(offx2 + i * o2x) + (offy2 + j * o2y) * d2[1]]

                    # Se os dois pixels forem não transparentes temos uma colisão
                    if c1 > 0 and c2 > 0:
                        return True

        # Caso chegue até aqui não há colisões
        return False

    def get_intersection_offsets(self, intersection_retangle, image_retangle, game_object):
        # Ve em que ponto da imagem retangulo de intersecção começa
        if game_object.scale_x < 0:
            offx = int(image_retangle.width - (intersection_retangle.x1 - image_retangle.x1) - 1)
            # object_2_x_orientation
            ox = -1
        else:
            offx = int(intersection_retangle.x1 - image_retangle.x1)
            # object_2_x_orientation
            ox = 1

        if game_object.scale_y < 0:
            offy = int(image_retangle.height - (intersection_retangle.y1 - image_retangle.y1) - 1)
            # object_2_y_orientation
            oy = -1
        else:
            offy = int(intersection_retangle.y1 - image_retangle.y1)
            # object_2_y_orientation
            oy = 1
        return offx, offy, ox, oy

    def get_image(self, sprite):
        """Returns the image data for the sprite"""

        # if this is an animated sprite, grab the current frame
        if sprite._animation:
            image = sprite._animation.frames[sprite._frame_index].image
        # otherwise just grab the image
        else:
            image = sprite._texture

        # if the image is already cached, use the cached copy
        if image in self.image_data_cache:
            image_data = self.image_data_cache[image]
        # otherwise grab the image's alpha channel, and cache it
        else:
            image_data = image.get_image_data().get_data('A', image.width)
            self.image_data_cache[image] = image_data

        # return a tuple containing the image data, along with the width and height
        return image_data, image.width, image.height
