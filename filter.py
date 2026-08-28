import argparse
import math
from PIL import Image


def grayscale(image):
    height = len(image)
    width = len(image[0])

    for i in range(height):
        for j in range(width):
            r, g, b = image[i][j]

            gray = round((r + g + b) / 3)

            image[i][j] = [gray, gray, gray]


def reflect(image):
    height = len(image)
    width = len(image[0])

    for i in range(height):
        for j in range(width // 2):
            image[i][j], image[i][width - 1 - j] = image[i][width - 1 - j],image[i][j]


def blur(image):
    height = len(image)
    width = len(image[0])

    # Keep original pixels unchanged while calculating
    original = [
        row[:] for row in image
    ]

    for i in range(height):
        for j in range(width):

            total_r = 0
            total_g = 0
            total_b = 0
            count = 0

            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):

                    ni = i + di
                    nj = j + dj

                    if 0 <= ni < height and 0 <= nj < width:
                        r, g, b = original[ni][nj]

                        total_r += r
                        total_g += g
                        total_b += b

                        count += 1

            image[i][j] = [
                round(total_r / count),
                round(total_g / count),
                round(total_b / count)
            ]


def edges(image):
    height = len(image)
    width = len(image[0])

    gx_kernel = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ]

    gy_kernel = [
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ]

    original = [
        row[:] for row in image
    ]

    for i in range(height):
        for j in range(width):

            gx_r = gx_g = gx_b = 0
            gy_r = gy_g = gy_b = 0

            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):

                    ni = i + di
                    nj = j + dj

                    # Outside the image = black pixel
                    if 0 <= ni < height and 0 <= nj < width:
                        r, g, b = original[ni][nj]
                    else:
                        r = g = b = 0

                    kx = gx_kernel[di + 1][dj + 1]
                    ky = gy_kernel[di + 1][dj + 1]

                    gx_r += r * kx
                    gx_g += g * kx
                    gx_b += b * kx

                    gy_r += r * ky
                    gy_g += g * ky
                    gy_b += b * ky

            r = min(255, round(math.sqrt(gx_r ** 2 + gy_r ** 2)))
            g = min(255, round(math.sqrt(gx_g ** 2 + gy_g ** 2)))
            b = min(255, round(math.sqrt(gx_b ** 2 + gy_b ** 2)))

            image[i][j] = [r, g, b]


def load_image(filename):
    """Load image and convert it to a 2D RGB list."""

    img = Image.open(filename).convert("RGB")

    width, height = img.size
    pixels = list(img.getdata())

    return [
        [
            list(pixels[i * width + j])
            for j in range(width)
        ]
        for i in range(height)
    ]


def save_image(image, filename):
    """Convert 2D RGB list back to an image."""

    height = len(image)
    width = len(image[0])

    img = Image.new("RGB", (width, height))

    pixels = [
        tuple(pixel)
        for row in image
        for pixel in row
    ]

    img.putdata(pixels)
    img.save(filename)


def main():
    parser = argparse.ArgumentParser(
        description="CS50 Filter (More) - Python implementation"
    )

    parser.add_argument("input", help="input image")
    parser.add_argument("output", help="output image")

    parser.add_argument(
        "filter",
        choices=["grayscale", "reflect", "blur", "edges"],
        help="filter to apply"
    )

    args = parser.parse_args()

    image = load_image(args.input)

    if args.filter == "grayscale":
        grayscale(image)

    elif args.filter == "reflect":
        reflect(image)

    elif args.filter == "blur":
        blur(image)

    elif args.filter == "edges":
        edges(image)

    save_image(image, args.output)

if __name__ == "__main__":
    main()
