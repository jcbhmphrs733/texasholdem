from .ParentBot import ParentBot
from treys import Card


class Outlaw(ParentBot):
    def __init__(self):
        super().__init__(name="Outlaw")

from .ParentBot import ParentBot
from treys import Card


class Outlaw(ParentBot):
    def __init__(self):
        super().__init__(name="Outlaw")

    def make_decision(self, community_cards, pot, bets):
        # Randomized bluffing bot
        import random
        return random.choice(["call", "raise", "fold"])

    def evaluate_hand(self, community_cards):
        """
        Outlaw's wild hand evaluation for all stages.
        Returns (strength, description) where lower = better.
        """
        if len(community_cards) == 0:
            return self.evaluate_preflop()
        else:
            # Post-flop evaluation - wild approach
            return self._evaluate_postflop(community_cards)

    def evaluate_preflop(self):
        """
        Outlaw's wild preflop evaluation.
        Loves low cards and weird combinations.
        """
        if len(self.hand) != 2:
            return (9999, "No cards")
        
        card1_rank = Card.get_rank_int(self.hand[0])
        card2_rank = Card.get_rank_int(self.hand[1])
        card1_suit = Card.get_suit_int(self.hand[0])
        card2_suit = Card.get_suit_int(self.hand[1])
        
        # Wild evaluation - loves low cards and gapped hands
        if card1_rank == card2_rank:
            if card1_rank <= 6:  # Low pairs are "cool"
                base_strength = (7 - card1_rank) * 150
            else:
                base_strength = card1_rank * 50  # High pairs are "boring"
        elif card1_suit == card2_suit:
            # Loves suited gaps
            gap = abs(card1_rank - card2_rank)
            if gap >= 3:
                base_strength = gap * 50  # Big gaps are exciting
            else:
                base_strength = (card1_rank + card2_rank) * 8
        else:
            # Weird offsuit combinations
            if min(card1_rank, card2_rank) <= 4:  # Low cards
                base_strength = 100 + (card1_rank + card2_rank) * 5
            else:
                base_strength = (card1_rank + card2_rank) * 3
        
        max_possible = 6 * 150
        strength = max_possible - base_strength
        description = self._describe_hole_cards()
        
        return (strength, description)

    def _evaluate_postflop(self, community_cards):
        """
        Wild post-flop evaluation.
        Unpredictable assessments of hand strength.
        """
        all_cards = self.hand + community_cards
        
        # Wild hand recognition - unpredictable values
        import random
        wild_factor = random.uniform(0.5, 2.0)  # Random multiplier
        
        if self._has_flush(all_cards):
            return (int(200 * wild_factor), "Flush (wild confidence)")
        elif self._has_straight(all_cards):
            return (int(250 * wild_factor), "Straight (wild confidence)")
        elif self._has_trips(all_cards):
            return (int(400 * wild_factor), "Three of a kind (wild)")
        elif self._has_two_pair(all_cards):
            return (int(800 * wild_factor), "Two pair (wild)")
        elif self._has_pair(all_cards):
            # Outlaw values low pairs highly
            lowest_rank = min(Card.get_rank_int(card) for card in self.hand)
            if lowest_rank <= 4:
                return (int(600 * wild_factor), "Low pair (outlaw special)")
            else:
                return (int(1400 * wild_factor), "High pair (boring)")
        elif self._has_nothing_special(all_cards):
            return (int(1800 * wild_factor), "Chaos hand (bluff time)")
        else:
            return (int(3000 * wild_factor), "Mystery hand")

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
    
    def _has_nothing_special(self, cards):
        """Check for weird combinations Outlaw likes."""
        ranks = [Card.get_rank_int(card) for card in cards]
        # Likes disconnected low cards
        return len(set(ranks)) == len(ranks) and max(ranks) - min(ranks) > 6

    def get_win_percentage(self, community_cards):
        """
        Outlaw's erratic win percentage calculation.
        Either very high or very low confidence.
        """
        strength, _ = self.evaluate_hand(community_cards)
        
        # Outlaw is unpredictable - either very confident or very pessimistic
        card1_rank = Card.get_rank_int(self.hand[0])
        if card1_rank % 2 == 0:  # Even cards make him confident
            if strength < 500:
                percentage = 90
            elif strength < 1000:
                percentage = 75
            elif strength < 2000:
                percentage = 55
            else:
                percentage = 35
        else:  # Odd cards make him doubt
            if strength < 500:
                percentage = 60
            elif strength < 1000:
                percentage = 40
            elif strength < 2000:
                percentage = 20
            else:
                percentage = 10
        
        return round(percentage, 1)
