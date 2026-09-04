while True:
    try:
        n = int(input("Height: "))

        if 0 < n < 9:
            break

    except ValueError:
        n = int(input("Height: "))

for i in range(1, n + 1):
    print((n - i) * ' ' + i * '#' + '  ' + i * '#')
