pairs  = [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F"), ("Z","N"),
        ("A","Z"), ("B","Z"), ("C","Z"), ("D","Z"), ("E","Z"), ("F","Z"),
        ("A","N"), ("B","N"), ("C","N"), ("D","N"), ("E","N"), ("F","N"),]

from graphform import GraphForm
from p5 import *

gf = GraphForm(pairs)

draw = gf.draw
setup = gf.setup
run()