from math import *
speed(30)

R0 = 200
K  = 2
KR = 100

#pentagonal bipyramid with a gap
labels = ["A", "B", "C", "D", "E", "F", "Z", "N"]
pairs  = [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F"), ("Z","N"),
          ("A","Z"), ("B","Z"), ("C","Z"), ("D","Z"), ("E","Z"), ("F","Z"),
          ("A","N"), ("B","N"), ("C","N"), ("D","N"), ("E","N"), ("F","N"),]

#pentagonal bipyramid
#labels = ["A", "B", "C", "D", "E", "Z", "N"]
#pairs  = [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","A"), ("Z","N"),
#          ("A","Z"), ("B","Z"), ("C","Z"), ("D","Z"), ("E","Z"),
#          ("A","N"), ("B","N"), ("C","N"), ("D","N"), ("E","N"),]

#hexagonal bipyramid
#labels = ["A", "B", "C", "D", "E", "F", "Z", "N"]
#pairs  = [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F"), ("F","A"), ("Z","N"),
#          ("A","Z"), ("B","Z"), ("C","Z"), ("D","Z"), ("E","Z"), ("F","Z"),
#          ("A","N"), ("B","N"), ("C","N"), ("D","N"), ("E","N"), ("F","N")]

#hexagonal ring
#calculate the optimal distance for twisted ring.
import numpy as np
th = pi*5/6 #150 degree
R = np.matrix([[1.0, 0.0, 0.0],
               [0.0, cos(th), -sin(th)],
               [0.0, sin(th), cos(th)]])
O = np.zeros(3)
A = np.array([1.0, 0.0, 0.0])
B = np.array([-1.0/3.0, -sqrt(8.0/9.0),0])
print np.linalg.norm(B)
C = np.dot(R,(-B))
print C
print np.linalg.norm(C)
C += A
print np.linalg.norm(B-O)
print np.linalg.norm(O-A)
print np.linalg.norm(A-C)
print np.linalg.norm(B-C)
L = np.linalg.norm(B-C)
S = np.linalg.norm(B-A)

labels = ["A", "B", "C", "D", "E", "F"]
pairs  = [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F"), ("F","A"),
          ("A", "D", L), ("B", "E", L), ("C", "F", L),
          ("A","C",S), ("B","D",S), ("C","E",S), ("D","F",S), ("E","A",S), ("F","B",S),]




def force(vertices, edges):
    for ab in edges.keys():
        a,b = ab
        vertex0 = vertices[a]
        vertex1 = vertices[b]
        L       = edges[ab]
        d = vertex0.position - vertex1.position
        r = np.linalg.norm(d)
        f = K * (r - R0*L) * d / r
        vertex0.force -= f
        vertex1.force += f

def repulsiveforce(vertices, edges):
    for a,b in edges.keys():
        vertex0 = vertices[a]
        vertex1 = vertices[b]
        d = vertex0.position - vertex1.position
        r = np.linalg.norm(d)
        f = KR * d / r
        vertex0.force += f
        vertex1.force -= f



#combinatorial function is available in python2.6
def combinations(elems, n):
    result = []
    if n == 1:
        for i in elems:
            result.append([i])
    else:
        tmp = list(elems)
        while len(tmp) > 0:
            head = tmp.pop(0)
            print head,tmp
            sub = combinations(tmp,n-1)
            print "sub", sub
            for i in sub:
                result.append(i+[head])
    print elems, n, "=>", result
    return result




def drawedges(edges):
    for a,b in edges.keys():
        vertex0 = vertices[a]
        vertex1 = vertices[b]
        line(vertex0.position[0], vertex0.position[1], 
             vertex1.position[0], vertex1.position[1])


class Vertex():
    def __init__(self, label, pos=None):
        self.label    = label
        if pos == None:
            self.position = np.array([random()*500,random()*500,random()*500])
        else:
            self.position = np.array(pos)
        self.velocity = np.zeros(3)
        self.force    = np.zeros(3)
    def force2vel(self):
        self.velocity = self.force
    def progress(self,deltatime):
        self.position += self.velocity * deltatime
    def draw(self):
        oval(self.position[0]-1, self.position[1]-1,2,2)
    def resetf(self):
        self.force = np.zeros(3)

def edgeExists( edges, i,j ):
    return edges.has_key((i,j)) or edges.has_key((j,i))


vertices = dict()
edges    = dict()

for i in labels:
    #position, velocity, force
    vertices[i] = Vertex(i)
for x in pairs:
    if len(x) == 2:
        i,j = x
        L = 1.0
    else:
        i,j,L = x
    edges[frozenset((i,j))] = L


repulsive = dict()
for i,j in combinations(labels,2):
    if not edgeExists(edges,i,j):
       repulsive[(i,j)] = True



    
repulse = False
hold = None
keyhold = None
idle = 0
def draw():
    global hold,keyhold,repulse,face,idle
    colormode(HSB)
    force(vertices,edges)
    for vertex in vertices.values():
        vertex.force2vel()
        vertex.progress(0.1)
        vertex.resetf()
    if repulse:
        repulsiveforce(vertices,repulsive)
        text("Repulsive",40,40)
    stroke(0)
    drawedges(edges)
    #マウスでノードをひっぱる。
    if mousedown:
        if hold == None:
            min = 100000.0
            nod = None
            for vertex in vertices.values():
                dx = MOUSEX - vertex.position[0]
                dy = MOUSEY - vertex.position[1]
                d  = dx**2+dy**2
                if d < min:
                    min = d
                    hold = vertex
        dx = MOUSEX - hold.position[0]
        dy = MOUSEY - hold.position[1]
        hold.position[0] += dx/2
        hold.position[1] += dy/2
        idle = 0
    else:
        hold = None
        idle += 1
        if idle > 100:
            th = 0.01
            R = np.array([[cos(th), 0.0, -sin(th)],
                          [0.0, 1.0, 0.0],
                          [sin(th),0.0, cos(th)]])
            com = np.zeros(3)
            for vertex in vertices.values():
                com += vertex.position
            com /= len(vertices)
            for vertex in vertices.values():
                vertex.position = np.dot(R, vertex.position - com) + com
                vertex.velocity = np.dot(R, vertex.velocity)
                vertex.force    = np.dot(R, vertex.force)
    
    if keydown:
        if not keyhold:
            if key == "s":
                canvas.save("graphform.pdf")
                print "Saved"
            if key == "r":
                repulse = not repulse
            if key == "f":
                face = not face
            if key == "c":
                com = np.zeros(3)
                for vertex in vertices.values():
                    com += vertex.position
                com /= len(vertices)
                print "Edge lengths"
                for edge in edges:
                    a,b = edge
                    if edges[edge] == 1.0:
                        pa = vertices[a].position
                        pb = vertices[b].position
                        print np.linalg.norm(pa-pb)/R0
                print "Radii"
                for vertex in vertices:
                    print np.linalg.norm(vertices[vertex].position -com)/R0
                print "Positions"
                for vertex in labels:
                    print (vertices[vertex].position -com)/R0
        keyhold = True
    else:
        keyhold = None
    