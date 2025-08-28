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

    def evaluate_preflop(self) -> tuple:
        """
        Evaluate preflop hand strength and return (strength, description).
        Lower strength values indicate better hands (consistent with treys).
        Override this method to implement custom preflop evaluation.
        """
        from treys import Card
        
        if len(self.hand) != 2:
            return (9999, "No cards")
        
        # Simple high card evaluation for preflop
        card1_rank = Card.get_rank_int(self.hand[0])
        card2_rank = Card.get_rank_int(self.hand[1])
        
        # Calculate base strength (higher = stronger)
        if card1_rank == card2_rank:
            base_strength = card1_rank * 100  # Pairs get big bonus
        elif Card.get_suit_int(self.hand[0]) == Card.get_suit_int(self.hand[1]):
            base_strength = (card1_rank + card2_rank) * 10  # Suited gets bonus
        else:
            base_strength = card1_rank + card2_rank  # Regular high card
        
        # Invert to match treys convention (lower = better)
        max_possible = 12 * 100  # Pocket Aces would be 12 * 100 = 1200
        strength = max_possible - base_strength
        
        # Generate description
        description = self._describe_hole_cards()
        
        return (strength, description)
    
    def _describe_hole_cards(self) -> str:
        """Describe hole cards for preflop analysis."""
        from treys import Card
        
        if len(self.hand) != 2:
            return "No cards"
            
        card1_rank = Card.get_rank_int(self.hand[0])
        card2_rank = Card.get_rank_int(self.hand[1])
        card1_suit = Card.get_suit_int(self.hand[0])
        card2_suit = Card.get_suit_int(self.hand[1])
        
        if card1_rank == card2_rank:
            rank_str = Card.STR_RANKS[card1_rank]
            return f"Pocket {rank_str}s"
        
        suited = "suited" if card1_suit == card2_suit else "offsuit"
        high_rank = Card.STR_RANKS[max(card1_rank, card2_rank)]
        low_rank = Card.STR_RANKS[min(card1_rank, card2_rank)]
        
        return f"{high_rank}{low_rank} {suited}"
