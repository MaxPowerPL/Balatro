import pyglet
from pyglet.window import key
import sys

import consts
from background import ShaderBackground
from card import Card
from menu import MainMenu
from options import OptionsMenu

window = pyglet.window.Window(
    caption="Blind Bet",
    resizable=True,
    fullscreen=consts.settings.fullscreen,
    vsync=True
)

# Batche
menu_batch = pyglet.graphics.Batch()
game_batch = pyglet.graphics.Batch()
options_batch = pyglet.graphics.Batch()

cards_group = pyglet.graphics.Group(order=1)
ui_group = pyglet.graphics.Group(order=2)

current_state = consts.STATE_MENU
is_options_open = False

# --- FUNKCJE STERUJĄCE ---
def start_game():
    global current_state
    if is_options_open: return
    current_state = consts.STATE_GAME
    recalculate_game_layout()

def open_options():
    global is_options_open
    print("Otwieram opcje...")
    is_options_open = True
    options_menu.visible = True
    # Wymuszamy przeliczenie pozycji przy otwarciu (dla pewności)
    options_menu.update_layout()

def close_options():
    global is_options_open
    print("Zamykam opcje...")
    is_options_open = False
    options_menu.visible = False

def exit_game():
    if is_options_open: return
    pyglet.app.exit()

# --- INICJALIZACJA ---
background = ShaderBackground(window.width, window.height)

main_menu = MainMenu(window.width, window.height, menu_batch, start_game, open_options, exit_game)
options_menu = OptionsMenu(window, options_batch, close_options)

my_hand = []
hand_data = ['pik_as', 'kier_krol', 'trefl_10', 'karo_2', 'BACK']
for card_name in hand_data:
    new_card = Card(card_name, 0, 0, game_batch, cards_group)
    my_hand.append(new_card)

game_label = pyglet.text.Label(
    'Kliknij kartę | ESC - powrót do menu', font_name='Arial', font_size=24,
    x=window.width//2, y=window.height - 50,
    anchor_x='center', anchor_y='center',
    batch=game_batch, group=ui_group
)

def recalculate_game_layout(dt=None):
    if current_state != consts.STATE_GAME: return
    screen_w, screen_h = window.width, window.height
    for card in my_hand: card.update_scale(screen_w, screen_h)

    current_card_width = my_hand[0].sprite.width
    spacing = current_card_width * 1.1
    start_x = (screen_w / 2) - (len(my_hand) * spacing) / 2 + (spacing / 2)
    base_y = screen_h * 0.3

    for i, card in enumerate(my_hand):
        target_x = start_x + (i * spacing)
        card.set_position(target_x, base_y)
        card.target_y = base_y + 50 if card.is_selected else base_y

    game_label.x = screen_w // 2; game_label.y = screen_h - 50

pyglet.clock.schedule_once(recalculate_game_layout, 0.1)

def update(dt):
    background.update(dt, window.width, window.height)
    if current_state == consts.STATE_GAME and not is_options_open:
        for card in my_hand: card.update(dt)

pyglet.clock.schedule_interval(update, 1/60.0)

# --- ZDARZENIA ---
@window.event
def on_resize(width, height):
    # 1. Odświeżamy układ menu głównego
    if current_state == consts.STATE_MENU:
        main_menu.update_layout(width, height)

    # 2. Odświeżamy układ gry
    elif current_state == consts.STATE_GAME:
        recalculate_game_layout()

    # 3. Odświeżamy opcje (ważne!)
    options_menu.update_layout()

    super(pyglet.window.Window, window).on_resize(width, height)

@window.event
def on_draw():
    window.clear()
    background.draw()

    if current_state == consts.STATE_MENU:
        menu_batch.draw()
    elif current_state == consts.STATE_GAME:
        game_batch.draw()

    if is_options_open:
        options_batch.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    if is_options_open:
        options_menu.on_mouse_press(x, y, button, modifiers)
        return

    if current_state == consts.STATE_MENU:
        main_menu.on_mouse_press(x, y, button, modifiers)
    elif current_state == consts.STATE_GAME:
        for card in reversed(my_hand):
            if card.check_click(x, y):
                card.is_selected = not card.is_selected
                card.target_y += 50 if card.is_selected else -50
                break

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if is_options_open:
        options_menu.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

@window.event
def on_mouse_release(x, y, button, modifiers):
    if is_options_open:
        options_menu.on_mouse_release(x, y, button, modifiers)

@window.event
def on_mouse_motion(x, y, dx, dy):
    if is_options_open:
        options_menu.on_mouse_motion(x, y, dx, dy)
        return

    if current_state == consts.STATE_MENU:
        main_menu.on_mouse_motion(x, y, dx, dy)

@window.event
def on_key_press(symbol, modifiers):
    global current_state, is_options_open

    if symbol == key.ESCAPE:
        # 1. Jeśli opcje są otwarte -> Zamknij opcje i ZATRZYMAJ SIĘ
        if is_options_open:
            close_options()
            return pyglet.event.EVENT_HANDLED

        # 2. Jeśli jesteśmy w GRZE -> Wróć do MENU
        if current_state == consts.STATE_GAME:
            print("ESC: Powrót do menu")
            current_state = consts.STATE_MENU

            # WAŻNE: Odświeżamy układ menu, żeby przyciski były na środku
            # (szczególnie jeśli w trakcie gry zmieniłeś tryb fullscreen)
            main_menu.update_layout(window.width, window.height)

            return pyglet.event.EVENT_HANDLED

        # 3. Jeśli jesteśmy w MENU -> Zamknij aplikację
        if current_state == consts.STATE_MENU:
            print("ESC: Wyjście z gry")
            window.close()
            return pyglet.event.EVENT_HANDLED

if __name__ == "__main__":
    pyglet.app.run()