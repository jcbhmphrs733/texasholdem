from .ParentBot import ParentBot

class Outlaw(ParentBot):
    def __init__(self):
        super().__init__(name="Outlaw")

    def make_decision(self, community_cards, pot, bets):
        # Randomized bluffing bot
        import random
        return random.choice(["call", "raise", "fold"])
