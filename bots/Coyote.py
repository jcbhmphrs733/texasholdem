from .ParentBot import ParentBot

class Coyote(ParentBot):
    def __init__(self):
        super().__init__(name="Coyote")

    def make_decision(self, community_cards, pot, bets):
        # Always calls if cheap, folds otherwise
        if bets and max(bets) > 100:
            return "fold"
        return "call"

    def evaluate_preflop(self) -> tuple:
        """
        Coyote's conservative preflop evaluation.
        Heavily penalizes weak hands and favors strong pairs.
        """
        from treys import Card
        
        if len(self.hand) != 2:
            return (9999, "No cards")
        
        card1_rank = Card.get_rank_int(self.hand[0])
        card2_rank = Card.get_rank_int(self.hand[1])
        
        # Conservative evaluation - really favor pairs
        if card1_rank == card2_rank:
            base_strength = card1_rank * 150  # Extra bonus for pairs
        elif Card.get_suit_int(self.hand[0]) == Card.get_suit_int(self.hand[1]):
            base_strength = (card1_rank + card2_rank) * 8  # Less bonus for suited
        else:
            base_strength = (card1_rank + card2_rank) * 0.5  # Penalize offsuit
        
        max_possible = 12 * 150
        strength = max_possible - base_strength
        description = self._describe_hole_cards()
        
        return (strength, description)
