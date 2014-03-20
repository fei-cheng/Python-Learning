"""
    Write a method to decide if two strings are anagrams or not.
"""

def areAnagrams(strA, strB):
    return sorted(strA) == sorted(strB)

print areAnagrams("ab3sd","bsda3")
print areAnagrams("hello","world")
