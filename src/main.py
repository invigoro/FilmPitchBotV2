from tmdbv3api import TMDb, Discover, Movie
from packages.classes import *
from packages.year_helpers import *
from packages.tmbd_helpers import *
from packages.text_helpers import *
from config import TMDB_API_KEY
tmdb = TMDb()
tmdb.api_key = TMDB_API_KEY
tmdb.language = 'en'
tmdb.debug = True

MIN_YEAR = 1925
YEAR_TOLERANCE = 3
PAGE_MAX = 10

year = getRandomYear(MIN_YEAR, inverseSquareFunction)
print(year)


films = getFilms(year, YEAR_TOLERANCE, PAGE_MAX)
overviews = list(map(lambda film: film.overview, films))

bigrams = createBigrams(overviews)
trigrams = createTrigrams(overviews)

