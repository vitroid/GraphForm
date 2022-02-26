#!/usr/bin/env python3

# pentagonal bipyramid
from p5 import *
from graphform import GraphForm
pairs = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "A"), ("Z", "N"),
         ("A", "Z"), ("B", "Z"), ("C", "Z"), ("D", "Z"), ("E", "Z"),
         ("A", "N"), ("B", "N"), ("C", "N"), ("D", "N"), ("E", "N"), ]


gf = GraphForm(pairs)

draw = gf.draw
setup = gf.setup
run()
