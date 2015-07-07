#!/usr/bin/env python

class Evaluable(object):
    def __init__(self, name, ctx):
        self.name = name
        self.ctx = ctx
        self.init()
    def init(self): pass
    def eval(self): return []
    def is_terminus(self): return False

class BlakeyException(Exception):
    pass

class Function(Evaluable):
    def init(self):
        self.patterns = []
        self.function = None
    def set_patterns(self, patterns):
        self.patterns = patterns
    def set_function(self, function):
        self.function = function
    def eval(self):
        if self.function is None:
            raise Exception, "function has not been set for %s" % self.name
        func = self.ctx.get_function(self.function)
        return func(self.ctx, self.name, self.patterns)

class Tick(object):
    def __init__(self):
        self.notes = []
    def add_note(self, note):
        self.notes.append(note)
        return self
    def append(self, note):
        self.add_note(note)
    def copy(self):
        t = Tick()
        t.notes.extend(self.notes)
        return t
    def extend(self, other_tick):
        self.notes.extend(other_tick.notes)

class Pattern(Evaluable):
    def init(self):
        self.body = []
        self.attributes = {}
    def is_terminus(self):
        return True
    def set_body(self, body):
        self.body = body
    def append_to_body(self, tick):
        self.body.append(tick)
    def copy_current_attributes_from_context(self, ctx):
        self.attributes = ctx.copy_attributes()
    def get_resolution(self):
        return self.attributes["resolution"]
    def get_bpm(self):
        return self.attributes["bpm"]
    def eval(self): return []
    def get_ticks(self): return self.body
    def copy(self):
        p = self.__class__(self.name, self.ctx)
        p.set_body([])
        for beat in self.body:
            p.append_to_body(beat.copy())
        p.attributes = self.attributes.copy()
        return p 

class PatternParser(object):
    def __init__(self, name, ctx):
        self.name = name
        self.ctx = ctx
        self.init()
    def init(self): pass
    def parse(self, lines): pass

