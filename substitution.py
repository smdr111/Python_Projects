import sys

if len(sys.argv) != 2:
    print("Usage: substitution.py key")
    sys.exit(1)

key = sys.argv[1]

if len(key) != 26 or not key.isalpha() or len(set(key.lower())) != 26:
    print("Invalid key")
    sys.exit(1)

key = key.lower()
alphabet = "abcdefghijklmnopqrstuvwxyz"

plaintext = input("plaintext: ")

ciphertext = ""

for char in plaintext:
    if char.isalpha():
        index = alphabet.index(char.lower())
        encrypted = key[index]

        if char.isupper():
            encrypted = encrypted.upper()

        ciphertext += encrypted
    else:
        ciphertext += char

print("ciphertext:", ciphertext)
