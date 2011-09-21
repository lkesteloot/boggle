# Copyright 2011 Lawrence Kesteloot

"""Provides a class to time a snippet of code."""

import time

class Timer(object):
    """Times an event."""

    def __init__(self):
        self.start_time = time.time()

    def print_elapsed(self, label):
        elapsed = time.time() - self.start_time
        print "%s: %dms" % (label, elapsed*1000)
