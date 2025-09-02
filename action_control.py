import random


class Player:
    def __init__(self, name):
        self.name = name
        self.chips = 1000
        self.current_bet = 0
        self.hand = []

    def make_decision(self, game_state):
        # Simplified decision-making process
        action_history = game_state.get('action_history', [])
        if game_state.get('bet_holder'):
            return random.choice(["fold", "call", "call and raise"])
        else:
            return random.choice(["fold", "check", "raise"])


players = [Player(name='tom'), Player(name='eric'), Player(name='johhny'), Player(
    name='bob'), Player(name='craig'), Player(name='alice'), Player(name='dave')]


for round in range(2):  # play two rounds

    active_players = players[:]

    print("Now starting round " + str(round))

    action_history = []  # List of (player, action) tuples
    folded_players = []
    dealer_position = 0

    game_state = {
        'round': round,
        'bet_holder': None,
        'active_players': active_players,
        'action_history': action_history,
        'folded_players': folded_players
    }

    for stage in range(4):  # preflop, flop, turn, river
        print("players in " + ("preflop:" if stage == 0 else "flop:" if stage ==
              1 else "turn:" if stage == 2 else "river:"))
        print(", ".join([p.name for p in active_players]), end=", ")
        print()

        active_pos = dealer_position + 3
        bet_holder = None
        acted_players = set()

        while True:  # individual player decision loop
            if len(active_players) == 0:
                break
            active_pos = active_pos % len(active_players)  # Always wrap index
            player = active_players[active_pos]
            print(f"\nIt's {player.name}'s turn to act. Active pos: {active_pos}")

            # Update game state for this player
            game_state = {
                'round': round,
                'bet_holder': bet_holder,
                'active_players': active_players,
                'action_history': action_history,
                'folded_players': folded_players
            }
            action = player.make_decision(game_state)
            action_history.append((player, action))

            print(f"{player.name} chooses to {action}")
            acted_players.add(player)
            folded_this_turn = False
            if action == 'fold':  # player folded and will be removed from betting
                folded_players.append(player)
                # Remove player from active_players immediately
                del active_players[active_pos]
                folded_this_turn = True
                # If only one player left, end the round immediately
                if len(active_players) == 1:
                    print(f"\nOnly one player remains: {active_players[0].name}. Ending round.")
                    break
                if len(active_players) == 0:
                    break
            # player raised and will be current bet holder when game state updates
            elif action == 'raise' or action == 'call and raise':
                bet_holder = player
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
            if not folded_this_turn:
                active_pos += 1

            # Move to next player
            active_pos += 1

        # Remove folded players
        active_players = [p for p in active_players if p not in folded_players]
            # If only one player remains after a stage, end the hand immediately
        if len(active_players) == 1:
            print(f"Hand ends early. Winner: {active_players[0].name}")
            break

    print(f"Round {round} over - *new dealer.*")