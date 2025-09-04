from game_state import GameState
from treys import Evaluator, Card, Deck
from typing import List, Tuple, Dict, Any
from bots.Coyote import Coyote
from display import GameDisplay


def run_betting_round(game_state):
    players = game_state.players
    num_players = len(players)
    dealer = game_state.dealer_index
    stage = game_state.stage

    # --- Pot and betting setup ---
    if not hasattr(game_state, 'pot'):
        game_state.pot = 0
    if not hasattr(game_state, 'min_raise'):
        game_state.min_raise = 20
    if not hasattr(game_state, 'current_bet'):
        game_state.current_bet = 0

    # Determine blinds
    if len([p for p in players if not p.folded]) == 2:
        small_blind_index = (dealer + 1) % num_players
        big_blind_index = dealer
    else:
        small_blind_index = (dealer + 1) % num_players
        big_blind_index = (dealer + 2) % num_players

    small_blind = players[small_blind_index]
    big_blind = players[big_blind_index]

    # Pre-flop mandatory blinds
    if stage == "pre-flop":
        print(f"{small_blind.name} posts SMALL blind (mandatory raise).")
        sb_amt = 10
        small_blind.chips -= sb_amt
        small_blind.current_bet = sb_amt
        game_state.pot += sb_amt

        print(f"{big_blind.name} posts BIG blind (mandatory raise).")
        bb_amt = 20
        big_blind.chips -= bb_amt
        big_blind.current_bet = bb_amt
        game_state.pot += bb_amt
        game_state.current_bet = bb_amt

        # Pre-flop first acting player
        if len([p for p in players if not p.folded]) == 2:
            current_index = small_blind_index
        else:
            current_index = (big_blind_index + 1) % num_players
    else:
        # Reset current_bet for all players for new stage
        for p in players:
            p.current_bet = 0
        game_state.current_bet = 0
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
            # Award pot to winner
            winner.chips += game_state.pot
            print(f"{winner.name} wins the pot of {game_state.pot} chips!")
            game_state.pot = 0
            return True

        # Calculate amount to call
        to_call = game_state.current_bet - player.current_bet
        min_raise = game_state.min_raise

        # Player decision
        action, amount = player.make_decision(game_state)
        print(f"{player.name} decides to {action.upper()}.")

        if action == "fold":
            player.folded = True
            acted_players.add(player)
        elif action == "call":
            # Player matches current bet
            call_amt = amount
            if call_amt > 0:
                player.chips -= call_amt
                player.current_bet += call_amt
                game_state.pot += call_amt
            print(f"{player.name} CALLS for {call_amt} chips.")
        elif action == "raise":
            raise_amt = amount
            to_call = game_state.current_bet - player.current_bet
            total_amt = to_call + raise_amt
            player.chips -= total_amt
            player.current_bet += total_amt
            game_state.pot += total_amt
            game_state.current_bet = player.current_bet
            print(f"{player.name} RAISES to {player.current_bet} chips.")
        elif action == "check":
            print(f"{player.name} checks.")
            acted_players.add(player)
        elif action in ["raise", "call and raise"]:
            # Player must call, then raise
            to_call = game_state.current_bet - player.current_bet
            raise_amt = min_raise
            total_amt = to_call + raise_amt
            player.chips -= total_amt
            player.current_bet += total_amt
            game_state.pot += total_amt
            game_state.current_bet = player.current_bet
            print(f"--- {player.name} RAISES --- for total {total_amt} chips (call {to_call} + raise {raise_amt})")
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


def play_hand(players, dealer_index):
    # === Setup deck and deal hole cards ===
    deck = Deck()
    for p in players:
        p.hand = [deck.draw(1)[0], deck.draw(1)[0]]
        p.folded = False
        p.current_bet = 0

    game_state = GameState(players)
    game_state.dealer_index = dealer_index
    hand_over = False

    # Display initial hands
    GameDisplay.display_stage_header("NEW HAND")
    GameDisplay.display_hands(players, dealer_index)

    # === Betting rounds and community cards ===
    community_cards = []

    for stage in game_state.stages:
        game_state.reset_for_stage(stage)
        if stage == "flop":
            community_cards = [deck.draw(1)[0] for _ in range(3)]
            GameDisplay.display_stage_header("FLOP")
            GameDisplay.display_community(community_cards, "Flop")
        elif stage == "turn":
            community_cards.append(deck.draw(1)[0])
            GameDisplay.display_stage_header("TURN")
            GameDisplay.display_community(community_cards, "Turn")
        elif stage == "river":
            community_cards.append(deck.draw(1)[0])
            GameDisplay.display_stage_header("RIVER")
            GameDisplay.display_community(community_cards, "River")

        hand_over = run_betting_round(game_state)

        # Track the dealer's name before eliminations
        prev_dealer_name = players[game_state.dealer_index].name if players else None

        # Remove broke players after each stage
        broke_players = [p for p in players if p.chips <= 0]
        for p in broke_players:
            print(f"[ELIMINATED] {p.name} is out of chips and eliminated from the game!")
            players.remove(p)

        # After eliminations, update dealer_index to next player after previous dealer
        if players and prev_dealer_name:
            idx = next((i for i, p in enumerate(players) if p.name == prev_dealer_name), None)
            if idx is not None:
                dealer_index = (idx - 1) % len(players)
            else:
                dealer_index = 0
            game_state.dealer_index = dealer_index

        # Show chip counts and wait for user
        print("\nCurrent chip counts:")
        for p in players:
            print(f"{p.name}: {p.chips}")
        GameDisplay.wait_for_user("Press Enter to continue to the next stage...")

        # Prevent next stage if only one player remains
        active_players = [p for p in players if not p.folded]
        if hand_over or len(active_players) <= 1:
            return dealer_index

    # === Showdown and hand evaluation ===
    active_players = [p for p in players if not p.folded]
    if len(active_players) > 1:
        evaluator = Evaluator()
        hand_ranks = []
        for p in active_players:
            rank = evaluator.evaluate(p.hand, community_cards)
            desc = evaluator.class_to_string(evaluator.get_rank_class(rank))
            hand_ranks.append((p, rank, desc))
        hand_ranks.sort(key=lambda x: x[1])
        best_rank = hand_ranks[0][1]
        winners = [p for p, r, d in hand_ranks if r == best_rank]
        win_names = ", ".join([w.name for w in winners])
        win_desc = hand_ranks[0][2]
        # Split pot if tie
        pot_share = game_state.pot // len(winners)
        for w in winners:
            w.chips += pot_share
        GameDisplay.display_game_summary(
            [(p.name, r, d) for p, r, d in hand_ranks], community_cards
        )
        print(
            f"\n[WIN] {win_names} win(s) the pot of {game_state.pot} chips with {win_desc}!")
        game_state.pot = 0
    elif len(active_players) == 1:
        winner = active_players[0]
        winner.chips += game_state.pot
        print(
            f"\n[WIN] {winner.name} wins the pot of {game_state.pot} chips! (everyone else folded)")
        game_state.pot = 0

    # Pause before new hand
    GameDisplay.wait_for_user("Press Enter to start a new hand...")

    # Final dealer_index update and print
    if len(players) > 0:
        print(f"\nDealer button moves to {players[dealer_index].name}.")
    else:
        print("\nNo players left to rotate dealer.")
    print("\n=== Hand complete ===")
    return dealer_index
