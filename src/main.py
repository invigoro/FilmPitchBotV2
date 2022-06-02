from tmdbv3api import TMDb
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
OVERVIEW_SENTENCE_GOAL_LENGTH = 55
OVERVIEW_MAX_LENGTH = 200
TITLE_GOAL_LENGTH = 30
CAST_COUNT_MAX = 5
CAST_COUNT_MIN = 2

year = getRandomYear(MIN_YEAR, inverseSquareFunction)

films = getFilms(year, YEAR_TOLERANCE, PAGE_MAX)
the_movie = generatedProduction()
the_movie.setYear(year)

# First, get the overview
text = list(map(lambda film: film.overview, films))
bigrams = createBigrams(text)
trigrams = createTrigrams(text)
overview = []
while True:
    seed = getRandomSentenceStart(text)
    sen = generateSentence(bigrams, trigrams, seed, None, OVERVIEW_SENTENCE_GOAL_LENGTH)
    if(countSentenceCharacters(overview) + countSentenceCharacters(sen) > OVERVIEW_MAX_LENGTH):
        break
    overview.extend(sen)
the_movie.overview = " ".join(overview)

# Second, get the title
text = list(map(lambda film: film.title, films))
bigrams = createBigrams(text)
trigrams = createTrigrams(text)
seed = getRandomSentenceStart(text)
the_movie.title = " ".join(generateSentence(bigrams, trigrams, seed, None, TITLE_GOAL_LENGTH))

# Last, get a cast list & director
ids = list(map(lambda film: film.id, films))
the_movie.cast = getCastMembers(ids, CAST_COUNT_MIN, CAST_COUNT_MAX)
the_movie.director = getDirector(ids)

print(the_movie.getInfo())