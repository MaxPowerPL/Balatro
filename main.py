import pyglet
from pyglet.window import key

import config.consts as consts
from ui.background import ShaderBackground
from ui.menu import MainMenu
from ui.options import OptionsMenu
from ui.game_ui_manager import GameUIManager
from core.game_state import GameState
from core.game_manager import GameManager
from core.game_logic import HandEvaluator

# Inicjalizacja okna
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
window = pyglet.window.Window(
    caption="Blind Bet",
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    resizable=True,
    fullscreen=consts.settings.fullscreen,
    vsync=consts.settings.vsync,
    visible=False
)

# Centrowanie okna
if not consts.settings.fullscreen:
    s = window.display.get_default_screen()
    window.set_location(
        max(0, (s.width - WINDOW_WIDTH) // 2),
        max(0, (s.height - WINDOW_HEIGHT) // 2)
    )
window.set_visible(True)

# Batche i grupy
menu_batch = pyglet.graphics.Batch()
game_batch = pyglet.graphics.Batch()
options_batch = pyglet.graphics.Batch()
grp_cards = pyglet.graphics.Group(order=50)

# Stan gry
game_state = GameState()
game_manager = None
ui_manager = None
background = ShaderBackground(window.width, window.height)

# Funkcje callbacków
def toggle_info_popup():
    if ui_manager:
        ui_manager.popup_info.update_stats(game_state.hand_stats)
        ui_manager.popup_info.set_visible(True)

def sort_rank():
    if game_manager:
        game_manager.sort_by_rank()
        recalculate_layout()

def sort_suit():
    if game_manager:
        game_manager.sort_by_suit()
        recalculate_layout()

def play_hand():
    if game_manager and ui_manager:
        if game_manager.play_hand(ui_manager):
            recalculate_layout()
            game_manager.check_game_end(ui_manager)

def discard_hand():
    if game_manager and ui_manager:
        if game_manager.discard_hand(ui_manager):
            recalculate_layout()

def check_game_end():
    if game_manager and ui_manager:
        game_manager.check_game_end(ui_manager)

def restart_game():
    global game_manager, ui_manager

    game_state.reset_game()
    game_manager.deck.reset()

    for c in game_state.my_hand:
        c.delete()
    game_state.my_hand.clear()

    if ui_manager:
        ui_manager.overlay_gameover.hide()

    game_state.current_state = consts.STATE_GAME
    game_manager.draw_cards(game_state.MAX_HAND_SIZE)
    ui_manager.update_values()
    recalculate_layout()

def start_game():
    global game_manager, ui_manager

    game_state.current_state = consts.STATE_GAME

    # Słownik callbacków dla UI
    callbacks = {
        'toggle_info_popup': toggle_info_popup,
        'open_options': open_options,
        'play_hand': play_hand,
        'discard_hand': discard_hand,
        'sort_rank': sort_rank,
        'sort_suit': sort_suit,
        'restart_game': restart_game
    }

    ui_manager = GameUIManager(window, game_batch, game_state, callbacks)
    game_manager = GameManager(game_state, window, game_batch, grp_cards)

    restart_game()

def recalculate_layout(dt=None):
    if game_state.current_state != consts.STATE_GAME or not ui_manager:
        return

    s = ui_manager.ui_scale
    sidebar_w = 300 * s
    cx = sidebar_w + (window.width - sidebar_w) / 2
    cy = window.height / 2

    # Aktualizacja skali kart
    for c in game_state.my_hand:
        c.update_scale(window.width, window.height)

    # Obliczanie szerokości wachlarza
    card_width = game_state.my_hand[0].sprite.width if game_state.my_hand else 0
    total_w = len(game_state.my_hand) * (card_width * 0.7)
    start_x = cx - total_w / 2 + (card_width * 0.15)

    for i, c in enumerate(game_state.my_hand):
        tx = start_x + i * (c.sprite.width * 0.7)
        ty = cy + (30 * s if c.is_selected else 0)
        c.set_target(tx, ty)
        c.sprite.group = pyglet.graphics.Group(order=80 if c.is_selected else 50 + i)

def open_options():
    game_state.is_options_open = True
    options_menu.visible = True
    options_menu.update_layout()

def close_options():
    game_state.is_options_open = False
    options_menu.visible = False

def exit_game():
    pyglet.app.exit()

# Menu
main_menu = MainMenu(window.width, window.height, menu_batch, start_game, open_options, exit_game)
options_menu = OptionsMenu(window, options_batch, close_options)

# Update loop
def update(dt):
    background.update(dt, window.width, window.height)

    if (game_state.current_state == consts.STATE_GAME and
        not game_state.is_options_open and ui_manager and
        not ui_manager.popup_info.visible):

        for c in game_state.my_hand:
            c.update(dt)

        # Aktualizacja podglądu
        selected = [c for c in game_state.my_hand if c.is_selected]
        if selected:
            n, c, m, t = HandEvaluator.evaluate(selected)
            ui_manager.update_preview(n, c, m)
        else:
            ui_manager.update_preview("Wybierz", 0, 0)

pyglet.clock.schedule_interval(update, 1/60.0)

# Event handlery
@window.event
def on_draw():
    window.clear()
    background.draw()

    if game_state.current_state == consts.STATE_MENU:
        menu_batch.draw()
    elif game_state.current_state in [consts.STATE_GAME, consts.STATE_GAME_OVER]:
        game_batch.draw()

    if game_state.is_options_open:
        options_batch.draw()

@window.event
def on_resize(w, h):
    background.update(0, w, h)

    if game_state.current_state == consts.STATE_MENU:
        main_menu.update_layout(w, h)

    if ui_manager:
        ui_manager.rebuild_layout()
        recalculate_layout()

    options_menu.update_layout()
    super(pyglet.window.Window, window).on_resize(w, h)

@window.event
def on_mouse_press(x, y, b, m):
    if game_state.is_options_open:
        options_menu.on_mouse_press(x, y, b, m)
        return

    if game_state.current_state == consts.STATE_MENU:
        main_menu.on_mouse_press(x, y, b, m)

    elif game_state.current_state == consts.STATE_GAME_OVER:
        if ui_manager:
            ui_manager.overlay_gameover.check_click(x, y)

    elif game_state.current_state == consts.STATE_GAME and ui_manager:
        # Obsługa Popup Info
        if ui_manager.popup_info.visible:
            ui_manager.popup_info.check_click(x, y)
            return

        # Obsługa przycisków
        for btn in ui_manager.buttons:
            if btn.check_click(x, y):
                return

        # Obsługa kart
        for c in reversed(game_state.my_hand):
            if c.check_click(x, y):
                c.is_selected = not c.is_selected
                recalculate_layout()
                return

@window.event
def on_mouse_motion(x, y, dx, dy):
    if game_state.is_options_open:
        options_menu.on_mouse_motion(x, y, dx, dy)
        return

    if game_state.current_state == consts.STATE_MENU:
        main_menu.on_mouse_motion(x, y, dx, dy)

    elif game_state.current_state == consts.STATE_GAME and ui_manager:
        if ui_manager.popup_info.visible:
            ui_manager.popup_info.check_hover(x, y)
            return

        for b in ui_manager.buttons:
            b.check_hover(x, y)

    elif game_state.current_state == consts.STATE_GAME_OVER and ui_manager:
        ui_manager.overlay_gameover.check_hover(x, y)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.ESCAPE:
        if game_state.is_options_open:
            close_options()
        elif ui_manager and ui_manager.popup_info.visible:
            ui_manager.popup_info.set_visible(False)
        elif game_state.current_state == consts.STATE_GAME:
            game_state.current_state = consts.STATE_MENU
            main_menu.update_layout(window.width, window.height)
        else:
            window.close()
        return pyglet.event.EVENT_HANDLED

if __name__ == "__main__":
    pyglet.app.run()
