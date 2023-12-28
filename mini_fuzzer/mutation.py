import random
import string
import sys

from config import DECREMENT_VALUE, INCREMENT_VALUE, INTERESTING_VALUE

sys.path.append("../mini_fuzzer/config.py")


# Flip a random bit in a random character
def bitflip(s: str) -> str:
    if s == "":
        return ""

    rand = random.SystemRandom()
    chr_pos = rand.randint(0, len(s) - 1)
    origin_chr = s[chr_pos]
    bit_pos = rand.randint(0, ord(origin_chr).bit_length() - 1)
    fliped_chr = chr(ord(origin_chr) ^ (1 << bit_pos))
    if not fliped_chr.isprintable() or ord(fliped_chr) == 0: # prevent control character and null character
        return s
    else: 
        return s[:chr_pos] + fliped_chr + s[chr_pos + 1 :]

# Flip a random character
def byteflip(s:str) -> str:
    if s == "":
        return ""

    rand = random.SystemRandom()
    chr_pos = rand.randint(0, len(s) - 1)
    fliped_chr = chr(ord(s[chr_pos]) ^ 0xFF)
    if not fliped_chr.isprintable() or ord(fliped_chr) == 0: 
        return s
    else: 
        return s[:chr_pos] + fliped_chr + s[chr_pos + 1 :]


# Increase by a constant value
def arithmetic_inc(s: str) -> str:
    num = 0
    if s.isdigit():
       num = int(s)
    else:
        try:
            num = float(s)
        except ValueError:
            return s
    return str(num + INCREMENT_VALUE)        


 # Decrease by a constant value
def arithmetic_dec(s: str) -> str:
    num = 0
    if s.isdigit():
       num = int(s)
    else:
        try:
            num = float(s)
        except ValueError:
            return s
    return str(num - DECREMENT_VALUE)        
   

# Return a interesting value 
def add_interesting_value(s: str) -> str:
    return str(random.choice(INTERESTING_VALUE))


# Add a random character at random location
def add_random_character(s: str) -> str:
    random_char = random.choice(string.printable)
    insert_pos = random.randint(0, len(s))
    return s[:insert_pos] + random_char + s[insert_pos:]


# Delete a random character at random location
def delete_random_character(s: str) -> str:
    if s == "":
        return s
    delete_pos = random.randint(0, len(s) - 1)
    return s[:delete_pos] + s[delete_pos + 1:]


