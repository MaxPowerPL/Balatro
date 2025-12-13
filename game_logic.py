import random
from collections import Counter
import consts

SUITS = ['pik', 'kier', 'trefl', 'karo']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'walet', 'dama', 'krol', 'as']

class Deck:
    def __init__(self):
        self.cards = []; self.reset()
    def reset(self):
        self.cards = [(s, v) for s in SUITS for v in VALUES]
        self.shuffle()
    def shuffle(self): random.shuffle(self.cards)
    def draw(self, count):
        return [self.cards.pop() for _ in range(count) if self.cards]
    def remaining(self): return len(self.cards)

class HandEvaluator:
    @staticmethod
    def evaluate(cards):
        if not cards: return "High Card", 0, 0, 0

        sorted_cards = sorted(cards, key=lambda c: c.rank_val)
        ranks = [c.rank_val for c in sorted_cards]
        suits = [c.suit for c in sorted_cards]
        counts = Counter(ranks)
        counts_sorted = sorted(counts.items(), key=lambda x: (-x[1], -x[0])) # Ilość malejąco

        # --- DETEKCJA ---

        # Kolor: Czy mamy 5 kart w tym samym kolorze?
        # Warunek: Musi być dokładnie 5 kart wybranych do zagrania, i wszystkie muszą mieć ten sam kolor.
        is_flush = (len(cards) == 5) and (len(set(suits)) == 1)

        # Strit
        unique_ranks = sorted(list(set(ranks)))
        is_straight = False
        if len(unique_ranks) >= 5:
            for i in range(len(unique_ranks) - 4):
                if unique_ranks[i+4] - unique_ranks[i] == 4: is_straight = True; break
            if not is_straight and 14 in unique_ranks: # As jako 1
                low_ace = [1 if r==14 else r for r in unique_ranks]
                low_ace.sort()
                for i in range(len(low_ace) - 4):
                    if low_ace[i+4] - low_ace[i] == 4: is_straight = True; break

        hand_name = "High Card"
        scoring_cards = []

        # --- HIERARCHIA (Poprawiona) ---

        # 1. Poker Królewski / Poker
        if is_flush and is_straight:
            if set(ranks).issuperset({10, 11, 12, 13, 14}): hand_name = "Royal Flush"
            else: hand_name = "Straight Flush"
            scoring_cards = sorted_cards

        # 2. Kareta
        elif counts_sorted[0][1] == 4:
            hand_name = "Four of a Kind"
            target = counts_sorted[0][0]
            scoring_cards = [c for c in sorted_cards if c.rank_val == target]

        # 3. Full
        elif counts_sorted[0][1] == 3 and len(counts_sorted) > 1 and counts_sorted[1][1] >= 2:
            hand_name = "Full House"
            scoring_cards = sorted_cards

        # 4. Kolor (Flush) - TUTAJ BYŁ BŁĄD, TERAZ JEST WYŻEJ
        elif is_flush:
            hand_name = "Flush"
            scoring_cards = sorted_cards

        # 5. Strit
        elif is_straight:
            hand_name = "Straight"
            scoring_cards = sorted_cards

        # 6. Trójka
        elif counts_sorted[0][1] == 3:
            hand_name = "Three of a Kind"
            target = counts_sorted[0][0]
            scoring_cards = [c for c in sorted_cards if c.rank_val == target]

        # 7. Dwie Pary
        elif counts_sorted[0][1] == 2 and len(counts_sorted) > 1 and counts_sorted[1][1] == 2:
            hand_name = "Two Pair"
            t1, t2 = counts_sorted[0][0], counts_sorted[1][0]
            scoring_cards = [c for c in sorted_cards if c.rank_val in (t1, t2)]

        # 8. Para
        elif counts_sorted[0][1] == 2:
            hand_name = "Pair"
            target = counts_sorted[0][0]
            scoring_cards = [c for c in sorted_cards if c.rank_val == target]

        # 9. Wysoka Karta
        else:
            hand_name = "High Card"
            if sorted_cards: scoring_cards = [sorted_cards[-1]]

        base_chips, base_mult = consts.HAND_SCORES[hand_name]
        card_chips = sum(c.chips_val for c in scoring_cards)
        return hand_name, base_chips + card_chips, base_mult, (base_chips + card_chips) * base_mult