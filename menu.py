import pyglet
from ui import Button
import consts

class MainMenu:
    def __init__(self, window_width, window_height, batch, start_game_func, options_func, exit_game_func):
        self.batch = batch
        self.group = pyglet.graphics.Group(order=10)

        self.start_game_func = start_game_func
        self.options_func = options_func
        self.exit_game_func = exit_game_func

        self.logo_sprite = None
        self.buttons = []

        self.build_ui(window_width, window_height)

    def build_ui(self, window_width, window_height):
        # 1. Czyszczenie
        if self.logo_sprite:
            self.logo_sprite.delete()
            self.logo_sprite = None

        for btn in self.buttons:
            btn.delete()
        self.buttons = []

        # 2. LOGO
        try:
            logo_img = pyglet.image.load('assets/logo.png')

            texture = logo_img.get_texture()
            pyglet.gl.glBindTexture(texture.target, texture.id)
            pyglet.gl.glTexParameteri(texture.target, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
            pyglet.gl.glTexParameteri(texture.target, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)

            texture.anchor_x = texture.width // 2
            texture.anchor_y = texture.height // 2

            logo_y = window_height * 0.65

            self.logo_sprite = pyglet.sprite.Sprite(
                img=texture,
                x=window_width // 2,
                y=logo_y,
                batch=self.batch,
                group=self.group
            )

            # Skalowanie
            target_width = window_width * 0.6
            scale = target_width / texture.width
            self.logo_sprite.scale = scale

        except Exception as e:
            print(f"Błąd ładowania logo: {e}")
            self.logo_sprite = pyglet.text.Label(
                "MISSING LOGO", font_name='Arial', font_size=40,
                x=window_width//2, y=window_height * 0.7, anchor_x='center',
                batch=self.batch, group=self.group
            )

        # 3. PRZYCISKI
        btn_width = 200; btn_height = 60; spacing = 20

        start_x = (window_width / 2) - ( (btn_width * 3 + spacing * 2) / 2 )
        y_pos = window_height * 0.15

        self.buttons.append(Button("GRAJ", start_x, y_pos, btn_width, btn_height,
            consts.BTN_COLOR_PLAY, self.start_game_func, self.batch, self.group))

        self.buttons.append(Button("OPCJE", start_x + btn_width + spacing, y_pos, btn_width, btn_height,
            consts.BTN_COLOR_OPT, self.options_func, self.batch, self.group))

        self.buttons.append(Button("WYJDŹ", start_x + (btn_width + spacing) * 2, y_pos, btn_width, btn_height,
            consts.BTN_COLOR_EXIT, self.exit_game_func, self.batch, self.group))

    def update_layout(self, width, height):
        self.build_ui(width, height)

    def on_mouse_motion(self, x, y, dx, dy):
        for btn in self.buttons:
            btn.check_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.buttons:
            btn.check_click(x, y)