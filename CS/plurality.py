import sys

if len(sys.argv) < 3:
    print("Usage: [candidate...]")
    sys.exit(1)

candidates = [ i.upper() for i in sys.argv[1:] ]
scores = {i : 0  for i in candidates}
n = len(candidates)

for i in range(n):
    vote = input("Vote: ").upper()
    while vote not in candidates:
        print("Invalid vote!")
        vote = input("Vote: ").upper()
    scores[vote] += 1

max_value = max(scores.values())

for key, value in scores.items():
    if value == max_value:
        print(key.title())





