from treys import Deck
from bots.Outlaw import Outlaw
from bots.Mirage import Mirage
from bots.Coyote import Coyote
from game_engine import PokerGameEngine
from display import GameDisplay
import os

def texas_holdem_sim():
    """
    Main game simulation with comprehensive hand evaluation at each stage.
    """
    game_engine = PokerGameEngine()
    display = GameDisplay()
    
    while True:
        # Initialize new game
        deck = Deck()
        players = [Outlaw(), Mirage(), Coyote()]
        
        # Deal hole cards
        for bot in players:
            bot.receive_cards([deck.draw(1)[0], deck.draw(1)[0]])

        # === PREFLOP ===
        os.system('cls')
        display.display_stage_header("HOLE CARDS (PREFLOP)")
        display.display_hands(players)
        display.display_community([], "Community")
        preflop_rankings = game_engine.evaluate_preflop(players)
        display.display_hand_rankings(preflop_rankings, "Preflop Hand Strength")
        display.display_winning_percentages(game_engine.get_winning_percentage(players, []))
        display.wait_for_user("Press Enter to continue to the Flop...")

        # === FLOP ===
        flop = [deck.draw(1)[0] for _ in range(3)]
        display.display_stage_header("FLOP")
        display.display_hands(players)
        display.display_community(flop, "Community")
        flop_rankings = game_engine.evaluate_flop(players, flop)
        display.display_hand_rankings(flop_rankings, "Post-Flop Rankings")
        flop_percentages = game_engine.get_winning_percentage(players, flop)
        display.display_winning_percentages(flop_percentages)
        display.wait_for_user("Press Enter to continue to the Turn...")

        # === TURN ===
        flop.append(deck.draw(1)[0])  # Add turn card
        turn_cards = flop.copy()
        display.display_stage_header("TURN")
        display.display_hands(players)
        display.display_community(turn_cards, "Community")
        turn_rankings = game_engine.evaluate_turn(players, turn_cards)
        display.display_hand_rankings(turn_rankings, "Post-Turn Rankings")
        turn_percentages = game_engine.get_winning_percentage(players, turn_cards)
        display.display_winning_percentages(turn_percentages)
        display.wait_for_user("Press Enter to continue to the River...")

        # === RIVER ===
        turn_cards.append(deck.draw(1)[0])  # Add river card
        final_community = turn_cards.copy()
        display.display_stage_header("RIVER")
        display.display_hands(players)
        display.display_community(final_community, "Community")
        final_rankings = game_engine.evaluate_river(players, final_community)
        display.display_hand_rankings(final_rankings, "Final Rankings")
        final_percentages = game_engine.get_winning_percentage(players, final_community)
        display.display_winning_percentages(final_percentages)
        display.wait_for_user("Press Enter to start a new game...")

if __name__ == "__main__":
    texas_holdem_sim()
