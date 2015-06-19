#!/usr/bin/env python 

import ply.lex as lex

tokens = (
  'IDENT', 
  'COLON',
  'DASH',
)

t_IDENT = r'[a-zA-Z_]+'
t_COLON = r':'
t_DASH = r'\-'

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()


lexer.input("test: hello-haha_efef")
for tok in lexer:
    print tok
