import pyglet
from pyglet import shapes
import consts
from ui import Button, Slider, Checkbox # Importujemy nasze nowe klocki

class OptionsMenu:
    def __init__(self, window, batch, on_close_func):
        self.window = window
        self.batch = batch
        self.on_close_func = on_close_func
        self.visible = False

        # Grupa o wysokim priorytecie, żeby rysować NAD menu głównym
        self.bg_group = pyglet.graphics.Group(order=20)
        self.ui_group = pyglet.graphics.Group(order=21)

        self.elements = []
        self.sprites = [] # Tło panelu

        self._build_ui()

    def _build_ui(self):
        cx, cy = self.window.width // 2, self.window.height // 2
        w, h = 600, 500

        # 1. Tło Panelu (Cień pod spodem + Panel właściwy)
        shadow = shapes.Rectangle(cx - w//2 + 10, cy - h//2 - 10, w, h, color=(0,0,0), batch=self.batch, group=self.bg_group)
        shadow.opacity = 100
        panel = shapes.BorderedRectangle(cx - w//2, cy - h//2, w, h, border=4, color=consts.UI_PANEL_BG, border_color=consts.UI_PANEL_BORDER, batch=self.batch, group=self.bg_group)
        self.sprites.extend([shadow, panel])

        # Nagłówek
        title = pyglet.text.Label("USTAWIENIA", font_name='Arial', font_size=30, x=cx, y=cy + h//2 - 40, anchor_x='center', batch=self.batch, group=self.ui_group)
        title.bold = True
        self.sprites.append(title)

        # --- SEKCJA VIDEO ---
        start_y = cy + 120

        # Slider: Efekt CRT (Pikselizacja)
        slider_crt = Slider(
            "Jakość Obrazu (Efekt CRT)", 20.0, 500.0, consts.settings.crt_intensity,
            cx - 150, start_y, 300, 20,
            self.set_crt, self.batch, self.ui_group
        )
        self.elements.append(slider_crt)

        # Checkbox: Fullscreen
        chk_fs = Checkbox(
            "Pełny Ekran", consts.settings.fullscreen,
            cx - 150, start_y - 60, 24,
            self.set_fullscreen, self.batch, self.ui_group
        )
        self.elements.append(chk_fs)

        # --- SEKCJA AUDIO ---

        slider_vol = Slider(
            "Głośność Ogólna", 0, 100, consts.settings.volume_master,
            cx - 150, start_y - 130, 300, 20,
            self.set_volume, self.batch, self.ui_group
        )
        self.elements.append(slider_vol)

        # Przycisk ZAMKNIJ / WSTECZ (Na dole panelu)
        btn_close = Button(
            "WSTECZ", cx - 100, cy - h//2 + 30, 200, 50,
            consts.BTN_COLOR_OPT, self.close, self.batch, self.ui_group
        )
        self.elements.append(btn_close)

    # --- CALLBACKI (Funkcje wykonawcze) ---
    def set_crt(self, val):
        consts.settings.crt_intensity = val
        # Zmiana jest widoczna natychmiast, bo background.py czyta settings w każdej klatce

    def set_fullscreen(self, is_checked):
        consts.settings.fullscreen = is_checked
        self.window.set_fullscreen(is_checked)

    def set_volume(self, val):
        consts.settings.volume_master = val
        # Tu w przyszłości dodasz mixer.music.set_volume(val / 100)

    def close(self):
        self.on_close_func()

    # --- INPUT ---
    def on_mouse_press(self, x, y, button, modifiers):
        if not self.visible: return

        # Sprawdzamy UI
        hit = False
        for el in self.elements:
            if isinstance(el, Slider):
                if el.check_press(x, y): hit = True
            elif isinstance(el, Button):
                if el.check_click(x, y): hit = True
            elif isinstance(el, Checkbox):
                if el.check_click(x, y): hit = True

        # Jeśli kliknięto w UI, zablokuj propagację w dół (żeby nie klikać menu pod spodem)
        return True

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self.visible: return
        for el in self.elements:
            if isinstance(el, Slider):
                el.check_drag(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        if not self.visible: return
        for el in self.elements:
            if isinstance(el, Slider):
                el.check_release()

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.visible: return
        for el in self.elements:
            if isinstance(el, Button):
                el.check_hover(x, y)