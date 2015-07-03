#!/usr/bin/env python 

from blakey import eval

def test_eval():
    track, ctx= eval.eval_string("""
bpm: 150
resolution: 8

pattern: beat1
|hhhhhhhh|
|-b---s--|

pattern: beat2
|HHHHHHHH|
|-b---s--|

choice: beat
beat1
beat2

sequence: random_beat
beat
beat
beat
beat
beat
beat

sequence: song
random_beat
random_beat
random_beat
random_beat
random_beat
random_beat

""")
    nr_of_bars = 0
    nr_beat1 = 0
    for bar in track:
        if bar.current_beat != 0.0:
            nr_of_bars += 1
            note = bar[0][2][0]
            if note.to_shorthand() == 'F#':
                nr_beat1 += 1

    expected_nr_of_bars = 36
    assert nr_of_bars == expected_nr_of_bars, "Not enough bars, mate"
    assert nr_beat1 != expected_nr_of_bars, "Doesn't look random to me, mate"
    assert nr_beat1 != 0, "Doesn't look random to me, mate"
