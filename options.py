import pyglet
from pyglet import shapes
import consts
from ui import Button, Slider, Checkbox

# Nazwy zakładek
TAB_GAME = "GRA"
TAB_VIDEO = "WIDEO"
TAB_AUDIO = "AUDIO"
TABS_ORDER = [TAB_GAME, TAB_VIDEO, TAB_AUDIO]

class OptionsMenu:
    def __init__(self, window, batch, on_close_func):
        self.window = window
        self.batch = batch
        self.on_close_func = on_close_func
        self.visible = False
        self.current_tab = None

        # --- GRUPY RYSOWANIA (Warstwy) ---
        self.bg_group = pyglet.graphics.Group(order=20)        # Główne tło i cień
        self.nav_group = pyglet.graphics.Group(order=21)       # Przyciski zakładek
        self.content_bg_group = pyglet.graphics.Group(order=21)# Tło prawej sekcji
        self.content_ui_group = pyglet.graphics.Group(order=22)# Suwaki i treści

        # Kontenery na elementy UI
        self.bg_sprites = []
        self.nav_buttons = {}
        self.tab_content = {tab: [] for tab in TABS_ORDER}
        self.headers = []

        self._build_structure()
        self._build_tabs()
        self._build_all_content()

        # Na start wybieramy pierwszą zakładkę
        self.select_tab(TABS_ORDER[0])

    def _build_structure(self):
        """Buduje główne ramy okna opcji (tło, panele)."""
        cx, cy = self.window.width // 2, self.window.height // 2
        w, h = 800, 550
        self.panel_x = cx - w // 2
        self.panel_y = cy - h // 2
        self.panel_w = w
        self.panel_h = h

        # Wymiary sekcji nawigacji (lewa) i zawartości (prawa)
        self.nav_w = 200
        self.content_x = self.panel_x + self.nav_w
        self.content_w = w - self.nav_w

        # Cień i tła
        shadow = shapes.Rectangle(self.panel_x + 10, self.panel_y - 10, w, h, color=(0,0,0), batch=self.batch, group=self.bg_group)
        shadow.opacity = 100
        main_bg = shapes.BorderedRectangle(self.panel_x, self.panel_y, w, h, border=4, color=consts.UI_PANEL_BG, border_color=consts.UI_PANEL_BORDER, batch=self.batch, group=self.bg_group)
        content_bg = shapes.Rectangle(self.content_x, self.panel_y + 4, self.content_w - 4, h - 8, color=consts.UI_CONTENT_BG, batch=self.batch, group=self.content_bg_group)

        self.bg_sprites.extend([shadow, main_bg, content_bg])

        # Przycisk Zamknij
        btn_close = Button(
            "WRÓĆ", self.panel_x + 20, self.panel_y + 20, self.nav_w - 40, 50,
            consts.BTN_COLOR_EXIT, self.close, self.batch, self.nav_group
        )
        self.always_visible_ui = [btn_close]

    def _build_tabs(self):
        """Tworzy przyciski nawigacyjne po lewej stronie."""
        btn_h = 60
        spacing = 10
        start_y = self.panel_y + self.panel_h - btn_h - 20

        for i, tab_name in enumerate(TABS_ORDER):
            callback = lambda name=tab_name: self.select_tab(name)
            btn = Button(
                tab_name,
                self.panel_x + 10, start_y - i * (btn_h + spacing),
                self.nav_w - 20, btn_h,
                consts.UI_TAB_INACTIVE,
                callback,
                self.batch, self.nav_group,
                font_size=18
            )
            self.nav_buttons[tab_name] = btn

    def _create_header(self, text, y_offset):
        """Pomocnik do tworzenia nagłówków sekcji."""
        # Dodajemy czwarty element koloru (Alpha = 255)
        color_with_alpha = (*consts.UI_HEADER_TEXT, 255)

        label = pyglet.text.Label(
            text.upper(), font_name='Arial', font_size=22,
            x=self.content_x + 30, y=self.panel_y + self.panel_h - y_offset,
            color=color_with_alpha, batch=self.batch, group=self.content_ui_group
        )
        label.bold = True
        return label

    def _build_all_content(self):
        """Buduje UI dla wszystkich zakładek."""
        self._build_content_game()
        self._build_content_video()
        self._build_content_audio()

        # POPRAWKA BŁĘDU:
        # Na start ukrywamy wszystko, ale sprawdzamy typ obiektu!
        for tab in TABS_ORDER:
            for element in self.tab_content[tab]:
                if hasattr(element, 'set_visible'):
                    element.set_visible(False)
                elif isinstance(element, pyglet.text.Label):
                    # Ręczne ukrywanie Labela (Alpha = 0)
                    c = list(element.color)
                    c[3] = 0
                    element.color = tuple(c)

    def _build_content_video(self):
        elements = self.tab_content[TAB_VIDEO]
        start_y = self.panel_y + self.panel_h - 100
        x_pos = self.content_x + 50

        elements.append(self._create_header("Obraz", 60))

        slider_crt = Slider(
            "Intensywność Efektu CRT", 20.0, 500.0, consts.settings.crt_intensity,
            x_pos, start_y, 350, 24,
            self.set_crt, self.batch, self.content_ui_group
        )
        elements.append(slider_crt)

        chk_fs = Checkbox(
            "Pełny Ekran", consts.settings.fullscreen,
            x_pos, start_y - 80, 28,
            self.set_fullscreen, self.batch, self.content_ui_group
        )
        elements.append(chk_fs)

    def _build_content_audio(self):
        elements = self.tab_content[TAB_AUDIO]
        start_y = self.panel_y + self.panel_h - 100
        x_pos = self.content_x + 50

        elements.append(self._create_header("Głośność", 60))

        vol_master = Slider("Głośność Główna", 0, 100, consts.settings.volume_master,
            x_pos, start_y, 350, 24, self.set_vol_master, self.batch, self.content_ui_group)

        vol_music = Slider("Muzyka", 0, 100, consts.settings.volume_music,
            x_pos, start_y - 80, 350, 24, self.set_vol_music, self.batch, self.content_ui_group)

        vol_sfx = Slider("Efekty Dźwiękowe", 0, 100, consts.settings.volume_sfx,
            x_pos, start_y - 160, 350, 24, self.set_vol_sfx, self.batch, self.content_ui_group)

        elements.extend([vol_master, vol_music, vol_sfx])

    def _build_content_game(self):
        elements = self.tab_content[TAB_GAME]
        start_y = self.panel_y + self.panel_h - 100
        x_pos = self.content_x + 50

        elements.append(self._create_header("Rozgrywka", 60))

        chk_tut = Checkbox("Pokaż Samouczki", consts.settings.show_tutorials,
            x_pos, start_y, 28, lambda x: None, self.batch, self.content_ui_group)
        elements.append(chk_tut)

        slider_speed = Slider("Szybkość Animacji", 0.5, 2.0, consts.settings.game_speed,
            x_pos, start_y - 80, 350, 24, lambda x: None, self.batch, self.content_ui_group)
        elements.append(slider_speed)

    # --- LOGIKA PRZEŁĄCZANIA ZAKŁADEK ---
    def select_tab(self, tab_name):
        if tab_name == self.current_tab: return
        print(f"Przełączam zakładkę na: {tab_name}")

        # 1. Ukryj starą zawartość
        if self.current_tab:
            for element in self.tab_content[self.current_tab]:
                if hasattr(element, 'set_visible'):
                    element.set_visible(False)
                elif isinstance(element, pyglet.text.Label):
                    c = list(element.color)
                    c[3] = 0
                    element.color = tuple(c)

        # 2. Pokaż nową zawartość
        self.current_tab = tab_name
        for element in self.tab_content[tab_name]:
            if hasattr(element, 'set_visible'):
                element.set_visible(True)
            elif isinstance(element, pyglet.text.Label):
                c = list(element.color)
                c[3] = 255
                element.color = tuple(c)

        # 3. Zaktualizuj wygląd przycisków nawigacyjnych
        for name, btn in self.nav_buttons.items():
            if name == tab_name:
                btn.set_color(consts.UI_TAB_ACTIVE)
                btn.set_text_color(consts.UI_TAB_TEXT_ACTIVE)
            else:
                btn.set_color(consts.UI_TAB_INACTIVE)
                btn.set_text_color(consts.UI_TAB_TEXT_INACTIVE)

    # --- CALLBACKI ---
    def set_crt(self, val): consts.settings.crt_intensity = val
    def set_fullscreen(self, val):
        consts.settings.fullscreen = val
        self.window.set_fullscreen(val)
    def set_vol_master(self, val): consts.settings.volume_master = val
    def set_vol_music(self, val): consts.settings.volume_music = val
    def set_vol_sfx(self, val): consts.settings.volume_sfx = val
    def close(self): self.on_close_func()

    # --- INPUT ---
    def _get_active_elements(self):
        return list(self.nav_buttons.values()) + self.always_visible_ui + self.tab_content.get(self.current_tab, [])

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.visible: return

        hit = False
        for el in self._get_active_elements():
            if isinstance(el, Slider):
                if el.check_press(x, y): hit = True
            elif isinstance(el, Button):
                if el.check_click(x, y): hit = True
            elif isinstance(el, Checkbox):
                if el.check_click(x, y): hit = True
        return True

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self.visible: return
        for el in self.tab_content.get(self.current_tab, []):
            if isinstance(el, Slider):
                el.check_drag(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        if not self.visible: return
        for el in self.tab_content.get(self.current_tab, []):
            if isinstance(el, Slider):
                el.check_release()

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.visible: return
        for el in self._get_active_elements():
            if isinstance(el, Button):
                el.check_hover(x, y)