import random


# Flip a random bit in a random character
def bitflip(s: str) -> str:
    if s == "":
        return ""

    rand = random.SystemRandom()
    chr_position = rand.randint(0, len(s))
    origin_chr = s[chr_position]
    bit_position = rand.randint(0, ord(origin_chr).bit_length())
    fliped_chr = chr(ord(origin_chr) ^ (1 << bit_position))

    return s[:chr_position] + fliped_chr + s[chr_position + 1 :]
