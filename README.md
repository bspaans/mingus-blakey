The Blakey Drum Computer
========================

# Install

```
pip install ply
pip install mingus
python setup.py install
```

# Usage

```
blakey INPUTFILE [OUTPUTFILE]
```

The input file should be in the format described below. Defining the output file is optional and defaults to the input files path, with its extension replaced by '.mid'.

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

# Percussion mapping

