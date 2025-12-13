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

        self.rect = shapes.Rectangle(x, y, width, height, color=color, batch=batch, group=group)

        darker = (int(color[0]*0.7), int(color[1]*0.7), int(color[2]*0.7))
        self.shadow = shapes.Rectangle(x, y - 4, width, 4, color=darker, batch=batch, group=group)

        self.label = pyglet.text.Label(
            label_text, font_name='Arial', font_size=font_size,
            x=x + width // 2, y=y + height // 2,
            anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 255),
            batch=batch, group=pyglet.graphics.Group(order=group.order + 1)
        )
        self.label.bold = True
        self.is_hovered = False

        self.sprites = [self.rect, self.shadow, self.label]

    def delete(self):
        for s in self.sprites: s.delete()

    def set_visible(self, is_visible):
        self.visible = is_visible
        self.rect.visible = is_visible
        self.shadow.visible = is_visible
        opacity = 255 if is_visible else 0
        c = list(self.label.color); c[3] = opacity; self.label.color = tuple(c)

    def set_color(self, color):
        self.color = color
        self.rect.color = color
        darker = (int(color[0]*0.7), int(color[1]*0.7), int(color[2]*0.7))
        self.shadow.color = darker

    def set_text_color(self, color_rgb):
        self.label.color = (*color_rgb, 255)

    def check_hover(self, mx, my):
        if not self.visible: return False
        in_x = self.x < mx < self.x + self.width
        in_y = self.y < my < self.y + self.height

        if in_x and in_y and not self.is_hovered:
            self.is_hovered = True
            # Skalujemy efekt podniesienia (nie na sztywno 3px)
            offset = max(2, self.height * 0.05)
            self.rect.y = self.base_y + offset
            self.label.y = (self.base_y + offset) + self.height // 2
            self.shadow.height = 4 + offset
            self.shadow.y = self.base_y - offset
        elif not (in_x and in_y) and self.is_hovered:
            self.is_hovered = False
            self.rect.y = self.base_y
            self.label.y = self.base_y + self.height // 2
            self.shadow.height = 4
            self.shadow.y = self.base_y - 4
        return self.is_hovered

    def check_click(self, mx, my):
        if self.visible and self.is_hovered and self.func:
            self.func()
            return True
        return False

class Slider:
    def __init__(self, label_text, val_min, val_max, current_val, x, y, width, height, callback, batch, group, font_size=16):
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
            label_text, font_name='Arial', font_size=font_size,
            x=x + width // 2, y=y + height + (height * 0.8), # Odstęp zależny od wysokości
            anchor_x='center', color=(*consts.BTN_COLOR_TEXT, 255),
            batch=batch, group=group
        )
        self.label.bold = True

        self.bg_rect = shapes.Rectangle(x, y, width, height, color=consts.UI_SLIDER_BG, batch=batch, group=group)
        self.fill_width = self._calc_fill_width()
        self.fill_rect = shapes.Rectangle(x, y, self.fill_width, height, color=consts.UI_SLIDER_FILL, batch=batch, group=group)

        self.val_label = pyglet.text.Label(
            f"{int(self.value)}", font_name='Arial', font_size=font_size,
            x=x + width + (height * 0.8), y=y + height // 2,
            anchor_y='center', color=(*consts.BTN_COLOR_TEXT, 255),
            batch=batch, group=group
        )
        self.val_label.bold = True

        self.sprites = [self.label, self.bg_rect, self.fill_rect, self.val_label]

    def delete(self):
        for s in self.sprites: s.delete()

    def set_visible(self, is_visible):
        self.visible = is_visible
        self.bg_rect.visible = is_visible
        self.fill_rect.visible = is_visible
        opacity = 255 if is_visible else 0
        c1 = list(self.label.color); c1[3] = opacity; self.label.color = tuple(c1)
        c2 = list(self.val_label.color); c2[3] = opacity; self.val_label.color = tuple(c2)

    def _calc_fill_width(self):
        percent = (self.value - self.min) / (self.max - self.min)
        return int(percent * self.width)

    def update_val_from_mouse(self, mx):
        rel_x = mx - self.x
        rel_x = max(0, min(rel_x, self.width))
        percent = rel_x / self.width
        new_val = self.min + percent * (self.max - self.min)

        self.fill_rect.width = int(rel_x)

        if int(new_val) != int(self.value):
            self.val_label.text = f"{int(new_val)}"

        self.value = new_val

        if self.callback: self.callback(self.value)

    def check_press(self, mx, my):
        if not self.visible: return False
        # Hitbox z marginesem
        margin = self.height * 0.5
        if self.x <= mx <= self.x + self.width and self.y - margin <= my <= self.y + self.height + margin:
            self.dragging = True
            self.update_val_from_mouse(mx)
            return True
        return False

    def check_drag(self, mx, my):
        if self.visible and self.dragging: self.update_val_from_mouse(mx)

    def check_release(self): self.dragging = False

class Checkbox:
    def __init__(self, label_text, is_checked, x, y, size, callback, batch, group, font_size=16):
        self.is_checked = is_checked
        self.x = x
        self.y = y
        self.size = size
        self.callback = callback
        self.visible = True

        self.label = pyglet.text.Label(
            label_text, font_name='Arial', font_size=font_size,
            x=x + size + (size * 0.5), y=y + size // 2 + 2,
            anchor_y='center', color=(*consts.BTN_COLOR_TEXT, 255),
            batch=batch, group=group
        )
        self.label.bold = True

        self.rect = shapes.BorderedRectangle(x, y, size, size, border=max(2, int(size*0.1)), color=consts.UI_CHECKBOX_BG, border_color=consts.UI_PANEL_BORDER, batch=batch, group=group)

        inner_margin = max(3, int(size * 0.2))
        self.inner = shapes.Rectangle(x+inner_margin, y+inner_margin, size-(inner_margin*2), size-(inner_margin*2), color=consts.UI_CHECKBOX_FILL, batch=batch, group=group)
        self.inner.visible = is_checked

        self.sprites = [self.label, self.rect, self.inner]

    def delete(self):
        for s in self.sprites: s.delete()

    def set_visible(self, is_visible):
        self.visible = is_visible
        self.rect.visible = is_visible
        if not is_visible:
            self.inner.visible = False
        else:
            self.inner.visible = self.is_checked
        opacity = 255 if is_visible else 0
        c = list(self.label.color); c[3] = opacity; self.label.color = tuple(c)

    def check_click(self, mx, my):
        if not self.visible: return False
        if self.x <= mx <= self.x + self.size and self.y <= my <= self.y + self.size:
            self.is_checked = not self.is_checked
            self.set_visible(self.visible)
            if self.callback: self.callback(self.is_checked)
            return True
        return False