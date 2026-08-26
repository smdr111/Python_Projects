import sys


candidates = []
candidate_count = 0
voter_count = 0

preferences = []
locked = []
pairs = []


def vote(ranks, rank, name):
    if name not in candidates:
        return False

    ranks[rank] = candidates.index(name)
    return True


def record_preferences(ranks):
    for i in range(candidate_count):
        for j in range(i + 1, candidate_count):
            preferences[ranks[i]][ranks[j]] += 1


def add_pairs():
    for i in range(candidate_count):
        for j in range(i + 1, candidate_count):

            if preferences[i][j] > preferences[j][i]:
                pairs.append((i, j))

            elif preferences[j][i] > preferences[i][j]:
                pairs.append((j, i))


def sort_pairs():
    pairs.sort(
        key=lambda pair: preferences[pair[0]][pair[1]],
        reverse=True
    )


def creates_cycle(winner, loser):
    if loser == winner:
        return True

    for i in range(candidate_count):
        if locked[loser][i]:
            if creates_cycle(winner, i):
                return True

    return False


def lock_pairs():
    for winner, loser in pairs:
        if not creates_cycle(winner, loser):
            locked[winner][loser] = True


def print_winner():
    for i in range(candidate_count):

        # Does anybody point toward candidate i?
        has_incoming = False

        for j in range(candidate_count):
            if locked[j][i]:
                has_incoming = True
                break

        if not has_incoming:
            print(candidates[i])
            return


def main():

    global candidates
    global candidate_count
    global voter_count
    global preferences
    global locked

    # Need at least one candidate
    if len(sys.argv) < 2:
        print("Usage: python tideman.py [candidate ...]")
        sys.exit(1)

    # Candidates come from command line
    candidates = sys.argv[1:]
    candidate_count = len(candidates)

    # Initialize preferences
    preferences = [
        [0 for _ in range(candidate_count)]
        for _ in range(candidate_count)
    ]

    # Initialize locked graph
    locked = [
        [False for _ in range(candidate_count)]
        for _ in range(candidate_count)
    ]

    # Number of voters
    voter_count = int(input("Number of voters: "))

    # Collect votes
    for _ in range(voter_count):

        ranks = [-1] * candidate_count

        for rank in range(candidate_count):
            name = input(f"Rank {rank + 1}: ")

            if not vote(ranks, rank, name):
                print("Invalid vote")
                sys.exit(1)

        record_preferences(ranks)

    # Build pairs
    add_pairs()

    # Strongest victories first
    sort_pairs()

    # Lock victories without creating cycles
    lock_pairs()

    # Find winner
    print_winner()

if __name__ == "main":
    main()
