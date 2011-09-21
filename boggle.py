#!/usr/bin/python

# Copyright 2011 Lawrence Kesteloot

"""Solves a Boggle board using a variety of data structures."""

import random

from timer import Timer
import trie_dictionary
import prefix_dictionary
import binary_search_dictionary
import progressive_binary_search_dictionary
import progressive_text_binary_search_dictionary

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
    index = row*size + column
    if used[index]:
        return

    # Extend the word.
    ch = board[index]
    word += ch

    # See if the new word is in the dictionary.
    child = node.get_child(ch, word)
    if child is not None:
        # If the child is a terminal (the end of a word) then we've found a word.
        if child.is_terminal:
            solutions.add(word)

        # Recurse with eight neighbors.
        used[index] = True
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr != 0 or dc != 0:
                    search(board, size, row + dr, column + dc, child, used, word, solutions)
        used[index] = False

def solve_board(board, size, dictionary):
    """Solve the board, returning a set of all words found in the dictionary."""

    # Keep track of which dice we've used.
    used = [False]*(size*size)

    solutions = set()

    # Try each die for words starting there.
    for row in range(size):
        for column in range(size):
            search(board, size, row, column, dictionary, used, "", solutions)

    return solutions

def main():
    size = 4

    # Try these classes.
    classes = [
        trie_dictionary.TrieDictionary,
        prefix_dictionary.PrefixDictionary,
        binary_search_dictionary.BinarySearchDictionary,
        progressive_binary_search_dictionary.ProgressiveBinarySearchDictionary,
        progressive_text_binary_search_dictionary.ProgressiveTextBinarySearchDictionary,
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
