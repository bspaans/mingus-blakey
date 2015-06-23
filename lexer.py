#!/usr/bin/env python 

import ply.lex as lex
import sys

tokens = (
  'IDENT', 
  'INTEGER',
  'COLON',
  'SEQUENCE',
  'PATTERN',
  'BPM',
  'LOOP', 
  'PATTERN_LINE',
  'NEWLINE',
)


reserved = ['pattern', 'sequence', 'bpm', 'loop']
t_INTEGER = r'[0-9]+'
t_COLON = r':'
t_PATTERN_LINE = r'\|.*\|'
t_NEWLINE = r'\n'

def t_ID(t):
    r'[a-zA-Z_]+'
    t.type = t.value.upper() if t.value in reserved else 'IDENT'
    return t


t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == '__main__':
    f = open(sys.argv[1])
    s = f.read()
    print s
    lexer.input(s)
    for token in lexer:
        print token
