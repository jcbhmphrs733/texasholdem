from .ParentBot import ParentBot

class Mirage(ParentBot):
    def __init__(self):
        super().__init__(name="Mirage")

    def make_decision(self, community_cards, pot, bets):
        # Mirage plays aggressively
        return "raise" if pot < 200 else "call"

    def evaluate_preflop(self) -> tuple:
        """
        Mirage's aggressive preflop evaluation.
        Values suited connectors and big cards highly.
        """
        from treys import Card
        
        if len(self.hand) != 2:
            return (9999, "No cards")
        
        card1_rank = Card.get_rank_int(self.hand[0])
        card2_rank = Card.get_rank_int(self.hand[1])
        
        # Aggressive evaluation - loves suited hands and high cards
        if card1_rank == card2_rank:
            base_strength = card1_rank * 100  # Standard pair bonus
        elif Card.get_suit_int(self.hand[0]) == Card.get_suit_int(self.hand[1]):
            # Extra bonus for suited connectors
            if abs(card1_rank - card2_rank) <= 2:
                base_strength = (card1_rank + card2_rank) * 15  # Connector bonus
            else:
                base_strength = (card1_rank + card2_rank) * 12  # High suited bonus
        else:
            # Still decent for high offsuit cards
            base_strength = (card1_rank + card2_rank) * 2
        
        max_possible = 12 * 100
        strength = max_possible - base_strength
        description = self._describe_hole_cards()
        
        return (strength, description)
