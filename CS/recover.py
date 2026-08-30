import sys

BLOCK_SIZE = 512
JPEG_SIGNATURE = b"\xff\xd8\xff"


def is_jpeg(block):
    """
    Check whether the first 4 bytes of a 512-byte block
    indicate the beginning of a JPEG.
    """

    return (
        block[0] == 0xFF
        and block[1] == 0xD8
        and block[2] == 0xFF
        and 0xE0 <= block[3] <= 0xEF
    )


def main():
    # --------------------------------------------------
    # 1. Check command-line arguments
    # --------------------------------------------------

    if len(sys.argv) != 2:
        print("Usage: python recover.py FILE")
        return 1

    input_file = sys.argv[1]

    # --------------------------------------------------
    # 2. Open the memory card
    # --------------------------------------------------

    try:
        card = open(input_file, "rb")
    except FileNotFoundError:
        print(f"Could not open {input_file}")
        return 1

    # --------------------------------------------------
    # 3. Variables for recovered JPEGs
    # --------------------------------------------------

    image_number = 0
    output_file = None

    # --------------------------------------------------
    # 4. Read the card 512 bytes at a time
    # --------------------------------------------------

    while True:

        block = card.read(BLOCK_SIZE)

        # No more data
        if not block:
            break

        # --------------------------------------------------
        # 5. Check whether this block starts a JPEG
        # --------------------------------------------------

        if len(block) == BLOCK_SIZE and is_jpeg(block):

            # If we were already writing a JPEG,
            # close the previous JPEG first.
            if output_file is not None:
                output_file.close()

            # Create filename:
            # 000.jpg
            # 001.jpg
            # 002.jpg
            # ...
            filename = f"{image_number:03}.jpg"

            output_file = open(filename, "wb")

            image_number += 1

        # --------------------------------------------------
        # 6. If we are currently inside a JPEG,
        #    write this block to the JPEG.
        # --------------------------------------------------

        if output_file is not None:
            output_file.write(block)

    # --------------------------------------------------
    # 7. Close the final JPEG
    # --------------------------------------------------

    if output_file is not None:
        output_file.close()

    # --------------------------------------------------
    # 8. Close the memory card
    # --------------------------------------------------

    card.close()


if __name__ == "__main__":
    main()
