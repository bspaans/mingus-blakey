#!/usr/bin/env python

import argparse
from os import path

from mingus.containers import Track, Bar, NoteContainer, Note
from mingus.containers.instrument import MidiPercussionInstrument
from mingus.midi import midi_file_out

import eval

class Options:
    def __init__(self, input, output = None):
        self.input = input
        self.output = output

    def get_output_file(self):
        if self.output is None:
            input_base = path.splitext(self.input)[0]
            return input_base + ".mid"
        return self.output

def to_midi(filename, track, bpm = 120):
    midi_file_out.write_Track(filename, track, bpm)
    print "Written", filename

def get_args():
    parser = argparse.ArgumentParser(prog='blakey',
            description='Drum machine programming')
    parser.add_argument('input', metavar='INPUT', nargs=1, 
            help='the input file path')
    parser.add_argument('output', metavar='OUTPUT', nargs='?', 
            help='the optional output file path. Default is ./INPUT.mid')
    args = parser.parse_args()
    return Options(args.input[0], args.output)



def main():
    options = get_args()
    track, ctx = eval.eval_file(options.input)
    to_midi(options.get_output_file(), track, ctx.get_attr("bpm"))

if __name__ == '__main__':
    main()
