#!/usr/bin/env python 

import ply.yacc as yacc
import sys

from lexer import tokens, INTEGER_VARS

class Section(object):
    def __init__(self, section_type, name):
        self.section_type = section_type
        self.name = name
        self.body = []
    def __str__(self):
        return '%s: %s\n%s' % (self.section_type.lower(), self.name, "\n".join(self.body))
    def __repr__(self):
        return str(self)
    def set_body(self, body):
        self.body = body

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
        if name in INTEGER_VARS:
            self.value = int(value)
    def __str__(self):
        return "%s: %s" % (self.name, self.value)
    def __repr__(self):
        return str(self)

def add_to_list(p):
    if p[1] is None and len(p) < 3:
        return []
    else:
        if p[1] is not None:
            p[3].insert(0, p[1])
        return p[3] 

def p_statements(p):
    '''statements : statement NEWLINE statements
                  | empty NEWLINE statements
                  | empty'''
    p[0] = add_to_list(p)


def p_empty(p):
    '''empty :'''
    pass

def p_statement(p):
    '''statement : var_decl
                 | section
                 | pattern'''
    p[0] = p[1]

def p_section(p):
    '''section : section_header NEWLINE section_body'''
    p[1].set_body(p[3])
    p[0] = p[1]

def p_section_header(p):
    '''section_header : section_type COLON IDENT'''
    p[0] = Section(p[1], p[3])

def p_section_type(p):
    '''section_type : SEQUENCE
                    | COMBINE'''
    p[0] = p[1]

def p_section_body(p):
    '''section_body : IDENT NEWLINE section_body
                    | empty '''

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
    if p[1] is not None:
        p[1] = p[1].replace("|", "")
    p[0] = add_to_list(p)

def p_value_integer(p):
    '''value : INTEGER 
             | IDENT'''
    p[0] = p[1]

def p_var_decl(p):
    '''var_decl : BPM COLON INTEGER
                | LOOP COLON INTEGER
                | RESOLUTION COLON INTEGER
                '''
    p[0] = VarDecl(p[1], p[3])


parser = yacc.yacc()

def parse_string(s):
    return parser.parse(s)

def parse_file(f):
    f = open(f)
    s = f.read()
    return parse_string(s)

if __name__ == '__main__':
    print parse_file(sys.argv[1])
