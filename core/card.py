import pyglet
import utils.resources as resources
import config.consts as consts

class Card:
    def __init__(self, suit, value_str, x, y, batch, group):
        # suit: 'pik', 'kier', 'trefl', 'karo'
        # value_str: '2', '10', 'as', 'krol'

        self.suit = suit
        self.value_str = value_str
        self.name = f"{suit}_{value_str}"
        self.is_selected = False
        self.to_delete = False # Flaga do usuwania animowanego

        # Obliczamy wartość logiczną (dla sortowania i sprawdzania strita)
        # 2..9 = int, 10=10, J=11, Q=12, K=13, A=14
        if value_str.isdigit():
            self.rank_val = int(value_str)
        else:
            mapping = {'walet': 11, 'dama': 12, 'krol': 13, 'as': 14}
            self.rank_val = mapping.get(value_str, 0)

        # Wartość punktowa (Chips)
        self.chips_val = consts.CARD_VALUES.get(value_str, 0)

        # Grafika
        img = resources.deck_images.get(self.name, resources.card_back_image)
        self.sprite = pyglet.sprite.Sprite(img=img, x=x, y=y, batch=batch, group=group)

        self.target_y = y
        self.target_x = x

    def update_scale(self, window_width, window_height):
        desired_height = window_height * 0.25
        scale_float = desired_height / 54
        scale_int = int(scale_float)
        if scale_int < 1: scale_int = 1
        self.sprite.scale = scale_int

    def set_position(self, x, y):
        # Ustawienie natychmiastowe (np. przy rozdaniu)
        self.sprite.x = int(x)
        self.sprite.y = int(y)
        self.target_x = x
        self.target_y = y

    def set_target(self, x, y):
        # Ustawienie celu animacji
        self.target_x = x
        self.target_y = y

    def update(self, dt):
        # Interpolacja (Lerp) zarówno X jak i Y
        speed = 15 * consts.settings.game_speed

        diff_x = self.target_x - self.sprite.x
        self.sprite.x += diff_x * dt * speed

        diff_y = self.target_y - self.sprite.y
        self.sprite.y += diff_y * dt * speed

    def check_click(self, x, y):
        w = self.sprite.width
        h = self.sprite.height
        in_x = (self.sprite.x - w/2) < x < (self.sprite.x + w/2)
        in_y = (self.sprite.y - h/2) < y < (self.sprite.y + h/2)
        return in_x and in_y

    def delete(self):
        self.sprite.delete()