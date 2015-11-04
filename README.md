The Blakey Drum Computer
========================

# Install

```
pip install ply
pip install mingus
pip install softsynth
python setup.py install
```

# Usage

```
blakey INPUTFILE [OUTPUTFILE]
```

The input file format is described below. 

A midi file is always created as part of the output. The location can be specified and defaults to the input file's location with its extension replaced by '.mid'. For example, these two commands do the same thing:

```
blakey examples/blues.blak examples/blues.mid
blakey examples/blues.blak
```


Additionally, you can also output a wave file with `--wave` or `-w`:

```
blakey INPUTFILE [OUTPUTFILE] --wave
```

This will create both the midi file and the wav file. 

```
blakey examples/blues.blak --wave
```

Will create both `examples/blues.mid` and `examples/blues.wav`.

```
blakey examples/blues.blak other_path.mid --wave
```

Will create `other_path.mid` and `other_path.wav`

If you have pyaudio installed you can also stream the output directly with `--stream` or `-s`:

```
blakey examples/blues.blak --stream
```

If you don't have pyaudio you can still stream the audio by piping it into aplay:

```
blakey examples/blues.blak --wave --stdout | aplay -f S16_LE -r 44100 -c 1
```


# Write drum patterns as text

```
bpm: 120
resolution: 8

pattern: simple_beat
|h-h-h-h-|
|--s---s-|
|b---b---|
```

This defines a simple beat using a closed hi-hat, bass drum and snare. 
We can also use a different resolution, such as quarter notes:

```
bpm: 120
resolution: 4

pattern: simple_beat
|hhhh|
|-s-s|
|b-b-|
```

# Combining patterns

```
bpm: 120
resolution: 8

pattern: hihat
|h-h-h-h-|

pattern: snare
|--s---s-|

pattern: base
|b---b---|

combine: simple_beat
hihat
snare
base
```

You can also combine patterns with different resolutions:

```
bpm: 120
resolution: 8

pattern: hihat
|h-h-h-h-|

resolution: 4
pattern: snare
|-s-s|

pattern: base
|b-b-|

combine: simple_beat
hihat
snare
base
```

# Sequencing patterns

The sequence declaration can be used to combine patterns in sequence:

```
bpm: 120
resolution: 4

pattern: simple_beat_opening
|Chhh|
|-s-s|
|b-b-|

pattern: simple_beat_regular
|hhhh|
|-s-s|
|b-b-|

sequence: simple_beat
simple_beat_opening 
simple_beat_regular
simple_beat_regular
simple_beat_regular
```

# Choice patterns

The choice declaration can be used to pick a random sequence or pattern:

```
bpm: 120
resolution: 8

pattern: hihat
|h-h-h-h-|

pattern: hihat2
|-h-h-h-h|

choice: surprise_me
hihat
hihat2

sequence: surprise_song
surprise_me
surprise_me
surprise_me
surprise_me
```

# Percussion mapping

TODO

# Running tests

```
nosetests
```
