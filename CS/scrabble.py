letters = {"a": 1, "b": 3, "c": 3, "d": 2, "e": 1, "f": 4, "g": 2, "h": 4, "i": 1, "j": 8, "k": 5, "l": 1, "m": 3, "n": 1, "o": 1, "p": 3, "q": 10, "r": 1, "s": 1, "t": 1, "u": 1, "v": 4, "w": 4, "x": 8, "y": 4, "z": 10}

player1 = input("Player 1: ").lower()
player2 = input("Player 2: ").lower()

score1 = sum(letters.get(i) for i in player1)
score2 = sum(letters.get(i) for i in player2)

if score1 > score2: print("Player 1 wins!")
elif score1 < score2: print("Player 2 wins!")
else: print("Tie!")
