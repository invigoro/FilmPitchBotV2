from datetime import date
import random
import sys

# Get random weighted year
def getRandomYear(min, weightingFunc):
    today = date.today().year
    if(min > today or min < 1890):
        sys.exit("Invalid start year.")

    range = today - min
    year = random.randint(0, range)
    return today - weightingFunc(range, year)

# Weights years closer to today using inverse square
def inverseSquareFunction(range, year): 
    return int(((year / range)**2) * range)