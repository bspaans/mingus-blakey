#!/usr/bin/env python

import evaluable
import functions
from context import Context
from mingus.containers.instrument import MidiPercussionInstrument

class PercussionPattern(evaluable.Pattern):
    def get_ticks(self):
        for tick in self.body:
            for note in tick.notes:
                note.channel = 9
        return self.body

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

