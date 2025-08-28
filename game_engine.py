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
    
    def get_winning_percentage(self, players, community_cards, simulations=1000) -> Dict[str, float]:
        """
        Calculate subjective win percentages based on each bot's own hand evaluation.
        Percentages may not sum to 100% as they reflect individual bot psychology.
        """
        percentages = {}
        
        if len(community_cards) == 0:
            # Preflop: Use each bot's preflop evaluation
            for player in players:
                strength, _ = player.evaluate_preflop()
                # Convert strength to percentage (lower strength = higher confidence)
                # Scale from 0-100% based on strength relative to possible range
                max_strength = 1800  # Worst possible hand strength
                min_strength = 0     # Best possible hand strength
                
                # Normalize to 0-100 range, then invert (lower strength = higher %)
                normalized = (max_strength - strength) / max_strength
                percentage = max(5, min(95, normalized * 100))  # Keep between 5-95%
                percentages[player.name] = round(percentage, 1)
        
        else:
            # Post-flop: Use actual hand evaluation with subjective adjustment
            for player in players:
                # Get objective hand strength
                hand_rank = self.evaluator.evaluate(player.hand, community_cards)
                
                # Apply subjective multiplier based on bot's preflop confidence
                preflop_strength, _ = player.evaluate_preflop()
                
                # Calculate confidence multiplier (how optimistic/pessimistic each bot is)
                if hasattr(player, 'name'):
                    if player.name == "Coyote":
                        confidence_multiplier = 0.8  # Conservative, underestimates chances
                    elif player.name == "Mirage":
                        confidence_multiplier = 1.3  # Aggressive, overestimates chances
                    elif player.name == "Outlaw":
                        import random
                        confidence_multiplier = random.uniform(0.5, 1.8)  # Unpredictable
                    else:
                        confidence_multiplier = 1.0  # Neutral
                else:
                    confidence_multiplier = 1.0
                
                # Convert hand rank to percentage (7462 is worst possible)
                base_percentage = ((7462 - hand_rank) / 7462) * 100
                
                # Apply subjective adjustment
                subjective_percentage = base_percentage * confidence_multiplier
                
                # Keep in reasonable bounds
                percentage = max(1, min(99, subjective_percentage))
                percentages[player.name] = round(percentage, 1)
        
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
