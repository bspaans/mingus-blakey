#!/usr/bin/env python

import functions

class Context(object):
    def __init__(self):
        self.context = {}
        self.functions = {}
        self.stdlib = functions.stdlib
        self.attr = {"resolution": 8, "bpm": 120}
        self.init()
    def init(self):
        pass
    def set_attr(self, name, value):
        self.attr[name] = value
    def get_attr(self, name):
        return self.attr[name]
    def copy_attributes(self):
        return self.attr.copy()
    def set(self, name, pattern):
        self.context[name] = pattern
    def get(self, name):
        if name not in self.context:
            raise Exception, "pattern %s is undefined" % name
        return self.context[name]
    def get_function(self, name):
        if name not in self.functions:
            raise Exception, "function %s is undefined" % name
        return self.functions[name]
    def set_functions(self, functions):
        for name, func in functions.iteritems():
            self.functions[name] = func
    def __str__(self):
        return str({"attributes": self.attr, "functions": self.functions,
            "context": self.context})
    def __repr__(self):
        return str(self)

class DefaultContext(Context):
    def init(self):
        self.functions = self.stdlib
