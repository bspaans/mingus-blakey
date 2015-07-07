#!/usr/bin/env python

import random
import evaluable
import resampler
import stacktrace

def _eval_choice(ctx, name, patterns):
    return [random.choice(patterns)]

def _eval_sequence(ctx, name, patterns):
    return patterns

def _eval_combine(ctx, name, patterns):
    compiled_patterns = []
    for p in patterns:
        compiled_patterns.extend(call_eval_from_python(ctx, p))
    r = resampler.Resampler()
    result = reduce(r.resample_and_merge, compiled_patterns)
    return result

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
                evaled = elem.eval()
                if type(evaled) == list:
                    stack.extend(map(lambda e: (e_level + 1, e), evaled))
                elif evaled.is_terminus():
                    result.append(evaled)
                else:
                    raise evaluable.BlakeyException, "unexpected item in bagging area: %s" % (str(evaled))
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
        "combine": _eval_combine,
        "eval": _eval
}
