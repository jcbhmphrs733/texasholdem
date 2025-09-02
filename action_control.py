import random


class Player:
    def __init__(self, name):
        self.name = name
        self.chips = 1000
        self.current_bet = 0
        self.hand = []
        self.folded = False

    def make_decision(self, game_state):
        # Simplified decision-making process
        action_history = game_state.get('action_history', [])
        if game_state.get('bet_holder'):
            return random.choice(["fold", "call", "call and raise"])
        else:
            return random.choice(["fold", "check", "raise"])


players = [Player(name='alice'), Player(name='bob'), Player(name='craig'),  Player(name='dave')]

dealer_position = 0

for round in range(1):  # play one round

    active_players = players[:]
    action_history = []  # List of (player, action) tuples
    folded_players = []

    game_state = {
        'round': round,
        'bet_holder': None,
        'active_players': active_players,
        'action_history': action_history,
        'folded_players' : folded_players,
    }

    for stage in range(4):  # preflop, flop, turn, river
        print("players in " + ("preflop:" if stage == 0 else "flop:" if stage ==
              1 else "turn:" if stage == 2 else "river:"))
        print(", ".join([p.name for p in active_players]), end=", ")
        print()

        bet_holder = None
        acted_players = set()

        for active_player in active_players: # individual player decision loop
            
            if not active_player.folded:
                print(f"\nIt's {active_player.name}'s turn to act. Active pos: {active_pos}")
            
            else:
                break # skip players that have already folded.
                

            # Update game state for this player
            game_state = {
                'round': round,
                'bet_holder': bet_holder,
                'active_players': active_players,
                'action_history': action_history,
                
            }
            action = active_player.make_decision(game_state) # player makes decision
            action_history.append((active_player, action)) # record decision in game state action history

            print(f"{active_player.name} chooses to {action}")
            
            acted_players.add(active_player)
            
            if action == 'fold':  # player folded and will be removed from betting
                # Remove player from active_players immediately
                folded_players.append(active_player)
                # If only one player left, end the round immediately
                if len(active_players) == 1:
                    print(f"\nOnly one player remains: {active_players[0].name}. Ending round.")
                    break
                
            # player raised and will be current bet holder when game state updates
            elif action == 'raise' or action == 'call and raise':
                bet_holder = active_player
                # After a raise, everyone except the raiser needs to act again
                acted_players = set([bet_holder])

            # If all active players except bet_holder have acted, and no new raise, move to next stage
            if bet_holder is not None:
                others = set(active_players) - set([bet_holder])
                if others.issubset(acted_players):
                    print(f"\nAll players except {bet_holder.name} have acted. Betting round complete.")
                    break
            else:
                if len(acted_players) == len(active_players):
                    print("\nAll players checked or folded. Moving to next stage")
                    print("Players advancing to next stage:", (", ".join([p.name for p in active_players])))
                    break

            # Only increment active_pos if we did NOT remove a player (i.e., if not folded)
            if not active_player.folded:
                active_pos += 1

        if len(active_players) == 1:
            print(f"Hand ends early. Winner: {active_players[0].name}")
            break

    print(f"Round {round} over - *new dealer.*")