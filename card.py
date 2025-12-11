import pyglet
import resources  # Importujemy nasze zasoby

class Card:
    def __init__(self, name, x, y, batch, group):
        self.name = name
        self.is_selected = False

        if name == 'BACK':
            img = resources.card_back_image
        else:
            img = resources.deck_images[name]

        self.sprite = pyglet.sprite.Sprite(img=img, x=x, y=y, batch=batch, group=group)
        self.target_y = y

    def update_scale(self, window_width, window_height):
        desired_height = window_height * 0.25
        # 54 to wysokość Twojej grafiki karty
        scale_float = desired_height / 54
        scale_int = int(scale_float)
        if scale_int < 1: scale_int = 1
        self.sprite.scale = scale_int

    def set_position(self, x, y):
        self.sprite.x = int(x)
        self.target_y = y

    def update(self, dt):
        # Fizyka ruchu (Lerp)
        diff = self.target_y - self.sprite.y
        self.sprite.y += diff * dt * 15

    def check_click(self, x, y):
        w = self.sprite.width
        h = self.sprite.height
        in_x = (self.sprite.x - w/2) < x < (self.sprite.x + w/2)
        in_y = (self.sprite.y - h/2) < y < (self.sprite.y + h/2)
        return in_x and in_y