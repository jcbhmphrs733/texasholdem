from treys import Deck
from bots.Coyote import Coyote
from game_engine import PokerGameEngine
from display import GameDisplay
import os

def texas_holdem_sim():
    """
    Main game simulation with actual poker gameplay including betting rounds.
    """
    game_engine = PokerGameEngine()
    display = GameDisplay()
    
    while True:
        # Initialize new game
        deck = Deck()
        players = [
            Coyote(name="The Coyote"),
            Coyote(name="The Wolf"),
            Coyote(name="The Pup"),
            Coyote(name="The Fox"),
        ]
        
        # Deal hole cards
        for bot in players:
            bot.receive_cards([deck.draw(1)[0], deck.draw(1)[0]])

        # Start the hand
        game_engine.start_new_hand(players)
        
        os.system('cls')
        print("[POKER] NEW POKER HAND STARTING")
        print("=" * 50)
        
        # Show initial hands
        current_dealer = (game_engine.dealer_position - 1) % len(players)  # -1 because button rotated
        display.display_hands(players, current_dealer)
        print(f"Pot: ${game_engine.pot}")
        print(f"Active players: {[p.name for p in game_engine.active_players]}")
        
        # === PREFLOP BETTING ===
        print("\n[BET] PREFLOP BETTING ROUND")
        print("-" * 30)
        
        hand_continues, preflop_actions = game_engine.conduct_betting_round([], "preflop")
        display.display_actions(preflop_actions, "Preflop Actions")
        
        print(f"After preflop - Pot: ${game_engine.pot}")
        print(f"Active: {[p.name for p in game_engine.active_players]}")
        print(f"Folded: {[p.name for p in game_engine.folded_players]}")
        
        if not hand_continues:
            winner = game_engine.get_winner([])
            pot_won = game_engine.award_pot_to_winner(winner)
            print(f"\n[WIN] {winner.name} wins ${pot_won} (everyone else folded)")
            display.wait_for_user("Press Enter to start a new game...")
            continue

        display.wait_for_user("Press Enter to continue to the Flop...")

        # === FLOP ===
        flop = [deck.draw(1)[0] for _ in range(3)]
        print(f"\n[FLOP] FLOP")
        display.display_community(flop, "Flop")
        
        hand_continues, flop_actions = game_engine.conduct_betting_round(flop, "flop")
        display.display_actions(flop_actions, "Flop Actions")
        print(f"After flop - Pot: ${game_engine.pot}")
        print(f"Active: {[p.name for p in game_engine.active_players]}")
        
        if not hand_continues:
            winner = game_engine.get_winner(flop)
            pot_won = game_engine.award_pot_to_winner(winner)
            print(f"\n[WIN] {winner.name} wins ${pot_won}")
            display.wait_for_user("Press Enter to start a new game...")
            continue

        display.wait_for_user("Press Enter to continue to the Turn...")

        # === TURN ===
        turn_card = deck.draw(1)[0]
        turn_cards = flop + [turn_card]
        print(f"\n[TURN] TURN")
        display.display_community(turn_cards, "Turn")
        
        hand_continues, turn_actions = game_engine.conduct_betting_round(turn_cards, "turn")
        display.display_actions(turn_actions, "Turn Actions")
        print(f"After turn - Pot: ${game_engine.pot}")
        print(f"Active: {[p.name for p in game_engine.active_players]}")
        
        if not hand_continues:
            winner = game_engine.get_winner(turn_cards)
            pot_won = game_engine.award_pot_to_winner(winner)
            print(f"\n[WIN] {winner.name} wins ${pot_won}")
            display.wait_for_user("Press Enter to start a new game...")
            continue

        display.wait_for_user("Press Enter to continue to the River...")

        # === RIVER ===
        river_card = deck.draw(1)[0]
        river_cards = turn_cards + [river_card]
        print(f"\n[RIVER] RIVER")
        display.display_community(river_cards, "River")
        
        hand_continues, river_actions = game_engine.conduct_betting_round(river_cards, "river")
        display.display_actions(river_actions, "River Actions")
        print(f"After river - Pot: ${game_engine.pot}")
        print(f"Active: {[p.name for p in game_engine.active_players]}")

        # === SHOWDOWN ===
        winner = game_engine.get_winner(river_cards)
        pot_won = game_engine.award_pot_to_winner(winner)
        print(f"\n[WIN] SHOWDOWN - {winner.name} wins ${pot_won}!")
        
        # Show final hands
        final_rankings = game_engine.evaluate_with_community(game_engine.active_players, river_cards)
        display.display_hand_rankings(final_rankings, "Final Hand Rankings")
        
        display.wait_for_user("Press Enter to start a new game...")

if __name__ == "__main__":
    texas_holdem_sim()
