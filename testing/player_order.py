import os
import random
os.system('cls')


players = ['tom','eric', 'johhny', 'bob', 'craig', 'alice', 'dave']

dealer_index = 0

for round in range(5):  # 5 rounds no money limit
    print("Now starting round " + str(round) + " " + 30*"*")
    print("dealer index is at seat: " + str(dealer_index))
    for j, player in enumerate(players):  # list round participants
        print(f"at seat {j} is {player} ({'dealer' if j == dealer_index else ('small blind' if j == (dealer_index + 1) % len(players) else ('big blind' if j == (dealer_index + 2) % len(players) else ''))})")

    active_players = players[:]
    for i in range(4):  # preflop, flop, turn, river
        print("players in " + ("preflop:" if i == 0 else "flop:" if i ==
              1 else "turn:" if i == 2 else "river:"))
        print(active_players, end=", ")
        print()
        while True:
            players_folded = []

            for k, player in enumerate(active_players):
                if random.random() < 0.5:  # 50% chance to "call"
                    print(f"{player} calls")
                else:                           # 30% chance to "fold"
                    print(f"{player} folds")
                    players_folded.append(player)
                    continue
            active_players = [p for p in active_players if p not in players_folded]

            if not active_players:
                print("All players folded.")
                break

    print(f" Round {round} over - new dealer." + 20*"-")

    dealer_index = (dealer_index + 1) % len(players)
