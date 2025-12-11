import pyglet
from pyglet import shapes

window = pyglet.window.Window(width=1280, height=720, caption="Balatro", resizable=True)

main_batch = pyglet.graphics.Batch()

cards = []

for i in range(5):
    card = shapes.Rectangle(
        x = 100 + (i * 150),
        y = 300,
        width = 100,
        height = 140,
        color = (200, 50, 50),
        batch = main_batch
    )

    card.dy = 0
    cards.append(card)

label = pyglet.text.Label(
    'Kliknij myszką, aby podbić karty!',
    font_name = 'Arial',
    font_size = 24,
    x = window.width // 2,
    y = window.height - 50,
    anchor_x = 'center',
    anchor_y = 'center',
    batch = main_batch
)

def update(dt):
    for card in cards:
        card.y += card.dy * dt * 60

        card.dy -= 0.5

        if card.y < 300:
            card.y = 300
            card.dy = 0

        if card.y > 450:
            card.y = 450
            card.dy = -3

pyglet.clock.schedule_interval(update, 1/60.0)

@window.event
def on_draw():
    window.clear()
    main_batch.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    for card in cards:
        check_x = card.x < x < card.x + card.width
        check_y = card.y < y < card.y + card.height

        if check_x and check_y:
            card.dy = 15
            print("Trafiony!")

if __name__ == "__main__":
    pyglet.app.run()