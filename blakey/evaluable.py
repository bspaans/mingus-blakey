#!/usr/bin/env python



class Evaluable(object):
    def __init__(self, name, ctx):
        self.name = name
        self.ctx = ctx
        self.init()
    def init(self):
        pass
    def eval(self):
        return []
    def is_terminus(self):
        return False

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
    def copy(self):
        t = Tick()
        for n in self.notes:
            t.notes.append(n)
        return t
    def extend(self, other_tick):
        for note in other_tick.notes:
            self.notes.append(note)


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
    def eval(self):
        return []
    def get_ticks(self):
        return self.body

    def copy(self):
        p = Pattern(self.name, self.ctx)
        p.set_body([])
        for beat in self.body:
            p.append_to_body(beat.copy())
        p.attributes = self.attributes.copy()
        return p 

    def resample_patterns(self, pattern):
        p1 = self.copy()
        p2 = self.copy()
        new_resolution = lcm(self.get_resolution(), new_resolution)
        if p1.get_resolution() != new_resolution:
            p1.resample()
        if p2.get_resolution() != new_resolution:
            p2.resample()
        return p1, p2

    def resample(self, new_resolution):
        self.set_body(self.get_resampled_body(new_resolution))
        self.attributes["resolution"] = new_resolution

    def get_resampled_body(self, new_resolution):
        beat_every = new_resolution / self.get_resolution()
        new_body = []
        i, j = 0, 0
        while j < len(self.body):
            if i % beat_every == 0:
                new_body.append(self.body[j])
                j += 1
            else:
                new_body.append(None)
            i += 1
        while i % beat_every != 0:
            new_body.append(None)
            i += 1
        return new_body

class PatternParser(object):
    def __init__(self, name, ctx):
        self.name = name
        self.ctx = ctx
        self.init()
    def init(self):
        pass
    def parse(self, lines):
        pass

def lcm(*numbers):
    """Return lowest common multiple."""    
    def lcm(a, b):
        return (a * b) // gcd(a, b)
    return reduce(lcm, numbers, 1)
