from .ParentBot import ParentBot
from treys import Card


class Mirage(ParentBot):
    def __init__(self):
        super().__init__(name="Mirage")

    def make_decision(self, community_cards, pot, bets):
        # Mirage plays aggressively
        return "raise" if pot < 200 else "call"

    def evaluate_hand(self, community_cards):
        """
        Mirage's aggressive hand evaluation for all stages.
        Returns (strength, description) where lower = better.
        """
        if len(community_cards) == 0:
            return self.evaluate_preflop()
        else:
            # Post-flop evaluation - aggressive approach
            return self._evaluate_postflop(community_cards)

    def evaluate_preflop(self):
        """
        Mirage's aggressive preflop evaluation.
        Values suited connectors and big cards highly.
        """
        if len(self.hand) != 2:
            return (9999, "No cards")
        
        card1_rank = Card.get_rank_int(self.hand[0])
        card2_rank = Card.get_rank_int(self.hand[1])
        card1_suit = Card.get_suit_int(self.hand[0])
        card2_suit = Card.get_suit_int(self.hand[1])
        
        # Aggressive evaluation - loves suited hands and high cards
        if card1_rank == card2_rank:
            base_strength = card1_rank * 100  # Standard pair bonus
        elif card1_suit == card2_suit:
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

    def _evaluate_postflop(self, community_cards):
        """
        Aggressive post-flop evaluation.
        Confident with draws and made hands.
        """
        all_cards = self.hand + community_cards
        
        # Aggressive hand recognition
        if self._has_flush(all_cards):
            return (100, "Flush")
        elif self._has_straight(all_cards):
            return (150, "Straight")
        elif self._has_trips(all_cards):
            return (300, "Three of a kind")
        elif self._has_two_pair(all_cards):
            return (600, "Two pair")
        elif self._has_pair(all_cards):
            return (1200, "One pair")
        elif self._has_flush_draw(all_cards):
            return (1000, "Flush draw")
        elif self._has_straight_draw(all_cards):
            return (1100, "Straight draw")
        else:
            return (2500, "High card")

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
    
    def _has_straight(self, cards):
        """Check for straight."""
        ranks = sorted(set(Card.get_rank_int(card) for card in cards))
        if len(ranks) < 5:
            return False
        for i in range(len(ranks) - 4):
            if ranks[i+4] - ranks[i] == 4:
                return True
        return False
    
    def _has_flush(self, cards):
        """Check for flush."""
        suits = [Card.get_suit_int(card) for card in cards]
        suit_counts = {}
        for suit in suits:
            suit_counts[suit] = suit_counts.get(suit, 0) + 1
        return 5 in suit_counts.values()
    
    def _has_straight_draw(self, cards):
        """Aggressive straight draw check - includes gutshots."""
        ranks = sorted(set(Card.get_rank_int(card) for card in cards))
        # Check for any 4-card straight possibility
        for i in range(len(ranks) - 3):
            if ranks[i+3] - ranks[i] <= 4:
                return True
        return False
    
    def _has_flush_draw(self, cards):
        """Aggressive flush draw check."""
        suits = [Card.get_suit_int(card) for card in cards]
        suit_counts = {}
        for suit in suits:
            suit_counts[suit] = suit_counts.get(suit, 0) + 1
        return max(suit_counts.values()) >= 4  # 4-card flush draws

    def get_win_percentage(self, community_cards):
        """
        Mirage's aggressive win percentage calculation.
        Always overestimates chances.
        """
        strength, _ = self.evaluate_hand(community_cards)
        
        # Aggressive mapping - always optimistic
        if strength < 300:
            percentage = 95  # Great hand, very confident
        elif strength < 800:
            percentage = 80  # Good hand, confident
        elif strength < 1500:
            percentage = 60  # Okay hand, still optimistic
        elif strength < 2000:
            percentage = 40  # Weak hand but hopeful
        else:
            percentage = 25  # Bad hand but might bluff
        
        return round(percentage, 1)
