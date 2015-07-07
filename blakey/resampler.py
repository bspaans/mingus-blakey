from fractions import gcd

class Resampler(object):

    def resample_and_merge(self, pattern1, pattern2):
        p1 = pattern1.copy()
        p2 = pattern2.copy()
        new_resolution = lcm(p1.get_resolution(), p2.get_resolution())
        p1.set_body(self.get_resampled_body(p1, new_resolution))
        p2.set_body(self.get_resampled_body(p2, new_resolution))
        for i, tick in enumerate(p1.body):
            tick.extend(p2.body[i])
        p1.attributes["resolution"] = new_resolution
        return p1

    def get_resampled_body(self, pattern, new_resolution):
        beat_every = new_resolution / pattern.get_resolution()
        new_body = []
        i, j = 0, 0
        while j < len(pattern.body):
            if i % beat_every == 0:
                new_body.append(pattern.body[j])
                j += 1
            else:
                new_body.append(evaluable.Tick())
            i += 1
        while i % beat_every != 0:
            new_body.append(evaluable.Tick())
            i += 1
        return new_body

def lcm(*numbers):
    """Return lowest common multiple."""    
    def lcm(a, b):
        return (a * b) // gcd(a, b)
    return reduce(lcm, numbers, 1)
