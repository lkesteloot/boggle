# Copyright 2011 Lawrence Kesteloot

class PrefixDictionary(object):
    """Stores a map of all words and prefixes of words (and whether each entry is
    a prefix or a word). This is moderately fast to build and has fast lookup,
    though slower than the Trie."""

    def __init__(self):
        # Prefix dict, from prefix to whether terminal or not.
        self.words = {}

        # We make fake internal nodes when searching, and this field tells the
        # user whether we found a word or just a prefix.
        self.is_terminal = False

    def get_child(self, ch, word):
        is_word = self.words.get(word, None)
        if is_word is None:
            return None

        child = PrefixDictionary()
        child.words = self.words
        child.is_terminal = is_word

        return child

    @classmethod
    def make_dictionary(cls, words):
        """Read the dictionary into a prefix dict and return the dict. The keys of
        the dict are the prefix (or word), the value is whether the key is a prefix
        (False) or a word (True)."""

        dictionary = cls()

        # Read every word.
        for word in words:
            # Add all the prefixes.
            for i in range(len(word)):
                prefix = word[:i]
                if prefix not in dictionary.words:
                    dictionary.words[prefix] = False

            # Add the word.
            dictionary.words[word] = True

        return dictionary
