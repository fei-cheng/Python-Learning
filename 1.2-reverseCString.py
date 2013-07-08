"""
    Write code to reverse a C-Style String.
    (C-String means that “abcd” is represented as five characters, including the null character.)
"""

def swap(a, b):
    a = a ^ b
    b = a ^ b
    a = a ^ b
    return a, b

def reverse(s):
    idx =  len(s) - 1
    reversed_str = ''
    while idx >= 0:
        reversed_str += s[idx]
        idx -= 1
    return reversed_str


s = "algorithm"

print s[::-1]
print reverse(s)
print reduce(lambda x, y: y+x, s)
