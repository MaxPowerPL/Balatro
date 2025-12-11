import pyglet
from pyglet import shapes
import consts

class Button:
    def __init__(self, label_text, x, y, width, height, color, func, batch, group, font_size=20):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.func = func
        self.base_y = y
        self.color = color
        self.visible = True

        # Główne tło
        self.rect = shapes.Rectangle(x, y, width, height, color=color, batch=batch, group=group)

        # Cień
        darker = (int(color[0]*0.7), int(color[1]*0.7), int(color[2]*0.7))
        self.shadow = shapes.Rectangle(x, y - 5, width, 5, color=darker, batch=batch, group=group)

        # Tekst
        self.label = pyglet.text.Label(
            label_text, font_name='Arial', font_size=font_size,
            x=x + width // 2, y=y + height // 2,
            anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 255),
            batch=batch, group=pyglet.graphics.Group(order=group.order + 1)
        )
        self.label.bold = True
        self.is_hovered = False

        # Zbieramy wszystkie komponenty graficzne
        self.sprites = [self.rect, self.shadow, self.label]

    def set_visible(self, is_visible):
        self.visible = is_visible
        # Ustawiamy przezroczystość na 0 jeśli niewidoczne (prosty hack w Pyglet)
        opacity = 255 if is_visible else 0
        self.rect.opacity = opacity
        self.shadow.opacity = opacity
        # Etykieta tekstowa wymaga innego podejścia do koloru
        current_color = list(self.label.color)
        current_color[3] = opacity # Kanał Alpha
        self.label.color = tuple(current_color)

    def set_color(self, color):
        self.color = color
        self.rect.color = color
        darker = (int(color[0]*0.7), int(color[1]*0.7), int(color[2]*0.7))
        self.shadow.color = darker

    def set_text_color(self, color_rgb):
        # Dodajemy kanał alpha (255)
        self.label.color = (color_rgb[0], color_rgb[1], color_rgb[2], 255)

    def check_hover(self, mx, my):
        if not self.visible: return False
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
        if self.visible and self.is_hovered and self.func:
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
        self.callback = callback
        self.dragging = False
        self.visible = True

        # Etykieta nad suwakiem
        self.label = pyglet.text.Label(
            label_text, font_name='Arial', font_size=14,
            x=x + width // 2, y=y + height + 10,
            anchor_x='center', color=(*consts.BTN_COLOR_TEXT, 255),
            batch=batch, group=group
        )
        self.label.bold = True

        # Tło paska
        self.bg_rect = shapes.Rectangle(x, y, width, height, color=consts.UI_SLIDER_BG, batch=batch, group=group)

        # Pasek wypełnienia
        self.fill_width = self._calc_fill_width()
        self.fill_rect = shapes.Rectangle(x, y, self.fill_width, height, color=consts.UI_SLIDER_FILL, batch=batch, group=group)

        # Tekst wartości
        self.val_label = pyglet.text.Label(
            str(int(self.value)), font_name='Arial', font_size=14,
            x=x + width + 15, y=y + height // 2,
            anchor_y='center', color=(*consts.BTN_COLOR_TEXT, 255),
            batch=batch, group=group
        )
        self.val_label.bold = True

        self.sprites = [self.label, self.bg_rect, self.fill_rect, self.val_label]

    def set_visible(self, is_visible):
        self.visible = is_visible
        opacity = 255 if is_visible else 0
        self.bg_rect.opacity = opacity
        self.fill_rect.opacity = opacity

        c_label = list(self.label.color); c_label[3] = opacity
        self.label.color = tuple(c_label)

        c_val = list(self.val_label.color); c_val[3] = opacity
        self.val_label.color = tuple(c_val)

    def _calc_fill_width(self):
        percent = (self.value - self.min) / (self.max - self.min)
        return int(percent * self.width)

    def update_val_from_mouse(self, mx):
        rel_x = mx - self.x
        rel_x = max(0, min(rel_x, self.width))
        percent = rel_x / self.width
        self.value = self.min + percent * (self.max - self.min)
        self.fill_rect.width = int(rel_x)
        self.val_label.text = str(int(self.value))
        if self.callback:
            self.callback(self.value)

    def check_press(self, mx, my):
        if not self.visible: return False
        if self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height:
            self.dragging = True
            self.update_val_from_mouse(mx)
            return True
        return False

    def check_drag(self, mx, my):
        if self.visible and self.dragging:
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
        self.visible = True

        self.label = pyglet.text.Label(
            label_text, font_name='Arial', font_size=14,
            x=x + size + 15, y=y + size // 2,
            anchor_y='center', color=(*consts.BTN_COLOR_TEXT, 255),
            batch=batch, group=group
        )
        self.label.bold = True

        self.rect = shapes.BorderedRectangle(x, y, size, size, border=3, color=consts.UI_CHECKBOX_BG, border_color=consts.UI_PANEL_BORDER, batch=batch, group=group)
        self.inner = shapes.Rectangle(x+5, y+5, size-10, size-10, color=consts.UI_CHECKBOX_FILL, batch=batch, group=group)
        self.inner.visible = is_checked

        self.sprites = [self.label, self.rect, self.inner]

    def set_visible(self, is_visible):
        self.visible = is_visible
        opacity = 255 if is_visible else 0
        self.rect.opacity = opacity
        self.rect.border_opacity = opacity
        # Inner jest widoczny tylko jeśli checkbox jest visible ORAZ checked
        self.inner.opacity = opacity if self.is_checked else 0

        c_label = list(self.label.color); c_label[3] = opacity
        self.label.color = tuple(c_label)

    def check_click(self, mx, my):
        if not self.visible: return False
        if self.x <= mx <= self.x + self.size and self.y <= my <= self.y + self.size:
            self.is_checked = not self.is_checked
            # Aktualizujemy widoczność środka
            self.set_visible(self.visible)
            if self.callback:
                self.callback(self.is_checked)
            return True
        return False