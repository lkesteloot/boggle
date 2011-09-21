# Copyright 2011 Lawrence Kesteloot

def binary_search(words, word, low=0, high=None):
    """Return an (index, found) tuple, where index is either where the word was
    found or where it should be, and found is whether it was found."""

    if high is None:
        high = len(words) - 1

    while low <= high:
        mid = low + (high - low)/2
        mid_word = words[mid]

        if word < mid_word:
            high = mid - 1
        elif word > mid_word:
            low = mid + 1
        else:
            return (mid, True)

    return (low, False)

def make_next_word(word):
    """Returns next_word such that "word < longer_word < next_word" if and only if
    word is a prefix of longer_word.

    For example, "a" returns "b", "hello" returns "hellp", "pooz" returns "pop",
    and "z" returns "{"."""

    if not word:
        return "{"

    prefix = word[:-1]
    last_ch = word[-1]
    if last_ch == "z":
        return make_next_word(prefix)
    else:
        return prefix + chr(ord(last_ch) + 1)

# Quick tests.
assert make_next_word("a") == "b"
assert make_next_word("hello") == "hellp"
assert make_next_word("pooz") == "pop"
assert make_next_word("z") == "{"
assert make_next_word("zzz") == "{"
