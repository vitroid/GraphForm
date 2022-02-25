# pentagonal bipyramid
pairs = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "A"), ("Z", "N"),
            ("A", "Z"), ("B", "Z"), ("C", "Z"), ("D", "Z"), ("E", "Z"),
            ("A", "N"), ("B", "N"), ("C", "N"), ("D", "N"), ("E", "N"), ]

from graphform import GraphForm
from p5 import *

gf = GraphForm(pairs)

draw = gf.draw
setup = gf.setup
run()