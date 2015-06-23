#!/usr/bin/env python

import yacc
import sys
import math
from fractions import gcd
from mingus.containers.instrument import MidiPercussionInstrument
from mingus.containers import Track, Bar, NoteContainer, Note

def lcm(self, *numbers):
    """Return lowest common multiple."""    
    def lcm(a, b):
        return (a * b) // gcd(a, b)
    return reduce(lcm, numbers, 1)


class Pattern(object):
    def __init__(self, name):
        self.name = name
        self.body = []
        self.attributes = {}
    def copy_current_attributes_from_context(self, ctx):
        self.attributes = ctx.copy_attributes()
    def set_body(self, body):
        self.body = body
    def copy(self):
        p = Pattern(self.name)
        p.body = []
        for beat in self.body:
            if type(beat) == list:
                copied_beat = []
                for b in beat:
                    copied_beat.append(b)
                p.body.append(copied_beat)
            else:
                p.body.append(beat)
        p.attributes = self.attributes.copy()
        return p 
    def __str__(self):
        return str(self.body)
    def get_resolution(self):
        return self.attributes["resolution"]
    def resample(self, new_resolution):
        current_resolution = self.get_resolution()
        if current_resolution == new_resolution:
            return self.body

        new_resolution = lcm(current_resolution, new_resolution)
        beat_every = new_resolution / current_resolution
        new_body = []
        j = 0
        for i in xrange(new_resolution):
            if i % beat_every == 0:
                new_body.append(self.body[j])
                j += 1
            else:
                new_body.append(None)
        self.body = new_body
        self.attributes["resolution"] = new_resolution


class Context(object):
    def __init__(self):
        self.context = {}
        self.attr = {"resolution": 8, "bpm": 120}
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
            print "unknown pattern", name
            return []
        return self.context[name]

def merge_pattern_bodies(bodies):
    max_len = max(map(len, bodies))
    result = [None] * max_len
    for body in bodies:
        for i, beat in enumerate(body):
            if beat is not None:
                if result[i] is None:
                    result[i] = []
                if type(beat) is list:
                    result[i].extend(beat)
                else:
                    result[i].append(beat)
    return result

def eval_pattern_body(body):
    evaled = []
    for line in body:
        result = []
        for char in line:
            if char.isspace():
                continue
            if char == '-':
                char = None
            result.append(char)
        evaled.append(result)
    return merge_pattern_bodies(evaled)

def eval_pattern(ctx, pattern):
    body = eval_pattern_body(pattern.body)
    result = Pattern(pattern.name)
    result.copy_current_attributes_from_context(ctx)
    result.set_body(body)
    ctx.set(pattern.name, result)

def eval_section(ctx, section):
    if section.section_type == 'combine':
        return eval_combine(ctx, section)
    elif section.section_type == 'sequence':
        return eval_sequence(ctx, section)

def eval_sequence(ctx, sequence):
    result = []
    for pattern in sequence.body:
        ptrn = ctx.get(pattern)
        if type(ptrn) is Pattern:
            result.append(ptrn.copy())
        else:
            result.extend(map(lambda p: p.copy(), ptrn))
    ctx.set(sequence.name, result)


def lookup_patterns(ctx, patterns):
    result = []
    for p in patterns:
        ptrn = ctx.get(p)
        if type(ptrn) is Pattern:
            result.append(ptrn)
        else:
            result.extend(ptrn)
    return result

def merge_two_patterns(pattern1, pattern2):
    resolution1 = pattern1.get_resolution()
    resolution2 = pattern2.get_resolution()
    if resolution1 != resolution2:
        new_resolution = lcm(resolution1, resolution2)
        pattern1.resample(new_resolution)
        pattern2.resample(new_resolution)
    bodies = [pattern1.body, pattern2.body]
    pattern1.set_body(merge_pattern_bodies(bodies))
    return pattern1

def eval_combine(ctx, section):
    patterns = lookup_patterns(ctx, section.body)
    result = reduce(merge_two_patterns, patterns)
    ctx.set(section.name, result)

def get_result_of_last_statement(ctx, statement):
    if statement is None:
        print "Nothing to do, bozo"
        sys.exit(0)
    stmt = ctx.get(statement)
    return convert_pattern_to_mingus_track(ctx, stmt)

percussion = MidiPercussionInstrument()
def convert_pattern_char_to_note(char):
    if char == 'h':
        return percussion.closed_hi_hat()
    elif char == 'H':
        return percussion.open_hi_hat()
    elif char == '-':
        return None
    elif char == 'b':
        return percussion.bass_drum_1()
    elif char == 's':
        return percussion.acoustic_snare()
    elif char == 'C':
        return percussion.crash_cymbal_1()
    print "Error: unknown symbol", char
    sys.exit(1)


def convert_pattern_to_mingus_track(ctx, pattern):
    result = Track()
    result.instrument = MidiPercussionInstrument()
    sequence = pattern 
    if type(pattern) is not list:
        sequence = [pattern]
    for pattern in sequence:
        resolution = pattern.attributes["resolution"]
        for beat in pattern.body:
            nc = NoteContainer()
            if beat is None:
                result.add_notes(nc, resolution)
                continue
            for b in beat:
                note = convert_pattern_char_to_note(b)
                note.channel = 9
                nc.add_note(note)
            result.add_notes(nc, resolution)
    return result

def eval_statements(statements):
    ctx = Context()
    last_statement = None
    for statement in statements:
        if type(statement) is yacc.VarDecl:
            ctx.set_attr(statement.name, statement.value)
        elif type(statement) is yacc.Pattern:
            eval_pattern(ctx, statement)
            last_statement = statement.name
        elif type(statement) is yacc.Section:
            eval_section(ctx, statement)
            last_statement = statement.name
    return get_result_of_last_statement(ctx, last_statement), ctx

def eval_file(file):
    return eval_statements(yacc.parse_file(file))


if __name__ == '__main__':
    print eval_file(sys.argv[1])
