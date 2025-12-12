import pyglet
from pyglet import shapes
import consts
from ui import Button, Slider, Checkbox

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

        # Warstwy
        self.bg_group = pyglet.graphics.Group(order=20)
        self.nav_group = pyglet.graphics.Group(order=21)
        self.content_bg_group = pyglet.graphics.Group(order=21)
        self.content_ui_group = pyglet.graphics.Group(order=22)

        self.bg_sprites = []
        self.nav_buttons = {}
        self.tab_content = {tab: [] for tab in TABS_ORDER}
        self.headers = []

        self._build_structure()
        self._build_tabs()
        self._build_all_content()

        self.select_tab(TABS_ORDER[0])

    def _build_structure(self):
        cx, cy = self.window.width // 2, self.window.height // 2
        w, h = 900, 600
        self.panel_x = cx - w // 2
        self.panel_y = cy - h // 2
        self.panel_w = w
        self.panel_h = h

        self.nav_w = 220
        self.content_x = self.panel_x + self.nav_w
        self.content_w = w - self.nav_w

        shadow = shapes.Rectangle(self.panel_x + 10, self.panel_y - 10, w, h, color=(0,0,0), batch=self.batch, group=self.bg_group)
        shadow.opacity = 150
        main_bg = shapes.BorderedRectangle(self.panel_x, self.panel_y, w, h, border=4, color=consts.UI_PANEL_BG, border_color=consts.UI_PANEL_BORDER, batch=self.batch, group=self.bg_group)
        content_bg = shapes.Rectangle(self.content_x, self.panel_y + 4, self.content_w - 4, h - 8, color=consts.UI_CONTENT_BG, batch=self.batch, group=self.content_bg_group)

        self.bg_sprites.extend([shadow, main_bg, content_bg])

        btn_close = Button(
            "WRÓĆ", self.panel_x + 20, self.panel_y + 20, self.nav_w - 40, 60,
            consts.BTN_COLOR_EXIT, self.close, self.batch, self.nav_group, font_size=24
        )
        self.always_visible_ui = [btn_close]

    def _build_tabs(self):
        btn_h = 70
        spacing = 15
        start_y = self.panel_y + self.panel_h - btn_h - 30

        for i, tab_name in enumerate(TABS_ORDER):
            callback = lambda name=tab_name: self.select_tab(name)
            btn = Button(
                tab_name,
                self.panel_x + 15, start_y - i * (btn_h + spacing),
                self.nav_w - 30, btn_h,
                consts.UI_TAB_INACTIVE,
                callback, self.batch, self.nav_group, font_size=22
            )
            self.nav_buttons[tab_name] = btn

    def _create_header(self, text, y_pos):
        color_with_alpha = (*consts.UI_HEADER_TEXT, 255)
        label = pyglet.text.Label(
            text.upper(), font_name='Arial', font_size=28,
            x=self.content_x + 40, y=y_pos,
            color=color_with_alpha, batch=self.batch, group=self.content_ui_group
        )
        label.bold = True
        return label

    def _build_all_content(self):
        self._build_content_game()
        self._build_content_video()
        self._build_content_audio()

        for tab in TABS_ORDER:
            for element in self.tab_content[tab]:
                if hasattr(element, 'set_visible'): element.set_visible(False)
                elif isinstance(element, pyglet.text.Label):
                    c = list(element.color); c[3] = 0; element.color = tuple(c)

    def _build_content_video(self):
        elements = self.tab_content[TAB_VIDEO]
        cursor_y = self.panel_y + self.panel_h - 80
        x_pos = self.content_x + 60

        elements.append(self._create_header("Obraz", cursor_y))
        cursor_y -= 80

        slider_crt = Slider(
            "Intensywność Efektu CRT", 20.0, 500.0, consts.settings.crt_intensity,
            x_pos, cursor_y, 400, 24,
            self.set_crt, self.batch, self.content_ui_group
        )
        elements.append(slider_crt)
        cursor_y -= 100

        chk_fs = Checkbox(
            "Pełny Ekran", consts.settings.fullscreen,
            x_pos, cursor_y, 32,
            self.set_fullscreen, self.batch, self.content_ui_group
        )
        elements.append(chk_fs)

    def _build_content_audio(self):
        elements = self.tab_content[TAB_AUDIO]
        cursor_y = self.panel_y + self.panel_h - 80
        x_pos = self.content_x + 60

        elements.append(self._create_header("Głośność", cursor_y))
        cursor_y -= 80

        sliders_data = [
            ("Głośność Główna", 0, 100, consts.settings.volume_master, self.set_vol_master),
            ("Muzyka", 0, 100, consts.settings.volume_music, self.set_vol_music),
            ("Efekty Dźwiękowe", 0, 100, consts.settings.volume_sfx, self.set_vol_sfx)
        ]

        for title, min_v, max_v, val, func in sliders_data:
            s = Slider(title, min_v, max_v, val, x_pos, cursor_y, 400, 24, func, self.batch, self.content_ui_group)
            elements.append(s)
            cursor_y -= 90

    def _build_content_game(self):
        elements = self.tab_content[TAB_GAME]
        cursor_y = self.panel_y + self.panel_h - 80
        x_pos = self.content_x + 60

        elements.append(self._create_header("Rozgrywka", cursor_y))
        cursor_y -= 80

        chk_tut = Checkbox("Pokaż Samouczki", consts.settings.show_tutorials,
            x_pos, cursor_y, 32, self.set_tutorials, self.batch, self.content_ui_group)
        elements.append(chk_tut)
        cursor_y -= 100

        slider_speed = Slider("Szybkość Animacji", 0.5, 2.0, consts.settings.game_speed,
            x_pos, cursor_y, 400, 24, self.set_speed, self.batch, self.content_ui_group)
        elements.append(slider_speed)

    def select_tab(self, tab_name):
        if tab_name == self.current_tab: return

        if self.current_tab:
            for element in self.tab_content[self.current_tab]:
                if hasattr(element, 'set_visible'): element.set_visible(False)
                elif isinstance(element, pyglet.text.Label):
                    c = list(element.color); c[3] = 0; element.color = tuple(c)

        self.current_tab = tab_name
        for element in self.tab_content[tab_name]:
            if hasattr(element, 'set_visible'): element.set_visible(True)
            elif isinstance(element, pyglet.text.Label):
                c = list(element.color); c[3] = 255; element.color = tuple(c)

        for name, btn in self.nav_buttons.items():
            if name == tab_name:
                btn.set_color(consts.UI_TAB_ACTIVE)
                btn.set_text_color(consts.UI_TAB_TEXT_ACTIVE)
            else:
                btn.set_color(consts.UI_TAB_INACTIVE)
                btn.set_text_color(consts.UI_TAB_TEXT_INACTIVE)

    # --- CALLBACKI (TYLKO AKTUALIZACJA PAMIĘCI) ---
    # Usunąłem stąd 'consts.settings.save()', żeby nie zapisywać co klatkę!

    def set_crt(self, val):
        consts.settings.crt_intensity = val

    def set_fullscreen(self, val):
        consts.settings.fullscreen = val
        self.window.set_fullscreen(val)
        # Fullscreen to pojedyncze kliknięcie, więc tu save jest bezpieczny, ale dla porządku zrobimy to w input

    def set_vol_master(self, val):
        consts.settings.volume_master = val

    def set_vol_music(self, val):
        consts.settings.volume_music = val

    def set_vol_sfx(self, val):
        consts.settings.volume_sfx = val

    def set_tutorials(self, val):
        consts.settings.show_tutorials = val

    def set_speed(self, val):
        consts.settings.game_speed = val

    def close(self):
        # Zapisz przy wyjściu z opcji dla pewności
        consts.settings.save()
        self.on_close_func()

    # --- INPUT ---
    def _get_active_elements(self):
        return list(self.nav_buttons.values()) + self.always_visible_ui + self.tab_content.get(self.current_tab, [])

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.visible: return

        was_clicked = False
        for el in self._get_active_elements():
            if isinstance(el, Slider):
                if el.check_press(x, y): was_clicked = True
            elif isinstance(el, Button) or isinstance(el, Checkbox):
                if el.check_click(x, y):
                    was_clicked = True
                    # Checkboxy i przyciski to pojedyncze akcje, więc możemy zapisać od razu
                    if isinstance(el, Checkbox):
                        consts.settings.save()

        return True

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self.visible: return
        for el in self.tab_content.get(self.current_tab, []):
            if isinstance(el, Slider):
                el.check_drag(x, y)
                # TU NIE ZAPISUJEMY! To dzieje się co klatkę.

    def on_mouse_release(self, x, y, button, modifiers):
        if not self.visible: return

        slider_was_released = False
        for el in self.tab_content.get(self.current_tab, []):
            if isinstance(el, Slider):
                # Sprawdzamy, czy ten slider był ciągnięty
                if el.dragging:
                    el.check_release()
                    slider_was_released = True

        # ZAPISUJEMY TYLKO TERAZ!
        # Gdy użytkownik puści myszkę po przesunięciu suwaka.
        if slider_was_released:
            print("Suwak puszczony -> Zapisuję ustawienia...")
            consts.settings.save()

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.visible: return
        for el in self._get_active_elements():
            if isinstance(el, Button): el.check_hover(x, y)

    def update_layout(self):
        self.rebuild_ui()

    def rebuild_ui(self):
        # 1. Czyszczenie starego UI
        for s in self.bg_sprites: s.delete()
        self.bg_sprites = []

        for btn in self.nav_buttons.values(): btn.delete()
        self.nav_buttons = {}

        for tab in TABS_ORDER:
            for el in self.tab_content[tab]:
                if hasattr(el, 'delete'): el.delete()
            self.tab_content[tab] = []

        for el in self.always_visible_ui:
            if hasattr(el, 'delete'): el.delete()
        self.always_visible_ui = []

        # 2. Budowa na nowo
        self._build_structure()
        self._build_tabs()
        self._build_all_content()

        # 3. Przywrócenie stanu (zakładki)
        temp_tab = self.current_tab
        self.current_tab = None
        self.select_tab(temp_tab)

        if not self.visible:
            self._hide_everything()

    def _hide_everything(self):
        for el in self.bg_sprites: el.opacity = 0
        for el in self._get_active_elements():
            if hasattr(el, 'set_visible'): el.set_visible(False)
        for tab in TABS_ORDER:
            for el in self.tab_content[tab]:
                if hasattr(el, 'set_visible'): el.set_visible(False)
                elif isinstance(el, pyglet.text.Label):
                    c = list(el.color); c[3] = 0; el.color = tuple(c)