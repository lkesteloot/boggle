#!/usr/bin/python

"""Solves a Boggle board using a variety of data structures."""

import sys
import random
import cStringIO
import time

import wordlist

class Timer(object):
    """Times an event."""

    def __init__(self):
        self.start_time = time.time()

    def print_elapsed(self, label):
        elapsed = time.time() - self.start_time
        print "%s: %dms" % (label, elapsed*1000)

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
        pos, found = binary_search(self.words, word)

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

class ProgressiveBinarySearchDictionary(object):
    """This is like the binary search dictionary above, except we keep the low and high
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
        next_word = make_next_word(word)

        # Starting at the current span, narrow the low and high independently.
        (new_low, low_found) = binary_search(self.words, word, self.low, self.high)
        (new_high, _) = binary_search(self.words, next_word, self.low, self.high)

        # The high binary search will find the next word off the end, so back up one.
        new_high -= 1

        if new_low <= new_high:
            return ProgressiveBinarySearchDictionary(self.words, low_found, new_low, new_high)
        else:
            return None

    @classmethod
    def make_dictionary(cls, words):
        return cls(sorted(words))

class ProgressiveTextBinarySearchDictionary(object):
    """This is the same algorithm as the above progressive binary search, but it operates
    on a single string of words, each terminated by a \n. It's quite slow to search, because
    each little operating must move forward or backward one one by scanning letters. The
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
        next_word = make_next_word(word)

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

def read_all_words():
    """Return an unsorted list of all words to process."""

    words = []

    timer = Timer()
    text = open("/usr/share/dict/words").read()
    timer.print_elapsed("Reading words file")

    timer = Timer()
    lines = text.split("\n")
    timer.print_elapsed("Splitting words file")

    timer = Timer()
    for word in lines:
        # Get rid of \n
        word = word.strip()

        # Skip capitalized words. Here we should also skip words with hyphens
        # and other symbols, but our dictionary doesn't have any anyway.
        if word and word[0].islower():
            # We work entirely in upper case.
            word = word.upper()

            # Skip short words.
            if len(word) >= 3:
                words.append(word)
    timer.print_elapsed("Processing %d words" % len(lines))

    return words

def generate_board(size=4):
    """Generate a random board and return it as a single array, row-major order."""

    if False:
        # Random
        board = []

        alphabet = range(ord("A"), ord("Z") + 1)

        for i in range(size*size):
            board.append(chr(random.choice(alphabet)))
    else:
        # New dice. http://www.luke-g.com/boggle/dice.html
        dice = [
                "AAEEGN",
                "ELRTTY",
                "AOOTTW",
                "ABBJOO",
                "EHRTVW",
                "CIMOTU",
                "DISTTY",
                "EIOSST",
                "DELRVY",
                "ACHOPS",
                "HIMNQU",
                "EEINSU",
                "EEGHNW",
                "AFFKPS",
                "HLNNRZ",
                "DEILRX",
        ]

        assert size*size == len(dice)

        random.shuffle(dice)

        board = list(random.choice(die) for die in dice)

    return board

def print_board(board, size):
    """Print a row-major order board."""

    for row in range(size):
        for column in range(size):
            print board[row*size + column],
        print
    print

def search(board, size, row, column, node, used, word, solutions):
    """Search the board for the end of a word starting a (row,column) and starting
    with prefix "word" in the dictionary node "node". Add words to the "solutions" set."""

    # Off the end of the board.
    if row < 0 or row >= size or column < 0 or column >= size:
        return

    # Already visited in this word.
    i = row*size + column
    if used[i]:
        return

    # Extend the word.
    ch = board[i]
    word += ch

    # See if the new word is in the dictionary.
    child = node.get_child(ch, word)
    if child is not None:
        if child.is_terminal:
            solutions.add(word)

        # Recurse with neighbors.
        used[i] = True
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr != 0 or dc != 0:
                    search(board, size, row + dr, column + dc, child, used, word, solutions)
        used[i] = False

def solve_board(board, size, dictionary):
    """Solve the board, returning a set of all words found in the dictionary."""

    used = [False]*(size*size)

    solutions = set()

    for row in range(size):
        for column in range(size):
            search(board, size, row, column, dictionary, used, "", solutions)

    return solutions

def main():
    size = 4

    # Try these classes.
    classes = [
            TrieDictionary,
            PrefixDictionary,
            BinarySearchDictionary,
            ProgressiveBinarySearchDictionary,
            ProgressiveTextBinarySearchDictionary,
    ]

    # Read the dictionary from disk.
    timer = Timer()
    words = read_all_words()
    timer.print_elapsed("Reading all words")

    # Create each of the dictionaries.
    dictionaries = []
    for cls in classes:
        timer = Timer()
        dictionaries.append(cls.make_dictionary(words))
        timer.print_elapsed("Creating %s" % cls.__name__)

    # Generate a random board.
    board = generate_board(size)
    print_board(board, size)

    # Solve the board using each of the dictionaries. We solve the board multiple
    # times to reduce noise.
    solutions = []
    for dictionary in dictionaries:
        timer = Timer()
        for i in range(20):
            solution = solve_board(board, size, dictionary)
        timer.print_elapsed("Solving with %s" % dictionary.__class__.__name__)
        solutions.append(solution)

    # Compare each dictionary solution to the first one to make sure we're implementing
    # these right.
    for i in range(1, len(solutions)):
        if solutions[0] != solutions[i]:
            print "In %s but not in %s: %s" % (
                    classes[0].__name__,
                    classes[i].__name__,
                    ", ".join(sorted(solutions[0].difference(solutions[i]))))
            print "In %s but not in %s: %s" % (
                    classes[i].__name__,
                    classes[0].__name__,
                    ", ".join(sorted(solutions[i].difference(solutions[0]))))

    print "All words: " + ", ".join(sorted(solutions[0]))

if __name__ == "__main__":
    main()
