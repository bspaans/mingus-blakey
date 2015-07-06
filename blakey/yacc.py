#!/usr/bin/env python 

import ply.yacc as yacc
import sys

import context
import evaluable
import pattern
from lexer import tokens, INTEGER_VARS

CTX = None


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
    p[1].set_patterns(p[3])
    CTX.set(p[1].name, p[1])
    p[0] = p[1].name

def p_section_header(p):
    '''section_header : section_type COLON IDENT'''
    func = evaluable.Function(p[3], CTX)
    func.set_function(p[1])
    p[0] = func

def p_section_type(p):
    '''section_type : SEQUENCE
                    | COMBINE
                    | CHOICE'''
    p[0] = p[1]

def p_section_body(p):
    '''section_body : IDENT NEWLINE section_body
                    | empty '''
    p[0] = add_to_list(p)


def p_pattern(p):
    'pattern : pattern_header NEWLINE pattern_body'
    pattern = p[1].parse(p[3])
    CTX.set(p[1].name, pattern)
    p[0] = p[1].name

def p_pattern_header(p):
    'pattern_header : PATTERN COLON value'
    p[0] = pattern.PercussionPatternParser(p[3], CTX)

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
    value = int(p[3]) if p[1] in INTEGER_VARS else p[3]
    CTX.set_attr(p[1], value)
    p[0] = None


parser = yacc.yacc()

def parse_string(s):
    global CTX
    CTX = context.DefaultContext()
    result = parser.parse(s)
    return CTX, result[-1]

def parse_string_with_context(s, ctx):
    global CTX
    CTX = ctx
    result = parser.parse(s)
    return CTX, result[-1]

def parse_file(f):
    f = open(f)
    s = f.read()
    f.close()
    return parse_string(s + "\n")

def parse_file_with_context(s, ctx):
    f = open(f)
    s = f.read()
    f.close()
    return parse_string_with_context(s + "\n", ctx)

if __name__ == '__main__':
    print parse_file(sys.argv[1])
