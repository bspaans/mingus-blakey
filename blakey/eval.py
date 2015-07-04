#!/usr/bin/env python

import yacc
import sys
import math
import random
from fractions import gcd
from mingus.containers.instrument import MidiPercussionInstrument
from mingus.containers import Track, Bar, NoteContainer, Note






def merge_two_patterns(pattern1, pattern2):
    resample_patterns(pattern1, pattern2)
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



def convert_pattern_to_mingus_track(ctx, pattern):
    result = Track()
    result.instrument = MidiPercussionInstrument()
    sequence = pattern 
    if type(pattern) is Choice:
        sequence = [pattern.choice()]
    elif type(pattern) is not list:
        sequence = [pattern]
    for pattern in sequence:
        resolution = pattern.attributes["resolution"]
        for beat in pattern.body:
            nc = NoteContainer()
            if beat is None:
                placed = result.add_notes(nc, resolution)
                continue
            for b in beat:
                note = convert_pattern_char_to_note(b)
                note.channel = 9
                nc.add_note(note)
            placed = result.add_notes(nc, resolution)
            if not placed:
                result.bars[-1].current_beat = result.bars[-1].length
                max_length = result.bars[-1].length - \
                        result.bars[-1].current_beat 
                if max_length == 0.0:
                    print "wut"
                    continue
                else:
                    print result.add_notes(nc, 1.0 / max_length)
                    print max_length, 1.0 / max_length, resolution, result.bars[-1].current_beat +  max_length
    return result


def eval_file(file):
    return eval_statements(yacc.parse_file(file))

def eval_string(string):
    return eval_statements(yacc.parse_string(string))


if __name__ == '__main__':
    print eval_file(sys.argv[1])
