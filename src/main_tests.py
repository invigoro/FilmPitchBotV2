from packages.year_helpers import *
from packages.tmbd_helpers_test import *
from datetime import date

sq = inverseSquareFunction(110, 25)
assert sq >= 0 and sq <= 110
inverseSquareFunction(125, 90)
assert sq >= 0 and sq <= 125

year = getRandomYear(1955, inverseSquareFunction)
assert year >= 1955 and year <= date.today().year

