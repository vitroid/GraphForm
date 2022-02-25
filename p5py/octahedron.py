pairs = [("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"), ("B", "C"), ("C", "D"),
        ("D", "E"), ("E", "B"), ("B", "F"), ("C", "F"), ("D", "F"), ("E", "F")]

from graphform import GraphForm
from p5 import *

gf = GraphForm(pairs)

draw = gf.draw
setup = gf.setup
run()