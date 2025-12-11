# --- STANY GRY ---
STATE_MENU = 0
STATE_GAME = 1
# Opcje są nakładką (overlay), więc nie muszą być osobnym stanem głównym,
# ale dla porządku w main loopie będziemy sprawdzać flagę.

# --- KOLORY (R, G, B) ---
BTN_COLOR_PLAY = (51, 153, 255)    # Niebieski
BTN_COLOR_OPT = (255, 170, 0)      # Pomarańczowy
BTN_COLOR_EXIT = (255, 85, 85)     # Czerwony
BTN_COLOR_COLL = (70, 200, 100)    # Zielony
BTN_COLOR_TEXT = (255, 255, 255)   # Biały

# Kolory UI Opcji (Styl Balatro - Ciemny szary i Czerwony)
UI_PANEL_BG = (50, 55, 60)         # Ciemnoszare tło panelu
UI_PANEL_BORDER = (200, 200, 200)  # Jasna ramka
UI_SLIDER_BG = (30, 30, 30)        # Tło paska suwaka
UI_SLIDER_FILL = (255, 60, 60)     # Wypełnienie suwaka (Czerwone)

# --- KLASA USTAWIEŃ (Singleton) ---
class GameSettings:
    def __init__(self):
        # Wartości domyślne
        self.fullscreen = True
        self.crt_intensity = 120.0 # Im mniej tym większe piksele
        self.crt_warp = 0.5        # Siła wyginania (symulacja)
        self.volume_master = 50
        self.volume_music = 100
        self.volume_sfx = 100

# Tworzymy jedną instancję ustawień dostępną dla całej gry
settings = GameSettings()

# --- USTAWIENIA PALET TŁA (Bez zmian) ---
PALETTES = [
    { "name": "OGIEŃ", "c1": (0.4, 0.0, 0.0), "c2": (1.0, 0.3, 0.0), "c3": (1.0, 0.9, 0.0) },
    { "name": "MATRIX", "c1": (0.0, 0.1, 0.0), "c2": (0.0, 0.6, 0.1), "c3": (0.8, 1.0, 0.8) },
    { "name": "CYBERPUNK", "c1": (0.05, 0.0, 0.2), "c2": (0.0, 0.6, 1.0), "c3": (1.0, 0.0, 0.8) },
    { "name": "VOID", "c1": (0.1, 0.0, 0.1), "c2": (0.3, 0.0, 0.3), "c3": (0.1, 0.1, 0.1) },
    { "name": "TOKSYCZNY", "c1": (0.1, 0.1, 0.0), "c2": (0.5, 0.0, 0.5), "c3": (0.7, 1.0, 0.0) }
]