#!/usr/bin/env python 

import ply.lex as lex

tokens = (
  'IDENT', 
  'INTEGER',
  'COLON',
  'DASH',
  'SEQUENCE',
  'PATTERN',
  'BPM',
  'LOOP', 
  'NEWLINE'
)


reserved = ['pattern', 'sequence', 'bpm', 'loop']
t_INTEGER = r'[0-9]+'
t_COLON = r':'
t_DASH = r'\-'
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
