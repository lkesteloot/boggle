# Copyright 2011 Lawrence Kesteloot

import utils

class ProgressiveBinarySearchDictionary(object):
    """This is like the binary search dictionary, except we keep the low and high
    values of the binary search as we zoom in on the word. "low" points to the first
    word that we could possibly make, and "high" to the last. So if we've traversed
    "GE" so far, "low" would point to the first word that starts with "GE" and "high"
    to the last word that starts with "GE".

    We find the last word by incrementing "GE" to "GF", finding the location of that,
    and backing up one word.

    This is as fast to create as the standard binary search, but somewhat faster to search
    because we're not starting the binary search from scratch each time. On the other hand,
    we're doing two binary searches per hit, so it's not as much of a win as we'd like."""

    def __init__(self, words, is_terminal=False, low=0, high=None):
        # Ordered list of words.
        self.words = words
        self.is_terminal = is_terminal

        # As we recurse, this narrows down to the word or an empty span.
        self.low = low
        self.high = high if high is not None else len(words) - 1

    def get_child(self, ch, word):
        # Find the next word after this one, to mark the end of the span.
        next_word = utils.make_next_word(word)

        # Starting at the current span, narrow the low and high independently.
        (new_low, low_found) = utils.binary_search(self.words, word, self.low, self.high)
        (new_high, _) = utils.binary_search(self.words, next_word, self.low, self.high)

        # The high binary search will find the next word off the end, so back up one.
        new_high -= 1

        if new_low <= new_high:
            return ProgressiveBinarySearchDictionary(self.words, low_found, new_low, new_high)
        else:
            return None

    @classmethod
    def make_dictionary(cls, words):
        return cls(sorted(words))
