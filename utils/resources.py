import pyglet

# --- ŁADOWANIE ZASOBÓW ---
# Wykonuje się raz przy starcie importu

cards_image = pyglet.image.load('assets/images/cards_sheet.png')
cards_texture = cards_image.get_texture()

# Fix ostrości (Pixel Art) - Metoda Nuklearna
pyglet.gl.glBindTexture(cards_texture.target, cards_texture.id)
pyglet.gl.glTexParameteri(cards_texture.target, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
pyglet.gl.glTexParameteri(cards_texture.target, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)

# Cięcie na siatkę
card_grid = pyglet.image.ImageGrid(cards_texture, rows=5, columns=13)

# Ustawienie Anchor Point (Środek)
for img in card_grid:
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2

# Tworzenie słownika nazw
deck_images = {}
card_back_image = card_grid[0]
suits = ['karo', 'trefl', 'kier', 'pik']
values = ['as', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'walet', 'dama', 'krol']

for row_index, suit in enumerate(suits):
    for col_index, value in enumerate(values):
        grid_index = ((row_index + 1) * 13) + col_index
        card_name = f"{suit}_{value}"
        deck_images[card_name] = card_grid[grid_index]

pills_image = pyglet.image.load('assets/images/pills.png')
pills_texture = pills_image.get_texture()

pyglet.gl.glBindTexture(pills_texture.target, pills_texture.id)
pyglet.gl.glTexParameteri(pills_texture.target, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
pyglet.gl.glTexParameteri(pills_texture.target, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)

pill_chip_img = pills_texture.get_region(0, 0, 22, 10) # x, y, width, height
pill_mult_img = pills_texture.get_region(22, 0, 22, 10) # x, y, width, height

pill_chip_img.anchor_x = pill_chip_img.width // 2
pill_chip_img.anchor_y = pill_chip_img.height // 2
pill_mult_img.anchor_x = pill_mult_img.width // 2
pill_mult_img.anchor_y = pill_mult_img.height // 2