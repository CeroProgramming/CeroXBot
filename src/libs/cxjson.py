from json import load as l
from json import dump as d

def load(fp):
    with open(fp, 'r') as f:
        res = l(f)
    return res

def dump(data, fp):
    with open(fp, 'w') as f:
        d(data, f)
    return
