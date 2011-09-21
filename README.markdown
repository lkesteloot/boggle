Boggle
======

Copyright 2011 Lawrence Kesteloot. Not affiliated with Hasbro or Boggle.

Generates Boogle boards and solves them using a variety of data structures
and algorithms. Run with:

    % python boggle.py

The solvers are:

1. **TrieDictionary**. This is a standard Trie. It takes forever to build, probably
    because of the node creation time in Python. It's the fastest to search.

2. **PrefixDictionary**. Stores a map of all words and prefixes
    of words (and whether each entry is
    a prefix or a word). This is moderately fast to build and has fast lookup,
    though slower than the Trie.

3. **BinarySearchDictionary**. Keeps a list of words and does a binary search for
    each prefix or word lookup. It's very fast to build but relatively slow to
    look up.

4. **ProgressiveBinarySearchDictionary**. This is like the binary search dictionary,
    except we keep the low and high
    values of the binary search as we zoom in on the word. "low" points to the first
    word that we could possibly make, and "high" to the last. So if we've traversed
    "GE" so far, "low" would point to the first word that starts with "GE" and "high"
    to the last word that starts with "GE".

    We find the last word by incrementing "GE" to "GF", finding the location of that,
    and backing up one word.

    This is as fast to create as the standard binary search, but somewhat faster to search
    because we're not starting the binary search from scratch each time. On the other hand,
    we're doing two binary searches per hit, so it's not as much of a win as we'd like.

5. **ProgressiveTextBinarySearchDictionary**. This is the same algorithm as
    the progressive binary search, but it operates
    on a single string of words, each terminated by a \n. It's quite slow to search, because
    each little operating must move forward or backward one word by scanning letters. The
    advantage is that creating it is just loading the file into memory with no processing,
    saving both time and memory.

