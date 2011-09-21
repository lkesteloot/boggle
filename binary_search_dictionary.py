# Copyright 2011 Lawrence Kesteloot

import utils

class BinarySearchDictionary(object):
    """This keeps a list of words and does a binary search for each prefix or word lookup.
    It's very fast to build but relatively slow to look up."""

    def __init__(self, words, is_terminal=False):
        # Ordered list of words.
        self.words = words

        # We use this class as a pseudo-internal node after a search, and this field tells
        # the caller whether we found a word or a prefix.
        self.is_terminal = is_terminal

    def get_child(self, ch, word):
        pos, found = utils.binary_search(self.words, word)

        if found:
            # Found word.
            return BinarySearchDictionary(self.words, True)
        else:
            if pos < len(self.words) and self.words[pos].startswith(word):
                # Found prefix.
                return BinarySearchDictionary(self.words, False)
            else:
                return None

    @classmethod
    def make_dictionary(cls, words):
        return cls(sorted(words))
