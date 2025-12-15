from core.game_logic import Deck, HandEvaluator
from core.card import Card
import config.consts as consts

class GameManager:
    """Zarządzanie mechanikami gry"""

    def __init__(self, game_state, window, batch, card_group):
        self.state = game_state
        self.window = window
        self.batch = batch
        self.card_group = card_group
        self.deck = Deck()

    def draw_cards(self, count):
        """Dobieranie kart z talii"""
        for _ in range(count):
            if self.deck.remaining() > 0:
                c_data = self.deck.draw(1)[0]
                card = Card(
                    c_data[0], c_data[1],
                    self.window.width // 2,
                    self.window.height // 2,
                    self.batch, self.card_group
                )
                self.state.my_hand.append(card)

    def play_hand(self, ui_manager):
        """Zagranie wybranych kart"""
        selected = [c for c in self.state.my_hand if c.is_selected]

        if not selected or len(selected) > 5 or self.state.hands_left <= 0:
            return False

        # Ewaluacja układu
        name, chips, mult, total = HandEvaluator.evaluate(selected)

        # Aktualizacja statystyk
        if name in self.state.hand_stats:
            self.state.hand_stats[name] += 1

        self.state.round_score += total
        self.state.hands_left -= 1

        # Usuwanie i dobieranie
        for c in selected:
            c.delete()
            self.state.my_hand.remove(c)

        self.draw_cards(self.state.MAX_HAND_SIZE - len(self.state.my_hand))
        ui_manager.update_values()

        return True

    def discard_hand(self, ui_manager):
        """Odrzucenie wybranych kart"""
        selected = [c for c in self.state.my_hand if c.is_selected]

        if not selected or len(selected) > 5 or self.state.discards_left <= 0:
            return False

        self.state.discards_left -= 1

        for c in selected:
            c.delete()
            self.state.my_hand.remove(c)

        self.draw_cards(self.state.MAX_HAND_SIZE - len(self.state.my_hand))
        ui_manager.update_values()

        return True

    def check_game_end(self, ui_manager):
        """Sprawdzenie warunków końca gry"""
        if self.state.round_score >= self.state.target_score:
            # Wygrana rundy
            self.state.reset_round()
            self.deck.reset()

            for c in self.state.my_hand:
                c.delete()
            self.state.my_hand.clear()

            self.draw_cards(self.state.MAX_HAND_SIZE)
            ui_manager.update_values()

        elif self.state.hands_left <= 0:
            # Przegrana
            self.state.current_state = consts.STATE_GAME_OVER
            ui_manager.overlay_gameover.show(False)

    def sort_by_rank(self):
        """Sortowanie kart po randze"""
        self.state.my_hand.sort(key=lambda c: c.rank_val, reverse=True)

    def sort_by_suit(self):
        """Sortowanie kart po kolorze"""
        self.state.my_hand.sort(key=lambda c: (c.suit, c.rank_val))
