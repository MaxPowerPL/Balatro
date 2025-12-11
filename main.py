import pyglet
from pyglet.window import key
import sys

# IMPORTY MODUŁÓW
import consts
from background import ShaderBackground
from card import Card
from menu import MainMenu

# 1. KONFIGURACJA OKNA
window = pyglet.window.Window(caption="Balatro Clone", resizable=True, fullscreen=True, vsync=True)

# --- BATCHE (Grupy rysowania) ---
# Rozdzielamy menu i grę, żeby się nie mieszały
menu_batch = pyglet.graphics.Batch()
game_batch = pyglet.graphics.Batch()

# Grupy dla gry
cards_group = pyglet.graphics.Group(order=1)
ui_group = pyglet.graphics.Group(order=2)

# 2. STAN GRY
current_state = consts.STATE_MENU

# 3. FUNKCJE PRZEŁĄCZAJĄCE STANY
def start_game():
    global current_state
    print("Przycisk GRAJ kliknięty -> Przełączam na grę")
    current_state = consts.STATE_GAME
    # Tutaj można zresetować rozdanie kart
    recalculate_game_layout()

def exit_game():
    print("Zamykanie gry...")
    pyglet.app.exit()

# 4. INICJALIZACJA OBIEKTÓW
# Tło jest wspólne dla obu stanów
background = ShaderBackground(window.width, window.height)

# MENU
main_menu = MainMenu(window.width, window.height, menu_batch, start_game, exit_game)

# GRA (Karty)
my_hand = []
hand_data = ['pik_as', 'kier_krol', 'trefl_10', 'karo_2', 'BACK']

for card_name in hand_data:
    new_card = Card(card_name, 0, 0, game_batch, cards_group)
    my_hand.append(new_card)

# UI Gry (Przycisk powrotu do menu pod ESC)
game_label = pyglet.text.Label(
    'Kliknij kartę | ESC - powrót do menu', font_name='Arial', font_size=24,
    x=window.width//2, y=window.height - 50,
    anchor_x='center', anchor_y='center',
    batch=game_batch, group=ui_group
)

# 5. LOGIKA UKŁADU (LAYOUT) - Tylko dla gry
def recalculate_game_layout(dt=None):
    if current_state != consts.STATE_GAME: return

    screen_w = window.width
    screen_h = window.height

    for card in my_hand:
        card.update_scale(screen_w, screen_h)

    current_card_width = my_hand[0].sprite.width
    spacing = current_card_width * 1.1
    total_width = (len(my_hand) * spacing)

    start_x = (screen_w / 2) - (total_width / 2) + (spacing / 2)
    base_y = screen_h * 0.3

    for i, card in enumerate(my_hand):
        target_x = start_x + (i * spacing)
        card.set_position(target_x, base_y)
        if card.is_selected:
            card.target_y = base_y + 50
        else:
            card.target_y = base_y

    game_label.x = screen_w // 2
    game_label.y = screen_h - 50

pyglet.clock.schedule_once(recalculate_game_layout, 0.1)

# 6. PĘTLA GRY (UPDATE)
def update(dt):
    # Tło działa zawsze (w menu i w grze)
    background.update(dt, window.width, window.height)

    if current_state == consts.STATE_GAME:
        for card in my_hand:
            card.update(dt)

pyglet.clock.schedule_interval(update, 1/60.0)

# 7. ZDARZENIA (EVENTS)
@window.event
def on_resize(width, height):
    if current_state == consts.STATE_GAME:
        recalculate_game_layout()
    # Tu można dodać odświeżanie pozycji przycisków menu przy zmianie okna
    super(pyglet.window.Window, window).on_resize(width, height)

@window.event
def on_draw():
    window.clear()

    # 1. Rysujemy tło (jest pod wszystkim)
    background.draw()

    # 2. Rysujemy odpowiedni Batch w zależności od stanu
    if current_state == consts.STATE_MENU:
        menu_batch.draw()
    elif current_state == consts.STATE_GAME:
        game_batch.draw()

@window.event
def on_mouse_motion(x, y, dx, dy):
    if current_state == consts.STATE_MENU:
        main_menu.on_mouse_motion(x, y, dx, dy)

@window.event
def on_mouse_press(x, y, button, modifiers):
    if current_state == consts.STATE_MENU:
        main_menu.on_mouse_press(x, y, button, modifiers)

    elif current_state == consts.STATE_GAME:
        for card in reversed(my_hand):
            if card.check_click(x, y):
                card.is_selected = not card.is_selected
                if card.is_selected:
                    card.target_y += 50
                else:
                    card.target_y -= 50
                break

@window.event
def on_key_press(symbol, modifiers):
    global current_state

    if symbol == key.ESCAPE:
        if current_state == consts.STATE_GAME:
            # Powrót do menu
            current_state = consts.STATE_MENU
        else:
            # Wyjście z gry (jeśli jesteśmy w menu)
            window.close()

if __name__ == "__main__":
    pyglet.app.run()