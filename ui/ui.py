import pyglet
from pyglet import shapes
import config.consts as consts

# --- BUTTON ---
class Button:
    def __init__(self, label_text, x, y, width, height, color, func, batch, group, font_size=20):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.func = func
        self.color = color
        self.visible = True
        self.batch = batch
        self.group = group

        self.rect = shapes.Rectangle(x, y, width, height, color=color, batch=batch, group=group)
        darker_color = (int(color[0]*0.7), int(color[1]*0.7), int(color[2]*0.7))
        self.shadow = shapes.Rectangle(x, y - 4, width, 4, color=darker_color, batch=batch, group=group)

        self.label = pyglet.text.Label(label_text, font_name='Arial', font_size=font_size,
                                       x=x + width//2, y=y + height//2, anchor_x='center', anchor_y='center',
                                       color=(255, 255, 255, 255), batch=batch, group=pyglet.graphics.Group(order=group.order+1))
        self.label.bold = True
        self.is_hovered = False
        self.sprites = [self.rect, self.shadow, self.label]

    def delete(self):
        for s in self.sprites: s.delete()

    def set_visible(self, is_visible):
        self.visible = is_visible
        for s in self.sprites:
            s.batch = self.batch if is_visible else None

    def check_hover(self, mx, my):
        if not self.visible: return False
        in_x = self.x < mx < self.x + self.width
        in_y = self.y < my < self.y + self.height

        if in_x and in_y and not self.is_hovered:
            self.is_hovered = True
            self.rect.y += 2
            self.label.y += 2
            self.shadow.height += 2
        elif not (in_x and in_y) and self.is_hovered:
            self.is_hovered = False
            self.rect.y -= 2
            self.label.y -= 2
            self.shadow.height -= 2
        return self.is_hovered

    def check_click(self, mx, my):
        if self.visible and self.is_hovered and self.func:
            self.func()
            return True
        return False

    def set_color(self, color):
        self.color = color
        self.rect.color = color
        darker = (int(color[0]*0.7), int(color[1]*0.7), int(color[2]*0.7))
        self.shadow.color = darker

    def set_text_color(self, color_rgb):
        self.label.color = (*color_rgb, 255)

# --- SLIDER ---
class Slider:
    def __init__(self, label_text, val_min, val_max, current_val, x, y, width, height, callback, batch, group, font_size=16):
        self.min, self.max, self.value = val_min, val_max, current_val
        self.x, self.y, self.width, self.height = x, y, width, height
        self.callback = callback
        self.dragging = False
        self.visible = True
        self.batch = batch

        self.label = pyglet.text.Label(label_text, font_name='Arial', font_size=font_size, x=x+width//2, y=y+height*1.8, anchor_x='center', color=(*consts.BTN_COLOR_TEXT, 255), batch=batch, group=group)
        self.label.bold = True

        self.bg_rect = shapes.Rectangle(x, y, width, height, color=consts.UI_SLIDER_BG, batch=batch, group=group)
        self.fill_width = int((self.value - self.min) / (self.max - self.min) * self.width)
        self.fill_rect = shapes.Rectangle(x, y, self.fill_width, height, color=consts.UI_SLIDER_FILL, batch=batch, group=group)

        self.val_label = pyglet.text.Label(f"{int(self.value)}", font_name='Arial', font_size=font_size, x=x+width+height, y=y+height//2, anchor_y='center', color=(*consts.BTN_COLOR_TEXT, 255), batch=batch, group=group)
        self.val_label.bold = True

        self.sprites = [self.label, self.bg_rect, self.fill_rect, self.val_label]

    def delete(self):
        for s in self.sprites: s.delete()

    def set_visible(self, is_visible):
        self.visible = is_visible
        for s in self.sprites: s.batch = self.batch if is_visible else None

    def update_val_from_mouse(self, mx):
        rel_x = max(0, min(mx - self.x, self.width))
        self.value = self.min + (rel_x / self.width) * (self.max - self.min)
        self.fill_rect.width = int(rel_x)
        self.val_label.text = f"{int(self.value)}"
        if self.callback: self.callback(self.value)

    def check_press(self, mx, my):
        if not self.visible: return False
        if self.x <= mx <= self.x + self.width and self.y - 10 <= my <= self.y + self.height + 10:
            self.dragging = True; self.update_val_from_mouse(mx); return True
        return False
    def check_drag(self, mx, my):
        if self.visible and self.dragging: self.update_val_from_mouse(mx)
    def check_release(self): self.dragging = False

# --- CHECKBOX ---
class Checkbox:
    def __init__(self, label_text, is_checked, x, y, size, callback, batch, group, font_size=16):
        self.is_checked, self.x, self.y, self.size = is_checked, x, y, size
        self.callback, self.visible, self.batch = callback, True, batch

        self.label = pyglet.text.Label(label_text, font_name='Arial', font_size=font_size, x=x+size*1.5, y=y+size//2+2, anchor_y='center', color=(*consts.BTN_COLOR_TEXT, 255), batch=batch, group=group)
        self.label.bold = True

        self.rect = shapes.BorderedRectangle(x, y, size, size, border=2, color=consts.UI_CHECKBOX_BG, border_color=consts.UI_PANEL_BORDER, batch=batch, group=group)
        self.inner = shapes.Rectangle(x+4, y+4, size-8, size-8, color=consts.UI_CHECKBOX_FILL, batch=batch, group=group)
        self.inner.visible = is_checked
        self.sprites = [self.label, self.rect, self.inner]

    def delete(self):
        for s in self.sprites: s.delete()

    def set_visible(self, is_visible):
        self.visible = is_visible
        self.label.batch = self.batch if is_visible else None
        self.rect.batch = self.batch if is_visible else None
        self.inner.batch = self.batch if (is_visible and self.is_checked) else None

    def check_click(self, mx, my):
        if not self.visible: return False
        if self.x <= mx <= self.x + self.size and self.y <= my <= self.y + self.size:
            self.is_checked = not self.is_checked
            self.set_visible(self.visible)
            if self.callback: self.callback(self.is_checked)
            return True
        return False

# --- SCORE PILL ---
class ScorePill:
    def __init__(self, x, y, width, batch, group, ui_scale):
        self.ui_scale = ui_scale
        height = 60 * ui_scale; w_part = width / 2
        self.bg = shapes.Rectangle(x-4, y-4, width+8, height+8, color=(20,20,20), batch=batch, group=group)
        self.chips_rect = shapes.Rectangle(x, y, w_part, height, color=consts.COLOR_CHIPS, batch=batch, group=pyglet.graphics.Group(order=group.order+1))
        self.mult_rect = shapes.Rectangle(x + w_part, y, w_part, height, color=consts.COLOR_MULT, batch=batch, group=pyglet.graphics.Group(order=group.order+1))

        self.lbl_chips = pyglet.text.Label("0", font_name='Arial', font_size=24*ui_scale, x=x+w_part/2-10*ui_scale, y=y+height/2, anchor_x='center', anchor_y='center', batch=batch, group=pyglet.graphics.Group(order=group.order+2))
        self.lbl_chips.bold = True

        self.lbl_mult = pyglet.text.Label("0", font_name='Arial', font_size=24*ui_scale, x=x+w_part*1.5+10*ui_scale, y=y+height/2, anchor_x='center', anchor_y='center', batch=batch, group=pyglet.graphics.Group(order=group.order+2))
        self.lbl_mult.bold = True

        self.x_bg = shapes.Circle(x+w_part, y+height/2, 15*ui_scale, color=(20,20,20), batch=batch, group=pyglet.graphics.Group(order=group.order+2))

        self.lbl_x = pyglet.text.Label("X", font_name='Arial', font_size=18*ui_scale, x=x+w_part, y=y+height/2, anchor_x='center', anchor_y='center', color=(255,255,255,255), batch=batch, group=pyglet.graphics.Group(order=group.order+3))
        self.lbl_x.bold = True

        self.lbl_name = pyglet.text.Label("", font_name='Arial', font_size=20*ui_scale, x=x+width/2, y=y+height+20*ui_scale, anchor_x='center', anchor_y='center', batch=batch, group=pyglet.graphics.Group(order=group.order+2))
        self.lbl_name.bold = True

        self.elements = [self.bg, self.chips_rect, self.mult_rect, self.lbl_chips, self.lbl_mult, self.x_bg, self.lbl_x, self.lbl_name]

    def update(self, chips, mult, name):
        self.lbl_chips.text = str(int(chips)); self.lbl_mult.text = str(int(mult))
        self.lbl_name.text = consts.HAND_NAMES_PL.get(name, name)
    def delete(self):
        for el in self.elements: el.delete()