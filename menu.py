import pyglet
from pyglet import shapes
import consts

class Button:
    def __init__(self, label_text, x, y, width, height, color, func, batch, group):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.func = func # Funkcja, która się odpali po kliknięciu
        self.base_y = y # Zapamiętujemy pozycję, żeby przycisk mógł "skakać"

        # Kształt przycisku (Tło)
        self.rect = shapes.Rectangle(x, y, width, height, color=color, batch=batch, group=group)

        # Ozdobny "Cień/Bok" przycisku (dla efektu 3D)
        darker_color = (int(color[0]*0.7), int(color[1]*0.7), int(color[2]*0.7))
        self.shadow = shapes.Rectangle(x, y - 5, width, 5, color=darker_color, batch=batch, group=group)

        # Tekst na przycisku
        self.label = pyglet.text.Label(
            label_text,
            font_name='Arial',
            font_size=20,
            # USUNĄŁEM bold=True stąd, bo powodowało błąd
            x=x + width // 2,
            y=y + height // 2,
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 255, 255),
            batch=batch,
            group=pyglet.graphics.Group(order=group.order + 1) # Tekst zawsze nad przyciskiem
        )
        # Ustawiamy pogrubienie bezpieczną metodą po stworzeniu obiektu
        self.label.bold = True

        self.is_hovered = False

    def check_hover(self, mouse_x, mouse_y):
        # Sprawdzamy czy myszka jest nad przyciskiem
        in_x = self.x < mouse_x < self.x + self.width
        in_y = self.y < mouse_y < self.y + self.height

        if in_x and in_y:
            if not self.is_hovered:
                self.is_hovered = True
                # Efekt podniesienia przycisku
                self.rect.y = self.base_y + 5
                self.label.y = (self.base_y + 5) + self.height // 2
                self.shadow.height = 10 # Cień się wydłuża
                self.shadow.y = self.base_y - 5
        else:
            if self.is_hovered:
                self.is_hovered = False
                # Powrót na dół
                self.rect.y = self.base_y
                self.label.y = self.base_y + self.height // 2
                self.shadow.height = 5
                self.shadow.y = self.base_y - 5

        return self.is_hovered

    def check_click(self, mouse_x, mouse_y):
        if self.is_hovered:
            if self.func:
                self.func() # Uruchom przypisaną akcję (np. start gry)
            return True
        return False

class MainMenu:
    def __init__(self, window_width, window_height, batch, start_game_func, exit_game_func):
        self.batch = batch
        # Grupa dla UI menu (żeby było nad tłem)
        self.group = pyglet.graphics.Group(order=10)

        # LOGO
        self.logo_label = pyglet.text.Label(
            "BALATRO CLONE",
            font_name='Arial',
            font_size=60,
            # USUNĄŁEM bold=True stąd
            x=window_width // 2,
            y=window_height - 150,
            anchor_x='center',
            anchor_y='center',
            batch=batch,
            group=self.group
        )
        self.logo_label.bold = True # Ustawiamy pogrubienie tutaj

        # Cień loga (dla efektu retro)
        self.logo_shadow = pyglet.text.Label(
            "BALATRO CLONE",
            font_name='Arial',
            font_size=60,
            # USUNĄŁEM bold=True stąd
            x=window_width // 2 + 5,
            y=window_height - 155,
            anchor_x='center',
            anchor_y='center',
            color=(0, 0, 0, 150),
            batch=batch,
            group=pyglet.graphics.Group(order=9)
        )
        self.logo_shadow.bold = True # Ustawiamy pogrubienie tutaj

        # PRZYCISKI
        self.buttons = []

        btn_width = 200
        btn_height = 60
        spacing = 20
        start_x = (window_width / 2) - ( (btn_width * 3 + spacing * 2) / 2 )
        y_pos = 150

        # 1. GRAJ (Niebieski)
        self.buttons.append(Button(
            "GRAJ",
            start_x, y_pos, btn_width, btn_height,
            consts.BTN_COLOR_PLAY,
            start_game_func, batch, self.group
        ))

        # 2. OPCJE (Pomarańczowy - na razie pusty)
        self.buttons.append(Button(
            "OPCJE",
            start_x + btn_width + spacing, y_pos, btn_width, btn_height,
            consts.BTN_COLOR_OPT,
            None, batch, self.group
        ))

        # 3. WYJDŹ (Czerwony)
        self.buttons.append(Button(
            "WYJDŹ",
            start_x + (btn_width + spacing) * 2, y_pos, btn_width, btn_height,
            consts.BTN_COLOR_EXIT,
            exit_game_func, batch, self.group
        ))

    def on_mouse_motion(self, x, y, dx, dy):
        for btn in self.buttons:
            btn.check_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.buttons:
            btn.check_click(x, y)

    def set_visible(self, visible):
        if visible:
            self.logo_label.color = (255, 255, 255, 255)
        else:
            self.logo_label.text = ""