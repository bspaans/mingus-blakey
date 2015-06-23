#!/usr/bin/env python

import yacc
import sys

class Context(object):
    def __init__(self):
        self.context = {}
        self.attr = {}
    def set_attr(self, name, value):
        self.attr[name] = value
    def set(self, name, pattern):
        self.context[name] = pattern
    def get(self, name):
        if name not in self.context:
            print "unknown pattern", name
            return []
        return self.context[name]

def merge_pattern_bodies(bodies):
    max_len = max(map(len, bodies))
    result = [None] * max_len
    for body in bodies:
        for i, beat in enumerate(body):
            if beat is not None:
                if result[i] is None:
                    result[i] = []
                result[i].append(beat)
    return result

def eval_pattern_body(body):
    evaled = []
    for line in body:
        result = []
        for char in line:
            if char.isspace():
                continue
            if char == '-':
                char = None
            result.append(char)
        evaled.append(result)
    return merge_pattern_bodies(evaled)

def eval_pattern(ctx, pattern):
    body = eval_pattern_body(pattern.body)
    ctx.set(pattern.name, body)

def eval_sequence(ctx, sequence):
    result = []
    for pattern in sequence.body:
        ptrn = ctx.get(pattern)
        result.extend(ptrn)
    ctx.set(sequence.name, result)

def output_result_of_last_statement(ctx, statement):
    if statement is None:
        print "Nothing to do, bozo"
        sys.exit(0)
    print ctx.get(statement)


def eval_statements(statements):
    ctx = Context()
    last_statement = None
    for statement in statements:
        if type(statement) is yacc.VarDecl:
            ctx.set_attr(statement.name, statement.value)
        elif type(statement) is yacc.Pattern:
            eval_pattern(ctx, statement)
            last_statement = statement.name
        elif type(statement) is yacc.Sequence:
            eval_sequence(ctx, statement)
            last_statement = statement.name
    output_result_of_last_statement(ctx, last_statement)

def eval_file(file):
    eval_statements(yacc.parse_file(file))

if __name__ == '__main__':
    eval_file(sys.argv[1])
