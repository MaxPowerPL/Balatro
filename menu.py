import pyglet
# WAŻNE: Importujemy Button z nowego pliku ui, a nie definiujemy go tutaj
from ui import Button
import consts

class MainMenu:
    def __init__(self, window_width, window_height, batch, start_game_func, options_func, exit_game_func):
        self.batch = batch
        self.group = pyglet.graphics.Group(order=10)

        # LOGO
        self.logo_label = pyglet.text.Label(
            "BALATRO CLONE", font_name='Arial', font_size=60,
            x=window_width // 2, y=window_height - 150,
            anchor_x='center', anchor_y='center', batch=batch, group=self.group
        )
        self.logo_label.bold = True

        self.logo_shadow = pyglet.text.Label(
            "BALATRO CLONE", font_name='Arial', font_size=60,
            x=window_width // 2 + 5, y=window_height - 155,
            anchor_x='center', anchor_y='center', color=(0, 0, 0, 150),
            batch=batch, group=pyglet.graphics.Group(order=9)
        )
        self.logo_shadow.bold = True

        self.buttons = []
        btn_width = 200; btn_height = 60; spacing = 20
        start_x = (window_width / 2) - ( (btn_width * 3 + spacing * 2) / 2 )
        y_pos = 150

        # 1. GRAJ
        self.buttons.append(Button("GRAJ", start_x, y_pos, btn_width, btn_height,
            consts.BTN_COLOR_PLAY, start_game_func, batch, self.group))

        # 2. OPCJE (Teraz działa!)
        self.buttons.append(Button("OPCJE", start_x + btn_width + spacing, y_pos, btn_width, btn_height,
            consts.BTN_COLOR_OPT, options_func, batch, self.group))

        # 3. WYJDŹ
        self.buttons.append(Button("WYJDŹ", start_x + (btn_width + spacing) * 2, y_pos, btn_width, btn_height,
            consts.BTN_COLOR_EXIT, exit_game_func, batch, self.group))

    def on_mouse_motion(self, x, y, dx, dy):
        for btn in self.buttons:
            btn.check_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.buttons:
            btn.check_click(x, y)