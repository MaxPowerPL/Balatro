import pyglet
from ui.ui import Button
import config.consts as consts

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
        # 1. Obliczamy skalę UI względem bazowej wysokości 720p
        # Jeśli okno ma 1080p, scale będzie 1.0
        ui_scale = window_height / 1080.0

        # 2. Czyszczenie
        if self.logo_sprite:
            self.logo_sprite.delete()
            self.logo_sprite = None

        for btn in self.buttons:
            btn.delete()
        self.buttons = []

        # 3. LOGO
        try:
            logo_img = pyglet.image.load('assets/images/logo.png')

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

            # Skalowanie Logo
            target_width = window_width * 0.6
            scale = target_width / logo_img.width
            self.logo_sprite.scale = scale

        except Exception as e:
            print(f"Błąd ładowania logo: {e}")
            self.logo_sprite = pyglet.text.Label(
                "MISSING LOGO", font_name='Arial', font_size=int(40 * ui_scale),
                x=window_width//2, y=window_height * 0.7, anchor_x='center',
                batch=self.batch, group=self.group
            )

        # 4. PRZYCISKI SKALOWALNE
        btn_width = 200 * ui_scale
        btn_height = 60 * ui_scale
        spacing = 20 * ui_scale
        font_size = 20 * ui_scale

        start_x = (window_width / 2) - ( (btn_width * 3 + spacing * 2) / 2 )
        y_pos = window_height * 0.15

        self.buttons.append(Button("GRAJ", start_x, y_pos, btn_width, btn_height,
            consts.BTN_COLOR_PLAY, self.start_game_func, self.batch, self.group, font_size=font_size))

        self.buttons.append(Button("OPCJE", start_x + btn_width + spacing, y_pos, btn_width, btn_height,
            consts.BTN_COLOR_OPT, self.options_func, self.batch, self.group, font_size=font_size))

        self.buttons.append(Button("WYJDŹ", start_x + (btn_width + spacing) * 2, y_pos, btn_width, btn_height,
            consts.BTN_COLOR_EXIT, self.exit_game_func, self.batch, self.group, font_size=font_size))

    def update_layout(self, width, height):
        self.build_ui(width, height)

    def on_mouse_motion(self, x, y, dx, dy):
        for btn in self.buttons:
            btn.check_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.buttons:
            btn.check_click(x, y)