#!/usr/bin/env python 

from mingus.containers.instrument import MidiPercussionInstrument
from mingus.containers import Track, Bar, NoteContainer, Note

example = """
bpm: 120    

meter: 4/4
resolution: 12

section:
C-h h-h h-h h-h h-h h-h h-h h-h    h-h h-h h-h h-h h-h h-C h-h C-h
b-- s-- b-- s-- b-- s-- b-- sss    b-- s-- b-- s-- b-- s-- b-- s--

"""

# build up beats from base blocks?
# blocks are named drum patterns
# use named sequences to combine patterns
# room for experimental combinations (mixing, ANDing, ORing, XORing repeating patterns)
#    and procedural generation
# 
# could provide a "standard library" of base blocks with drum rudiments
#

future_format = """
bpm: 120    

meter: 4/4
resolution: 12

block: start_with_crash
C-h h-h
b-- s--

block: regular
h-h h-h
b-- s--

block: ending
h-h h-h
b-- sss

sequence: bar
start_with_crash
regular
regular
ending

sequence: bar_without_crash_at_start
regular
regular
regular
ending

sequence: main
bar
bar_without_crash_at_start
bar_without_crash_at_start
bar_without_crash_at_start

"""

percussion = MidiPercussionInstrument()

def parse_bpm_command(line):
    bpm_str = line[4:].strip()
    if not bpm_str.isdigit():
        print "Error: bpm is not an integer:", bpm_str
        sys.exit(1)
    return int(bpm_str)

def parse_meter_command(line):
    meter_str = line[6:].strip()
    if meter_str.find("/") == -1:
        print "Error: invalid meter format:", meter_str
        sys.exit(1)
    return (4, 4)

def parse_resolution_command(line):
    res_str = line[11:].strip()
    if not res_str.isdigit():
        print "Error: resolution is not an integer:", res_str
        sys.exit(1)
    return int(res_str)

def parse_section_line(line):
    result = []
    for char in line:
        if char == 'h':
            result.append(percussion.closed_hi_hat())
        elif char == '-':
            result.append(None)
        elif char == 'b':
            result.append(percussion.bass_drum_1())
        elif char == 's':
            result.append(percussion.acoustic_snare())
        elif char == 'C':
            result.append(percussion.crash_cymbal_1())
    return result

def section_to_track(section, resolution, meter):
    max_len = max(map(len, section))
    result = Track()
    result.instrument = percussion
    for i in range(max_len):
        nc = NoteContainer()
        for s in section:
            if i < len(s) and s[i] is not None:
                nc.add_note(s[i])
                s[i].channel = 9
        result.add_notes(nc, resolution)
    return result

def parse_string(string):
    lines = string.split("\n")
    bpm = 120
    meter = (4, 4)
    resolution = 4
    result = []
    section = []
    in_section = False
    for line in lines:
        if line.strip() == '' or line.startswith('#') or line.startswith('//'):
            if in_section and len(section) > 0:
                result.append(section_to_track(section, resolution, meter)) # commit section
                section = []
            continue
        elif line.startswith("bpm:"):
            bpm = parse_bpm_command(line)
            continue
        elif line.startswith("meter:"):
            meter = parse_meter_command(line)
            continue
        elif line.startswith("resolution:"):
            resolution = parse_resolution_command(line)
            continue
        elif line.startswith("section:"):
            in_section = True
            continue
        else:
            section.append(parse_section_line(line))
    print result
    return result, bpm

