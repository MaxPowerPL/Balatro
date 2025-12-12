import json
import os

# --- PLIK ZAPISU ---
SETTINGS_FILE = "settings.json"

# --- STANY GRY ---
STATE_MENU = 0
STATE_GAME = 1

# --- KOLORY UI ---
BTN_COLOR_PLAY = (51, 153, 255)
BTN_COLOR_OPT = (255, 170, 0)
BTN_COLOR_EXIT = (255, 85, 85)

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

# --- KLASA USTAWIEŃ Z ZAPISEM ---
class GameSettings:
    def __init__(self):
        # 1. Wartości Domyślne (Fallback)
        self.fullscreen = True
        self.crt_intensity = 150.0
        self.volume_master = 80
        self.volume_music = 100
        self.volume_sfx = 100
        self.game_speed = 1.0
        self.show_tutorials = True

        # 2. Próba wczytania z pliku przy starcie
        self.load()

    def save(self):
        """Zapisuje obecne ustawienia do pliku JSON."""
        data = {
            "fullscreen": self.fullscreen,
            "crt_intensity": self.crt_intensity,
            "volume_master": self.volume_master,
            "volume_music": self.volume_music,
            "volume_sfx": self.volume_sfx,
            "game_speed": self.game_speed,
            "show_tutorials": self.show_tutorials
        }
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(data, f, indent=4)
            print("Ustawienia zapisane.")
        except Exception as e:
            print(f"Błąd zapisu ustawień: {e}")

    def load(self):
        """Wczytuje ustawienia z pliku JSON (jeśli istnieje)."""
        if not os.path.exists(SETTINGS_FILE):
            return # Brak pliku -> zostajemy przy domyślnych

        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)

                # Używamy .get() żeby nie wywaliło błędu przy starych plikach config
                self.fullscreen = data.get("fullscreen", True)
                self.crt_intensity = data.get("crt_intensity", 150.0)
                self.volume_master = data.get("volume_master", 80)
                self.volume_music = data.get("volume_music", 100)
                self.volume_sfx = data.get("volume_sfx", 100)
                self.game_speed = data.get("game_speed", 1.0)
                self.show_tutorials = data.get("show_tutorials", True)
                print("Ustawienia wczytane.")
        except Exception as e:
            print(f"Błąd odczytu ustawień (używam domyślnych): {e}")

settings = GameSettings()

# --- USTAWIENIA PALET TŁA ---
PALETTES = [
    { "name": "OGIEŃ (Balatro Classic)", "c1": (0.4, 0.0, 0.0), "c2": (1.0, 0.3, 0.0), "c3": (1.0, 0.9, 0.0) },
    { "name": "MATRIX", "c1": (0.0, 0.1, 0.0), "c2": (0.0, 0.6, 0.1), "c3": (0.8, 1.0, 0.8) },
    { "name": "LÓD / CYBERPUNK", "c1": (0.05, 0.0, 0.2), "c2": (0.0, 0.6, 1.0), "c3": (1.0, 0.0, 0.8) },
    { "name": "VOID (Pustka)", "c1": (0.1, 0.0, 0.1), "c2": (0.3, 0.0, 0.3), "c3": (0.1, 0.1, 0.1) },
    { "name": "TOKSYCZNY", "c1": (0.1, 0.1, 0.0), "c2": (0.5, 0.0, 0.5), "c3": (0.7, 1.0, 0.0) }
]