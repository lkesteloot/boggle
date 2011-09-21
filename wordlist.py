# Copyright 2011 Lawrence Kesteloot

"""Methods for manipulating and searching a single string that's a bunch of words, each
terminated by a \n."""

def previous_word_index(words, pos):
    """If "pos" points to the middle of a word, returns the position of the beginning
    of that word. If pos points to the first character of a word, returns position of
    previous word. If pos points to the first character in the string, returns -1."""

    if pos == 0:
        return -1
    else:
        # This handles all cases above.
        return words.rfind("\n", 0, max(pos - 1, 0)) + 1

# Test cases.
TEST_WORDS = "one\ntwo\nthree\n"
assert previous_word_index(TEST_WORDS, 0) == -1
assert previous_word_index(TEST_WORDS, 2) == 0
assert previous_word_index(TEST_WORDS, 3) == 0
assert previous_word_index(TEST_WORDS, 4) == 0
assert previous_word_index(TEST_WORDS, 5) == 4
assert previous_word_index(TEST_WORDS, 6) == 4
assert previous_word_index(TEST_WORDS, 13) == 8
assert previous_word_index(TEST_WORDS, 14) == 8
del TEST_WORDS

def current_word_index(words, pos):
    """Returns the index of the first word the pos is on. The \n is considered to be
    part of the word it terminates."""

    # This handles all cases above.
    return words.rfind("\n", 0, pos) + 1

# Test cases.
TEST_WORDS = "one\ntwo\nthree\n"
assert current_word_index(TEST_WORDS, 0) == 0
assert current_word_index(TEST_WORDS, 2) == 0
assert current_word_index(TEST_WORDS, 3) == 0
assert current_word_index(TEST_WORDS, 4) == 4
assert current_word_index(TEST_WORDS, 5) == 4
assert current_word_index(TEST_WORDS, 6) == 4
assert current_word_index(TEST_WORDS, 13) == 8
del TEST_WORDS

def next_word_index(words, pos):
    """Return the next word than the one at pos. Moves forward until the subsequent
    \n (which could be at pos), and return the index after that (which could be past
    the end of the string)."""

    return words.find("\n", pos) + 1

# Test cases.
TEST_WORDS = "one\ntwo\nthree\n"
assert next_word_index(TEST_WORDS, 0) == 4
assert next_word_index(TEST_WORDS, 2) == 4
assert next_word_index(TEST_WORDS, 3) == 4
assert next_word_index(TEST_WORDS, 4) == 8
assert next_word_index(TEST_WORDS, 5) == 8
assert next_word_index(TEST_WORDS, 6) == 8
assert next_word_index(TEST_WORDS, 13) == len(TEST_WORDS)
assert next_word_index(TEST_WORDS, len(TEST_WORDS) - 1) == len(TEST_WORDS)
del TEST_WORDS

def word_at_index(words, pos):
    """Return the word starting at pos and going until (but not including) the \n."""

    return words[pos:words.find("\n", pos)]

# Test cases.
TEST_WORDS = "one\ntwo\nthree\n"
assert word_at_index(TEST_WORDS, 0) == "one"
assert word_at_index(TEST_WORDS, 4) == "two"
assert word_at_index(TEST_WORDS, 8) == "three"
del TEST_WORDS

def binary_text_search(words, word, low, high):
    """Return an (index, found) tuple, where index is either where the word was
    found or where it should be, and found is whether it was found."""

    while low <= high:
        mid = low + (high - low)/2
        mid = current_word_index(words, mid)
        mid_word = word_at_index(words, mid)

        if word < mid_word:
            high = previous_word_index(words, mid)
        elif word > mid_word:
            low = next_word_index(words, mid)
        else:
            return (mid, True)

    return (low, False)
