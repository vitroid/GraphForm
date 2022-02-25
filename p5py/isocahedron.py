from logging import getLogger, basicConfig, INFO, DEBUG
from p5 import *
from graphform import GraphForm
pairs = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
         (0, 8), (0, 9), (0, 10), (0, 11), (0, 12),
         (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
         (2, 3), (3, 4), (4, 5), (5, 6), (6, 2),
         (2, 7), (3, 8), (4, 9), (5, 10), (6, 11),
         (2, 8), (3, 9), (4, 10), (5, 11), (6, 7),
         (7, 8), (8, 9), (9, 10), (10, 11), (11, 7),
         (7, 12), (8, 12), (9, 12), (10, 12), (11, 12), ]


basicConfig(level=DEBUG, format="%(levelname)s %(message)s")
logger = getLogger()
logger.debug("Debug mode.")

gf = GraphForm(pairs)

draw = gf.draw
setup = gf.setup
run()
