# for NodeBox.app
from math import *
from nodebox_wrapper import *  # pretend the Nodebox
from logging import getLogger, basicConfig, INFO, DEBUG
import nodebox_wrapper

from math import *
speed(30)

R0 = 200
K = 2.5
KRmax = 80
KR = 0
# pentagonal bipyramid with a gap
# labels = ["A", "B", "C", "D", "E", "F", "Z", "N"]


# hexagonal bipyramid
#labels = ["A", "B", "C", "D", "E", "F", "Z", "N"]
# pairs  = [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F"), ("F","A"), ("Z","N"),
#         ("A","Z"), ("B","Z"), ("C","Z"), ("D","Z"), ("E","Z"), ("F","Z"),
#        ("A","N"), ("B","N"), ("C","N"), ("D","N"), ("E","N"), ("F","N")]


# icosahedron with a gap
#labels = [0, 1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
# pairs  = [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),
#          (0,8),(0,9),(0,10),(0,11),(0,12),
#          (0,13),(0,14),(0,15),(0,16),(0,17),(0,18),
#          (0,19),(0,20),(0,21),(0,22),
#          (1,2),(2,3),(3,1),
#          (1,4),(2,4),(2,5),(3,5),(3,6),(1,6),
#          (1,7),(4,7),(2,8),(5,8),(3,9),(6,9),
#          (2,10),(4,10),(3,11),(5,11),(1,12),(6,12),
#          (4,13),(7,13),(5,14),(8,14),(6,15),(9,15),
#          (4,16),(10,16),(5,17),(11,17),(6,18),(12,18),
#          (10,19),(16,19),(11,20),(17,20),(12,21),(18,21),
#          (18,22),(21,22),]


# # Kasper 24-hedron
# labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
# pairs = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
#          (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14),
#          (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
#          (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 2),
#          (2, 8), (3, 9), (4, 10), (5, 11), (6, 12), (7, 13),
#          (2, 13), (3, 8), (4, 9), (5, 10), (6, 11), (7, 12),
#          (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 8),
#          (8, 14), (9, 14), (10, 14), (11, 14), (12, 14), (13, 14)]

# # Kasper 26-hedron
# labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
# pairs = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
#          (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15),
#          (1, 2), (2, 3), (3, 1),
#          (1, 4), (2, 4), (2, 5), (3, 5), (3, 6), (1, 6),
#          (1, 7), (4, 7), (6, 7),
#          (2, 8), (4, 8), (5, 8),
#          (3, 9), (5, 9), (6, 9),
#          (7, 10), (8, 11), (9, 12),
#          (10, 6), (11, 4), (12, 5),
#          (7, 11), (8, 12), (9, 10),
#          (10, 13), (13, 11), (11, 14), (14, 12), (12, 15), (15, 10),
#          (7, 13), (8, 14), (9, 15),
#          (13, 14), (14, 15), (15, 13), ]

# # Kasper 20-hedron
# labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# pairs = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
#          (0, 8), (0, 9), (0, 10), (0, 11), (0, 12),
#          (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
#          (2, 3), (3, 4), (4, 5), (5, 6), (6, 2),
#          (2, 7), (3, 8), (4, 9), (5, 10), (6, 11),
#          (2, 8), (3, 9), (4, 10), (5, 11), (6, 7),
#          (7, 8), (8, 9), (9, 10), (10, 11), (11, 7),
#          (7, 12), (8, 12), (9, 12), (10, 12), (11, 12), ]

# # Kasper 28-hedron
# labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
# pairs = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
#          (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16),
#          (1, 2), (2, 3), (3, 1),
#          (1, 4), (2, 4), (2, 5), (3, 5), (3, 6), (1, 6),
#          (1, 7), (4, 7), (6, 7),
#          (2, 8), (4, 8), (5, 8),
#          (3, 9), (5, 9), (6, 9),
#          (7, 10), (8, 11), (9, 12),
#          (10, 6), (11, 4), (12, 5),
#          (10, 13), (11, 14), (12, 15),
#          (13, 7), (14, 8), (15, 9),
#          (13, 4), (13, 11),
#          (14, 5), (14, 12),
#          (15, 6), (15, 10),
#          (10, 16), (11, 16), (12, 16), (13, 16), (14, 16), (15, 16),
#          ]

# # pentagonal bipyramid
# labels = ["A", "B", "C", "D", "E", "Z", "N"]
# pairs = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "A"), ("Z", "N"),
#          ("A", "Z"), ("B", "Z"), ("C", "Z"), ("D", "Z"), ("E", "Z"),
#          ("A", "N"), ("B", "N"), ("C", "N"), ("D", "N"), ("E", "N"), ]

# # octahedron
# labels = ["A", "B", "C", "D", "E", "F"]
# pairs = [("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"), ("B", "C"), ("C", "D"),
#          ("D", "E"), ("E", "B"), ("B", "F"), ("C", "F"), ("D", "F"), ("E", "F")]

# # Dodecahedron
# labels = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
#           "10", "11", "12", "13", "14", "15", "16", "17", "18", "19"]
# pairs = [("0", "1"), ("1", "2"), ("2", "3"), ("3", "4"), ("4", "0"),
#          ("0", "5"), ("1", "6"), ("2", "7"), ("3", "8"), ("4", "9"),
#          ("10", "5"), ("11", "6"), ("12", "7"), ("13", "8"), ("14", "9"),
#          ("10", "6"), ("11", "7"), ("12", "8"), ("13", "9"), ("14", "5"),
#          ("10", "15"), ("11", "16"), ("12", "17"), ("13", "18"), ("14", "19"),
#          ("19", "15"), ("15", "16"), ("16", "17"), ("17", "18"), ("18", "19"), ]

# # Dodecahedra
# labels = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
#           "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
#           "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
#           "30", "31", "32", "33", "34",
#           ]
# pairs = [("0", "1"), ("1", "2"), ("2", "3"), ("3", "4"), ("4", "0"),
#          ("0", "5"), ("1", "6"), ("2", "7"), ("3", "8"), ("4", "9"),
#          ("10", "5"), ("11", "6"), ("12", "7"), ("13", "8"), ("14", "9"),
#          ("10", "6"), ("11", "7"), ("12", "8"), ("13", "9"), ("14", "5"),
#          ("10", "15"), ("11", "16"), ("12", "17"), ("13", "18"), ("14", "19"),
#          ("19", "15"), ("15", "16"), ("16", "17"), ("17", "18"), ("18", "19"),
#          ("20", "15"), ("21", "16"), ("22", "17"), ("23", "18"), ("24", "19"),
#          ("21", "25"), ("22", "26"), ("23", "27"), ("24", "28"), ("20", "29"),
#          ("20", "25"), ("21", "26"), ("22", "27"), ("23", "28"), ("24", "29"),
#          ("30", "25"), ("31", "26"), ("32", "27"), ("33", "28"), ("34", "29"),
#          ("30", "31"), ("31", "32"), ("32", "33"), ("33", "34"), ("34", "30"),
#          ]


def normalize(a):
    s = 0.0
    for i in range(3):
        s += a[i]**2
    s = 1.0 / sqrt(s)
    for i in range(3):
        a[i] *= s


def setdepth(triangle, pi, pj, pk):
    triangle["Z"] = pi.position[2] + pj.position[2] + pk.position[2]


def setcolor(triangle, a, b, c, decay):
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
    #hue = hue + 0.5
    if hue > 1.0:
        hue -= 1.0
    # final opacity is A+B
    A = 0.3
    B = 0.4
    opacity = (1. - 0.99**decay) * A + B
    triangle["C"] = color(hue, 0.8, abs(n[2]) * 0.4 + 0.6, opacity)


def drawfaces_(faces, vertices):
    stroke(0)
    strokewidth(3)
    k = faces.keys()
    for face in sorted(k, key=lambda x: -faces[x]["Z"]):
        fill(faces[face]["C"])
        va, vb, vc = face
        a = perspective(vertices[va])
        b = perspective(vertices[vb])
        c = perspective(vertices[vc])
        beginpath(a[0], a[1])
        lineto(b[0], b[1])
        lineto(c[0], c[1])
        # closepath()
        #lineto( a.position[0], a.position[1] )
        endpath()


def drawaface_obsolete(a, b, c):
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


def drawfaces(vertices, triangles, decay):
    for i, j, k in triangles.keys():
        setdepth(triangles[(i, j, k)], vertices[i], vertices[j], vertices[k])
        setcolor(triangles[(i, j, k)], vertices[i],
                 vertices[j], vertices[k], decay)
    drawfaces_(triangles, vertices)


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


def repulsiveforce(vertices, edges, mul):
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
            if r < R0 * mul:
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
            print (head, tmp)
            sub = combinations(tmp, n - 1)
            print ("sub", sub)
            for i in sub:
                result.append(i + [head])
    print (elems, n, "=>", result)
    return result


def perspective(v):
    zoom = 1  # 000 / (1000 - v.position[2])
    v.position[3] = v.position[0] * zoom
    v.position[4] = v.position[1] * zoom
    return v.position[3:5]
#    return v.position[0:2]


def drawedges(edges):
    for a, b in edges.keys():
        vertex0 = perspective(vertices[a])
        vertex1 = perspective(vertices[b])
        line(vertex0[0], vertex0[1],
             vertex1[0], vertex1[1])


def drawlabels(vertices):
    for v in vertices.values():
        vv = perspective(v)
        text(v.label, vv[0], vv[1])


class Vertex():
    def __init__(self, label, pos=None):
        self.label = label
        if pos is None:
            self.position = [
                random() * 500,
                random() * 500,
                random() * 500,
                0,
                0]  # last 2 are the pos on the screen
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



repulse = 0
hold = None
keyhold = None
face = True
label = True
decay = 0
vertices = dict()
edges = dict()
repulsive = dict()
triangles = dict()

def draw():
    global hold, keyhold, repulse, face, label, KR, decay, vertices, edges
    colormode(HSB)
    decay += 1
    force(vertices, edges)
    for vertex in vertices.values():
        vertex.force2vel()
        vertex.progress(0.05)
        vertex.resetf()
    if repulse:
        text("Repulsive", 40, 40)
        KR = KRmax - (KRmax - KR) * 0.9
    else:
        KR *= 0.9
    repulsiveforce(vertices, repulsive, repulse)
    stroke(0)
    if face:
        drawfaces(vertices, triangles, decay)
    else:
        drawedges(edges)
    if label:
        drawlabels(vertices)
    # マウスでノードをひっぱる。
    if nodebox_wrapper.mousedown:
        decay = 0
        if hold is None:
            min = 100000.0
            nod = None
            for vertex in vertices.values():
                dx = nodebox_wrapper.MOUSEX - vertex.position[3]
                dy = nodebox_wrapper.MOUSEY - vertex.position[4]
                d = dx**2 + dy**2
                if d < min:
                    min = d
                    hold = vertex
        dx = nodebox_wrapper.MOUSEX - hold.position[3]
        dy = nodebox_wrapper.MOUSEY - hold.position[4]
        hold.position[0] += dx / 2
        hold.position[1] += dy / 2
    else:
        hold = None

    if nodebox_wrapper.keydown:
        if not keyhold:
            # if nodebox_wrapper.key == "s":
            #     canvas.save("graphform.pdf")
            #     print ("Saved")
            if nodebox_wrapper.key == "r":
                if not repulse:
                    repulse = 4
                else:
                    repulse -= 1
            if nodebox_wrapper.key == "f":
                face = not face
            if nodebox_wrapper.key == "l":
                label = not label
        keyhold = True
    else:
        keyhold = None

def Render(pairs):
    labels = set()
    for i,j in pairs:
        labels.add(i)
        labels.add(j)
    labels = list(labels)

    for i in labels:
        #position, velocity, force
        vertices[i] = Vertex(i)
    for i in pairs:
        edges[i] = True


    for i, j in combinations(labels, 2):
        if not edgeExists(edges, i, j):
            repulsive[(i, j)] = True

    for i, j in edges.keys():
        for v in vertices.keys():
            if edgeExists(edges, i, v) and edgeExists(edges, j, v):
                s = sorted([i, j, v])
                triangles[tuple(s)] = dict()  # z axis and color
    animate(setup, draw)


def main():

    # basicConfig(level=INFO, format="%(levelname)s %(message)s")
    basicConfig(level=INFO, format="%(levelname)s %(message)s")
    logger = getLogger()
    logger.debug("Debug mode.")

    pairs  = [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F"), ("Z","N"),
            ("A","Z"), ("B","Z"), ("C","Z"), ("D","Z"), ("E","Z"), ("F","Z"),
            ("A","N"), ("B","N"), ("C","N"), ("D","N"), ("E","N"), ("F","N"),]
    Render(pairs)


if __name__ == "__main__":
    main()