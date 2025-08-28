from .ParentBot import ParentBot
from treys import Card


class Coyote(ParentBot):
    def __init__(self):
        super().__init__(name="Coyote")

    def make_decision(self, community_cards, pot, bets):
        # Always calls if cheap, folds otherwise
        if bets and max(bets) > 100:
            return "fold"
        return "call"

    def evaluate_hand(self, community_cards):
        """
        Coyote's conservative hand evaluation for all stages.
        Returns (strength, description) where lower = better.
        """
        if len(community_cards) == 0:
            return self.evaluate_preflop()
        else:
            # Post-flop evaluation - conservative approach
            return self._evaluate_postflop(community_cards)

    def evaluate_preflop(self):
        """
        Coyote's conservative preflop evaluation.
        Heavily penalizes weak hands and favors strong pairs.
        """
        if len(self.hand) != 2:
            return (9999, "No cards")
        
        card1_rank = Card.get_rank_int(self.hand[0])
        card2_rank = Card.get_rank_int(self.hand[1])
        card1_suit = Card.get_suit_int(self.hand[0])
        card2_suit = Card.get_suit_int(self.hand[1])
        
        # Conservative evaluation - really favor pairs
        if card1_rank == card2_rank:
            base_strength = card1_rank * 150  # Extra bonus for pairs
        elif card1_suit == card2_suit:
            base_strength = (card1_rank + card2_rank) * 8  # Less bonus for suited
        else:
            base_strength = (card1_rank + card2_rank) * 0.5  # Penalize offsuit
        
        max_possible = 12 * 150
        strength = max_possible - base_strength
        description = self._describe_hole_cards()
        
        return (strength, description)

    def _evaluate_postflop(self, community_cards):
        """
        Conservative post-flop evaluation.
        Only confident with strong made hands.
        """
        all_cards = self.hand + community_cards
        
        # Simple hand recognition - conservative bias
        if self._has_pair(all_cards):
            if self._has_trips(all_cards):
                return (200, "Three of a kind (conservative)")
            elif self._has_two_pair(all_cards):
                return (800, "Two pair (conservative)")
            else:
                return (1500, "One pair (conservative)")
        elif self._has_straight_draw(all_cards):
            return (3000, "Straight draw (too risky)")
        elif self._has_flush_draw(all_cards):
            return (2800, "Flush draw (too risky)")
        else:
            return (4000, "High card (fold)")

    def _has_pair(self, cards):
        """Check for any pair."""
        ranks = [Card.get_rank_int(card) for card in cards]
        return len(ranks) != len(set(ranks))
    
    def _has_trips(self, cards):
        """Check for three of a kind."""
        ranks = [Card.get_rank_int(card) for card in cards]
        rank_counts = {}
        for rank in ranks:
            rank_counts[rank] = rank_counts.get(rank, 0) + 1
        return 3 in rank_counts.values()
    
    def _has_two_pair(self, cards):
        """Check for two pair."""
        ranks = [Card.get_rank_int(card) for card in cards]
        rank_counts = {}
        for rank in ranks:
            rank_counts[rank] = rank_counts.get(rank, 0) + 1
        pairs = sum(1 for count in rank_counts.values() if count >= 2)
        return pairs >= 2
    
    def _has_straight_draw(self, cards):
        """Conservative straight draw check."""
        ranks = sorted(set(Card.get_rank_int(card) for card in cards))
        # Only open-ended straight draws
        for i in range(len(ranks) - 3):
            if ranks[i+3] - ranks[i] == 3:
                return True
        return False
    
    def _has_flush_draw(self, cards):
        """Conservative flush draw check."""
        suits = [Card.get_suit_int(card) for card in cards]
        suit_counts = {}
        for suit in suits:
            suit_counts[suit] = suit_counts.get(suit, 0) + 1
        return 4 in suit_counts.values()  # Only 4-card flush draws

    def get_win_percentage(self, community_cards):
        """
        Coyote's conservative win percentage calculation.
        Always underestimates chances.
        """
        strength, _ = self.evaluate_hand(community_cards)
        
        # Conservative mapping - always pessimistic
        if strength < 500:
            percentage = 85  # Great hand but still cautious
        elif strength < 1000:
            percentage = 65  # Good hand but worried
        elif strength < 2000:
            percentage = 35  # Okay hand but nervous
        elif strength < 3000:
            percentage = 15  # Weak hand, very pessimistic
        else:
            percentage = 5   # Terrible hand, wants to fold
        
        return round(percentage, 1)
