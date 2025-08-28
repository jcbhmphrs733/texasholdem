from treys import Deck
from bots.Outlaw import Outlaw
from bots.Mirage import Mirage
from bots.Coyote import Coyote
from game_engine import PokerGameEngine
from display import GameDisplay
from utils import Utils
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

        def display_comprehensive_analysis(players, community_cards, stage_name):
            """Display all analysis tables for a given stage."""
            display.display_stage_header(stage_name)
            
            # 1. Player hole cards
            display.display_hands(players)
            
            # 2. Community cards
            display.display_community(community_cards, "Community")
            
            # 3. Bot subjective hand rankings and win percentages
            subjective_rankings = game_engine.get_subjective_evaluations(players, community_cards)
            display.display_hand_rankings(subjective_rankings, "Bot Subjective Hand Rankings")
            
            subjective_percentages = game_engine.get_subjective_percentages(players, community_cards)
            display.display_winning_percentages(subjective_percentages, "Bot Subjective Win Chances")
            
            # 4. Objective treys rankings
            if community_cards:
                objective_rankings = game_engine.evaluate_with_community(players, community_cards)
            else:
                objective_rankings = game_engine.evaluate_preflop(players)
            display.display_hand_rankings(objective_rankings, "Objective Hand Rankings (Treys)")
            
            # 5. Monte Carlo win percentages
            monte_carlo_percentages = game_engine.get_monte_carlo_percentage(players, community_cards)
            display.display_winning_percentages(monte_carlo_percentages, "Monte Carlo Win Percentages")

        # === PREFLOP ===
        os.system('cls')
        display_comprehensive_analysis(players, [], "HOLE CARDS (PREFLOP)")
        display.wait_for_user("Press Enter to continue to the Flop...")

        # === FLOP ===
        flop = [deck.draw(1)[0] for _ in range(3)]
        display_comprehensive_analysis(players, flop, "FLOP")
        display.wait_for_user("Press Enter to continue to the Turn...")

        # === TURN ===
        turn_cards = flop + [deck.draw(1)[0]]
        display_comprehensive_analysis(players, turn_cards, "TURN")
        display.wait_for_user("Press Enter to continue to the River...")

        # === RIVER ===
        river_cards = turn_cards + [deck.draw(1)[0]]
        display_comprehensive_analysis(players, river_cards, "RIVER")
        
        # Final game summary
        display.display_game_summary(game_engine.evaluate_with_community(players, river_cards), river_cards)
        
        display.wait_for_user("Press Enter to start a new game...")

if __name__ == "__main__":
    texas_holdem_sim()
