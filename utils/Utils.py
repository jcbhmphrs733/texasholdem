from treys import Card, Evaluator

def _calculate_player_rankings(players, community_cards):
    """Calculate and return player rankings based on their hands and community cards."""
    evaluator = Evaluator()
    return {player.name: evaluator.evaluate(player.hand, community_cards) for player in players}

def _calculate_player_win_percentages(players, community_cards):
    """Calculate and return player winning percentages based on their hands and community cards."""
    evaluator = Evaluator()
    return {player.name: evaluator.get_five_card_hand(player.hand + community_cards) for player in players}

def _describe_hole_cards(self) -> str:
        """Describe hole cards for preflop analysis."""
        
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

