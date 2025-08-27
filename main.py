from treys import Deck, Card
from rich.console import Console
from rich.table import Table

console = Console()

def display_hands(players):
    table = Table(title="Player Hands")
    table.add_column("Player", style="cyan")
    table.add_column("Cards", style="magenta")

    for i, hand in enumerate(players):
        cards_str = " ".join([Card.int_to_pretty_str(c) for c in hand])
        table.add_row(f"Player {i+1}", cards_str)
    console.print(table)

def display_community(community):
    table = Table(title="Community Cards")
    table.add_column("Community", style="green")
    cards_str = " ".join([Card.int_to_pretty_str(c) for c in community])
    table.add_row(cards_str)
    console.print(table)

def texas_holdem_sim(num_players=4):
    while True:
        deck = Deck()
        players = [[deck.draw(1)[0], deck.draw(1)[0]] for _ in range(num_players)]

        # Show hole cards
        console.rule("[bold yellow]Hole Cards[/bold yellow]")
        display_hands(players)
        input("Press Enter to continue to the Flop...")

        # Flop
        community = [deck.draw(1)[0] for _ in range(3)]
        console.rule("[bold yellow]Flop[/bold yellow]")
        display_community(community)
        input("Press Enter to continue to the Turn...")

        # Turn
        community.append(deck.draw(1)[0])
        console.rule("[bold yellow]Turn[/bold yellow]")
        display_community(community)
        input("Press Enter to continue to the River...")

        # River
        community.append(deck.draw(1)[0])
        console.rule("[bold yellow]River[/bold yellow]")
        display_community(community)
        input("Press Enter to restart the game loop...")

if __name__ == "__main__":
    texas_holdem_sim(num_players=4)
