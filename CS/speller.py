import sys
import time


# Hash table
TABLE_SIZE = 10007
table = [[] for _ in range(TABLE_SIZE)]

# Number of words in dictionary
word_count = 0


def hash_word(word):
    """
    Convert a word into a bucket number.

    We use the characters in the word to produce
    a number between 0 and TABLE_SIZE - 1.
    """

    value = 0

    for char in word.lower():
        value = (value * 31 + ord(char)) % TABLE_SIZE

    return value


def load(dictionary):
    """
    Load every word from the dictionary
    into the hash table.
    """

    global word_count

    try:
        with open(dictionary, "r") as file:

            for line in file:
                word = line.strip().lower()

                if not word:
                    continue

                index = hash_word(word)

                table[index].append(word)

                word_count += 1

        return True

    except FileNotFoundError:
        return False


def check(word):
    """
    Return True if word is in the dictionary.
    Otherwise return False.
    """

    word = word.lower()

    index = hash_word(word)

    for dictionary_word in table[index]:

        if dictionary_word == word:
            return True

    return False


def size():
    """
    Return the number of words in the dictionary.
    """

    return word_count


def unload():
    """
    Free the hash table.

    Python handles memory automatically, so there is
    no manual free() like there is in C.

    We clear the lists to release our references.
    """

    global table

    for bucket in table:
        bucket.clear()

    table.clear()

    return True


def main():

    # --------------------------------------------------
    # Command-line arguments
    # --------------------------------------------------

    if len(sys.argv) == 2:

        dictionary = "dictionaries/large"
        text = sys.argv[1]

    elif len(sys.argv) == 3:

        dictionary = sys.argv[1]
        text = sys.argv[2]

    else:

        print("Usage: python speller.py [dictionary] text")
        sys.exit(1)


    # --------------------------------------------------
    # Load dictionary
    # --------------------------------------------------

    start = time.perf_counter()

    if not load(dictionary):

        print(f"Could not load {dictionary}")
        sys.exit(1)

    load_time = time.perf_counter() - start


    # --------------------------------------------------
    # Check text
    # --------------------------------------------------

    misspelled = 0
    words_in_text = 0

    start = time.perf_counter()

    try:

        with open(text, "r") as file:

            for line in file:

                # Split the line into words
                words = line.split()

                for word in words:

                    words_in_text += 1

                    # Remove punctuation around words
                    clean_word = word.strip(
                        ".,!?;:\"()[]{}<>"
                    )

                    if not check(clean_word):

                        misspelled += 1

    except FileNotFoundError:

        print(f"Could not open {text}")
        unload()
        sys.exit(1)

    check_time = time.perf_counter() - start


    # --------------------------------------------------
    # Size
    # --------------------------------------------------

    start = time.perf_counter()

    dictionary_size = size()

    size_time = time.perf_counter() - start


    # --------------------------------------------------
    # Unload
    # --------------------------------------------------

    start = time.perf_counter()

    unload()

    unload_time = time.perf_counter() - start


    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    print("WORDS MISSPELLED:", misspelled)
    print("WORDS IN DICTIONARY:", dictionary_size)
    print("WORDS IN TEXT:", words_in_text)

    print(f"TIME IN load:   {load_time:.6f}")
    print(f"TIME IN check:  {check_time:.6f}")
    print(f"TIME IN size:   {size_time:.6f}")
    print(f"TIME IN unload: {unload_time:.6f}")

    print(
        f"TIME IN TOTAL:  "
        f"{load_time + check_time + size_time + unload_time:.6f}"
    )


if __name__ == "__main__":
    main()
