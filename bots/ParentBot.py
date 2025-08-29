from treys import Card
from typing import Tuple, List, Dict, Any
from abc import ABC, abstractmethod


class ParentBot(ABC):
    def __init__(self, name="Unnamed Bot"):
        self.name = name
        self.hand = []
        self.chips = 1000  # Starting stack
        self.current_bet = 0
        self.game_history = []  # For learning bots

    def receive_cards(self, cards):
        """Assign starting hand to bot"""
        self.hand = cards

    @abstractmethod
    def make_decision(self, game_state: Dict[str, Any]) -> str:
        """
        Make a poker decision based on current game state.
        
        Args:
            game_state: Dictionary containing all game information:
                - 'hole_cards': Your two cards [card1, card2]
                - 'community_cards': Board cards (0-5 cards)
                - 'pot_size': Current pot amount
                - 'current_bet': Amount you need to call
                - 'min_raise': Minimum raise amount
                - 'betting_round': 'preflop', 'flop', 'turn', or 'river'
                - 'position': Your seat position (0=button, 1=small blind, etc.)
                - 'action_history': List of actions this round
                - 'opponent_stacks': Other players' chip counts
                - 'previous_hands': History for learning (optional)
        
        Returns:
            str: One of 'fold', 'call', 'check', 'raise', or 'all-in'
        """
        pass

    @abstractmethod  
    def observe(self, game_state: Dict[str, Any]) -> None:
        """
        Called after each action to let bot learn/adapt.
        
        Args:
            game_state: Same structure as make_decision, but includes
                       the action that just happened and its results.
        
        Simple bots can ignore this (just use 'pass').
        Advanced bots can track opponent patterns, betting history, etc.
        """
        pass

    # ===== HELPER FUNCTIONS FOR PARTICIPANTS =====
    # These are optional utilities to help guide bot development

    def _evaluate_hand_strength(self, hole_cards: List, community_cards: List) -> Tuple[int, str]:
        """
        Helper function to evaluate hand strength.
        Returns (strength, description) where lower strength = better hand.
        
        Example usage in your make_decision:
            strength, desc = self._evaluate_hand_strength(
                game_state['hole_cards'], 
                game_state['community_cards']
            )
            if strength < 500:  # Strong hand
                return 'raise'
        """
        if not community_cards:
            return self._evaluate_preflop(hole_cards)
        else:
            # Simple post-flop evaluation - participants can improve this
            return self._simple_postflop_eval(hole_cards, community_cards)

    def _evaluate_preflop(self, hole_cards: List) -> Tuple[int, str]:
        """
        Helper: Evaluate preflop hand strength.
        Participants can override this or use as starting point.
        """
        if len(hole_cards) != 2:
            return (9999, "No cards")
        
        card1_rank = Card.get_rank_int(hole_cards[0])
        card2_rank = Card.get_rank_int(hole_cards[1])
        card1_suit = Card.get_suit_int(hole_cards[0])
        card2_suit = Card.get_suit_int(hole_cards[1])
        
        # Basic preflop evaluation
        if card1_rank == card2_rank:
            base_strength = card1_rank * 100  # Pairs
        elif card1_suit == card2_suit:
            base_strength = (card1_rank + card2_rank) * 10  # Suited
        else:
            base_strength = card1_rank + card2_rank  # Offsuit
        
        max_possible = 12 * 100
        strength = max_possible - base_strength
        description = self._describe_hole_cards(hole_cards)
        
        return (strength, description)

    def _simple_postflop_eval(self, hole_cards: List, community_cards: List) -> Tuple[int, str]:
        """
        Helper: Basic post-flop evaluation.
        Participants can create much more sophisticated versions.
        """
        all_cards = hole_cards + community_cards
        
        # Very basic hand recognition
        if self._has_pair(all_cards):
            return (1500, "Pair or better")
        else:
            return (3000, "High card")

    def _calculate_pot_odds(self, pot_size: int, bet_to_call: int) -> float:
        """
        Helper: Calculate pot odds percentage.
        
        Example usage:
            pot_odds = self._calculate_pot_odds(
                game_state['pot_size'], 
                game_state['current_bet']
            )
            if pot_odds > 25:  # Good pot odds
                return 'call'
        """
        if bet_to_call == 0:
            return 100.0
        return (pot_size / (pot_size + bet_to_call)) * 100

    def _analyze_betting_pattern(self, action_history: List) -> Dict[str, Any]:
        """
        Helper: Analyze recent betting patterns.
        Returns info about aggression, betting trends, etc.
        
        Example usage:
            pattern = self._analyze_betting_pattern(game_state['action_history'])
            if pattern['aggressive_players'] > 2:
                return 'fold'  # Too much action
        """
        aggressive_actions = ['raise', 'all-in']
        total_actions = len(action_history)
        aggressive_count = sum(1 for action in action_history 
                             if action.get('action') in aggressive_actions)
        
        return {
            'total_actions': total_actions,
            'aggressive_actions': aggressive_count,
            'aggression_ratio': aggressive_count / max(1, total_actions),
            'last_action': action_history[-1] if action_history else None
        }

    # ===== UTILITY FUNCTIONS =====

    def _describe_hole_cards(self, hole_cards: List) -> str:
        """Describe hole cards for logging/debugging."""
        if len(hole_cards) != 2:
            return "No cards"
            
        card1_rank = Card.get_rank_int(hole_cards[0])
        card2_rank = Card.get_rank_int(hole_cards[1])
        card1_suit = Card.get_suit_int(hole_cards[0])
        card2_suit = Card.get_suit_int(hole_cards[1])
        
        if card1_rank == card2_rank:
            rank_str = Card.STR_RANKS[card1_rank]
            return f"Pocket {rank_str}s"
        
        suited = "suited" if card1_suit == card2_suit else "offsuit"
        high_rank = Card.STR_RANKS[max(card1_rank, card2_rank)]
        low_rank = Card.STR_RANKS[min(card1_rank, card2_rank)]
        
        return f"{high_rank}{low_rank} {suited}"

    def _has_pair(self, cards: List) -> bool:
        """Check if cards contain any pair."""
        ranks = [Card.get_rank_int(card) for card in cards]
        return len(ranks) != len(set(ranks))
