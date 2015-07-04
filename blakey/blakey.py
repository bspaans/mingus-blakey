#!/usr/bin/env python

import argparse
from os import path

from mingus.containers import Track, Bar, NoteContainer, Note
from mingus.containers.instrument import MidiPercussionInstrument
from mingus.midi import midi_file_out

from synth.wave_writer import WaveWriter
from synth.synthesizer import Synthesizer
import synth.options

import eval

class Options:
    def __init__(self, input, output = None, wave = False, stream = False, stdout = False):
        self.input = input
        self.output = output
        self.write_wave = wave 
        self.write_wave_to_stdout = stdout
        self.write_stream = stream

    def get_output_file(self, default_extension = '.mid'):
        if self.output is None:
            input_base = path.splitext(self.input)[0]
            return input_base + default_extension
        return self.output

def to_midi(filename, track, bpm = 120):
    midi_file_out.write_Track(filename, track, bpm)
    print "Written", filename

def to_wav(input, output, track, options, bpm):
    synth_options = synth.options.Options(input, output, bpm)
    synth_options.write_wave = True
    synth_options.write_wave_to_stdout = options.write_wave_to_stdout

    s = Synthesizer(synth_options).load_from_midi(input)
    WaveWriter(synth_options).output(s)

def stream(input, options, bpm):
    from synth import stream
    synth_options = synth.options.Options(bpm = bpm)
    s = Synthesizer(synth_options).load_from_midi(input)
    stream.stream_to_pyaudio(synth_options, s)

def get_args():
    parser = argparse.ArgumentParser(prog='blakey',
            description='Drum machine programming')
    parser.add_argument('input', metavar='INPUT', nargs=1, 
            help='the input file path')
    parser.add_argument('output', metavar='OUTPUT', nargs='?', 
            help='the optional output file path. Default is ./INPUT.mid')
    parser.add_argument('-w', '--wave', action='store_true',
            help='Output wave file.')
    parser.add_argument('-s', '--stream', action='store_true',
            help='Stream')
    parser.add_argument('--stdout', action='store_true',
            help='Also write PCM data to stdout. Only valid in conjunction with the --wave flag.')
    args = parser.parse_args()
    return Options(args.input[0], args.output, args.wave, args.stream)



def main():
    options = get_args()
    track, ctx = eval.eval_file(options.input)
    bpm = ctx.get_attr('bpm')

    midi_file = options.get_output_file('.mid')
    to_midi(midi_file, track, ctx.get_attr("bpm"))

    if options.write_wave:
        to_wav(midi_file, options.get_output_file('.wav'), track, options, bpm)
    if options.write_stream:
        stream(midi_file, options, bpm)

if __name__ == '__main__':
    main()
