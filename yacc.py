#!/usr/bin/env python 

import ply.yacc as yacc
import sys

from lexer import tokens


class Pattern(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Pattern %s' % self.name

class VarDecl(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __str__(self):
        return "Var %s = %s" % (self.name, self.value)


def p_statements(p):
    '''statement : sequence 
                 | pattern '''
    p[0] = p[1]

def p_sequence(p):
    'sequence : SEQUENCE COLON IDENT NEWLINE'
    p[0] = p[3]

def p_pattern(p):
    'pattern : PATTERN COLON value'
    p[0] = Pattern(p[3])

def p_value_integer(p):
    '''value : INTEGER 
             | IDENT'''
    p[0] = p[1]



parser = yacc.yacc()

while True:
    try:
        s = raw_input("aight> ")
    except:
        print "whatevs"
        sys.exit(1)
    result = parser.parse(s)
    print result
