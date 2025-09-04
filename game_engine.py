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
            # Find the index of the previous dealer (if still present)
            idx = next((i for i, p in enumerate(players) if p.name == prev_dealer_name), None)
            if idx is not None:
                # Dealer survived, move to previous player (reverse direction)
                dealer_index = (idx - 1) % len(players)
            else:
                # Dealer was eliminated, find the player who was next after the dealer in the old list
                # (i.e., the first player after the old dealer who is still in the list)
                # For robustness, just rotate to the next available player
                dealer_index = 0
            game_state.dealer_index = dealer_index

        # Show chip counts and wait for user
        print("\nCurrent chip counts:")
        for p in players:
            print(f"{p.name}: {p.chips}")
        GameDisplay.wait_for_user("Press Enter to continue to the next stage...")
        if hand_over or len(players) <= 1:
            break


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
        print(f"\n[WIN] {win_names} win(s) the pot of {game_state.pot} chips with {win_desc}!")
        game_state.pot = 0
    elif len(active_players) == 1:
        winner = active_players[0]
        winner.chips += game_state.pot
        print(f"\n[WIN] {winner.name} wins the pot of {game_state.pot} chips! (everyone else folded)")
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