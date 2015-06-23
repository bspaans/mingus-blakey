#!/usr/bin/env python 

import ply.yacc as yacc
import sys

from lexer import tokens


class Pattern(object):
    def __init__(self, name):
        self.name = name
        self.body = []
    def __str__(self):
        return 'pattern: %s\n%s' % (self.name, "\n".join(self.body))
    def __repr__(self):
        return str(self)
    def set_body(self, body):
        self.body = body

class VarDecl(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __str__(self):
        return "%s: %s" % (self.name, self.value)
    def __repr__(self):
        return str(self)

class Sequence(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'sequence: %s\n%s' % (self.name, "\n".join(self.body))
    def __repr__(self):
        return str(self)
    def set_body(self, body):
        self.body = body

def add_to_list(p):
    if p[1] is None:
        return []
    else:
        p[3].insert(0, p[1])
        return p[3] 

def p_statements(p):
    '''statements : statement NEWLINE statements
                  | empty'''
    p[0] = add_to_list(p)

def p_empty(p):
    '''empty :'''
    pass

def p_statement(p):
    '''statement : var_decl
                 | sequence
                 | pattern'''
    p[0] = p[1]

def p_sequence(p):
    '''sequence : sequence_header NEWLINE sequence_body'''
    p[1].set_body(p[3])
    p[0] = p[1]

def p_sequence_header(p):
    'sequence_header : SEQUENCE COLON IDENT '
    p[0] = Sequence(p[3])

def p_sequence_body(p):
    '''sequence_body : IDENT NEWLINE sequence_body 
                     | empty'''
    p[0] = add_to_list(p)

def p_pattern(p):
    'pattern : pattern_header NEWLINE pattern_body'
    p[1].set_body(p[3])
    p[0] = p[1]

def p_pattern_header(p):
    'pattern_header : PATTERN COLON value'
    p[0] = Pattern(p[3])

def p_pattern_body(p):
    '''pattern_body : PATTERN_LINE NEWLINE pattern_body 
                    | empty'''
    p[0] = add_to_list(p)

def p_value_integer(p):
    '''value : INTEGER 
             | IDENT'''
    p[0] = p[1]

def p_var_decl(p):
    '''var_decl : BPM COLON INTEGER
                | LOOP COLON INTEGER'''
    p[0] = VarDecl(p[1], p[3])


parser = yacc.yacc()

f = open(sys.argv[1])
s = f.read()
print s
#s = "bpm: 150\nloop: 3\n"
for statement in parser.parse(s):
    print statement
