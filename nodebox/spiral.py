from math import *
speed(30)

R0 = 200
K  = 2
KR = 10.0
KRAD=1.0
RI= 5.0
RO = 300.0



#spiral (6,1)
labels = []
pairs = []
inners = []
outers = []
m = 6
L = 14
for i in range(0,L-1):
    pairs.append((i,i+1))
for i in range(0,L-(m-1)):
    pairs.append((i,i+(m-1)))
for i in range(0,L-m):
    pairs.append((i,i+m))
for i in range(0,L-m):
    pairs.append((i,i*2+L))
    pairs.append((i+(m-1),i*2+L))
    pairs.append((i+m,i*2+L))
    pairs.append((i,i*2+L+1))
    pairs.append((i+1,i*2+L+1))
    pairs.append((i+m,i*2+L+1))
    print i*2+L+1
for i in range(0,L*3-2*m):
    labels.append(i)
for i in range(0,L):
    outers.append(i)
for i in range(L,3*L-2*m):
    inners.append(i)
    


def normalize(a):
    s = 0.0
    for i in range(3):
        s += a[i]**2
    s = 1.0/ sqrt(s)
    for i in range(3):
        a[i] *= s



def setdepth( triangle, pi,pj,pk ):
    triangle["Z"] = pi.position[2] + pj.position[2] + pk.position[2]


def setcolor( triangle, a,b,c ):
    ab = [0.0] * 3
    ac = [0.0] * 3
    for i in range(3):
        ab[i] = b.position[i] - a.position[i]
        ac[i] = c.position[i] - a.position[i]
    #normal vector
    n = [0.0] * 3
    n[0] = ab[1]*ac[2] - ab[2]*ac[1]
    n[1] = ab[2]*ac[0] - ab[0]*ac[2]
    n[2] = ab[0]*ac[1] - ab[1]*ac[0]
    normalize(n)
    hue = abs(n[0]+n[1]+n[2])/sqrt(3.0)
    #hue = hue + 0.5
    if hue > 1.0:
        hue -= 1.0
    triangle["C"] = color(hue,0.8,abs(n[2]),0.5)


def drawfaces_( faces, vertices ):
    stroke(0)
    k = faces.keys()
    for face in sorted(k, cmp=lambda x,y: cmp(faces[y]["Z"],faces[x]["Z"])):
        fill(faces[face]["C"])
        va,vb,vc = face
        a = vertices[va]
        b = vertices[vb]
        c = vertices[vc]
        beginpath( a.position[0], a.position[1] )
        lineto( b.position[0], b.position[1] )
        lineto( c.position[0], c.position[1] )
        lineto( a.position[0], a.position[1] )
        endpath();



def drawfaces( vertices, triangles ):
    for i,j,k in triangles.keys():
        setdepth( triangles[(i,j,k)], vertices[i], vertices[j], vertices[k] )
        setcolor( triangles[(i,j,k)], vertices[i], vertices[j], vertices[k] )
    drawfaces_( triangles, vertices )


def drawnodes( vertices ):
    for v in vertices.values():
        text(str(v.label),v.position[0],v.position[1])

def drawspiral( vertices ):
    stroke(0,1,1)
    strokewidth(3)
    nofill()
    beginpath(vertices[0].position[0], vertices[0].position[1])
    for v in vertices:
        lineto(v.position[0], v.position[1])
    moveto(vertices[0].position[0], vertices[0].position[1])
    endpath()


def sqdistance( p, q):
    s = 0.0
    for i in range(3):
        d = p[i] - q[i]
        s += d**2
    return s

#find the nearest suitable site.
def innerspiral( vertices, R0 ):
    i = 0
    j = 0
    print "Inner spiral pitch"
    while True:
        while True:
            j += 1
            if j >= len(vertices):
                break
            d = sqdistance( vertices[i].position, vertices[j].position )
            if d > R0**2:
                break
        if j >= len(vertices):
            break
        print vertices[i].label,"-",vertices[j].label," ",
        i += 1
        j -= 2
        if j <= i:
            j = i+1
    print
    return
    



def force(vertices, edges, fconst):
    for a,b in edges.keys():
        vertex0 = vertices[a]
        vertex1 = vertices[b]
        d = [0.0] * 3
        r = 0.0
        for i in range(3):
            d[i] = (vertex0.position[i] - vertex1.position[i])
            r += d[i]**2
        r = sqrt(r)
        for i in range(3):
            f = fconst * (r - R0) * d[i] / r
            vertex0.force[i] -= f
            vertex1.force[i] += f


def radialforce(vertices, radius, fconst):
    for v in vertices:
        d = [0.0]*3
        d[0] = v.position[0] - 400
        d[1] = 0.0
        d[2] = v.position[2]
        r = 0.0
        for i in range(3):
            r += d[i]**2
        r = sqrt(r)
        for i in range(3):
            f = fconst * (r - radius) * d[i] / r
            v.force[i] -= f






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
            #print "sub", sub
            for i in sub:
                result.append(i+[head])
    #print elems, n, "=>", result
    return result






def drawedges(edges):
    for a,b in edges.keys():
        vertex0 = vertices[a]
        vertex1 = vertices[b]
        line(vertex0.position[0], vertex0.position[1], 
             vertex1.position[0], vertex1.position[1])

def edgestat( edges ):
    s = 0.0
    ss = 0.0
    for a,b in edges.keys():
        d = sqdistance(vertices[a].position, vertices[b].position)
        s += sqrt(d)
        ss += d
    s /= len(edges)
    ss /= len(edges)
    print "Avg. edge length: ",s, sqrt(ss-s*s)
    

class Vertex():
    def __init__(self, label, pos=None):
        self.label    = label
        if pos == None:
            self.position = [random()*500,random()*500,random()*500]
        else:
            self.position = pos
        self.velocity = [0.0] * 3
        self.force    = [0.0] * 3
        self.neighbors = []
    def force2vel(self):
        self.velocity = list(self.force)
    def progress(self,deltatime):
        for i in range(3):
            self.position[i] += self.velocity[i] * deltatime
    def draw(self):
        oval(self.position[0]-1, self.position[1]-1,2,2)
    def resetf(self):
        self.force = [0.0] * 3

def edgeExists( edges, i,j ):
    return edges.has_key((i,j)) or edges.has_key((j,i))


vertices = dict()
edges    = dict()

theta = pi*2 / m
for i in range(L):
    vertices[labels[i]] = Vertex(labels[i], [RO*cos(theta*i)+400, i*R0/m, RO*sin(theta*i)])
for i in range(L,L*3-2*m):
    vertices[labels[i]] = Vertex(labels[i], [RI*cos(theta*i)+400, 
                                             (i-L+0.5)*R0/(2*m), RI*sin(theta*i)])
    
for i in pairs:
    edges[i] = True
    vertices[i[0]].neighbors.append(i[1])
    vertices[i[1]].neighbors.append(i[0])




triangles = dict()
for i,j in edges.keys():
    for v in vertices.keys():
        if edgeExists(edges,i,v) and edgeExists(edges,j,v):
            s = [i,j,v]
            s.sort()
            triangles[tuple(s)] = dict()  #z axis and color

inner = []
outer = []
for i in inners:
    inner.append(vertices[i])
for i in outers:
    outer.append(vertices[i])
    
hold = None
keyhold = None
face = False
def draw():
    global hold,keyhold,repulse,face,RO,RI
    colormode(HSB)
    force(vertices,edges,K)
    #angular force for stiffness
    radialforce(inner,RI,KRAD)
    radialforce(outer,RO,KRAD)

    for vertex in vertices.values():
        vertex.force2vel()
        vertex.progress(0.1)
        vertex.resetf()
    stroke(0)
    if face:
        drawfaces( vertices, triangles )
    else:
        drawedges(edges)
        drawnodes(vertices)
        edgestat(edges)
        innerspiral( inner, R0 )
        print "Inner/Outer radius: ",RI,RO
    drawspiral( inner )
    #slow relaxation of the radii
    s = sqdistance( vertices[m].position, vertices[m+1].position )
    if s > R0**2:
        RO *= 0.999
    else:
        RO *= 1.001
    s = sqdistance( vertices[m].position, vertices[L+m*2].position )
    if s > R0**2:
        RI *= 1.0003
    else:
        RI *= 0.9997
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
    else:
        hold = None
    
    if keydown:
        if not keyhold:
            if key == "s":
                canvas.save("graphform.pdf")
                print "Saved"
            if key == "f":
                face = not face
        keyhold = True
    else:
        keyhold = None
    