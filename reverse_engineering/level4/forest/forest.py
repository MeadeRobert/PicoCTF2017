from collections import namedtuple

s = "yuoteavpxqgrlsdhwfjkzi_cmbn"

Tree = namedtuple("Tree", "l r v")

def insert(c, t):
    if t == None:
        return Tree(None, None, c)
    elif c <= t.v:
        return Tree(insert(c, t.l), t.r, t.v)
    else:
        return Tree(t.l, insert(c, t.r), t.v)

m = None

for c in s:
    m = insert(c, m)

def find(t, p):
    if p == "":
        return t.v
    elif p[0] == 'L':
        return find(t.l, p[1:])
    else:
        return find(t.r, p[1:])

paths = "DLLDLDLLLLLDLLLLRLDLLDLDLLLRRDLLLLRDLLLLLDLLRLRRRDLLLDLLLDLLLLLDLLRDLLLRRLDLLLDLLLLLDLLLRLDLLDLLRLRRDLLLDLLRLRRRDLLRDLLLLLDLLLRLDLLDLLRLRRDLLLLLDLLRDLLLRRLDLLLDLLLLLDLLRDLLRLRRDLLLDLLLDLLRLRRRDLLLLLDLLLLRLDLLLRRLRRDDLLLRRDLLLRRLRDLLLRLDLRRDDLLLRLDLLLRRRDLLRLRRRDLRRLD".split('D')

r = ""

for p in paths:
    r += find(m, p)

print(r)
