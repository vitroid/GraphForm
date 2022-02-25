from logging import getLogger, basicConfig, INFO, DEBUG
import sys
from p5 import *
import itertools as it
import sys
import numpy as np
import networkx as nx
from attrdict import AttrDict

def debug(func):
    def wrapper(*args, **kwargs):
        logger = getLogger()
        logger.debug(func.__name__)
        func(*args, **kwargs)
    return wrapper

def Depth(pi, pj, pk):
    return pi[2] + pj[2] + pk[2]


def ArrangedColor(a, b, c, decay):
    logger = getLogger()
    ab = b-a
    ac = c-a
    # normal vector
    n = np.cross(ab, ac)
    n /= np.linalg.norm(n)
    hue = abs(np.sum(n)) / sqrt(3.0)
    #hue = hue + 0.5
    if hue > 1.0:
        hue -= 1.0
    # final opacity is A+B
    A = 0.3
    B = 0.4
    opacity = (1. - 0.99**decay) * A + B
    return Color(hue, 0.8, abs(n[2]) * 0.4 + 0.6, alpha=opacity)







class Vertex():
    """
    A vertex is a point mass with a label.
    """
    def __init__(self, label, pos=None):
        self.label = str(label)
        if pos is None:
            self.position = np.random.random(3) * 500
        else:
            self.position = pos
        self.velocity = np.zeros(3)
        self.force = np.zeros(3)

    def perspective(self, zoom=0.0):
        if zoom == 0:
            zoom = 1000 / (1000 - self.position[2])
        return self.position[:2] * zoom

    def force2vel(self):
        self.velocity = self.force + 0

    def progress(self, deltatime):
        self.position += self.velocity * deltatime

    # def draw(self):
    #     ellipse(self.position[0] - 1, self.position[1] - 1, 2, 2)
    def resetf(self):
        self.force = np.zeros(3)


def drawfaces_(faces, vertices):
    logger = getLogger()
    stroke(0)
    stroke_weight(2)
    k = faces.keys()
    for face in sorted(k, key=lambda x: -faces[x].depth):
        # triangle = PShape()
        va, vb, vc = face
        a = vertices[va].perspective(1.0)
        b = vertices[vb].perspective(1.0)
        c = vertices[vc].perspective(1.0)
        fill(faces[face].color)
        triangle(a,b,c)



class GraphForm():
    @debug
    def __init__(self, pairs):
        self.repulse = 1
        self.hold = None
        self.keyhold = None
        self.face = True
        self.label = True
        self.decay = 0
        self.vertices = dict()
        self.triangles = dict()

        self.R0 = 200
        self.K = 2.5
        # self.KRmax = 180
        self.KR = 180

        self.frames = 0

        labels = set()
        for i,j in pairs:
            labels.add(i)
            labels.add(j)
        labels = list(labels)

        self.g = nx.Graph(pairs)
        for i in labels:
            #position, velocity, force
            self.vertices[i] = Vertex(i)

        for i, j in self.g.edges():
            for v in self.g[j]:
                if v in self.g[i]:
                    s = tuple(sorted([i, j, v]))
                    self.triangles[s] = AttrDict({"depth": None, "color": None})

    def drawfaces(self):
        for i, j, k in self.triangles.keys():
            self.triangles[(i, j, k)].depth = Depth( self.vertices[i].position, self.vertices[j].position, self.vertices[k].position)
            self.triangles[(i, j, k)].color = ArrangedColor(self.vertices[i].position,
                    self.vertices[j].position, self.vertices[k].position, self.decay)
        drawfaces_(self.triangles, self.vertices)


    def force(self):
        for a, b in self.g.edges():
            vertex0 = self.vertices[a]
            vertex1 = self.vertices[b]
            d = vertex0.position - vertex1.position
            r = np.linalg.norm(d)
            f = self.K * (r - self.R0) * d / r
            vertex0.force -= f
            vertex1.force += f


    def repulsiveforce(self, mul):
        for a, b in it.combinations(self.g, 2):
            if not self.g.has_edge(a,b):
                vertex0 = self.vertices[a]
                vertex1 = self.vertices[b]
                d = vertex0.position - vertex1.position
                r = np.linalg.norm(d)
                if r < self.R0 * mul:
                    f = self.KR * d / r
                    vertex0.force += f
                    vertex1.force -= f


    def drawedges(self):
        for a, b in self.g.edges():
            vertex0 = self.vertices[a].perspective(1.0)
            vertex1 = self.vertices[b].perspective(1.0)
            line(vertex0, vertex1)


    def drawlabels(self):
        for v in self.vertices.values():
            vv = v.perspective(1.0)
            fill(0)
            no_stroke()
            text(v.label, vv[0], vv[1])

    def draw(self):
        logger = getLogger()
        background(1, 0, 1) # hsb
        self.frames += 1
        if self.frames == 100:
            self.repulse = 0
        self.decay += 1
        self.force()
        for vertex in self.vertices.values():
            vertex.force2vel()
            vertex.progress(0.05)
            vertex.resetf()
        if self.repulse:
            fill(0)
            no_stroke()
            text("Repulsive", 40, 40)
            self.KR = 100 # self.KRmax - (self.KRmax - self.KR) * 0.9
            self.repulsiveforce(1.2)
        else:
            self.KR *= 0.9
        stroke(0)
        if self.face:
            self.drawfaces()
        else:
            self.drawedges()
        if self.label:
            self.drawlabels()
        # # マウスでノードをひっぱる。
        if mouse_is_pressed:
            decay = 0
            if self.hold is None:
                min = 100000.0
                nod = None
                for vertex in self.vertices.values():
                    pixel = vertex.perspective(1.0)
                    dx = mouse_x - pixel[0]
                    dy = mouse_y - pixel[1]
                    d = dx**2 + dy**2
                    if d < min:
                        min = d
                        self.hold = vertex
            pixel = self.hold.perspective(1.0)
            dx = mouse_x - pixel[0]
            dy = mouse_y - pixel[1]
            self.hold.position[0] += dx / 2
            self.hold.position[1] += dy / 2
        else:
            self.hold = None

        if key_is_pressed:
            if not self.keyhold:
                # if nodebox_wrapper.key == "s":
                #     canvas.save("graphform.pdf")
                #     print ("Saved")
                if key == "r":
                    if not self.repulse:
                        self.repulse = 1
                    else:
                        self.repulse -= 1
                if key == "f":
                    self.face = not self.face
                if key == "l":
                    self.label = not self.label
                if key == "q":
                    sys.exit(0)
            self.keyhold = True
        else:
            self.keyhold = None

    @debug
    def setup(self):
        size(512, 512)
        color_mode('HSB', 1, 1, 1, 1)



if __name__ == "__main__":
    # basicConfig(level=INFO, format="%(levelname)s %(message)s")
    basicConfig(level=DEBUG, format="%(levelname)s %(message)s")
    logger = getLogger()
    logger.debug("Debug mode.")

    pairs  = [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F"), ("Z","N"),
            ("A","Z"), ("B","Z"), ("C","Z"), ("D","Z"), ("E","Z"), ("F","Z"),
            ("A","N"), ("B","N"), ("C","N"), ("D","N"), ("E","N"), ("F","N"),]
    gf = GraphForm(pairs)

    draw = gf.draw
    setup = gf.setup
    run()