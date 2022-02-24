from math import *
from nodebox_wrapper import *  # pretend the Nodebox
from logging import getLogger, basicConfig, INFO, DEBUG
import nodebox_wrapper

speed(30)

R0 = 200
K = 2
KR = 100

# pentagonal bipyramid with a gap
labels = ["A", "B", "C", "D", "E", "F", "Z", "N"]
pairs = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F"), ("Z", "N"),
         ("A", "Z"), ("B", "Z"), ("C", "Z"), ("D", "Z"), ("E", "Z"), ("F", "Z"),
         ("A", "N"), ("B", "N"), ("C", "N"), ("D", "N"), ("E", "N"), ("F", "N"), ]

# pentagonal bipyramid
#labels = ["A", "B", "C", "D", "E", "Z", "N"]
# pairs  = [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","A"), ("Z","N"),
#          ("A","Z"), ("B","Z"), ("C","Z"), ("D","Z"), ("E","Z"),
#          ("A","N"), ("B","N"), ("C","N"), ("D","N"), ("E","N"),]

# hexagonal bipyramid
#labels = ["A", "B", "C", "D", "E", "F", "Z", "N"]
# pairs  = [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F"), ("F","A"), ("Z","N"),
#          ("A","Z"), ("B","Z"), ("C","Z"), ("D","Z"), ("E","Z"), ("F","Z"),
#          ("A","N"), ("B","N"), ("C","N"), ("D","N"), ("E","N"), ("F","N")]


def normalize(a):
    s = 0.0
    for i in range(3):
        s += a[i]**2
    s = 1.0 / sqrt(s)
    for i in range(3):
        a[i] *= s


def drawaface(a, b, c):
    ab = [0.0] * 3
    ac = [0.0] * 3
    for i in range(3):
        ab[i] = b.position[i] - a.position[i]
        ac[i] = c.position[i] - a.position[i]
    # normal vector
    n = [0.0] * 3
    n[0] = ab[1] * ac[2] - ab[2] * ac[1]
    n[1] = ab[2] * ac[0] - ab[0] * ac[2]
    n[2] = ab[0] * ac[1] - ab[1] * ac[0]
    normalize(n)
    hue = abs(n[0] + n[1] + n[2]) / sqrt(3.0)
    fill(hue, 0.5, abs(n[2]), 0.5)
    beginpath(a.position[0], a.position[1])
    lineto(b.position[0], b.position[1])
    lineto(c.position[0], c.position[1])
    lineto(a.position[0], a.position[1])
    endpath()


def drawfaces(vertices, triangles):
    for i, j, k in triangles.keys():
        drawaface(vertices[i], vertices[j], vertices[k])


def force(vertices, edges):
    for a, b in edges.keys():
        vertex0 = vertices[a]
        vertex1 = vertices[b]
        d = [0.0] * 3
        r = 0.0
        for i in range(3):
            d[i] = (vertex0.position[i] - vertex1.position[i])
            r += d[i]**2
        r = sqrt(r)
        for i in range(3):
            f = K * (r - R0) * d[i] / r
            vertex0.force[i] -= f
            vertex1.force[i] += f


def repulsiveforce(vertices, edges):
    for a, b in edges.keys():
        vertex0 = vertices[a]
        vertex1 = vertices[b]
        d = [0.0] * 3
        r = 0.0
        for i in range(3):
            d[i] = (vertex0.position[i] - vertex1.position[i])
            r += d[i]**2
        r = sqrt(r)
        for i in range(3):
            f = KR * d[i] / r
            vertex0.force[i] += f
            vertex1.force[i] -= f


# combinatorial function is available in python2.6
def combinations(elems, n):
    result = []
    if n == 1:
        for i in elems:
            result.append([i])
    else:
        tmp = list(elems)
        while len(tmp) > 0:
            head = tmp.pop(0)
            print(head, tmp)
            sub = combinations(tmp, n - 1)
            print("sub", sub)
            for i in sub:
                result.append(i + [head])
    print(elems, n, "=>", result)
    return result


def drawedges(edges):
    for a, b in edges.keys():
        vertex0 = vertices[a]
        vertex1 = vertices[b]
        line(vertex0.position[0], vertex0.position[1],
             vertex1.position[0], vertex1.position[1])


class Vertex():
    def __init__(self, label, pos=None):
        self.label = label
        if pos is None:
            self.position = [random() * 500, random() * 500, random() * 500]
        else:
            self.position = pos
        self.velocity = [0.0] * 3
        self.force = [0.0] * 3

    def force2vel(self):
        self.velocity = list(self.force)

    def progress(self, deltatime):
        for i in range(3):
            self.position[i] += self.velocity[i] * deltatime

    def draw(self):
        oval(self.position[0] - 1, self.position[1] - 1, 2, 2)

    def resetf(self):
        self.force = [0.0] * 3


def edgeExists(edges, i, j):
    return (i, j) in edges or (j, i) in edges


vertices = dict()
edges = dict()

for i in labels:
    #position, velocity, force
    vertices[i] = Vertex(i)
for i in pairs:
    edges[i] = True


repulsive = dict()
for i, j in combinations(labels, 2):
    if not edgeExists(edges, i, j):
        repulsive[(i, j)] = True


triangles = dict()
for i, j in edges.keys():
    for v in vertices.keys():
        if edgeExists(edges, i, v) and edgeExists(edges, j, v):
            s = sorted([i, j, v])
            triangles[tuple(s)] = True


repulse = False
hold = None
keyhold = None
face = False


def draw():
    global hold, keyhold, repulse, face
    colormode(HSB)
    force(vertices, edges)
    for vertex in vertices.values():
        vertex.force2vel()
        vertex.progress(0.1)
        vertex.resetf()
    if repulse:
        repulsiveforce(vertices, repulsive)
        text("Repulsive", 40, 40)
    stroke(0)
    if face:
        drawfaces(vertices, triangles)
    else:
        drawedges(edges)
    # マウスでノードをひっぱる。
    logger.debug(nodebox_wrapper.mousedown)
    if nodebox_wrapper.mousedown:
        logger.debug((MOUSEX,MOUSEY))
        if hold is None:
            min = 100000.0
            nod = None
            for vertex in vertices.values():
                dx = nodebox_wrapper.MOUSEX - vertex.position[0]
                dy = nodebox_wrapper.MOUSEY - vertex.position[1]
                d = dx**2 + dy**2
                if d < min:
                    min = d
                    hold = vertex
        dx = nodebox_wrapper.MOUSEX - hold.position[0]
        dy = nodebox_wrapper.MOUSEY - hold.position[1]
        logger.debug((dx, dy))
        hold.position[0] += dx / 2
        hold.position[1] += dy / 2
    else:
        hold = None

    if nodebox_wrapper.keydown:
        logger.debug("keydown")
        if not keyhold:
            # if key == "s":
            #     canvas.save("graphform.pdf")
            #     print("Saved")
            if nodebox_wrapper.key == "r":
                repulse = not repulse
            if nodebox_wrapper.key == "f":
                face = not face
        keyhold = True
    else:
        keyhold = None


# basicConfig(level=INFO, format="%(levelname)s %(message)s")
basicConfig(level=INFO, format="%(levelname)s %(message)s")
logger = getLogger()
logger.debug("Debug mode.")

animate(setup, draw)
