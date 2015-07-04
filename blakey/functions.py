#!/usr/bin/env python

import random
import evaluable
import stacktrace

def _eval_choice(ctx, name, patterns):
    return [random.choice(patterns)]


def _eval_sequence(ctx, name, patterns):
    return patterns


def _eval(ctx, name, patterns):
    trace = stacktrace.StackTrace()
    stack = [(trace.start_level(), r) for r in reversed(patterns)]
    result = []
    while stack != []:
        e_level, e = stack.pop()
        trace.update_after_pop(e_level, e)
        try:
            elem = ctx.get(e)
            if elem.is_terminus():
                result.append(elem)
            else:
                print elem.eval(), e_level, e
                stack.extend(map(lambda s: (e_level + 1, s), reversed(elem.eval())))
        except Exception, e:
            trace.print_to_stderr(e)
    return result


def call_eval_from_python(ctx, name):
    f = evaluable.Function("top_level_eval", ctx)
    f.set_patterns([name])
    f.set_function("eval")
    return f.eval()



stdlib = {
        "choice": _eval_choice,
        "sequence": _eval_sequence, 
        "eval": _eval
}
