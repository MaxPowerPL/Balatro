import config.consts as consts

class GameState:
    """Centralne zarządzanie stanem gry"""

    def __init__(self):
        self.current_state = consts.STATE_MENU
        self.is_options_open = False

        # Stan rozgrywki
        self.hands_left = 4
        self.discards_left = 3
        self.round_score = 0
        self.target_score = 300
        self.money = 4
        self.round_num = 1

        # Statystyki użycia układów
        self.hand_stats = {k: 0 for k in consts.HAND_SCORES.keys()}

        # Karty
        self.my_hand = []
        self.MAX_HAND_SIZE = 8

    def reset_round(self):
        """Reset rundy po wygranej"""
        self.money += 5
        self.round_num += 1
        self.round_score = 0
        self.target_score = int(self.target_score * 1.5)
        self.hands_left = 4
        self.discards_left = 3

    def reset_game(self):
        """Pełny reset gry"""
        self.hands_left = 4
        self.discards_left = 3
        self.round_score = 0
        self.target_score = 300
        self.money = 4
        self.round_num = 1
        for k in self.hand_stats:
            self.hand_stats[k] = 0
