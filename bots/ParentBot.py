from treys import Card
from typing import Tuple, List


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

    def evaluate_hand(self, community_cards) -> Tuple[int, str]:
        """
        Evaluate current hand strength with community cards.
        Returns (strength, description) where lower strength = better hand.
        Must be implemented by each bot.
        """
        raise NotImplementedError("Each bot must implement their own hand evaluation logic.")

    def evaluate_preflop(self) -> Tuple[int, str]:
        """
        Evaluate preflop hand strength and return (strength, description).
        Lower strength values indicate better hands.
        Must be implemented by each bot.
        """
        raise NotImplementedError("Each bot must implement their own preflop evaluation logic.")
    
    def get_win_percentage(self, community_cards) -> float:
        """
        Calculate subjective win percentage based on bot's own evaluation.
        Must be implemented by each bot.
        """
        raise NotImplementedError("Each bot must implement their own win percentage calculation.")

    def _describe_hole_cards(self) -> str:
        """Describe hole cards for preflop analysis using treys Card class."""
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
