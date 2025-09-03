from .ParentBot import ParentBot
from treys import Card
import random
from itertools import combinations

class Coyote(ParentBot):
    """
    Example bot demonstrating the ParentBot interface.
    
    Coyote is a conservative player that:
    - Only plays premium hands
    - Folds to aggressive betting
    - Uses helper functions from ParentBot
    """
    
    def __init__(self, name="Coyote"):
        super().__init__(name=name)
        self.folded_hands = 0  # Track conservative behavior


    def make_decision(self, game_state):
        hole = self.hand
        community = game_state.community_cards
        stage = game_state.stage
        pot = game_state.pot
        to_call = game_state.to_call.get(self.name, 0)
        min_raise = game_state.min_raise
        stacks = game_state.active_player_stacks
        action_hist = game_state.action_history

        # --- Pre-flop: favor high, connected cards, but avoid risking too much of stack ---
        if stage == "pre-flop":
            ranks = [Card.get_rank_int(c) for c in hole]
            gap = abs(ranks[0] - ranks[1])
            high_card = max(ranks)
            low_card = min(ranks)
            pair = ranks[0] == ranks[1]
            suited = Card.get_suit_int(hole[0]) == Card.get_suit_int(hole[1])

            # Score: high cards, small gap, pair, suited
            score = high_card * 2 + (12 - gap) + (10 if pair else 0) + (2 if suited else 0)
            # Penalize low cards
            if low_card < 5:
                score -= 4

            # Risk management: don't risk more than 30% of stack pre-flop
            risk_limit = 0.3 * self.chips
            if to_call > risk_limit:
                return "fold"

            # Aggressive with high score
            if score >= 22:
                return "raise" if to_call == 0 else "call and raise"
            elif score >= 18:
                return "call" if to_call > 0 else "check"
            elif to_call == 0:
                return "check"
            else:
                return "fold"

        # --- Post-flop: simple hand evaluation without treys Evaluator ---
        all_cards = hole + community
        best_score = 0
        for combo in combinations(all_cards, 5):
            ranks = sorted([Card.get_rank_int(c) for c in combo], reverse=True)
            unique_ranks = set(ranks)
            is_pair = len(unique_ranks) == 4
            is_two_pair = len(unique_ranks) == 3
            is_trips = len(unique_ranks) == 3 and max(ranks.count(r) for r in unique_ranks) == 3
            is_straight = max(ranks) - min(ranks) == 4 and len(unique_ranks) == 5
            is_flush = len(set(Card.get_suit_int(c) for c in combo)) == 1
            # Score: flush > straight > trips > two pair > pair > high card
            score = 0
            if is_flush and is_straight:
                score = 100
            elif is_flush:
                score = 90
            elif is_straight:
                score = 80
            elif is_trips:
                score = 70
            elif is_two_pair:
                score = 60
            elif is_pair:
                score = 50
            else:
                score = max(ranks)
            if score > best_score:
                best_score = score

        # Risk management: don't risk more than 40% of stack post-flop
        risk_limit = 0.4 * self.chips
        if to_call > risk_limit:
            return "fold"

        # Aggressive with strong hand, but call if risk is high
        if best_score >= 90:
            if to_call > 0.25 * self.chips:
                return "call"
            return "raise" if to_call == 0 else "call and raise"
        elif best_score >= 70:
            return "call" if to_call > 0 else "check"
        elif best_score >= 50:
            return "call" if to_call > 0 else "check"
        elif to_call == 0:
            return "check"
        else:
            return "fold"