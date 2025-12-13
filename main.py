import pyglet
from pyglet import shapes
from pyglet.window import key
import sys

import consts
from background import ShaderBackground
from card import Card
from menu import MainMenu
from options import OptionsMenu
from ui import Button, ScorePill, HandHierarchyPopup, GameOverOverlay
from game_logic import Deck, HandEvaluator

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
window = pyglet.window.Window(caption="Blind Bet", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, resizable=True, fullscreen=consts.settings.fullscreen, vsync=consts.settings.vsync, visible=False)

if not consts.settings.fullscreen:
    s = window.display.get_default_screen()
    window.set_location(max(0, (s.width-WINDOW_WIDTH)//2), max(0, (s.height-WINDOW_HEIGHT)//2))
window.set_visible(True)

menu_batch, game_batch, options_batch = pyglet.graphics.Batch(), pyglet.graphics.Batch(), pyglet.graphics.Batch()
grp_sidebar = pyglet.graphics.Group(order=10)
grp_sidebar_ui = pyglet.graphics.Group(order=20)
grp_cards, grp_ui = pyglet.graphics.Group(order=50), pyglet.graphics.Group(order=100)

current_state, is_options_open = consts.STATE_MENU, False
deck, my_hand = Deck(), []
MAX_HAND_SIZE = 8
hands_left, discards_left, round_score, target_score, money, round_num = 4, 3, 0, 300, 4, 1

# Statystyki użycia układów
hand_stats = {k: 0 for k in consts.HAND_SCORES.keys()}

class GameUIManager:
    def __init__(self, window, batch):
        self.window, self.batch = window, batch
        self.ui_scale = 1.0
        self.elements = []
        self.buttons = []
        # Przekazujemy funkcję zamykającą
        self.popup_info = HandHierarchyPopup(window.width, window.height, batch, 1.0, self.close_popup)
        self.overlay_gameover = GameOverOverlay(window.width, window.height, batch, 1.0, restart_game)
        self.rebuild_layout()

    def close_popup(self):
        self.popup_info.set_visible(False)

    def rebuild_layout(self):
        for el in self.elements: el.delete()
        self.elements.clear()
        for b in self.buttons: b.delete()
        self.buttons.clear()

        s = self.window.height / 720.0; self.ui_scale = s
        sidebar_w = 300 * s
        margin = 15 * s; curr_y = self.window.height - margin

        self.elements.append(shapes.Rectangle(0, 0, sidebar_w, self.window.height, color=consts.SIDEBAR_BG, batch=self.batch, group=grp_sidebar))

        # 1. RUNDA
        panel_h = 180 * s; curr_y -= panel_h
        self.elements.append(shapes.BorderedRectangle(margin, curr_y, sidebar_w-2*margin, panel_h, border=3, color=consts.PANEL_BG_DARK, border_color=consts.PANEL_BORDER, batch=self.batch, group=grp_sidebar_ui))

        self.lbl_target = pyglet.text.Label(f"Cel: {target_score}", font_name='Arial', font_size=20*s, x=sidebar_w/2, y=curr_y+panel_h-40*s, anchor_x='center', color=(255, 100, 100, 255), batch=self.batch, group=pyglet.graphics.Group(order=21))
        self.lbl_target.bold = True

        self.lbl_round_score = pyglet.text.Label(f"{round_score}", font_name='Arial', font_size=32*s, x=sidebar_w/2, y=curr_y+60*s, anchor_x='center', batch=self.batch, group=pyglet.graphics.Group(order=21))
        self.lbl_round_score.bold = True

        self.elements.extend([self.lbl_target, self.lbl_round_score])
        curr_y -= 20 * s

        # 2. PUNKTACJA
        self.score_pill = ScorePill(margin, curr_y-100*s, sidebar_w-2*margin, self.batch, grp_sidebar_ui, s)
        self.elements.append(self.score_pill)
        curr_y -= 140 * s

        # 3. STATYSTYKI
        stats_h = 160 * s; curr_y -= stats_h
        self.elements.append(shapes.BorderedRectangle(margin, curr_y, sidebar_w-2*margin, stats_h, border=3, color=consts.PANEL_BG_DARK, border_color=consts.PANEL_BORDER, batch=self.batch, group=grp_sidebar_ui))

        lbl_h_title = pyglet.text.Label("RĘCE", font_name='Arial', font_size=12*s, x=margin+40*s, y=curr_y+stats_h-30*s, anchor_x='center', color=(180,180,180,255), batch=self.batch, group=pyglet.graphics.Group(order=21))
        lbl_h_title.bold = True

        self.lbl_hands_val = pyglet.text.Label(str(hands_left), font_name='Arial', font_size=28*s, x=margin+40*s, y=curr_y+stats_h-60*s, anchor_x='center', color=consts.BTN_COLOR_PLAY+(255,), batch=self.batch, group=pyglet.graphics.Group(order=21))
        self.lbl_hands_val.bold = True

        lbl_d_title = pyglet.text.Label("ZRZUTKI", font_name='Arial', font_size=12*s, x=sidebar_w-margin-40*s, y=curr_y+stats_h-30*s, anchor_x='center', color=(180,180,180,255), batch=self.batch, group=pyglet.graphics.Group(order=21))
        lbl_d_title.bold = True

        self.lbl_discards_val = pyglet.text.Label(str(discards_left), font_name='Arial', font_size=28*s, x=sidebar_w-margin-40*s, y=curr_y+stats_h-60*s, anchor_x='center', color=consts.BTN_COLOR_DISCARD+(255,), batch=self.batch, group=pyglet.graphics.Group(order=21))
        self.lbl_discards_val.bold = True

        self.lbl_money = pyglet.text.Label(f"${money}", font_name='Arial', font_size=28*s, x=sidebar_w/2, y=curr_y+40*s, anchor_x='center', color=consts.COLOR_MONEY+(255,), batch=self.batch, group=pyglet.graphics.Group(order=21))
        self.lbl_money.bold = True

        self.lbl_round_num = pyglet.text.Label(f"Runda: {round_num}", font_name='Arial', font_size=12*s, x=sidebar_w/2, y=curr_y+10*s, anchor_x='center', color=(150,150,150,255), batch=self.batch, group=pyglet.graphics.Group(order=21))

        self.elements.extend([lbl_h_title, self.lbl_hands_val, lbl_d_title, self.lbl_discards_val, self.lbl_money, self.lbl_round_num])

        # 4. PRZYCISKI
        btn_h = 50 * s; curr_y -= (btn_h + 20*s)
        self.buttons.append(Button("Podejście Info", margin, curr_y, sidebar_w-2*margin, btn_h, consts.BTN_COLOR_INFO, toggle_info_popup, self.batch, grp_sidebar_ui, font_size=16*s))
        curr_y -= (btn_h + 10*s)
        self.buttons.append(Button("Opcje", margin, curr_y, sidebar_w-2*margin, btn_h, consts.BTN_COLOR_SORT, open_options, self.batch, grp_sidebar_ui, font_size=16*s))

        cx = sidebar_w + (self.window.width-sidebar_w)/2; by = 50 * s; bw, bh = 160*s, 60*s
        self.buttons.append(Button("ZAGRAJ", cx+20*s, by, bw, bh, consts.BTN_COLOR_PLAY, play_hand, self.batch, grp_ui, font_size=22*s))
        self.buttons.append(Button("ODRZUĆ", cx-bw-20*s, by, bw, bh, consts.BTN_COLOR_DISCARD, discard_hand, self.batch, grp_ui, font_size=22*s))

        bs_w, bs_h, bs_y = 100*s, 40*s, by+bh+20*s
        self.buttons.append(Button("Ranga", cx-bs_w-10*s, bs_y, bs_w, bs_h, consts.BTN_COLOR_SORT, sort_rank, self.batch, grp_ui, font_size=14*s))
        self.buttons.append(Button("Kolor", cx+10*s, bs_y, bs_w, bs_h, consts.BTN_COLOR_SORT, sort_suit, self.batch, grp_ui, font_size=14*s))

    def update_values(self):
        self.lbl_target.text = f"Cel: {target_score}"; self.lbl_round_score.text = str(round_score)
        self.lbl_hands_val.text = str(hands_left); self.lbl_discards_val.text = str(discards_left)
        self.lbl_money.text = f"${money}"; self.lbl_round_num.text = f"Runda: {round_num}"
    def update_preview(self, name, chips, mult): self.score_pill.update(chips, mult, name)

ui_manager = None

def toggle_info_popup():
    if ui_manager:
        # Przekazujemy statystyki przed pokazaniem
        ui_manager.popup_info.update_stats(hand_stats)
        ui_manager.popup_info.set_visible(True)

def sort_rank(): my_hand.sort(key=lambda c: c.rank_val, reverse=True); recalculate_layout()
def sort_suit(): my_hand.sort(key=lambda c: (c.suit, c.rank_val)); recalculate_layout()

def draw_cards(count):
    for _ in range(count):
        if deck.remaining() > 0:
            c_data = deck.draw(1)[0]
            my_hand.append(Card(c_data[0], c_data[1], window.width//2, window.height//2, game_batch, grp_cards))
    recalculate_layout()

def play_hand():
    global hands_left, round_score
    selected = [c for c in my_hand if c.is_selected]
    if not selected or len(selected) > 5 or hands_left <= 0: return
    n, c, m, t = HandEvaluator.evaluate(selected)

    # Aktualizacja statystyk
    if n in hand_stats: hand_stats[n] += 1

    round_score += t; hands_left -= 1
    for c in selected: c.delete(); my_hand.remove(c)
    draw_cards(MAX_HAND_SIZE - len(my_hand))
    ui_manager.update_values()
    check_game_end()

def discard_hand():
    global discards_left
    selected = [c for c in my_hand if c.is_selected]
    if not selected or len(selected) > 5 or discards_left <= 0: return
    discards_left -= 1
    for c in selected: c.delete(); my_hand.remove(c)
    draw_cards(MAX_HAND_SIZE - len(my_hand))
    ui_manager.update_values()

def check_game_end():
    global money, round_num, target_score, round_score, hands_left, discards_left, current_state
    if round_score >= target_score:
        money += 5; round_num += 1; round_score = 0; target_score = int(target_score * 1.5)
        hands_left, discards_left = 4, 3
        deck.reset();
        for c in my_hand: c.delete()
        my_hand.clear(); draw_cards(MAX_HAND_SIZE)
        ui_manager.update_values()
    elif hands_left <= 0:
        current_state = consts.STATE_GAME_OVER
        ui_manager.overlay_gameover.show(False)

def restart_game():
    global hands_left, discards_left, round_score, target_score, money, round_num, current_state
    hands_left, discards_left, round_score, target_score, money, round_num = 4, 3, 0, 300, 4, 1

    # Reset stats
    for k in hand_stats: hand_stats[k] = 0

    deck.reset();
    for c in my_hand: c.delete()
    my_hand.clear()
    ui_manager.overlay_gameover.hide()
    current_state = consts.STATE_GAME
    draw_cards(MAX_HAND_SIZE); ui_manager.update_values()

def start_game():
    global current_state, ui_manager
    current_state = consts.STATE_GAME
    ui_manager = GameUIManager(window, game_batch)
    restart_game()

def recalculate_layout(dt=None):
    if current_state != consts.STATE_GAME: return
    s = ui_manager.ui_scale; sidebar_w = 300 * s
    cx = sidebar_w + (window.width - sidebar_w)/2; cy = window.height/2

    # --- POPRAWKA CENTROWANIA KART NA START ---
    # 1. Najpierw aktualizujemy skalę, żeby znać prawdziwą szerokość
    for c in my_hand: c.update_scale(window.width, window.height)

    # 2. Teraz obliczamy szerokość wachlarza
    card_width = my_hand[0].sprite.width if my_hand else 0
    total_w = len(my_hand) * (card_width * 0.7)

    start_x = cx - total_w/2 + (card_width * 0.15) # Lekka korekta

    for i, c in enumerate(my_hand):
        tx = start_x + i * (c.sprite.width * 0.7)
        ty = cy + (30*s if c.is_selected else 0)
        c.set_target(tx, ty)
        c.sprite.group = pyglet.graphics.Group(order=80 if c.is_selected else 50+i)

background = ShaderBackground(window.width, window.height)
def open_options(): global is_options_open; is_options_open = True; options_menu.visible = True; options_menu.update_layout()
def close_options(): global is_options_open; is_options_open = False; options_menu.visible = False
def exit_game(): pyglet.app.exit()

main_menu = MainMenu(window.width, window.height, menu_batch, start_game, open_options, exit_game)
options_menu = OptionsMenu(window, options_batch, close_options)

def update(dt):
    background.update(dt, window.width, window.height)
    if current_state == consts.STATE_GAME and not is_options_open and ui_manager and not ui_manager.popup_info.visible:
        for c in my_hand: c.update(dt)
        sel = [c for c in my_hand if c.is_selected]
        n, c, m, t = HandEvaluator.evaluate(sel) if sel else ("Wybierz", 0, 0, 0)
        ui_manager.update_preview(n, c, m)

pyglet.clock.schedule_interval(update, 1/60.0)

@window.event
def on_draw():
    window.clear(); background.draw()
    if current_state == consts.STATE_MENU: menu_batch.draw()
    elif current_state in [consts.STATE_GAME, consts.STATE_GAME_OVER]: game_batch.draw()
    if is_options_open: options_batch.draw()

@window.event
def on_resize(w, h):
    background.update(0, w, h)
    if current_state == consts.STATE_MENU: main_menu.update_layout(w, h)
    if ui_manager: ui_manager.rebuild_layout(); recalculate_layout()
    options_menu.update_layout(); super(pyglet.window.Window, window).on_resize(w, h)

@window.event
def on_mouse_press(x, y, b, m):
    if is_options_open: options_menu.on_mouse_press(x, y, b, m); return
    if current_state == consts.STATE_MENU: main_menu.on_mouse_press(x, y, b, m)
    elif current_state == consts.STATE_GAME_OVER: ui_manager.overlay_gameover.check_click(x, y)
    elif current_state == consts.STATE_GAME and ui_manager:

        # Obsługa Popup Info (teraz tylko przycisk zamyka)
        if ui_manager.popup_info.visible:
            ui_manager.popup_info.check_click(x, y)
            return

        for btn in ui_manager.buttons:
            if btn.check_click(x, y): return
        for c in reversed(my_hand):
            if c.check_click(x, y): c.is_selected = not c.is_selected; recalculate_layout(); return

@window.event
def on_mouse_motion(x, y, dx, dy):
    if is_options_open: options_menu.on_mouse_motion(x, y, dx, dy); return
    if current_state == consts.STATE_MENU: main_menu.on_mouse_motion(x, y, dx, dy)
    elif current_state == consts.STATE_GAME and ui_manager:
        if ui_manager.popup_info.visible:
            ui_manager.popup_info.check_hover(x, y)
            return
        for b in ui_manager.buttons: b.check_hover(x, y)
    elif current_state == consts.STATE_GAME_OVER: ui_manager.overlay_gameover.check_hover(x, y)

@window.event
def on_key_press(symbol, modifiers):
    global current_state
    if symbol == key.ESCAPE:
        if is_options_open: close_options()
        elif ui_manager and ui_manager.popup_info.visible: ui_manager.popup_info.set_visible(False)
        elif current_state == consts.STATE_GAME: current_state = consts.STATE_MENU; main_menu.update_layout(window.width, window.height)
        else: window.close()
        return pyglet.event.EVENT_HANDLED

if __name__ == "__main__": pyglet.app.run()