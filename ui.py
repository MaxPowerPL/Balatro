import pyglet
from pyglet import shapes
import consts

class Button:
    def __init__(self, label_text, x, y, width, height, color, func, batch, group):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.func = func
        self.base_y = y

        self.rect = shapes.Rectangle(x, y, width, height, color=color, batch=batch, group=group)

        darker = (int(color[0]*0.7), int(color[1]*0.7), int(color[2]*0.7))
        self.shadow = shapes.Rectangle(x, y - 5, width, 5, color=darker, batch=batch, group=group)

        self.label = pyglet.text.Label(
            label_text, font_name='Arial', font_size=20,
            x=x + width // 2, y=y + height // 2,
            anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 255),
            batch=batch, group=pyglet.graphics.Group(order=group.order + 1)
        )
        self.label.bold = True
        self.is_hovered = False

    def check_hover(self, mx, my):
        in_x = self.x < mx < self.x + self.width
        in_y = self.y < my < self.y + self.height

        if in_x and in_y and not self.is_hovered:
            self.is_hovered = True
            self.rect.y = self.base_y + 5
            self.label.y = (self.base_y + 5) + self.height // 2
            self.shadow.height = 10
            self.shadow.y = self.base_y - 5
        elif not (in_x and in_y) and self.is_hovered:
            self.is_hovered = False
            self.rect.y = self.base_y
            self.label.y = self.base_y + self.height // 2
            self.shadow.height = 5
            self.shadow.y = self.base_y - 5
        return self.is_hovered

    def check_click(self, mx, my):
        if self.is_hovered and self.func:
            self.func()
            return True
        return False

class Slider:
    def __init__(self, label_text, val_min, val_max, current_val, x, y, width, height, callback, batch, group):
        self.min = val_min
        self.max = val_max
        self.value = current_val
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback # Funkcja wywoływana przy zmianie
        self.dragging = False

        # Etykieta nad suwakiem
        self.label = pyglet.text.Label(
            label_text, font_name='Arial', font_size=14,
            x=x + width // 2, y=y + height + 10,
            anchor_x='center', color=consts.BTN_COLOR_TEXT,
            batch=batch, group=group
        )
        self.label.bold = True

        # Tło paska (ciemne)
        self.bg_rect = shapes.Rectangle(x, y, width, height, color=consts.UI_SLIDER_BG, batch=batch, group=group)
        self.bg_rect.opacity = 200

        # Pasek wypełnienia (czerwony)
        self.fill_width = self._calc_fill_width()
        self.fill_rect = shapes.Rectangle(x, y, self.fill_width, height, color=consts.UI_SLIDER_FILL, batch=batch, group=group)

        # Tekst wartości obok
        self.val_label = pyglet.text.Label(
            str(int(self.value)), font_name='Arial', font_size=14,
            x=x + width + 15, y=y + height // 2,
            anchor_y='center', color=consts.BTN_COLOR_TEXT,
            batch=batch, group=group
        )
        self.val_label.bold = True

    def _calc_fill_width(self):
        percent = (self.value - self.min) / (self.max - self.min)
        return int(percent * self.width)

    def update_val_from_mouse(self, mx):
        # Oblicz wartość na podstawie pozycji myszki X
        rel_x = mx - self.x
        rel_x = max(0, min(rel_x, self.width)) # Clamp
        percent = rel_x / self.width
        self.value = self.min + percent * (self.max - self.min)

        # Aktualizacja grafiki
        self.fill_rect.width = int(rel_x)
        self.val_label.text = str(int(self.value))

        # Wywołanie callbacka (np. zmiana głośności)
        if self.callback:
            self.callback(self.value)

    def check_press(self, mx, my):
        # Sprawdzamy czy kliknięto w pasek
        if self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height:
            self.dragging = True
            self.update_val_from_mouse(mx)
            return True
        return False

    def check_drag(self, mx, my):
        if self.dragging:
            self.update_val_from_mouse(mx)

    def check_release(self):
        self.dragging = False

class Checkbox:
    def __init__(self, label_text, is_checked, x, y, size, callback, batch, group):
        self.is_checked = is_checked
        self.x = x
        self.y = y
        self.size = size
        self.callback = callback

        self.label = pyglet.text.Label(
            label_text, font_name='Arial', font_size=14,
            x=x + size + 15, y=y + size // 2,
            anchor_y='center', color=consts.BTN_COLOR_TEXT,
            batch=batch, group=group
        )
        self.label.bold = True

        # Ramka
        self.rect = shapes.BorderedRectangle(x, y, size, size, border=2, color=(30,30,30), border_color=(200,200,200), batch=batch, group=group)

        # "Ptaszek" / Wypełnienie
        self.inner = shapes.Rectangle(x+4, y+4, size-8, size-8, color=consts.BTN_COLOR_PLAY, batch=batch, group=group)
        self.inner.visible = is_checked

    def check_click(self, mx, my):
        if self.x <= mx <= self.x + self.size and self.y <= my <= self.y + self.size:
            self.is_checked = not self.is_checked
            self.inner.visible = self.is_checked
            if self.callback:
                self.callback(self.is_checked)
            return True
        return False