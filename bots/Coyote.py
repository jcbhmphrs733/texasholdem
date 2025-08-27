from .ParentBot import ParentBot

class Coyote(ParentBot):
    def __init__(self):
        super().__init__(name="Coyote")

    def make_decision(self, community_cards, pot, bets):
        # Always calls if cheap, folds otherwise
        if bets and max(bets) > 100:
            return "fold"
        return "call"
