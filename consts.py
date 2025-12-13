import json
import os

# --- PLIK ZAPISU ---
SETTINGS_FILE = "settings.json"

# --- STANY GRY ---
STATE_MENU = 0
STATE_GAME = 1

# --- KOLORY ---
BTN_COLOR_PLAY = (51, 153, 255)
BTN_COLOR_OPT = (255, 170, 0)
BTN_COLOR_EXIT = (255, 85, 85)
BTN_COLOR_DISCARD = (255, 60, 60) # Czerwony dla odrzucania
BTN_COLOR_ACTION = (70, 150, 200) # Niebieski dla zagrywania

# UI Colors (bez zmian...)
UI_PANEL_BG = (40, 44, 52)
UI_PANEL_BORDER = (200, 200, 200)
UI_TAB_INACTIVE = (70, 75, 85)
UI_TAB_ACTIVE = (220, 60, 60)
UI_TAB_TEXT_INACTIVE = (180, 180, 180)
UI_TAB_TEXT_ACTIVE = (255, 255, 255)
UI_CONTENT_BG = (55, 60, 68)
UI_HEADER_TEXT = (255, 200, 100)
UI_SLIDER_BG = (30, 30, 30)
UI_SLIDER_FILL = (220, 60, 60)
UI_CHECKBOX_BG = (30, 30, 30)
UI_CHECKBOX_FILL = (220, 60, 60)
BTN_COLOR_TEXT = (255, 255, 255)

# --- DEFINICJE UKŁADÓW POKEROWYCH (Balatro Base) ---
# Format: (Chips, Mult)
HAND_SCORES = {
    "High Card": (5, 1),
    "Pair": (10, 2),
    "Two Pair": (20, 2),
    "Three of a Kind": (30, 3),
    "Straight": (30, 4),
    "Flush": (35, 4),
    "Full House": (40, 4),
    "Four of a Kind": (60, 7),
    "Straight Flush": (100, 8),
    "Royal Flush": (100, 8) # W Balatro to zazwyczaj to samo co Straight Flush, ale można wyróżnić
}

# Wartości kart (Chips)
# 2-9 = wartość, 10, J, Q, K = 10, A = 11
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    '10': 10, 'walet': 10, 'dama': 10, 'krol': 10, 'as': 11
}

# --- KLASA USTAWIEŃ (Bez zmian...) ---
class GameSettings:
    def __init__(self):
        self.fullscreen = True
        self.vsync = False
        self.crt_intensity = 150.0
        self.volume_master = 80
        self.volume_music = 100
        self.volume_sfx = 100
        self.game_speed = 1.0
        self.show_tutorials = True

        self._last_saved_data = {}

        self.load()

    def save(self):
        data = {
            "fullscreen": self.fullscreen,
            "vsync": self.vsync,
            "crt_intensity": self.crt_intensity,
            "volume_master": self.volume_master,
            "volume_music": self.volume_music,
            "volume_sfx": self.volume_sfx,
            "game_speed": self.game_speed,
            "show_tutorials": self.show_tutorials
        }

        if data == self._last_saved_data:
            return

        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(data, f, indent=4)
            self._last_saved_data = data
        except Exception as e:
            print(f"Błąd zapisu: {e}")

    def load(self):
        if not os.path.exists(SETTINGS_FILE): return
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                self.fullscreen = data.get("fullscreen", True)
                self.vsync = data.get("vsync", False)
                self.crt_intensity = data.get("crt_intensity", 150.0)
                self.volume_master = data.get("volume_master", 80)
                self.volume_music = data.get("volume_music", 100)
                self.volume_sfx = data.get("volume_sfx", 100)
                self.game_speed = data.get("game_speed", 1.0)
                self.show_tutorials = data.get("show_tutorials", True)

                self._last_saved_data = data
        except Exception as e:
            print(f"Błąd odczytu: {e}")

settings = GameSettings()

# --- PALETY (Bez zmian...) ---
PALETTES = [
    { "name": "OGIEŃ", "c1": (0.4, 0.0, 0.0), "c2": (1.0, 0.3, 0.0), "c3": (1.0, 0.9, 0.0) },
    { "name": "MATRIX", "c1": (0.0, 0.1, 0.0), "c2": (0.0, 0.6, 0.1), "c3": (0.8, 1.0, 0.8) },
    { "name": "CYBERPUNK", "c1": (0.05, 0.0, 0.2), "c2": (0.0, 0.6, 1.0), "c3": (1.0, 0.0, 0.8) },
    { "name": "VOID", "c1": (0.1, 0.0, 0.1), "c2": (0.3, 0.0, 0.3), "c3": (0.1, 0.1, 0.1) },
    { "name": "TOKSYCZNY", "c1": (0.1, 0.1, 0.0), "c2": (0.5, 0.0, 0.5), "c3": (0.7, 1.0, 0.0) }
]