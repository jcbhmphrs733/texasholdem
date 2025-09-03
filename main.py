from bots.Coyote import Coyote
from game_engine import play_hand


def main():
    players = [
        Coyote(name="Alice"),
        Coyote(name="Bob"),
        Coyote(name="Charlie"),
        Coyote(name="David"),
        Coyote(name="Erika")
    ]
    dealer_index = 0
    while True:
        dealer_index = play_hand(players, dealer_index)

if __name__ == "__main__":
    main()