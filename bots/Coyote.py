from .ParentBot import ParentBot
import random


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
        if game_state.bet_holder:
            return random.choice(["fold", "call", "call", "call", "call", "call and raise"])
        else:
            return random.choice(["fold", "check", "check", "check", "raise"])
        """
        # More aggressive decision making using ParentBot helpers.
        # # Use parent helper to evaluate hand strength
        # strength, description = self._evaluate_hand_strength(
        #     game_state['hole_cards'], 
        #     game_state['community_cards']
        # )
        
        # # Use parent helper to calculate pot odds
        # pot_odds = self._calculate_pot_odds(
        #     game_state['pot_size'], 
        #     game_state['current_bet']
        # )
        
        # # Use parent helper to analyze betting patterns
        # betting_analysis = self._analyze_betting_pattern(
        #     game_state['action_history']
        # )
        
        # # More aggressive decision logic
        # if strength < 1000:  # Strong hand - always raise
        #     return 'raise'
        # elif strength < 2500:  # Decent hand - call or raise based on odds
        #     if pot_odds > 20 or len(game_state['community_cards']) == 0:  # Preflop or good odds
        #         return 'call' if game_state['current_bet'] > 0 else 'check'
        #     else:
        #         return 'raise'  # Be aggressive
        # elif strength < 4000 and pot_odds > 25:  # Marginal hand with good odds
        #     return 'call' if game_state['current_bet'] > 0 else 'check'
        # elif strength < 5000 and game_state['current_bet'] == 0:  # Weak hand, but free card
        #     return 'check'
        # elif strength < 6000 and pot_odds > 40:  # Very marginal, but great odds
        #     return 'call'
        # else:
        #     # Only fold truly terrible hands or bad odds
        #     self.folded_hands += 1
        #     return 'fold'
        """

    def observe(self, game_state):
        """
        Learn from game events (simple implementation for now).
        """
        # Could track opponent betting patterns, hand outcomes, etc.
        # For now, just log interesting events
        if 'last_action' in game_state:
            last_action = game_state['last_action']
            if last_action.get('action') == 'raise' and last_action.get('amount', 0) > 200:
                # Someone made a big raise - note this for future decisions
                pass