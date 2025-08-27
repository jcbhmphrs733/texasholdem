from .ParentBot import ParentBot

class Mirage(ParentBot):
    def __init__(self):
        super().__init__(name="Mirage")

    def make_decision(self, community_cards, pot, bets):
        # Mirage plays aggressively
        return "raise" if pot < 200 else "call"
