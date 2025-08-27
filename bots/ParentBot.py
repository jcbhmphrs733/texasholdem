class ParentBot:
    def __init__(self, name="Unnamed Bot"):
        self.name = name
        self.hand = []
        self.chips = 1000  # Starting stack
        self.current_bet = 0

    def receive_cards(self, cards):
        """Assign starting hand to bot"""
        self.hand = cards

    def observe(self, community_cards, pot, bets):
        """
        Called whenever the game state updates.
        Can be used to update strategy.
        """
        pass

    def make_decision(self, community_cards, pot, bets):
        """
        Decide action. Must return one of:
        'fold', 'check', 'call', 'raise', or 'all-in'
        """
        raise NotImplementedError("This bot has no decision logic yet.")
