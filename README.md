<div align="center">

  <img src="assets/logo.png" alt="Blind Bet Logo" width="200" height="auto" />

  # Blind Bet (Python Edition)

  **Edukacyjna reimplementacja hitu roguelike "Balatro" stworzona od zera.**
  <br>
  *Brak silnika Unity/Godot. Czysty kod, matematyka i shadery.*

  <p>
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
    </a>
    <a href="https://pyglet.org/">
      <img src="https://img.shields.io/badge/Engine-Pyglet%202.0-FF5722?style=for-the-badge&logo=opengl&logoColor=white" alt="Engine" />
    </a>
    <a href="#">
      <img src="https://img.shields.io/badge/Status-Alpha%20Dev-important?style=for-the-badge" alt="Status" />
    </a>
    <a href="LICENSE">
      <img src="https://img.shields.io/github/license/MaxPowerPL/blind-bet?style=for-the-badge" alt="License" />
    </a>
  </p>

  <p>
    <a href="#-o-projekcie">🃏 O Projekcie</a> •
    <a href="#-funkcjonalności">✨ Funkcjonalności</a> •
    <a href="#-instalacja-i-uruchomienie">🚀 Instalacja</a> •
    <a href="#-struktura-projektu">📂 Struktura</a> •
    <a href="#-roadmapa">🗺️ Roadmapa</a>
  </p>
</div>

---

## 🃏 O Projekcie

Ten projekt to **klon gry Balatro** napisany całkowicie w języku **Python**, wykorzystujący bibliotekę **Pyglet** do obsługi grafiki oraz natywne shadery **OpenGL (GLSL)**.

Celem projektu jest nauka architektury gier 2D bez użycia gotowych silników ("Game Engines"), zrozumienie matematyki stojącej za animacjami, shaderami oraz optymalizacją renderowania (Batch Rendering).

### 🎮 Aktualna Wersja: `v0.3.0 (Alpha)`
Wersja ta wprowadza w pełni funkcjonalne menu opcji z trybami zakładek, system zapisu ustawień do JSON, responsywne skalowanie UI oraz zoptymalizowane shadery tła z dynamiczną pikselizacją sterowaną suwakiem.

---

## ✨ Funkcjonalności

Co już działa w tej wersji?

- [x] **Silnik Renderujący**: Oparty na `pyglet.graphics.Batch` (wysoka wydajność).
- [x] **Dynamiczne Tło (Shader GLSL)**:
  - Proceduralnie generowany efekt "Liquid Plasma".
  - **Dynamiczna pikselizacja w czasie rzeczywistym** sterowana suwakiem CRT Intensity.
  - Płynna zmiana palet kolorów (Ogień → Matrix → Cyberpunk → Void → Toksyczny).
  - Automatyczne przełączanie palet co 15 sekund z interpolacją.
- [x] **Fizyka Kart**:
  - Animacje oparte o interpolację liniową (`Lerp`).
  - Interakcja z myszką (Hover, Click, Drag).
  - Skalowanie "Pixel-Perfect" (Integer Scaling).
  - Pełna obsługa atlasu tekstur kart (52 karty + rewers).
- [x] **System UI**:
  - Własne implementacje Przycisków, Suwaków i Checkboxów.
  - Menu Główne z logo i trzema przyciskami (Graj, Opcje, Wyjdź).
  - **Zaawansowane Menu Opcji**:
    - System zakładek (Gra, Wideo, Audio).
    - Responsywne panele z automatycznym layoutem.
    - Efekty hover na przyciskach.
- [x] **System Ustawień**:
  - **Zapis i odczyt ustawień do pliku JSON** (`settings.json`).
  - Opcje Wideo: Pełny ekran, Intensywność efektu CRT.
  - Opcje Audio: Głośność główna, muzyka, efekty dźwiękowe (zarezerwowane).
  - Opcje Gry: Pokaż samouczki, szybkość animacji.
  - Automatyczny zapis przy zamknięciu menu opcji i po puszczeniu suwaków.
- [x] **Responsywność**:
  - Automatyczne skalowanie kart i UI do rozdzielczości okna.
  - Dynamiczne przeliczanie layoutu przy resize okna.
  - Obsługa przełączania trybu pełnoekranowego w locie.
- [x] **Zarządzanie Stanami Gry**:
  - System stanów (Menu → Gra).
  - ESC w grze wraca do menu, w menu zamyka grę.
  - Opcje jako overlay (można otworzyć z menu i z gry).

---

## 🛠️ Technologie

Projekt został zbudowany przy użyciu:

| Technologia | Opis |
| :--- | :--- |
| **Python 3.12** | Główny język logiki gry. |
| **Pyglet 2.0+** | Biblioteka okienkowa i obsługa OpenGL. |
| **GLSL 330** | Język shaderów (efekty wizualne tła). |
| **OOP** | Architektura obiektowa (klasy dla Kart, UI, Stanów). |
| **JSON** | Format zapisu ustawień gracza. |

---

## 🚀 Instalacja i Uruchomienie

Aby uruchomić grę na swoim komputerze, wykonaj następujące kroki:

### 1. Wymagania
Musisz mieć zainstalowanego [Python 3.10+](https://www.python.org/downloads/).

### 2. Klonowanie repozytorium
```bash
git clone https://github.com/MaxPowerPL/Blind-Bet.git
cd Blind-Bet
```

### 3. Konfiguracja środowiska (Zalecane)

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalacja zależności
```bash
pip install pyglet
```

### 5. Uruchomienie
```bash
python main.py
```

### 6. Sterowanie
- **Menu**: Kliknij przyciski myszką.
- **Gra**: Kliknij karty aby je zaznaczyć (podnoszą się).
- **ESC**: Powrót do menu z gry / Zamknięcie gry z menu / Zamknięcie opcji.
- **Opcje**: Pełnoekranowy tryb + suwaki intensywności efektów.

---

## 📂 Struktura Projektu
Profesjonalny podział kodu na moduły:

```text
📦 Blind Bet
 ┣ 📦 assets/
 ┃  ┣ 🖼️ cards_sheet.png    # Atlas tekstur kart (5x13 grid, Pixel Art)
 ┃  ┗ 🖼️ logo.png           # Logo gry (Blind Bet)
 ┣ 📜 main.py               # Główna pętla gry, zarządzanie oknem i stanami
 ┣ 📜 consts.py             # Stałe konfiguracyjne, kolory UI, klasa GameSettings
 ┣ 📜 resources.py          # Ładowanie i przetwarzanie grafik (Sprite Sheet)
 ┣ 📜 background.py         # Logika shaderów GLSL i renderowanie tła
 ┣ 📜 card.py               # Klasa Karty (fizyka, animacje, interakcja)
 ┣ 📜 menu.py               # Logika Menu Głównego (logo + przyciski)
 ┣ 📜 options.py            # Logika Menu Opcji (system zakładek, ustawienia)
 ┣ 📜 ui.py                 # Komponenty interfejsu (Button, Slider, Checkbox)
 ┗ 📜 settings.json         # Plik zapisu ustawień gracza (generowany automatycznie)
```

### Opis głównych modułów:

| Plik | Opis |
|------|------|
| `main.py` | Inicjalizacja okna Pyglet, zarządzanie stanami gry (Menu/Gra), główna pętla update/render, obsługa eventów (klawiatura, mysz, resize). |
| `consts.py` | Wszystkie stałe projektu (kolory UI, stany gry), klasa `GameSettings` z metodami `save()` i `load()` do zarządzania plikiem JSON. |
| `background.py` | Implementacja shaderów GLSL (vertex + fragment), proceduralna generacja efektu Plasma z interpolacją kolorów między paletami. |
| `card.py` | Klasa `Card` z logiką skalowania, pozycjonowania, animacji Lerp i detekcji kliknięć. |
| `menu.py` | Klasa `MainMenu` z dynamicznym ładowaniem logo (z fixem anchor point) i trzema przyciskami akcji. |
| `options.py` | Zaawansowana klasa `OptionsMenu` z systemem zakładek, builderem UI dla każdej sekcji, zarządzaniem widocznością elementów. |
| `ui.py` | Trzy komponenty: `Button` (z efektem hover i cieniem), `Slider` (z drag & drop), `Checkbox` (z wizualną zmianą stanu). |

---

## 🎨 System Shaderów

Gra wykorzystuje **OpenGL Shading Language (GLSL 330)** do generowania dynamicznego tła:

### Efekty wizualne:
- **Liquid Plasma**: Proceduralna animacja fal sinusoidalnych.
- **Pikselizacja**: Uniform `u_pixels` kontrolowany suwakiem "Intensywność CRT" (zakres 20-500).
- **Palety kolorów**: 5 predefiniowanych schematów kolorystycznych z automatycznym przełączaniem.
- **Interpolacja**: Płynne przejścia między paletami przy użyciu algorytmu Lerp.

### Dostępne palety:
1. **OGIEŃ** - Czerwono-pomarańczowo-żółta.
2. **MATRIX** - Zielona matrycowa.
3. **LÓD / CYBERPUNK** - Niebiesko-różowa.
4. **VOID (Pustka)** - Ciemna fioletowa.
5. **TOKSYCZNY** - Żółto-fioletowa.

---

## 🗺️ Roadmapa
Plany rozwoju projektu na najbliższe miesiące:

### Faza 1: Core Mechanics (Ukończona ✅)
- [x] Rendering kart i tła.
- [x] Podstawowe UI i Menu.
- [x] System shaderów CRT i Plasma.
- [x] Menu Opcji z systemem zakładek.
- [x] Zapis i odczyt ustawień do JSON.
- [x] Responsywne skalowanie przy resize okna.
- [x] Fix anchor point dla logo (Pixel-Perfect).

### Faza 2: Logika Pokera (Następny krok 🚧)
- [ ] Algorytm sprawdzania układów (Para, Trójka, Strit, Kolor, Full, Kareta, Poker).
- [ ] System punktacji (Chips + Mult).
- [ ] Mechanika odrzucania i dobierania kart.
- [ ] Generowanie talii i losowość (shuffle).
- [ ] UI wyświetlania znalezionego układu.

### Faza 3: Roguelike Elements
- [ ] Implementacja Jokerów (modyfikatory punktów).
- [ ] Sklep (kupowanie kart i ulepszeń).
- [ ] System Blindów (Small Blind, Big Blind, Boss Blinds).
- [ ] Progresja runów (Ante 1-8).
- [ ] Unlockable content (nowe talie, jokery).

### Faza 4: Audio & Polish
- [ ] Efekty dźwiękowe (SFX) przy klikaniu, punktacji, kupowaniu.
- [ ] Muzyka w tle (adaptive soundtrack).
- [ ] System zapisu gry (Save/Load progressu).
- [ ] Animacje wejścia/wyjścia kart (tweening).
- [ ] Particle effects przy wysokich wynikach.
- [ ] Screen shake i juice effects.

### Faza 5: Balancing & Content
- [ ] Balansowanie ekonomii (ceny, nagrody).
- [ ] Dodanie więcej Jokerów (50+ unikalnych).
- [ ] Voucher system (permanent upgrades).
- [ ] Spectral Cards i Planet Cards.
- [ ] Challenge Runs (modyfikatory trudności).

---

## 🐛 Znane Problemy i Rozwiązania

### ✅ Naprawione w v0.3.0:
- **Logo było przesunięte w menu**: Naprawiono przez ustawienie `anchor_x/y` bezpośrednio na obiekcie `texture` zamiast na `logo_img`.
- **Suwaki zapisywały co klatkę**: Zoptymalizowano - zapis następuje tylko przy puszczeniu myszy (`on_mouse_release`).
- **Checkbox nie pamiętał stanu po ukryciu**: Dodano logikę warunkową w `set_visible()`.

### 🔧 Do poprawy:
- [ ] Brak obsługi kontrolera/gamepad.
- [ ] Brak lokalizacji (tylko polski).
- [ ] Menu opcji nie obsługuje przewijania (wszystko musi zmieścić się na ekranie).

---

## 📜 Licencja

Ten projekt jest udostępniony na licencji **MIT License**. Zobacz plik [LICENSE](LICENSE) po więcej szczegółów.

---

<div align="center">

### ⭐ Jeśli podoba Ci się ten projekt, zostaw gwiazdkę na GitHubie! ⭐

☕ Stworzono używając Python & Pyglet.
<br>
<sub>Ten projekt jest fanowską wersją edukacyjną i nie jest powiązany z LocalThunk ani Playstack.</sub>

<p>
  <a href="https://github.com/MaxPowerPL/Blind-Bet/issues">🐛 Zgłoś Bug</a> •
  <a href="https://github.com/MaxPowerPL/Blind-Bet/issues">💡 Zaproponuj Funkcję</a> •
  <a href="https://github.com/MaxPowerPL/Blind-Bet/wiki">📖 Wiki</a>
</p>

**Status Projektu:** 🟢 Aktywnie Rozwijany

</div>