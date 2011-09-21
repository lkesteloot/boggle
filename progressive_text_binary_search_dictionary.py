# Copyright 2011 Lawrence Kesteloot

import wordlist
import utils

class ProgressiveTextBinarySearchDictionary(object):
    """This is the same algorithm as the progressive binary search, but it operates
    on a single string of words, each terminated by a \n. It's quite slow to search, because
    each little operating must move forward or backward one word by scanning letters. The
    advantage is that creating it is just loading the file into memory with no processing,
    saving both time and memory."""

    def __init__(self, words, is_terminal=False, low=0, high=None):
        # String of all words, each terminated by \n.
        self.words = words
        self.is_terminal = is_terminal

        # Character indices of first letter of word.
        self.low = low
        self.high = wordlist.current_word_index(words, len(words) - 1) if high is None else high

    def get_child(self, ch, word):
        next_word = utils.make_next_word(word)

        (new_low, low_found) = wordlist.binary_text_search(self.words, word, self.low, self.high)
        (new_high, _) = wordlist.binary_text_search(self.words, next_word, self.low, self.high)

        new_high = wordlist.previous_word_index(self.words, new_high)

        if new_low <= new_high:
            return ProgressiveTextBinarySearchDictionary(self.words, low_found, new_low, new_high)
        else:
            return None

    @classmethod
    def make_dictionary(cls, words):
        return cls("\n".join(sorted(words)) + "\n")

