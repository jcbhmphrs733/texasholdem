from prettytable import PrettyTable
from treys import Card
from rich.console import Console
from rich.rule import Rule
from typing import List, Tuple

console = Console()

class GameDisplay:
    """
    Handles all game display and console output formatting.
    """
    
    @staticmethod
    def display_hands(players):
        """Display player hole cards in a formatted table."""
        table = PrettyTable()
        table.field_names = ["Player", "Cards"]
        table.align["Player"] = "l"
        table.align["Cards"] = "l"
        
        for player in players:
            cards_str = " ".join([Card.int_to_pretty_str(c) for c in player.hand])
            table.add_row([player.name, cards_str])
        
        print(table)
    
    @staticmethod
    def display_community(community_cards, stage_name="Community Cards"):
        """Display community cards."""
        table = PrettyTable()
        table.field_names = [stage_name]
        table.align[stage_name] = "c"
        
        cards_str = " ".join([Card.int_to_pretty_str(c) for c in community_cards])
        table.add_row([cards_str])
        
        print(table)
    
    @staticmethod
    def display_hand_rankings(rankings: List[Tuple[str, int, str]], stage_name="Hand Rankings"):
        """Display player rankings with hand strength."""
        table = PrettyTable()
        table.field_names = ["Rank", "Player", "Hand", "Strength"]
        table.align["Player"] = "l"
        table.align["Hand"] = "l"
        table.align["Strength"] = "r"
        
        for i, (player_name, hand_rank, hand_description) in enumerate(rankings, 1):
            table.add_row([i, player_name, hand_description, f"{hand_rank:,}"])
        
        print(table)
    
    @staticmethod
    def display_winning_percentages(percentages: dict):
        """Display winning percentages for each player."""
        table = PrettyTable()
        table.field_names = ["Player", "Win %"]
        table.align["Player"] = "l"
        table.align["Win %"] = "r"
        
        # Sort by percentage descending
        sorted_players = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
        
        for player_name, percentage in sorted_players:
            table.add_row([player_name, f"{percentage}%"])
        
        print(table)
    
    @staticmethod
    def display_stage_header(stage_name: str):
        """Display a stage header with Rich formatting."""
        console.rule(f"[bold yellow]{stage_name}[/bold yellow]")
    
    @staticmethod
    def wait_for_user(message: str = "Press Enter to continue..."):
        """Wait for user input with a custom message."""
        input(f"\n{message}")
    
    @staticmethod
    def display_game_summary(final_rankings, community_cards):
        """Display final game summary."""
        
        # GameDisplay.display_community(community_cards, "Final Board")
        GameDisplay.display_hand_rankings(final_rankings, "Final Hand Rankings")
        
        winner = final_rankings[0]
        print(f"\n WINNER: {winner[0]} with {winner[2]}")