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
    while True:
        play_hand(players)

if __name__ == "__main__":
    main()