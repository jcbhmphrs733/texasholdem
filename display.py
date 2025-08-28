from treys import Card
from rich.console import Console
from rich.table import Table
from rich.text import Text
from typing import List, Tuple

console = Console()

def card_to_rich_display(card_int: int, style: str = "ascii") -> str:
    """
    Convert a treys card integer to a Rich-friendly display format.
    
    Args:
        card_int: The treys card integer
        style: Display style - "ascii", "text", or "unicode_safe"
    
    Returns:
        String representation suitable for Rich tables
    """
    try:
        if style == "ascii":
            # ASCII-only version that's table-friendly
            rank = Card.get_rank_int(card_int)
            suit = Card.get_suit_int(card_int)
            
            rank_str = Card.STR_RANKS[rank]
            # Treys suit mapping: 1=spades, 2=hearts, 4=diamonds, 8=clubs (bit flags)
            # But get_suit_int() returns 0-3, so let's check the actual mapping
            suit_chars = ['s', 'h', 'd', 'c']
            
            # Ensure suit index is valid
            if suit < 0 or suit >= len(suit_chars):
                # Fallback: try to use the built-in pretty string and extract
                fallback = Card.int_to_pretty_str(card_int)
                return fallback.replace('[', '').replace(']', '')
            
            suit_str = suit_chars[suit]
            return f"{rank_str}{suit_str}"
        
        elif style == "text":
            # For now, let's use a safer approach
            pretty = Card.int_to_pretty_str(card_int)
            # Convert [A♠] to "A of Spades"
            clean = pretty.replace('[', '').replace(']', '')
            if '♠' in clean:
                return clean.replace('♠', ' of Spades')
            elif '♥' in clean:
                return clean.replace('♥', ' of Hearts')
            elif '♦' in clean:
                return clean.replace('♦', ' of Diamonds')
            elif '♣' in clean:
                return clean.replace('♣', ' of Clubs')
            return clean
        
        elif style == "unicode_safe":
            # Just use the built-in but clean it up
            pretty = Card.int_to_pretty_str(card_int)
            return pretty.replace('[', '').replace(']', '')
        
        else:
            # Default to treys built-in
            return Card.int_to_pretty_str(card_int)
            
    except Exception as e:
        # Ultimate fallback
        return f"Card({card_int})"

def cards_to_rich_string(cards: List[int], style: str = "ascii", separator: str = " ") -> str:
    """
    Convert a list of card integers to a Rich-friendly string.
    """
    card_strings = [card_to_rich_display(card, style) for card in cards]
    return separator.join(card_strings)

class GameDisplay:
    """
    Handles all game display and console output formatting using Rich tables.
    """
    
    @staticmethod
    def display_hands(players):
        """Display player hole cards in a formatted table."""
        table = Table(
            show_header=True,
            header_style="bold magenta",
            border_style="bright_blue",
            min_width=40,
            expand=False
        )
        
        table.add_column("Player", style="cyan", no_wrap=True, justify="left", min_width=10)
        table.add_column("Cards", style="white", justify="left", min_width=15, no_wrap=True)
        
        for player in players:
            # Back to using the original treys card display
            cards_str = " ".join([Card.int_to_pretty_str(c) for c in player.hand])
            table.add_row(player.name, cards_str)
        
        console.print(table)
    
    @staticmethod
    def display_community(community_cards, stage_name="Community Cards"):
        """Display community cards."""
        table = Table(
            show_header=True,
            header_style="bold yellow",
            border_style="bright_yellow",
            min_width=40,
            expand=False
        )
        
        table.add_column(stage_name, style="white", justify="left", min_width=25, no_wrap=True)
        
        # Back to using the original treys card display
        cards_str = " ".join([Card.int_to_pretty_str(c) for c in community_cards])
        table.add_row(cards_str)
        
        console.print(table)
    
    @staticmethod
    def display_hand_rankings(rankings: List[Tuple[str, int, str]], stage_name="Hand Rankings"):
        """Display player rankings with hand strength."""
        table = Table(
            show_header=True,
            header_style="bold green",
            border_style="bright_green",
            show_lines=True,
            expand=False
        )
        
        table.add_column("Rank", style="bold", justify="center")
        table.add_column("Player", style="cyan", justify="left")
        table.add_column("Hand", style="white", justify="left")
        table.add_column("Strength", style="dim", justify="right")
        
        for i, (player_name, hand_rank, hand_description) in enumerate(rankings, 1):
            # Color rank based on position
            rank_style = "bold green" if i == 1 else "yellow" if i == 2 else "red" if i == 3 else "dim"
            rank_text = Text(str(i), style=rank_style)
            
            table.add_row(
                str(i),
                player_name, 
                hand_description, 
                f"{hand_rank:,}"
            )
        
        console.print(table)
    
    @staticmethod
    def display_winning_percentages(percentages: dict):
        """Display winning percentages for each player."""
        table = Table(
            show_header=True,
            header_style="bold bright_magenta",
            border_style="bright_magenta",
            title_style="bold bright_magenta",
            min_width=30,
            expand=False
        )
        
        table.add_column("Player", style="cyan", justify="left", min_width=10)
        table.add_column("Win %", style="bold", justify="right", min_width=8)
        
        # Sort by percentage descending
        sorted_players = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
        
        for player_name, percentage in sorted_players:
            # Color percentage based on value
            if percentage > 50:
                percent_style = "bold green"
            elif percentage > 25:
                percent_style = "bold yellow"
            else:
                percent_style = "bold red"
                
            percentage_text = Text(f"{percentage}%", style=percent_style)
            
            table.add_row(player_name, percentage_text)
        
        console.print(table)
    
    @staticmethod
    def display_stage_header(stage_name: str):
        """Display a stage header with Rich formatting."""
        console.rule(f"[bold yellow]{stage_name}[/bold yellow]")
    
    @staticmethod
    def wait_for_user(message: str = "Press Enter to continue..."):
        """Wait for user input with a custom message."""
        console.print(f"\n[dim]{message}[/dim]", end="")
        input()
    
    @staticmethod
    def display_game_summary(final_rankings, community_cards):
        """Display final game summary."""
        console.rule("[bold bright_cyan]FINAL RESULTS[/bold bright_cyan]")
        
        GameDisplay.display_community(community_cards, "Community")
        GameDisplay.display_hand_rankings(final_rankings, "Final Hand Rankings")
        
        winner = final_rankings[0]
        
        # Create a winner announcement table
        winner_table = Table(
            title="[bold bright_yellow]WINNER[/bold bright_yellow]",
            show_header=False,
            border_style="bright_yellow",
            title_style="bold bright_yellow",
            expand=False
        )
        
        winner_table.add_column("", style="bold bright_yellow", justify="center")
        winner_table.add_row(f"{winner[0]} wins with {winner[2]}")
        
        console.print(winner_table)