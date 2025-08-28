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
        Evaluate hole cards strength for all players.
        Returns list of (player_name, hand_strength, hand_description) sorted by strength.
        """
        player_strengths = []
        
        for player in players:
            # For preflop, we can use a simple high card evaluation
            # or implement preflop hand rankings
            strength = self._evaluate_hole_cards(player.hand)
            description = self._describe_hole_cards(player.hand)
            player_strengths.append((player.name, strength, description))
        
        # Sort by strength (lower score = better hand in treys)
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
    
    def _evaluate_hole_cards(self, hole_cards) -> int:
        """
        Simple preflop evaluation. You can enhance this with proper preflop rankings.
        For now, just return high card value.
        """
        # Simple high card evaluation for preflop
        card1_rank = Card.get_rank_int(hole_cards[0])
        card2_rank = Card.get_rank_int(hole_cards[1])
        
        # Pair bonus
        if card1_rank == card2_rank:
            return card1_rank * 100  # Pairs get big bonus
        
        # Suited bonus
        if Card.get_suit_int(hole_cards[0]) == Card.get_suit_int(hole_cards[1]):
            return (card1_rank + card2_rank) * 10  # Suited gets bonus
        
        # Regular high card
        return card1_rank + card2_rank
    
    def _describe_hole_cards(self, hole_cards) -> str:
        """Describe hole cards for preflop analysis."""
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
    
    def get_winning_percentage(self, players, community_cards, simulations=1000) -> Dict[str, float]:
        """
        Calculate win percentages using Monte Carlo simulation.
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
        ties = 0
        
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
    
    def get_detailed_simulation(self, players, community_cards, simulations=10000) -> Dict:
        """
        Run a more detailed Monte Carlo simulation with additional statistics.
        Returns win percentages, tie information, and hand frequency analysis.
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
        hand_types = {player.name: {} for player in players}
        total_ties = 0
        
        for _ in range(simulations):
            # Shuffle unknown cards and complete the board
            random.shuffle(unknown_cards)
            simulated_community = community_cards + unknown_cards[:cards_needed]
            
            # Evaluate all hands and track hand types
            hand_scores = []
            for player in players:
                score = self.evaluator.evaluate(player.hand, simulated_community)
                hand_class = self.evaluator.get_rank_class(score)
                hand_name = self.evaluator.class_to_string(hand_class)
                
                # Track hand type frequency
                if hand_name not in hand_types[player.name]:
                    hand_types[player.name][hand_name] = 0
                hand_types[player.name][hand_name] += 1
                
                hand_scores.append((player.name, score))
            
            # Find winner(s)
            best_score = min(hand_scores, key=lambda x: x[1])[1]
            winners = [name for name, score in hand_scores if score == best_score]
            
            if len(winners) == 1:
                wins[winners[0]] += 1
            else:
                total_ties += 1
                tie_value = 1.0 / len(winners)
                for winner in winners:
                    wins[winner] += tie_value
        
        # Convert to percentages
        win_percentages = {}
        for player_name, win_count in wins.items():
            percentage = (win_count / simulations) * 100
            win_percentages[player_name] = round(percentage, 1)
        
        # Convert hand frequencies to percentages
        hand_frequencies = {}
        for player_name, hands in hand_types.items():
            hand_frequencies[player_name] = {}
            for hand_name, count in hands.items():
                percentage = (count / simulations) * 100
                hand_frequencies[player_name][hand_name] = round(percentage, 1)
        
        return {
            'win_percentages': win_percentages,
            'hand_frequencies': hand_frequencies,
            'total_simulations': simulations,
            'total_ties': total_ties,
            'tie_percentage': round((total_ties / simulations) * 100, 1)
        }
