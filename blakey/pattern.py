#!/usr/bin/env python

import evaluable
import functions
from context import Context
from mingus.containers.instrument import MidiPercussionInstrument
from mingus.containers import Track, Bar, NoteContainer, Note

class PercussionPattern(evaluable.Pattern):
    pass

class PercussionPatternParser(evaluable.PatternParser):

    def init(self):
        self.percussion = MidiPercussionInstrument()
        self.perc_mapping = {
             'h': self.percussion.closed_hi_hat(),
             'H': self.percussion.open_hi_hat(),
             'b': self.percussion.bass_drum_1(),
             's': self.percussion.acoustic_snare(),
             'C': self.percussion.crash_cymbal_1(),
             't': self.percussion.high_tom(),
             'M': self.percussion.hi_mid_tom(),
             'm': self.percussion.low_mid_tom(),
             'l': self.percussion.low_floor_tom()
        }

    def parse(self, lines):
        tick_lists = []
        for line in lines:
            result = [ self.parse_char(char) for char in line if not char.isspace() ]
            tick_lists.append(result)
        new_body = self.merge_tick_lists(tick_lists)
        return self.new_percussion_pattern(new_body)

    def new_percussion_pattern(self, body):
        pattern = PercussionPattern(self.name, self.ctx)
        pattern.set_body(body)
        pattern.copy_current_attributes_from_context(self.ctx)
        return pattern

    def merge_tick_lists(self, lines):
        max_len = max(map(len, lines))
        result = [evaluable.Tick() for x in range(max_len)]
        for body in lines:
            for i, tick in enumerate(body):
                result[i].extend(tick)
        return result

    def parse_char(self, char):
        if char == '-':
            return evaluable.Tick()
        if char not in self.perc_mapping:
            raise evaluable.BlakeyException, \
                    "Error: unknown symbol in percussion pattern '%s'" % char
        return evaluable.Tick().add_note(self.perc_mapping[char])



ctx = Context()
ctx.set_attr("resolution", 8)
ctx.set_functions(functions.stdlib)
ctx.set("test", PercussionPatternParser("test", ctx).parse(["h-h-h-h-"]))

func = evaluable.Function("test_repeat", ctx)
func.set_function("sequence")
func.set_patterns(["test", "test"])

ctx.set("test_repeat", func)
patterns = functions.call_eval_from_python(ctx, "test_repeat")

def convert_pattern_to_mingus_track(ctx, pattern):
    result = Track()
    result.instrument = MidiPercussionInstrument()
    for pattern in patterns:
        resolution = pattern.attributes["resolution"]
        for tick in pattern.get_ticks():
            nc = NoteContainer(tick.notes)
            for n in nc.notes:
                n.channel = 9
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

print convert_pattern_to_mingus_track(ctx, patterns)
