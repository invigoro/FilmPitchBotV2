from datetime import date
import random
import sys

# Get random weighted year
def getRandomYear(min, weightingFunc):
    today = date.today().year
    if(min > today or min < 1890):
        sys.exit("Invalid start year.")

    range = today - min
    year = random.uniform(0, range)
    return today - weightingFunc(range, year)

# Weights years closer to today using inverse square
def inverseSquareFunction(range, year): 
    return inverseXFunction(range, year, 2)

def inverse1_75Function(range, year):
    return inverseXFunction(range, year, 1.75)

def inverse1_5Function(range, year):
    return inverseXFunction(range, year, 1.5)

def inverseXFunction(range, year, exp):
    return round(((float(year) / float(range))**float(exp)) * float(range))



def testAll():
    testDistribution()
def testDistribution():
    min = 1890
    max = date.today().year + 1
    func = inverse1_75Function
    years = {}
    for i in range(0, 1000):
        y = getRandomYear(1890, func)
        years[y] = years.get(y, 0) + 1
    for i in range(min, max):
        print(f"{i}, {years.get(i, 0)}")

