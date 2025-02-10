from logging import getLogger, basicConfig, INFO, DEBUG
import sys
import itertools as it
import sys
import numpy as np
import networkx as nx

class Interaction:
    def __init__(self, forcefunc):
        self.func = forcefunc

    def force(self, pairs, vertices):
        for a, b in pairs:
            vertex0 = vertices[a]
            vertex1 = vertices[b]
            d = vertex0.position - vertex1.position
            r = np.linalg.norm(d)
            f = self.func(r) * d / r
            vertex0.force -= f
            vertex1.force += f


def debug(func):
    def wrapper(*args, **kwargs):
        logger = getLogger()
        logger.debug(func.__name__)
        func(*args, **kwargs)

    return wrapper


class Vertex:
    """
    A vertex is a point mass with a label.
    """

    def __init__(self, label, pos=None):
        self.label = label
        if pos is None:
            self.position = np.random.random(3) * 500
        else:
            self.position = pos
        self.velocity = np.zeros(3)
        self.force = np.zeros(3)

    def force2vel(self):
        self.velocity = self.force + 0

    def progress(self, deltatime):
        self.position += self.velocity * deltatime

    def resetf(self):
        self.force = np.zeros(3)


def relax(g, node_pos=None, cell=None):
    # 隣接情報gを立体化する。
class GraphForm:
    @debug
    def __init__(self, pairs):
        self.repulse = 0
        self.hold = None
        self.keyhold = None
        self.decay = 0
        self.vertices = dict()
        self.triangles = dict()
        self.tetrahedra = set()
        self.tetrag = nx.Graph()  # adjacency graph of tetrahedra

        K = 2.5
        KR = 20
        R0 = 200
        #  立方体の一辺を1とすると面の対角線は√2、立方体の対角線は√3、隣接四面体間の距離は、√3/3
        # 面の対角線を1とするので、
        RT = R0 * (1 / 6) ** 0.5
        KT = 20

        self.attractive = Interaction(lambda r: K * (r - R0))

        def repel(r, K, rmin):
            """
            force function for replusive pairs
            """
            if r < rmin:
                return K * (r - rmin)
            return 0

        self.repulsive = Interaction(lambda r: repel(r, KR, R0 * 1.2))

        self.frames = 0

        labels = set()
        for i, j in pairs:
            labels.add(i)
            labels.add(j)
        labels = list(labels)

        self.g = nx.Graph(pairs)
        for i in labels:
            # position, velocity, force
            self.vertices[i] = Vertex(i)

        self.reps = [
            (i, j) for i, j in it.combinations(labels, 2) if not self.g.has_edge(i, j)
        ]

        for i, j in self.g.edges():
            for v in self.g[j]:
                if v in self.g[i]:
                    s = tuple(sorted([i, j, v]))
                    self.triangles[s] = Triangle(depth=None, color=None)

        for i, j, k in self.triangles:
            adj = tuple(set(self.g[i]) & set(self.g[j]) & set(self.g[k]))
            assert len(adj) <= 2
            pair = []
            for l in adj:
                s = tuple(sorted([i, j, k, l]))
                self.tetrahedra.add(s)
                pair.append(s)
            if len(pair) == 2:
                self.tetrag.add_edge(*pair)

        self.tetrepul = Interaction(lambda r: repel(r, KT, RT))

        # virtual vertices for tetrahedra
        self.vtet = dict()
        for t in self.tetrag:
            self.vtet[t] = Vertex(t)

    def draw(self):
        logger = getLogger()
        background(1, 0, 1)  # hsb
        self.frames += 1
        if self.frames == 100:
            self.repulse = 0
        self.decay += 1
        self.attractive.force(self.g.edges(), self.vertices)
        if self.repulse:
            fill(0)
            no_stroke()
            text("Repulsive", 40, 40)
            self.repulsive.force(self.reps, self.vertices)

        # 常に四面体同士は重ならないようにする。
        # if self.showtetrag:
        for vertex in self.vtet.values():
            vertex.resetf()
        for tetra, vertex in self.vtet.items():
            com = np.zeros(3)
            for v in tetra:
                com += self.vertices[v].position
            vertex.position = com / 4
        self.tetrepul.force(it.combinations(self.vtet, 2), self.vtet)
        # feedback the forces to its vertices
        for tetra, vertex in self.vtet.items():
            f = vertex.force
            for v in tetra:
                self.vertices[v].force += f

        for vertex in self.vertices.values():
            vertex.force2vel()
            vertex.progress(0.05)
            vertex.resetf()
        stroke(0)
        if self.showface:
            self.drawfaces()
        else:
            self.drawedges()
        if self.showlabel:
            self.drawlabels()
        if self.showtetrag:
            self.drawtetranetwork()
        # # マウスでノードをひっぱる。
        if mouse_is_pressed:
            decay = 0
            if self.hold is None:
                min = 100000.0
                nod = None
                for vertex in self.vertices.values():
                    pixel = vertex.perspective()
                    dx = mouse_x - pixel[0]
                    dy = mouse_y - pixel[1]
                    d = dx**2 + dy**2
                    if d < min:
                        min = d
                        self.hold = vertex
            pixel = self.hold.perspective()
            dx = mouse_x - pixel[0]
            dy = mouse_y - pixel[1]
            self.hold.position[0] += dx / 2
            self.hold.position[1] += dy / 2
        else:
            self.hold = None

        if key_is_pressed:
            if not self.keyhold:
                if key == "s":
                    save("graphform.png")
                    print("Saved")
                if key == "r":
                    if not self.repulse:
                        self.repulse = 1
                    else:
                        self.repulse -= 1
                if key == "f":
                    self.showface = not self.showface
                if key == "l":
                    self.showlabel = not self.showlabel
                if key == "t":
                    self.showtetrag = not self.showtetrag
                if key == "q":
                    sys.exit(0)
            self.keyhold = True
        else:
            self.keyhold = None

    @debug
    def setup(self):
        size(512, 512)
        color_mode("HSB", 1, 1, 1, 1)
        font = truetype("Arial.ttf", size=16)
        text_font(font)


if __name__ == "__main__":
    # basicConfig(level=INFO, format="%(levelname)s %(message)s")
    basicConfig(level=DEBUG, format="%(levelname)s %(message)s")
    logger = getLogger()
    logger.debug("Debug mode.")

    pairs = [
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
        ("D", "E"),
        ("E", "F"),
        ("Z", "N"),
        ("A", "Z"),
        ("B", "Z"),
        ("C", "Z"),
        ("D", "Z"),
        ("E", "Z"),
        ("F", "Z"),
        ("A", "N"),
        ("B", "N"),
        ("C", "N"),
        ("D", "N"),
        ("E", "N"),
        ("F", "N"),
    ]
    gf = GraphForm(pairs)

    draw = gf.draw
    setup = gf.setup
    run()
