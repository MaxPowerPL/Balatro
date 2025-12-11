# --- STANY GRY ---
STATE_MENU = 0
STATE_GAME = 1

# --- KOLORY PRZYCISKÓW (R, G, B) ---
BTN_COLOR_PLAY = (51, 153, 255)    # Niebieski
BTN_COLOR_OPT = (255, 170, 0)      # Pomarańczowy
BTN_COLOR_EXIT = (255, 85, 85)     # Czerwony

# --- NOWE KOLORY UI (STYL BALATRO) ---
# Główne tło panelu opcji
UI_PANEL_BG = (40, 44, 52)
UI_PANEL_BORDER = (200, 200, 200)

# Kolory zakładek (nawigacji po lewej)
UI_TAB_INACTIVE = (70, 75, 85)     # Ciemnoszary
UI_TAB_ACTIVE = (220, 60, 60)      # Czerwony/Pomarańczowy (aktywna)
UI_TAB_TEXT_INACTIVE = (180, 180, 180)
UI_TAB_TEXT_ACTIVE = (255, 255, 255)

# Tło obszaru zawartości (po prawej)
UI_CONTENT_BG = (55, 60, 68)
UI_HEADER_TEXT = (255, 200, 100)   # Kolor nagłówków sekcji

# Elementy interaktywne
UI_SLIDER_BG = (30, 30, 30)
UI_SLIDER_FILL = (220, 60, 60)     # Czerwony suwak
UI_CHECKBOX_BG = (30, 30, 30)
UI_CHECKBOX_FILL = (220, 60, 60)
BTN_COLOR_TEXT = (255, 255, 255)


# --- KLASA USTAWIEŃ (Singleton) ---
class GameSettings:
    def __init__(self):
        # Wartości domyślne
        self.fullscreen = True
        # Im mniej tym większe piksele (np. 50 = bardzo retro, 500 = prawie HD)
        self.crt_intensity = 150.0

        self.volume_master = 80
        self.volume_music = 100
        self.volume_sfx = 100

        # Nowe ustawienia (przykładowe dla zakładki GRA)
        self.game_speed = 1.0
        self.show_tutorials = True

settings = GameSettings()

# --- USTAWIENIA PALET TŁA ---
PALETTES = [
    { "name": "OGIEŃ (Balatro Classic)", "c1": (0.4, 0.0, 0.0), "c2": (1.0, 0.3, 0.0), "c3": (1.0, 0.9, 0.0) },
    { "name": "MATRIX", "c1": (0.0, 0.1, 0.0), "c2": (0.0, 0.6, 0.1), "c3": (0.8, 1.0, 0.8) },
    { "name": "LÓD / CYBERPUNK", "c1": (0.05, 0.0, 0.2), "c2": (0.0, 0.6, 1.0), "c3": (1.0, 0.0, 0.8) },
    { "name": "VOID (Pustka)", "c1": (0.1, 0.0, 0.1), "c2": (0.3, 0.0, 0.3), "c3": (0.1, 0.1, 0.1) },
    { "name": "TOKSYCZNY", "c1": (0.1, 0.1, 0.0), "c2": (0.5, 0.0, 0.5), "c3": (0.7, 1.0, 0.0) }
]