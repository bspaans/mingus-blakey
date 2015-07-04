#!/usr/bin/env python

import sys
import traceback
import evaluable

class StackTrace(object):
    def __init__(self):
        self.level = -1
        self.trace = []

    def start_level(self):
        return 0

    def update_after_pop(self, new_level, function):
        if new_level > self.level:
            self.trace.append(function)
            self.level += 1
        elif new_level < self.level:
            self.trace.pop()
            self.level -= 1

    def print_to_stderr(self, exception):
        if type(exception) is evaluable.BlakeyException:
            msg = str(exception)
            result = ["Error: " + msg, '', 'Trace:']
            for level, function in enumerate(self.trace):
                result.append("  %d. %s" % (level, function))
            sys.stderr.write("\n".join(result) + "\n")
        else:
            traceback.print_exc(exception)
