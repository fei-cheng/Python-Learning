"""
Implement an algorithm to determine if a string has all unique characters.
What if you can not use additional data structures?
"""


SHIFT = 5
LOWER = 31
NUM = [0, 0, 0, 0, 0, 0, 0, 0]

def seti(i):
    NUM[i>>SHIFT] |= (1 << (i & LOWER))

def test(i):
    return NUM[i>>SHIFT] & (1 << (i & LOWER))

def clear(i):
    NUM[i>>SHIFT] &= 0 ^ (1 << (i & LOWER))

def is_allUnique(st):
    for ch in st:
        n = ord(ch)
        if not test(n):
            seti(n)
        else:
            return False
    return True


print is_allUnique("algorithm")
print is_allUnique("character")
