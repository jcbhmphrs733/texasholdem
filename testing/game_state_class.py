import random

class GameState:
    def __init__(self, players):
        self.players = players
        self.dealer_index = 0
        self.bet_holder = None  # Tracks last raiser
        self.stage = "pre-flop"
        self.stages = ["pre-flop", "flop", "turn", "river"]
        self.active_players = [p for p in players]

    def reset_for_stage(self, stage):
        self.stage = stage
        self.bet_holder = None
        print(f"\n=== Starting {stage.upper()} ===")
        self.debug_active_players()

    def debug_active_players(self):
        active = [p.name for p in self.active_players if not p.folded]
        print(f"Active Players: {active}")

class Player:
    def __init__(self, name):
        self.name = name
        self.folded = False

    def make_decision(self, game_state):
        # Updated decision-making process
        if game_state.bet_holder:
            return random.choice(["fold", "call", "call", "call", "call", "call and raise"])
        else:
            return random.choice(["fold", "check", "check", "check", "raise"])

def run_betting_round(game_state):
    players = game_state.players
    num_players = len(players)
    dealer = game_state.dealer_index
    stage = game_state.stage

    # Determine blinds
    if len([p for p in players if not p.folded]) == 2:
        big_blind_index = dealer
        small_blind_index = (dealer + 1) % num_players
    else:
        small_blind_index = (dealer + 1) % num_players
        big_blind_index = (small_blind_index + 1) % num_players

    small_blind = players[small_blind_index]
    big_blind = players[big_blind_index]

    # Pre-flop mandatory blinds
    if stage == "pre-flop":
        print(f"{small_blind.name} posts SMALL blind (mandatory raise).")
        game_state.bet_holder = small_blind

        print(f"{big_blind.name} posts BIG blind (mandatory call + raise).")
        game_state.bet_holder = big_blind

        # Pre-flop first acting player
        if len([p for p in players if not p.folded]) == 2:
            current_index = small_blind_index
        else:
            current_index = (big_blind_index + 1) % num_players
    else:
        current_index = small_blind_index
        game_state.bet_holder = None  # No active raise yet

    acted_players = set()
    stage_over = False

    while not stage_over:
        player = players[current_index]

        if player.folded:
            current_index = (current_index + 1) % num_players
            continue

        # End hand if only one player remains
        active_players = [p for p in players if not p.folded]
        if len(active_players) == 1:
            winner = active_players[0]
            print(f"\n{winner.name} wins the hand! Everyone else folded.")
            return True

        # Player decision
        decision = player.make_decision(game_state)
        print(f"{player.name} decides to {decision.upper()}.")

        if decision == "fold":
            player.folded = True
            acted_players.add(player)
        elif decision == "call":
            print(f"{player.name} CALLS.")
            acted_players.add(player)
        elif decision == "check":
            print(f"{player.name} CHECKS.")
            acted_players.add(player)
        elif decision in ["raise", "call and raise"]:
            print(f"--- {player.name} RAISES ---")
            game_state.bet_holder = player
            # Reset acted_players; only raiser has acted so far
            acted_players = {player}

        # Advance turn
        current_index = (current_index + 1) % num_players

        # Stage ends if all active players except bet_holder have acted
        active_players = [p for p in players if not p.folded]
        if all(p in acted_players or p == game_state.bet_holder for p in active_players):
            stage_over = True

    print(f"=== {stage.upper()} betting round is over ===")
    return False

def play_hand(players):
    game_state = GameState(players)
    hand_over = False

    for stage in game_state.stages:
        game_state.reset_for_stage(stage)
        hand_over = run_betting_round(game_state)
        if hand_over:
            break

    # Rotate dealer
    game_state.dealer_index = (game_state.dealer_index + 1) % len(players)
    print("\n=== Hand complete ===")

# Example usage
players = [Player("Alice"), Player("Bob"), Player("Charlie"), Player("David"), Player("Erika")]
play_hand(players)
