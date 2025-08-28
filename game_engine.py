from treys import Evaluator, Card
from typing import List, Tuple, Dict

class PokerGameEngine:
    """
    Handles all poker game logic including hand evaluation and ranking players.
    """
    
    def __init__(self):
        self.evaluator = Evaluator()
    
    def evaluate_preflop(self, players) -> List[Tuple[str, int, str]]:
        """
        Evaluate hole cards strength for all players using each bot's own evaluation.
        Returns list of (player_name, hand_strength, hand_description) sorted by strength.
        """
        player_strengths = []
        
        for player in players:
            # Use each player's own preflop evaluation method
            strength, description = player.evaluate_preflop()
            player_strengths.append((player.name, strength, description))
        
        # Sort by strength (lower score = better hand in treys convention)
        return sorted(player_strengths, key=lambda x: x[1])
    
    def evaluate_with_community(self, players, community_cards) -> List[Tuple[str, int, str]]:
        """
        Evaluate players' best hands using their hole cards + community cards.
        Returns list of (player_name, hand_rank, hand_description) sorted by strength.
        """
        player_hands = []
        
        for player in players:
            # Get best 5-card hand from 7 cards (2 hole + 5 community)
            best_hand = player.hand + community_cards
            hand_rank = self.evaluator.evaluate(player.hand, community_cards)
            hand_class = self.evaluator.get_rank_class(hand_rank)
            hand_description = self.evaluator.class_to_string(hand_class)
            
            player_hands.append((player.name, hand_rank, hand_description))
        
        # Sort by hand rank (lower = better in treys)
        return sorted(player_hands, key=lambda x: x[1])
    
    def evaluate_flop(self, players, flop_cards) -> List[Tuple[str, int, str]]:
        """Evaluate hands after the flop (3 community cards)."""
        return self.evaluate_with_community(players, flop_cards)
    
    def evaluate_turn(self, players, community_cards) -> List[Tuple[str, int, str]]:
        """Evaluate hands after the turn (4 community cards)."""
        return self.evaluate_with_community(players, community_cards)
    
    def evaluate_river(self, players, community_cards) -> List[Tuple[str, int, str]]:
        """Evaluate final hands after the river (5 community cards)."""
        return self.evaluate_with_community(players, community_cards)
    
    def get_subjective_evaluations(self, players, community_cards) -> List[Tuple[str, int, str]]:
        """
        Get subjective hand evaluations from each bot's perspective.
        Returns list of (player_name, hand_strength, hand_description) sorted by strength.
        """
        player_evaluations = []
        
        for player in players:
            strength, description = player.evaluate_hand(community_cards)
            player_evaluations.append((player.name, strength, description))
        
        # Sort by strength (lower = better)
        return sorted(player_evaluations, key=lambda x: x[1])
    
    def get_subjective_percentages(self, players, community_cards) -> Dict[str, float]:
        """
        Get subjective win percentages from each bot's perspective.
        These may not sum to 100% as they reflect individual bot psychology.
        """
        percentages = {}
        
        for player in players:
            percentage = player.get_win_percentage(community_cards)
            percentages[player.name] = percentage
        
        return percentages
    
    def get_monte_carlo_percentage(self, players, community_cards, simulations=1000) -> Dict[str, float]:
        """
        Calculate objective win percentages using Monte Carlo simulation.
        Simulates unknown cards and counts wins for each player.
        Percentages will sum to 100%.
        """
        from treys import Deck
        import random
        
        # Get all known cards to exclude from simulation
        known_cards = set()
        for player in players:
            known_cards.update(player.hand)
        known_cards.update(community_cards)
        
        # Create deck with only unknown cards
        full_deck = Deck()
        unknown_cards = [card for card in full_deck.cards if card not in known_cards]
        
        # How many more community cards do we need?
        cards_needed = 5 - len(community_cards)
        
        wins = {player.name: 0 for player in players}
        
        for _ in range(simulations):
            # Shuffle unknown cards and complete the board
            random.shuffle(unknown_cards)
            simulated_community = community_cards + unknown_cards[:cards_needed]
            
            # Evaluate all hands
            hand_scores = []
            for player in players:
                score = self.evaluator.evaluate(player.hand, simulated_community)
                hand_scores.append((player.name, score))
            
            # Find winner(s) - lower score is better in treys
            best_score = min(hand_scores, key=lambda x: x[1])[1]
            winners = [name for name, score in hand_scores if score == best_score]
            
            if len(winners) == 1:
                wins[winners[0]] += 1
            else:
                # Handle ties by giving fractional wins
                tie_value = 1.0 / len(winners)
                for winner in winners:
                    wins[winner] += tie_value
        
        # Convert to percentages
        percentages = {}
        for player_name, win_count in wins.items():
            percentage = (win_count / simulations) * 100
            percentages[player_name] = round(percentage, 1)
        
        return percentages
