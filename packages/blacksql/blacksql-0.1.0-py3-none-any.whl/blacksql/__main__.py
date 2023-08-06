import sys
from . import core


with open(sys.argv[1], "r") as fl:
    final = core.format(fl.read())
    print(final)
