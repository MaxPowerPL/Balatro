<div align="center">

  <img src="logo.png" alt="Balatro Clone Logo" width="200" height="auto" />

  # Balatro Clone (Python Edition)

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
      <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
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

### 🎮 Aktualna Wersja: `v0.2.0 (Alpha)`
Wersja ta wprowadza w pełni funkcjonalne menu, system stanów gry, obsługę shaderów w tle oraz responsywne UI.

---

## ✨ Funkcjonalności

Co już działa w tej wersji?

- [x] **Silnik Renderujący**: Oparty na `pyglet.graphics.Batch` (wysoka wydajność).
- [x] **Dynamiczne Tło (Shader GLSL)**:
  - Proceduralnie generowany efekt "Liquid Plasma".
  - Obsługa pikselizacji w czasie rzeczywistym.
  - Płynna zmiana palet kolorów (Ogień → Matrix → Cyberpunk).
- [x] **Fizyka Kart**:
  - Animacje oparte o interpolację liniową (`Lerp`).
  - Interakcja z myszką (Hover, Click, Drag).
  - Skalowanie "Pixel-Perfect" (Integer Scaling).
- [x] **System UI**:
  - Własne implementacje Przycisków, Suwaków i Checkboxów.
  - Menu Główne i Menu Opcji (Overlay).
  - Stylizowany panel ustawień.
- [x] **Responsywność**: Automatyczne skalowanie kart i UI do rozdzielczości okna.

---

## 🛠️ Technologie

Projekt został zbudowany przy użyciu:

| Technologia | Opis |
| :--- | :--- |
| **Python 3.12** | Główny język logiki gry. |
| **Pyglet 2.0+** | Biblioteka okienkowa i obsługa OpenGL. |
| **GLSL 330** | Język shaderów (efekty wizualne tła). |
| **OOP** | Architektura obiektowa (klasy dla Kart, UI, Stanów). |

---

## 🚀 Instalacja i Uruchomienie

Aby uruchomić grę na swoim komputerze, wykonaj następujące kroki:

### 1. Wymagania
Musisz mieć zainstalowanego [Python 3.10+](https://www.python.org/downloads/).

### 2. Klonowanie repozytorium
```bash
git clone [https://github.com/TWOJA_NAZWA/balatro-clone-python.git](https://github.com/TWOJA_NAZWA/balatro-clone-python.git)
cd balatro-clone-python
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

---

## 📂 Struktura Projektu
Profesjonalny podział kodu na moduły:

```text
📦 balatro-clone
 ┣ 📜 main.py          # Główna pętla gry i zarządzanie oknem
 ┣ 📜 consts.py        # Stałe konfiguracyjne, kolory, ustawienia globalne
 ┣ 📜 resources.py     # Ładowanie i przetwarzanie grafik (Sprite Sheet)
 ┣ 📜 background.py    # Logika shaderów GLSL i renderowanie tła
 ┣ 📜 card.py          # Klasa Karty (fizyka, animacje, interakcja)
 ┣ 📜 menu.py          # Logika Menu Głównego
 ┣ 📜 options.py       # Logika Menu Opcji (Pop-up z suwakami)
 ┣ 📜 ui.py            # Komponenty interfejsu (Button, Slider, Checkbox)
 ┗ 🖼️ cards_sheet.png  # Atlas tekstur kart (Pixel Art)
```

---

## 🗺️ Roadmapa
Plany rozwoju projektu na najbliższe miesiące:

### Faza 1: Core Mechanics (Ukończona ✅)
- [x] Rendering kart i tła.
- [x] Podstawowe UI i Menu.
- [x] System shaderów CRT i Plasma.
- [x] Menu Opcji i obsługa ustawień.

### Faza 2: Logika Pokera (Następny krok 🚧)
- [ ] Algorytm sprawdzania układów (Para, Trójka, Full, Poker).
- [ ] System punktacji (Chips + Mult).
- [ ] Mechanika odrzucania i dobierania kart.
- [ ] Generowanie talii i losowość.

### Faza 3: Roguelike Elements
- [ ] Implementacja Jokerów (modyfikatory punktów).
- [ ] Sklep (kupowanie kart i ulepszeń).
- [ ] System Blindów (Boss Blinds).

### Faza 4: Audio & Polish
- [ ] Efekty dźwiękowe (SFX) przy klikaniu i punktacji.
- [ ] Muzyka w tle.
- [ ] System zapisu gry (Save/Load).

<br>

<div align="center">
Stworzono z ❤️ i ☕ używając Python & Pyglet.
<br>
<sub>Ten projekt jest fanowską wersją edukacyjną i nie jest powiązany z LocalThunk ani Playstack.</sub>
</div>