from treys import Deck
from bots.Outlaw import Outlaw
from bots.Mirage import Mirage
from bots.Coyote import Coyote
from game_engine import PokerGameEngine
from display import GameDisplay

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

        # === PREFLOP ANALYSIS ===
        display.display_stage_header("HOLE CARDS (PREFLOP)")
        display.display_hands(players)
        
        # Evaluate preflop hand strength
        preflop_rankings = game_engine.evaluate_preflop(players)
        display.display_hand_rankings(preflop_rankings, "Preflop Hand Strength")
        
        display.wait_for_user("Press Enter to continue to the Flop...")

        # === FLOP ===
        flop = [deck.draw(1)[0] for _ in range(3)]
        display.display_stage_header("FLOP")
        display.display_community(flop, "Flop")
        
        # Evaluate hands with flop
        flop_rankings = game_engine.evaluate_flop(players, flop)
        display.display_hand_rankings(flop_rankings, "Post-Flop Rankings")
        
        # Show winning percentages
        flop_percentages = game_engine.get_winning_percentage(players, flop)
        display.display_winning_percentages(flop_percentages)
        
        display.wait_for_user("Press Enter to continue to the Turn...")

        # === TURN ===
        flop.append(deck.draw(1)[0])  # Add turn card
        turn_cards = flop.copy()
        
        display.display_stage_header("TURN")
        display.display_community(turn_cards, "Turn")
        
        # Evaluate hands with turn
        turn_rankings = game_engine.evaluate_turn(players, turn_cards)
        display.display_hand_rankings(turn_rankings, "Post-Turn Rankings")
        
        # Show updated winning percentages
        turn_percentages = game_engine.get_winning_percentage(players, turn_cards)
        display.display_winning_percentages(turn_percentages)
        
        display.wait_for_user("Press Enter to continue to the River...")

        # === RIVER ===
        turn_cards.append(deck.draw(1)[0])  # Add river card
        final_community = turn_cards.copy()
        
        display.display_stage_header("RIVER")
        display.display_community(final_community, "River")
        
        # Final evaluation
        final_rankings = game_engine.evaluate_river(players, final_community)
        display.display_hand_rankings(final_rankings, "Final Rankings")
        
        # Final winning percentages (should be 100% for winner, 0% for others)
        final_percentages = game_engine.get_winning_percentage(players, final_community)
        display.display_winning_percentages(final_percentages)
        
        # Show game summary
        display.display_game_summary(final_rankings, final_community)
        
        display.wait_for_user("Press Enter to start a new game...")
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    texas_holdem_sim()
