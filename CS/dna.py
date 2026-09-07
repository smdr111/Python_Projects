import csv
import sys


def main():
    args = sys.argv
    if len(args) < 3:
        print("Usage: database and text...")
        sys.exit(1)


    with open(args[1]) as file:
        reader = csv.DictReader(file)
        row = [i for i in reader]
        strs = reader.fieldnames[1:]


    with open(args[2],'r') as file:
        data = file.read()
    target = longest_match(data,strs)

    # print(f"{row}\n{strs}\n{target}")
    for person in row:
        data = {key: value for key, value in person.items() if key != 'name'}
        if data == target:
            return print(person['name'])

    return print("No match")


def longest_match(sequence, subsequences):
    """Returns length of longest run of subsequence in sequence."""
    counts = {}
    for subsequence in subsequences:
        # Initialize variables
        longest_run = 0
        subsequence_length = len(subsequence)
        sequence_length = len(sequence)

        # Check each character in sequence for most consecutive runs of subsequence
        for i in range(sequence_length):

            # Initialize count of consecutive runs
            count = 0

            # Check for a subsequence match in a "substring" (a subset of characters) within sequence
            # If a match, move substring to next potential match in sequence
            # Continue moving substring and checking for matches until out of consecutive matches
            while True:

                # Adjust substring start and end
                start = i + count * subsequence_length
                end = start + subsequence_length

                # If there is a match in the substring
                if sequence[start:end] == subsequence:
                    count += 1

                # If there is no match in the substring
                else:
                    break

            # Update most consecutive matches found
            longest_run = max(longest_run, count)

        # After checking for runs at each character in sequence, return longest run found
        counts[subsequence] = str(longest_run)
    return counts

main()
