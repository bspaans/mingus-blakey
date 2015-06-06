#!/usr/bin/env python

from mingus.containers import Track, Bar, NoteContainer, Note
from mingus.containers.instrument import MidiPercussionInstrument
from mingus.midi import midi_file_out

import dsl

def to_midi(filename, track, bpm = 120):
    midi_file_out.write_Track(filename, track, bpm)


result, bpm = dsl.parse_string(dsl.example)
to_midi("test.mid", result[0], bpm)
