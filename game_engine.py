from treys import Evaluator, Card
from typing import List, Tuple, Dict, Any

class PokerGameEngine:
    """
    Handles all poker game logic including betting rounds and hand evaluation.
    """
    
    def __init__(self):
        self.evaluator = Evaluator()
        self.round = 0 
        self.pot = 0
        self.current_bet = 0
        self.active_players = []  # Players still in the hand
        self.folded_players = []  # Players who have folded
        self.dealer_position = 0  # Index of dealer button
        self.small_blind = 10
        self.big_blind = 20
        self.min_raise = 20

    def start_new_hand(self, players):
        """Initialize a new poker hand with rotating dealer button."""
        self.players = players  # Store original player order
        self.pot = 0
        self.current_bet = 0
        self.active_players = players.copy()
        self.folded_players = []

        # Rotate dealer button
        num_players = len(players)
        dealer = players[self.dealer_position]
        
        # Small blind is next player after dealer
        small_blind_pos = (self.dealer_position + 1) % num_players
        small_blind_player = players[small_blind_pos]
        
        # Big blind is next player after small blind
        big_blind_pos = (self.dealer_position + 2) % num_players
        big_blind_player = players[big_blind_pos]
        
        # Post blinds
        small_blind_player.current_bet = self.small_blind
        big_blind_player.current_bet = self.big_blind
        small_blind_player.chips -= self.small_blind
        big_blind_player.chips -= self.big_blind
        self.pot = self.small_blind + self.big_blind
        self.current_bet = self.big_blind  # Minimum bet to call
        
        print(f"[D] Dealer: {dealer.name}")
        print(f"[$] {small_blind_player.name} posts small blind (${self.small_blind})")
        print(f"[$] {big_blind_player.name} posts big blind (${self.big_blind})")
        print(f"Starting pot: ${self.pot}")
        print()
        
        # Move dealer button for next hand
        self.dealer_position = (self.dealer_position + 1) % num_players

    def conduct_betting_round(self, community_cards, betting_round_name):
        """
        Conduct a complete betting round with proper turn order.
        Returns (hand_continues, action_history).
        """
        if len(self.active_players) <= 1:
            return False, []
            
        action_history = []
        from display import GameDisplay

        # Determine betting order based on dealer position
        num_players = len(self.players)

        # --- Build correct betting order ---
        betting_order = []
        sb_pos = (self.dealer_position + 1) % num_players
        bb_pos = (self.dealer_position + 2) % num_players
        if betting_round_name == "preflop":
            first_to_act_pos = (bb_pos + 1) % num_players
            # Order: [after BB, ..., dealer, SB, BB]
            for i in range(num_players):
                pos = (first_to_act_pos + i) % num_players
                player = self.players[pos]
                if player in self.active_players:
                    betting_order.append(player)
            # On the first pass, skip SB and BB (they already posted blinds)
            first_pass_skip = set([self.players[sb_pos], self.players[bb_pos]])
        else:
            # Postflop: action starts with player after dealer
            first_to_act_pos = (self.dealer_position + 1) % num_players
            for i in range(num_players):
                pos = (first_to_act_pos + i) % num_players
                player = self.players[pos]
                if player in self.active_players:
                    betting_order.append(player)
            first_pass_skip = set()

        # Track who has acted and who needs to match the current bet
        acted = set()
        first_pass = True
        while True:
            all_called = True
            for player in betting_order.copy():
                if player not in self.active_players:
                    continue
                # If player is all-in, skip
                if hasattr(player, 'chips') and player.chips == 0:
                    continue
                # On first pass of preflop, skip SB and BB
                if first_pass and player in first_pass_skip:
                    continue
                # If player has already matched the current bet and acted, skip
                if player.current_bet == self.current_bet and player in acted:
                    continue

                # Create game state for this player
                game_state = {
                    'hole_cards': player.hand,
                    'community_cards': community_cards,
                    'pot_size': self.pot,
                    'current_bet': self.current_bet,
                    'min_raise': self.min_raise,  # Use configured minimum raise
                    'betting_round': betting_round_name,
                    'position': betting_order.index(player),
                    'total_players': len(betting_order),
                    'action_history': action_history,
                    'opponent_stacks': {p.name: p.chips for p in self.active_players if p != player}
                }

                # Get player's decision
                decision = player.make_decision(game_state)

                # Process the decision
                action_result = self._process_action(player, decision)
                action_history.append(action_result)

                # Print step-by-step action
                print(f"[STEP] {player.name} ({player.chips} chips) action: {decision.upper()} amount: {action_result['amount']}")
                GameDisplay.wait_for_user("Press Enter for next action...")

                # Let all players observe this action
                game_state['last_action'] = action_result
                for observer in self.active_players:
                    observer.observe(game_state)

                acted.add(player)

                # If player raised, everyone needs to act again
                if decision == 'raise':
                    acted = set([player])
                    all_called = False
                elif player.current_bet != self.current_bet:
                    all_called = False

                if len(self.active_players) <= 1:
                    break

            first_pass = False
            # End loop if all active players have matched the current bet or folded
            if all_called or len(self.active_players) <= 1:
                break

        return len(self.active_players) > 1, action_history

    def _process_action(self, player, decision):
        """Process a player's action and update game state."""
        action_result = {
            'player': player.name,
            'action': decision,
            'amount': 0
        }
        
        if decision == 'fold':
            self.active_players.remove(player)
            self.folded_players.append(player)
            
        elif decision == 'call':
            call_amount = self.current_bet - player.current_bet
            player.chips -= call_amount
            player.current_bet = self.current_bet
            self.pot += call_amount
            action_result['amount'] = call_amount
            
        elif decision == 'check':
            if self.current_bet > player.current_bet:
                # Can't check if there's a bet to call - treat as fold
                self.active_players.remove(player)
                self.folded_players.append(player)
                action_result['action'] = 'fold (tried to check with bet)'
            
        elif decision == 'raise':
            call_amount = self.current_bet - player.current_bet
            total_amount = call_amount + self.min_raise
            
            player.chips -= total_amount
            player.current_bet = self.current_bet + self.min_raise
            self.current_bet = player.current_bet
            self.pot += total_amount
            action_result['amount'] = total_amount
            
        elif decision == 'all-in':
            all_in_amount = player.chips
            player.chips = 0
            player.current_bet += all_in_amount
            if player.current_bet > self.current_bet:
                self.current_bet = player.current_bet
            self.pot += all_in_amount
            action_result['amount'] = all_in_amount
        
        return action_result

    def get_winner(self, community_cards):
        """Determine the winner from active players."""
        if len(self.active_players) == 1:
            return self.active_players[0]
        
        # Evaluate hands to find winner
        best_rank = float('inf')
        winner = None
        
        for player in self.active_players:
            hand_rank = self.evaluator.evaluate(player.hand, community_cards)
            if hand_rank < best_rank:  # Lower is better in treys
                best_rank = hand_rank
                winner = player
        
        return winner

    def award_pot_to_winner(self, winner):
        """Transfer the pot to the winner and reset betting state."""
        winner.chips += self.pot
        pot_amount = self.pot
        
        # Reset betting state for all players
        for player in self.players:
            player.current_bet = 0
        
        # Reset pot
        self.pot = 0
        self.current_bet = 0
        
        return pot_amount

    # ===== COMPATIBILITY METHODS FOR DISPLAY SYSTEM =====
    # These allow the existing display system to work while we transition

    
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
