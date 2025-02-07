#!/usr/bin/env python3

from p5 import *
from graphform import GraphForm

pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (2, 3), (3, 1), (1, 4), (2, 4), (3, 4)]

gf = GraphForm(pairs)

draw = gf.draw
setup = gf.setup
run()
