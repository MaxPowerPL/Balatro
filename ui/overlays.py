import pyglet
from pyglet import shapes
import config.consts as consts
from ui.ui import Button

class HandHierarchyPopup:
    """Popup z hierarchią układów pokerowych"""

    def __init__(self, window_w, window_h, batch, ui_scale, close_func):
        self.batch = batch
        self.close_func = close_func
        self.visible = False
        self.elements = []
        self.stat_labels = {}

        w = 800 * ui_scale
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

            # Tło wiersza
            if i % 2 == 0:
                stripe = shapes.Rectangle(x+20*ui_scale, row_y-15*ui_scale, w-40*ui_scale, row_h, color=(50,50,55), batch=batch, group=self.group_bg)
                self.elements.append(stripe)

            # Nazwa
            l_name = pyglet.text.Label(consts.HAND_NAMES_PL.get(hand, hand), font_name='Arial', font_size=16*ui_scale, x=x+40*ui_scale, y=row_y, batch=batch, group=self.group_content)
            l_name.bold = True
            self.elements.append(l_name)

            # Score Pills
            pill_w = 160 * ui_scale
            pill_h = 24 * ui_scale
            pill_x = x + w - 300 * ui_scale

            # Chips
            chips_rect = shapes.Rectangle(pill_x, row_y - 8*ui_scale, pill_w/2, pill_h, color=consts.COLOR_CHIPS, batch=batch, group=self.group_content)
            l_chips = pyglet.text.Label(str(c), font_name='Arial', font_size=14*ui_scale, x=pill_x + pill_w/4, y=row_y + 4*ui_scale, anchor_x='center', anchor_y='center', batch=batch, group=self.group_top)
            l_chips.bold = True

            # Mult
            mult_rect = shapes.Rectangle(pill_x + pill_w/2, row_y - 8*ui_scale, pill_w/2, pill_h, color=consts.COLOR_MULT, batch=batch, group=self.group_content)
            l_mult = pyglet.text.Label(str(m), font_name='Arial', font_size=14*ui_scale, x=pill_x + 3*pill_w/4, y=row_y + 4*ui_scale, anchor_x='center', anchor_y='center', batch=batch, group=self.group_top)
            l_mult.bold = True

            # "X"
            l_x = pyglet.text.Label("X", font_name='Arial', font_size=10*ui_scale, x=pill_x + pill_w/2, y=row_y+4*ui_scale, anchor_x='center', anchor_y='center', color=(0,0,0,255), batch=batch, group=self.group_top)
            l_x.bold = True

            self.elements.extend([chips_rect, mult_rect, l_chips, l_mult, l_x])

            # Statystyki
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
        """Aktualizuje liczniki użycia układów"""
        for hand, label in self.stat_labels.items():
            val = stats_dict.get(hand, 0)
            label.text = f"# {val}"

    def set_visible(self, val):
        self.visible = val
        for el in self.elements:
            if isinstance(el, Button):
                el.set_visible(val)
            else:
                el.batch = self.batch if val else None

    def check_click(self, x, y):
        if self.visible:
            return self.btn_back.check_click(x, y)
        return False

    def check_hover(self, x, y):
        if self.visible:
            self.btn_back.check_hover(x, y)


class GameOverOverlay:
    """Nakładka Game Over"""

    def __init__(self, window_w, window_h, batch, ui_scale, restart_func):
        self.group = pyglet.graphics.Group(order=2000)
        self.elements = []
        self.visible = False

        bg = shapes.Rectangle(0, 0, window_w, window_h, color=(0,0,0), batch=batch, group=self.group)
        bg.opacity = 0
        self.bg = bg
        self.elements.append(bg)

        self.lbl_title = pyglet.text.Label("", font_name='Arial', font_size=50*ui_scale, x=window_w/2, y=window_h/2+50*ui_scale, anchor_x='center', batch=batch, group=pyglet.graphics.Group(order=2001))
        self.lbl_title.bold = True
        self.elements.append(self.lbl_title)

        self.btn_restart = Button("ZAGRAJ PONOWNIE", window_w/2-150*ui_scale, window_h/2-80*ui_scale, 300*ui_scale, 80*ui_scale, consts.BTN_COLOR_PLAY, restart_func, batch, pyglet.graphics.Group(order=2001), font_size=24*ui_scale)
        self.elements.append(self.btn_restart)

        self.set_visible(False)

    def set_visible(self, val):
        self.visible = val
        for el in self.elements:
            if isinstance(el, Button):
                el.set_visible(val)
            else:
                el.batch = self.bg.batch if val else None

    def show(self, won):
        self.set_visible(True)
        self.bg.opacity = 200
        self.lbl_title.text = "WYGRANA!" if won else "GAME OVER"
        self.lbl_title.color = consts.COLOR_MONEY+(255,) if won else consts.BTN_COLOR_DISCARD+(255,)

    def hide(self):
        self.set_visible(False)

    def check_click(self, x, y):
        return self.btn_restart.check_click(x, y) if self.visible else False

    def check_hover(self, x, y):
        if self.visible:
            self.btn_restart.check_hover(x, y)
