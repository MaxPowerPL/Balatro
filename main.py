import pyglet
from pyglet.window import key
import sys

import consts
from background import ShaderBackground
from card import Card
from menu import MainMenu
from options import OptionsMenu
from ui import Button # Potrzebne do przycisków w grze
from game_logic import Deck, HandEvaluator

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

window = pyglet.window.Window(
    caption="Blind Bet",
    width=WINDOW_WIDTH,         # Używamy zdefiniowanej szerokości
    height=WINDOW_HEIGHT,       # Używamy zdefiniowanej wysokości
    resizable=False,
    fullscreen=consts.settings.fullscreen,
    vsync=consts.settings.vsync,
    visible=False
)

if not consts.settings.fullscreen:
    # Pobieramy aktywny ekran
    screen = window.display.get_default_screen()

    # Obliczamy środek, uwzględniając wymiary ekranu i okna
    # Dodajemy małą korektę (np. -20/40), jeśli Twój system ma bardzo grube ramki
    center_x = (screen.width - window.width) // 2
    center_y = (screen.height - window.height) // 2

    # Ustawiamy lokalizację przed pokazaniem okna
    window.set_location(max(0, center_x), max(0, center_y))

window.set_visible(True)

# Batche
menu_batch = pyglet.graphics.Batch()
game_batch = pyglet.graphics.Batch()
options_batch = pyglet.graphics.Batch()

cards_group_base = pyglet.graphics.Group(order=10)
ui_group = pyglet.graphics.Group(order=200)

current_state = consts.STATE_MENU
is_options_open = False

# --- ZMIENNE STANU GRY ---
deck = Deck()
my_hand = [] # Lista obiektów Card
MAX_HAND_SIZE = 8 # Ile kart trzymamy w ręce (jak w Balatro)
selected_cards = []

# --- UI GRY ---
game_buttons = []
info_label = pyglet.text.Label(
    "",
    font_name='Arial',
    font_size=20,
    batch=game_batch,
    group=ui_group,
    anchor_x='center'
)
info_label.bold = True # Ustawiamy pogrubienie tutaj

# 2. Naprawiony score_label (usunięto bold=True z nawiasu)
score_label = pyglet.text.Label(
    "SCORE: 0",
    font_name='Arial',
    font_size=30,
    color=(255,200,50,255),
    batch=game_batch,
    group=ui_group,
    anchor_x='center'
)
score_label.bold = True # Ustawiamy pogrubienie tutaj

# --- LOGIKA GRY ---

def draw_cards_to_hand():
    """Dobiera karty do ręki, aż będzie ich MAX_HAND_SIZE."""
    needed = MAX_HAND_SIZE - len(my_hand)
    if needed > 0:
        new_data = deck.draw(needed)
        for suit, val in new_data:
            # Tworzymy kartę poza ekranem (na dole) dla efektu wejścia
            c = Card(suit, val, window.width//2, -100, game_batch, cards_group_base)
            my_hand.append(c)
    recalculate_game_layout()

def update_card_layers():
    """
    Naprawia problem nachodzenia kart.
    Karty niezaznaczone: warstwy 10, 11, 12...
    Karty ZAZNACZONE: warstwy 110, 111, 112... (zawsze na wierzchu)
    """
    for i, card in enumerate(my_hand):
        base_order = 10
        if card.is_selected:
            base_order = 110 # Duży skok w górę dla zaznaczonych

        # Przypisujemy nową grupę z odpowiednim numerem porządkowym
        # i + base_order zapewnia, że karty po prawej są nad tymi po lewej
        card.sprite.group = pyglet.graphics.Group(order=base_order + i)

def play_hand():
    # Pobierz zaznaczone karty
    selected = [c for c in my_hand if c.is_selected]
    if len(selected) == 0:
        update_info("Wybierz karty!")
        return
    if len(selected) > 5:
        update_info("Maksymalnie 5 kart!")
        return

    # Ewaluacja
    hand_name, chips, mult, total = HandEvaluator.evaluate(selected)

    # Efekt (Log w konsoli na razie)
    print(f"Zagrano: {hand_name} | Chips: {chips} | Mult: {mult} | SCORE: {total}")
    score_label.text = f"Wynik: {total} ({hand_name})"

    # Usuwanie kart z ręki
    for c in selected:
        c.delete() # Usuń grafikę
        my_hand.remove(c) # Usuń z listy

    # Dobieranie nowych
    draw_cards_to_hand()

def discard_hand():
    selected = [c for c in my_hand if c.is_selected]
    if len(selected) == 0: return
    if len(selected) > 5:
        update_info("Możesz odrzucić max 5!")
        return

    print(f"Odrzucono {len(selected)} kart.")

    for c in selected:
        c.delete()
        my_hand.remove(c)

    draw_cards_to_hand()

def update_info(text):
    info_label.text = text
    # Można dodać timer do czyszczenia tekstu

# --- INICJALIZACJA ---
background = ShaderBackground(window.width, window.height)

# Przyciski w grze
def init_game_ui():
    game_buttons.clear()
    cx = window.width // 2

    # Przycisk ZAGRAJ (Action)
    btn_play = Button("ZAGRAJ", cx + 150, 150, 180, 60, consts.BTN_COLOR_ACTION, play_hand, game_batch, ui_group)

    # Przycisk ODRZUĆ (Discard)
    btn_discard = Button("ODRZUĆ", cx - 330, 150, 180, 60, consts.BTN_COLOR_DISCARD, discard_hand, game_batch, ui_group)

    game_buttons.extend([btn_play, btn_discard])

# Funkcje Menu
def start_game():
    global current_state
    if is_options_open: return
    current_state = consts.STATE_GAME

    # Reset gry
    deck.reset()
    for c in my_hand: c.delete()
    my_hand.clear()

    draw_cards_to_hand()
    init_game_ui()
    recalculate_game_layout()

def open_options():
    global is_options_open
    is_options_open = True
    options_menu.visible = True
    options_menu.update_layout()

def close_options():
    global is_options_open
    is_options_open = False
    options_menu.visible = False

def exit_game():
    if is_options_open: return
    pyglet.app.exit()

main_menu = MainMenu(window.width, window.height, menu_batch, start_game, open_options, exit_game)
options_menu = OptionsMenu(window, options_batch, close_options)

def recalculate_game_layout(dt=None):
    if current_state != consts.STATE_GAME: return
    screen_w, screen_h = window.width, window.height

    # Odświeżamy UI gry
    init_game_ui()
    info_label.x = screen_w // 2; info_label.y = screen_h // 2 + 100
    score_label.x = screen_w // 2; score_label.y = screen_h - 100

    # Skalowanie kart
    for c in my_hand: c.update_scale(screen_w, screen_h)

    if not my_hand: return

    current_card_width = my_hand[0].sprite.width
    spacing = current_card_width * 0.8 # Karty w ręce mogą na siebie nachodzić
    total_width = (len(my_hand) * spacing)
    start_x = (screen_w / 2) - (total_width / 2) + (spacing / 2)
    base_y = 300 # Wysokość kart na ekranie

    for i, card in enumerate(my_hand):
        target_x = start_x + (i * spacing)
        # Jeśli zaznaczona, wyżej
        target_y = base_y + 50 if card.is_selected else base_y
        card.set_target(target_x, target_y)

pyglet.clock.schedule_once(recalculate_game_layout, 0.1)

def update(dt):
    background.update(dt, window.width, window.height)
    if current_state == consts.STATE_GAME and not is_options_open:
        for card in my_hand: card.update(dt)

        # Ciągłe sprawdzanie układu zaznaczonych kart (dla podglądu wyniku)
        selected = [c for c in my_hand if c.is_selected]
        if selected:
            hand_name, _, _, _ = HandEvaluator.evaluate(selected)
            info_label.text = hand_name
        else:
            info_label.text = "Wybierz karty"

pyglet.clock.schedule_interval(update, 1/60.0)

# --- ZDARZENIA ---
@window.event
def on_resize(width, height):
    if current_state == consts.STATE_MENU:
        main_menu.update_layout(width, height)
    elif current_state == consts.STATE_GAME:
        recalculate_game_layout()
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
        # Sprawdzamy przyciski UI
        btn_hit = False
        for btn in game_buttons:
            if btn.check_click(x, y):
                btn_hit = True
                break

        # Jeśli nie kliknięto przycisku, sprawdzamy karty
        if not btn_hit:
            for card in reversed(my_hand): # Odwrócona kolejność (wierzch)
                if card.check_click(x, y):
                    card.is_selected = not card.is_selected
                    # Aktualizujemy pozycję docelową
                    base_y = 300
                    card.set_target(card.target_x, base_y + 50 if card.is_selected else base_y)

                    update_card_layers()
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
    elif current_state == consts.STATE_GAME:
        for btn in game_buttons:
            btn.check_hover(x, y)

@window.event
def on_key_press(symbol, modifiers):
    global current_state, is_options_open

    if symbol == key.ESCAPE:
        if is_options_open:
            close_options()
            return pyglet.event.EVENT_HANDLED

        if current_state == consts.STATE_GAME:
            current_state = consts.STATE_MENU
            main_menu.update_layout(window.width, window.height)
            return pyglet.event.EVENT_HANDLED

        if current_state == consts.STATE_MENU:
            window.close()
            return pyglet.event.EVENT_HANDLED

if __name__ == "__main__":
    pyglet.app.run()