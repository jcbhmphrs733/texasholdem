from .ParentBot import ParentBot

class Outlaw(ParentBot):
    def __init__(self):
        super().__init__(name="Outlaw")

    def make_decision(self, community_cards, pot, bets):
        # Randomized bluffing bot
        import random
        return random.choice(["call", "raise", "fold"])

    def evaluate_hand(self, community) -> tuple:
        """
        Outlaw's unpredictable hand evaluation.
        Randomly adjusts hand values to simulate unpredictable play.
        """
        from treys import Card
        import random
        
        if len(self.hand) != 2:
            return (9999, "No cards")
        
        card1_rank = Card.get_rank_int(self.hand[0])
        card2_rank = Card.get_rank_int(self.hand[1])
        
        # Standard evaluation with random variance
        if card1_rank == card2_rank:
            base_strength = card1_rank * 100
        elif Card.get_suit_int(self.hand[0]) == Card.get_suit_int(self.hand[1]):
            base_strength = (card1_rank + card2_rank) * 10
        else:
            base_strength = card1_rank + card2_rank
        
        # Add random variance to make evaluation unpredictable
        variance = random.randint(-200, 200)
        base_strength += variance
        
        max_possible = 12 * 100 + 200  # Account for positive variance
        strength = max_possible - base_strength
        description = self._describe_hole_cards()
        
        return (strength, description)
