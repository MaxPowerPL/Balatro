import pyglet
from pyglet import shapes
import consts

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

# --- HAND HIERARCHY POPUP (KOMPLETNIE NOWY WYGLĄD) ---
class HandHierarchyPopup:
    def __init__(self, window_w, window_h, batch, ui_scale, close_func):
        self.batch = batch
        self.close_func = close_func
        self.visible = False
        self.elements = []
        self.stat_labels = {} # Do aktualizacji statystyk

        w = 800 * ui_scale # Szersze
        h = 600 * ui_scale
        x = (window_w - w) // 2
        y = (window_h - h) // 2
        self.x, self.y = x, y

        self.group_bg = pyglet.graphics.Group(order=1000)
        self.group_content = pyglet.graphics.Group(order=1001)
        self.group_top = pyglet.graphics.Group(order=1002)

        # Tło
        bg = shapes.BorderedRectangle(x, y, w, h, border=4, color=(40,40,45), border_color=(200,200,200), batch=batch, group=self.group_bg)
        self.elements.append(bg)

        title = pyglet.text.Label("UKŁADY POKEROWE", font_name='Arial', font_size=24*ui_scale, x=x+w/2, y=y+h-40*ui_scale, anchor_x='center', batch=batch, group=self.group_content)
        title.bold = True
        self.elements.append(title)

        # Lista układów
        ordered_hands = ["Royal Flush", "Straight Flush", "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind", "Two Pair", "Pair", "High Card"]

        start_y = y + h - 100*ui_scale
        row_h = 38 * ui_scale

        for i, hand in enumerate(ordered_hands):
            c, m = consts.HAND_SCORES[hand]
            row_y = start_y - (i * row_h)

            # Tło wiersza (opcjonalnie, paski)
            if i % 2 == 0:
                stripe = shapes.Rectangle(x+20*ui_scale, row_y-15*ui_scale, w-40*ui_scale, row_h, color=(50,50,55), batch=batch, group=self.group_bg)
                self.elements.append(stripe)

            # 1. Nazwa
            l_name = pyglet.text.Label(consts.HAND_NAMES_PL.get(hand, hand), font_name='Arial', font_size=16*ui_scale, x=x+40*ui_scale, y=row_y, batch=batch, group=self.group_content)
            l_name.bold = True
            self.elements.append(l_name)

            # 2. Score Pills (Niebieski/Czerwony)
            pill_w = 160 * ui_scale
            pill_h = 24 * ui_scale
            pill_x = x + w - 300 * ui_scale # Pozycja pigułki

            # Chips (Niebieski)
            chips_rect = shapes.Rectangle(pill_x, row_y - 8*ui_scale, pill_w/2, pill_h, color=consts.COLOR_CHIPS, batch=batch, group=self.group_content)
            l_chips = pyglet.text.Label(str(c), font_name='Arial', font_size=14*ui_scale, x=pill_x + pill_w/4, y=row_y + 4*ui_scale, anchor_x='center', anchor_y='center', batch=batch, group=self.group_top)
            l_chips.bold = True

            # Mult (Czerwony)
            mult_rect = shapes.Rectangle(pill_x + pill_w/2, row_y - 8*ui_scale, pill_w/2, pill_h, color=consts.COLOR_MULT, batch=batch, group=self.group_content)
            l_mult = pyglet.text.Label(str(m), font_name='Arial', font_size=14*ui_scale, x=pill_x + 3*pill_w/4, y=row_y + 4*ui_scale, anchor_x='center', anchor_y='center', batch=batch, group=self.group_top)
            l_mult.bold = True

            # "X"
            l_x = pyglet.text.Label("X", font_name='Arial', font_size=10*ui_scale, x=pill_x + pill_w/2, y=row_y+4*ui_scale, anchor_x='center', anchor_y='center', color=(0,0,0,255), batch=batch, group=self.group_top)
            l_x.bold = True

            self.elements.extend([chips_rect, mult_rect, l_chips, l_mult, l_x])

            # 3. Statystyki Użycia (#)
            stat_x = x + w - 80 * ui_scale
            stat_bg = shapes.Rectangle(stat_x, row_y - 8*ui_scale, 50*ui_scale, pill_h, color=(30,30,30), batch=batch, group=self.group_content)
            l_stat = pyglet.text.Label("# 0", font_name='Arial', font_size=14*ui_scale, x=stat_x + 25*ui_scale, y=row_y+4*ui_scale, anchor_x='center', anchor_y='center', color=(255,200,50,255), batch=batch, group=self.group_top)
            l_stat.bold = True

            self.elements.extend([stat_bg, l_stat])
            self.stat_labels[hand] = l_stat

        # Przycisk WSTECZ
        btn_w = 200 * ui_scale
        self.btn_back = Button("WSTECZ", x + w/2 - btn_w/2, y + 30*ui_scale, btn_w, 50*ui_scale, consts.BTN_COLOR_SORT, self.close_window, batch, self.group_content, font_size=20*ui_scale)
        self.elements.append(self.btn_back)

        self.set_visible(False)

    def close_window(self):
        self.set_visible(False)

    def update_stats(self, stats_dict):
        """Aktualizuje liczniki # użycia układów"""
        for hand, label in self.stat_labels.items():
            val = stats_dict.get(hand, 0)
            label.text = f"# {val}"

    def set_visible(self, val):
        self.visible = val
        for el in self.elements:
            if isinstance(el, Button): el.set_visible(val)
            else: el.batch = self.batch if val else None

    def check_click(self, x, y):
        if self.visible:
            return self.btn_back.check_click(x, y)
        return False

    def check_hover(self, x, y):
        if self.visible:
            self.btn_back.check_hover(x, y)

# --- GAME OVER OVERLAY ---
class GameOverOverlay:
    def __init__(self, window_w, window_h, batch, ui_scale, restart_func):
        self.group = pyglet.graphics.Group(order=2000)
        self.elements = []
        self.visible = False

        bg = shapes.Rectangle(0, 0, window_w, window_h, color=(0,0,0), batch=batch, group=self.group)
        bg.opacity = 0
        self.bg = bg
        self.elements.append(bg)

        # FIX: bold usunięte
        self.lbl_title = pyglet.text.Label("", font_name='Arial', font_size=50*ui_scale, x=window_w/2, y=window_h/2+50*ui_scale, anchor_x='center', batch=batch, group=pyglet.graphics.Group(order=2001))
        self.lbl_title.bold = True
        self.elements.append(self.lbl_title)

        self.btn_restart = Button("ZAGRAJ PONOWNIE", window_w/2-150*ui_scale, window_h/2-80*ui_scale, 300*ui_scale, 80*ui_scale, consts.BTN_COLOR_PLAY, restart_func, batch, pyglet.graphics.Group(order=2001), font_size=24*ui_scale)
        self.elements.append(self.btn_restart)
        self.set_visible(False)

    def set_visible(self, val):
        self.visible = val
        for el in self.elements:
            if isinstance(el, Button): el.set_visible(val)
            else: el.batch = self.bg.batch if val else None

    def show(self, won):
        self.set_visible(True)
        self.bg.opacity = 200
        self.lbl_title.text = "WYGRANA!" if won else "GAME OVER"
        self.lbl_title.color = consts.COLOR_MONEY+(255,) if won else consts.BTN_COLOR_DISCARD+(255,)

    def hide(self): self.set_visible(False)
    def check_click(self, x, y): return self.btn_restart.check_click(x, y) if self.visible else False
    def check_hover(self, x, y):
        if self.visible: self.btn_restart.check_hover(x, y)