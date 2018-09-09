class JsonAccessor(object):
    """Wraps a JSON object as a python object."""
    def __init__(self, json):
        self._json = json

    def __getattr__(self, attr):
        j = self._json
        if attr not in j: raise AttributeError('Unknown attribute.')
        return j[attr]

    def __getitem__(self, key): return self._json[key]

    @property
    def json(self): return self._json

def _pluck(src, dst, mapping):
    for m in mapping:
        (s, d) = (m[0], m[1]) if len(m) == 2 else (m, '_' + m)
        setattr(dst, d, src[s])
    return dst
