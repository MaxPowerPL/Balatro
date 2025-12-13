import random
from collections import Counter
import consts

SUITS = ['pik', 'kier', 'trefl', 'karo']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'walet', 'dama', 'krol', 'as']

class Deck:
    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        """Tworzy nową, pełną talię 52 kart."""
        self.cards = []
        for suit in SUITS:
            for val in VALUES:
                # Przechowujemy krotki (suit, value_str)
                self.cards.append((suit, val))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, count):
        """Dobiera 'count' kart. Zwraca listę krotek."""
        drawn = []
        for _ in range(count):
            if self.cards:
                drawn.append(self.cards.pop())
        return drawn

    def remaining(self):
        return len(self.cards)

class HandEvaluator:
    @staticmethod
    def evaluate(cards):
        """
        Analizuje listę obiektów Card i zwraca:
        (Nazwa Układu, Punkty, Mnożnik, Lista kart punktujących)
        """
        if not cards:
            return "Brak kart", 0, 0, []

        # Sortujemy karty po rank_val (2..14)
        sorted_cards = sorted(cards, key=lambda c: c.rank_val)
        ranks = [c.rank_val for c in sorted_cards]
        suits = [c.suit for c in sorted_cards]

        # Zliczamy powtórzenia (np. {14: 2, 10: 2} -> dwie pary Asów i 10)
        counts = Counter(ranks)
        # Sortujemy powtórzenia: najpierw ilość, potem wartość (np. Kareta 5 > Trójka Asów)
        counts_sorted = sorted(counts.items(), key=lambda x: (-x[1], -x[0]))

        # Sprawdzanie Koloru (Flush)
        is_flush = len(set(suits)) == 1 and len(cards) >= 5

        # Sprawdzanie Strita (Straight)
        # Unikalne rangi, posortowane
        unique_ranks = sorted(list(set(ranks)))
        is_straight = False

        # Sprawdzamy ciągłość 5 kart
        if len(unique_ranks) >= 5:
            for i in range(len(unique_ranks) - 4):
                window = unique_ranks[i:i+5]
                if window[-1] - window[0] == 4:
                    is_straight = True
                    break
            # Specjalny przypadek: As jako 1 (A, 2, 3, 4, 5)
            if not is_straight and 14 in unique_ranks:
                low_ace_ranks = [1 if r == 14 else r for r in unique_ranks]
                low_ace_ranks.sort()
                for i in range(len(low_ace_ranks) - 4):
                    window = low_ace_ranks[i:i+5]
                    if window[-1] - window[0] == 4:
                        is_straight = True
                        break

        # --- LOGIKA HIERARCHII ---
        hand_name = "High Card"
        scoring_cards = [] # Karty, które biorą udział w układzie (do podświetlenia)

        # 1. Poker Królewski / Poker (Straight Flush)
        if is_flush and is_straight:
            hand_name = "Straight Flush" # W uproszczeniu, Royal to po prostu wysoki SF
            scoring_cards = sorted_cards # Wszystkie 5

        # 2. Kareta (4 of a Kind)
        elif counts_sorted[0][1] == 4:
            hand_name = "Four of a Kind"
            rank_to_find = counts_sorted[0][0]
            scoring_cards = [c for c in sorted_cards if c.rank_val == rank_to_find]

        # 3. Full (3 + 2)
        elif counts_sorted[0][1] == 3 and len(counts_sorted) > 1 and counts_sorted[1][1] >= 2:
            hand_name = "Full House"
            r1 = counts_sorted[0][0]
            r2 = counts_sorted[1][0]
            scoring_cards = [c for c in sorted_cards if c.rank_val == r1 or c.rank_val == r2]

        # 4. Kolor (Flush)
        elif is_flush:
            hand_name = "Flush"
            scoring_cards = sorted_cards # Wszystkie 5

        # 5. Strit (Straight)
        elif is_straight:
            hand_name = "Straight"
            scoring_cards = sorted_cards # Wszystkie 5 (uproszczenie)

        # 6. Trójka (3 of a Kind)
        elif counts_sorted[0][1] == 3:
            hand_name = "Three of a Kind"
            r1 = counts_sorted[0][0]
            scoring_cards = [c for c in sorted_cards if c.rank_val == r1]

        # 7. Dwie Pary (2 + 2)
        elif counts_sorted[0][1] == 2 and len(counts_sorted) > 1 and counts_sorted[1][1] == 2:
            hand_name = "Two Pair"
            r1 = counts_sorted[0][0]
            r2 = counts_sorted[1][0]
            scoring_cards = [c for c in sorted_cards if c.rank_val == r1 or c.rank_val == r2]

        # 8. Para (2)
        elif counts_sorted[0][1] == 2:
            hand_name = "Pair"
            r1 = counts_sorted[0][0]
            scoring_cards = [c for c in sorted_cards if c.rank_val == r1]

        # 9. Wysoka Karta
        else:
            hand_name = "High Card"
            # W High Card punktuje tylko najwyższa karta
            if sorted_cards:
                scoring_cards = [sorted_cards[-1]]

        # --- OBLICZANIE PUNKTÓW ---
        base_chips, base_mult = consts.HAND_SCORES[hand_name]

        # Sumujemy chipsy z kart PUNKTUJĄCYCH
        card_chips = sum(c.chips_val for c in scoring_cards)

        total_chips = base_chips + card_chips
        total_score = total_chips * base_mult

        return hand_name, total_chips, base_mult, total_score