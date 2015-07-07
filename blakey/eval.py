#!/usr/bin/env python

import yacc
import sys
import functions
from mingus.containers.instrument import MidiPercussionInstrument
from mingus.containers import Track

def get_result_of_last_statement(ctx, statement):
    patterns = []
    if statement is not None:
        patterns = functions.call_eval_from_python(ctx, statement)
    return convert_pattern_to_mingus_track(ctx, patterns), ctx

def convert_pattern_to_mingus_track(ctx, patterns):
    result = Track()
    result.instrument = MidiPercussionInstrument()
    for pattern in patterns:
        resolution = pattern.attributes["resolution"]
        for tick in pattern.get_ticks():
            placed = result.add_notes(tick.notes, resolution)
            if not placed:
                result.bars[-1].current_beat = result.bars[-1].length
                max_length = result.bars[-1].length - \
                        result.bars[-1].current_beat 
                if max_length == 0.0:
                    print "wut"
                    continue
                else:
                    print result.add_notes(tick.notes, 1.0 / max_length)
                    print max_length, 1.0 / max_length, resolution, result.bars[-1].current_beat +  max_length
    return result

def eval_file(file):
    return get_result_of_last_statement(*yacc.parse_file(file))

def eval_string(string):
    return get_result_of_last_statement(*yacc.parse_string(string))

if __name__ == '__main__':
    print eval_file(sys.argv[1])
