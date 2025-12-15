import pyglet
from pyglet import shapes
import config.consts as consts
from ui.ui import Button, ScorePill
from ui.overlays import HandHierarchyPopup, GameOverOverlay

class GameUIManager:
    """Zarządzanie interfejsem w trybie gry"""

    def __init__(self, window, batch, game_state, callbacks):
        self.window = window
        self.batch = batch
        self.state = game_state
        self.callbacks = callbacks
        self.ui_scale = 1.0
        self.elements = []
        self.buttons = []

        # Grupy renderowania
        self.grp_sidebar = pyglet.graphics.Group(order=10)
        self.grp_sidebar_ui = pyglet.graphics.Group(order=20)
        self.grp_ui = pyglet.graphics.Group(order=100)

        # Overlaye
        self.popup_info = HandHierarchyPopup(window.width, window.height, batch, 1.0, self.close_popup)
        self.overlay_gameover = GameOverOverlay(window.width, window.height, batch, 1.0, callbacks['restart_game'])

        self.rebuild_layout()

    def close_popup(self):
        self.popup_info.set_visible(False)

    def rebuild_layout(self):
        """Przebudowa UI po zmianie rozmiaru okna"""
        # Czyszczenie
        for el in self.elements:
            el.delete()
        self.elements.clear()

        for b in self.buttons:
            b.delete()
        self.buttons.clear()

        # Obliczenia skali
        s = self.window.height / 720.0
        self.ui_scale = s
        sidebar_w = 300 * s
        margin = 15 * s
        curr_y = self.window.height - margin

        # Sidebar
        self.elements.append(shapes.Rectangle(0, 0, sidebar_w, self.window.height, color=consts.SIDEBAR_BG, batch=self.batch, group=self.grp_sidebar))

        # 1. RUNDA
        panel_h = 180 * s
        curr_y -= panel_h
        self.elements.append(shapes.BorderedRectangle(margin, curr_y, sidebar_w-2*margin, panel_h, border=3, color=consts.PANEL_BG_DARK, border_color=consts.PANEL_BORDER, batch=self.batch, group=self.grp_sidebar_ui))

        self.lbl_target = pyglet.text.Label(f"Cel: {self.state.target_score}", font_name='Arial', font_size=20*s, x=sidebar_w/2, y=curr_y+panel_h-40*s, anchor_x='center', color=(255, 100, 100, 255), batch=self.batch, group=pyglet.graphics.Group(order=21))
        self.lbl_target.bold = True

        self.lbl_round_score = pyglet.text.Label(f"{self.state.round_score}", font_name='Arial', font_size=32*s, x=sidebar_w/2, y=curr_y+60*s, anchor_x='center', batch=self.batch, group=pyglet.graphics.Group(order=21))
        self.lbl_round_score.bold = True

        self.elements.extend([self.lbl_target, self.lbl_round_score])
        curr_y -= 20 * s

        # 2. PUNKTACJA
        self.score_pill = ScorePill(margin, curr_y-100*s, sidebar_w-2*margin, self.batch, self.grp_sidebar_ui, s)
        self.elements.append(self.score_pill)
        curr_y -= 140 * s

        # 3. STATYSTYKI
        stats_h = 160 * s
        curr_y -= stats_h
        self.elements.append(shapes.BorderedRectangle(margin, curr_y, sidebar_w-2*margin, stats_h, border=3, color=consts.PANEL_BG_DARK, border_color=consts.PANEL_BORDER, batch=self.batch, group=self.grp_sidebar_ui))

        lbl_h_title = pyglet.text.Label("RĘCE", font_name='Arial', font_size=12*s, x=margin+40*s, y=curr_y+stats_h-30*s, anchor_x='center', color=(180,180,180,255), batch=self.batch, group=pyglet.graphics.Group(order=21))
        lbl_h_title.bold = True

        self.lbl_hands_val = pyglet.text.Label(str(self.state.hands_left), font_name='Arial', font_size=28*s, x=margin+40*s, y=curr_y+stats_h-60*s, anchor_x='center', color=consts.BTN_COLOR_PLAY+(255,), batch=self.batch, group=pyglet.graphics.Group(order=21))
        self.lbl_hands_val.bold = True

        lbl_d_title = pyglet.text.Label("ZRZUTKI", font_name='Arial', font_size=12*s, x=sidebar_w-margin-40*s, y=curr_y+stats_h-30*s, anchor_x='center', color=(180,180,180,255), batch=self.batch, group=pyglet.graphics.Group(order=21))
        lbl_d_title.bold = True

        self.lbl_discards_val = pyglet.text.Label(str(self.state.discards_left), font_name='Arial', font_size=28*s, x=sidebar_w-margin-40*s, y=curr_y+stats_h-60*s, anchor_x='center', color=consts.BTN_COLOR_DISCARD+(255,), batch=self.batch, group=pyglet.graphics.Group(order=21))
        self.lbl_discards_val.bold = True

        self.lbl_money = pyglet.text.Label(f"${self.state.money}", font_name='Arial', font_size=28*s, x=sidebar_w/2, y=curr_y+40*s, anchor_x='center', color=consts.COLOR_MONEY+(255,), batch=self.batch, group=pyglet.graphics.Group(order=21))
        self.lbl_money.bold = True

        self.lbl_round_num = pyglet.text.Label(f"Runda: {self.state.round_num}", font_name='Arial', font_size=12*s, x=sidebar_w/2, y=curr_y+10*s, anchor_x='center', color=(150,150,150,255), batch=self.batch, group=pyglet.graphics.Group(order=21))

        self.elements.extend([lbl_h_title, self.lbl_hands_val, lbl_d_title, self.lbl_discards_val, self.lbl_money, self.lbl_round_num])

        # 4. PRZYCISKI
        btn_h = 50 * s
        curr_y -= (btn_h + 20*s)
        self.buttons.append(Button("Podejście Info", margin, curr_y, sidebar_w-2*margin, btn_h, consts.BTN_COLOR_INFO, self.callbacks['toggle_info_popup'], self.batch, self.grp_sidebar_ui, font_size=16*s))

        curr_y -= (btn_h + 10*s)
        self.buttons.append(Button("Opcje", margin, curr_y, sidebar_w-2*margin, btn_h, consts.BTN_COLOR_SORT, self.callbacks['open_options'], self.batch, self.grp_sidebar_ui, font_size=16*s))

        # Przyciski gry
        cx = sidebar_w + (self.window.width-sidebar_w)/2
        by = 50 * s
        bw, bh = 160*s, 60*s

        self.buttons.append(Button("ZAGRAJ", cx+20*s, by, bw, bh, consts.BTN_COLOR_PLAY, self.callbacks['play_hand'], self.batch, self.grp_ui, font_size=22*s))
        self.buttons.append(Button("ODRZUĆ", cx-bw-20*s, by, bw, bh, consts.BTN_COLOR_DISCARD, self.callbacks['discard_hand'], self.batch, self.grp_ui, font_size=22*s))

        bs_w, bs_h, bs_y = 100*s, 40*s, by+bh+20*s
        self.buttons.append(Button("Ranga", cx-bs_w-10*s, bs_y, bs_w, bs_h, consts.BTN_COLOR_SORT, self.callbacks['sort_rank'], self.batch, self.grp_ui, font_size=14*s))
        self.buttons.append(Button("Kolor", cx+10*s, bs_y, bs_w, bs_h, consts.BTN_COLOR_SORT, self.callbacks['sort_suit'], self.batch, self.grp_ui, font_size=14*s))

    def update_values(self):
        """Aktualizacja wartości na UI"""
        self.lbl_target.text = f"Cel: {self.state.target_score}"
        self.lbl_round_score.text = str(self.state.round_score)
        self.lbl_hands_val.text = str(self.state.hands_left)
        self.lbl_discards_val.text = str(self.state.discards_left)
        self.lbl_money.text = f"${self.state.money}"
        self.lbl_round_num.text = f"Runda: {self.state.round_num}"

    def update_preview(self, name, chips, mult):
        """Aktualizacja podglądu wyniku"""
        self.score_pill.update(chips, mult, name)
