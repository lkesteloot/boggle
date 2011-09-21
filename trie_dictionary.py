# Copyright 2011 Lawrence Kesteloot

import sys

class TrieDictionary:
    """This dictionary uses a Trie data structure, with a list for the 26 possible children.
    I tried a dictionary for the children and the speed was the same. This class is really
    the node of the tree. This is the slowest of the data structures to create (by far)
    but the fastest to solve."""

    def __init__(self):
        # 0-25 (a-z) array of children.
        self.children = [None]*26

        # Whether this is the end of a word.
        self.is_terminal = False

    def get_child(self, ch, word=None):
        # 65 is ord("A")
        index = ord(ch) - 65
        return self.children[index]

    def _add_word(self, word):
        """Adds a word to the trie."""

        if word == "":
            self.is_terminal = True
        else:
            ch = word[0]
            # 65 is ord("A")
            index = ord(ch) - 65

            # Get or make child.
            child = self.children[index]
            if not child:
                child = TrieDictionary()
                self.children[index] = child

            # Recurse on rest of word.
            child._add_word(word[1:])

    @classmethod
    def make_dictionary(cls, words):
        """Read the dictionary into a trie and return the root node."""

        # Root of the trie.
        root = cls()

        count = 0

        # Add every word.
        for word in words:
            root._add_word(word)

            # Progress bar.
            count += 1
            if count % 10000 == 0:
                sys.stdout.write("%d%%\r" % (count * 100 / len(words)))
                sys.stdout.flush()

        return root
