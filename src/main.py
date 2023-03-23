from tmdbv3api import TMDb
from packages.classes import *
from packages.math_helpers import *
from packages.tmbd_helpers import *
from packages.text_helpers import *
from config import *
from packages.twitter_helpers import Twitter
from packages.openai_helpers import *


tmdb = TMDb()
tmdb.api_key = TMDB_API_KEY
tmdb.language = 'en'
tmdb.debug = True
openAIInitialize(OPENAI_API_KEY)

MIN_YEAR = 1925
YEAR_TOLERANCE = 3
PAGE_MAX = 50
OVERVIEW_SENTENCE_GOAL_LENGTH = 85
OVERVIEW_MAX_LENGTH = 180
TITLE_GOAL_LENGTH = 30
CAST_COUNT_MAX = 3
CAST_COUNT_MIN = 1

year = getRandomYear(MIN_YEAR, inverseSquareFunction)

films = getFilms(year, YEAR_TOLERANCE, PAGE_MAX)
the_movie = generatedProduction()
the_movie.setYear(year)

# First, get the overview
text = list(map(lambda film: film.overview, films))
bigrams = createBigrams(text)
trigrams = createTrigrams(text)
seed = getRandomSentenceStart(text)
overview = generateSentence(bigrams, trigrams, seed, None, OVERVIEW_SENTENCE_GOAL_LENGTH)
while True:
    seed = getRandomSentenceStart(text)
    sen = generateSentence(bigrams, trigrams, seed, None, OVERVIEW_SENTENCE_GOAL_LENGTH)
    if(countSentenceCharacters(overview) + countSentenceCharacters(sen) > OVERVIEW_MAX_LENGTH):
        break
    overview.extend(sen)
the_movie.overview = " ".join(overview).strip()

### OpenAI reword
OVERVIEW_MIN_SENTENCES = 1
OVERVIEW_MAX_SENTENCES = 3
OVERVIEW_RANDOMNESS = 0.5
the_movie.overview = getAIOverview(the_movie.overview, OVERVIEW_MIN_SENTENCES, OVERVIEW_MAX_SENTENCES, OVERVIEW_MAX_LENGTH, OVERVIEW_RANDOMNESS).strip()

# Second, get the title
# Also search for other titles containing the same word
text = list(map(lambda film: film.title, films))
seed = getRandomSentenceStart(text)
bigrams = mergeGrams(createBigrams(text), bigrams)
trigrams = mergeGrams(createTrigrams(text), trigrams)
newTitles = searchMovies(seed, PAGE_MAX)
text = list(map(lambda film: film.title, newTitles))
bigrams = mergeGrams(createBigrams(text), bigrams)
trigrams = mergeGrams(createTrigrams(text), trigrams)

### OpenAI reword
TITLE_RANDOMNESS = 0.7
the_movie.title = fixGrammarAI(" ".join(generateSentence(bigrams, trigrams, seed, None, TITLE_GOAL_LENGTH)).strip(". ").title())
the_movie.title = rewriteTitleAI(the_movie.title, TITLE_RANDOMNESS).strip().strip('\"')


### OpenAI image
TAGLINE_MIN_WORDS = 2
TAGLINE_MAX_WORDS = 8
TAGLINE_MAX_LENGTH = 30
TAGLINE_RANDOMNESS = 0.5
the_movie.tagline = getAITagLine(the_movie.overview, TAGLINE_MIN_WORDS, TAGLINE_MAX_WORDS, TAGLINE_MAX_LENGTH, TAGLINE_RANDOMNESS).strip()
the_movie.imgUrl = getAIPoster(the_movie.title, the_movie.year, the_movie.tagline)

# Last, get a cast list & director
ids = list(map(lambda film: film.id, films))
the_movie.cast = getCastMembers(ids, CAST_COUNT_MIN, CAST_COUNT_MAX)
the_movie.director = getDirector(ids)

formatted = the_movie.getInfo280()

twitter = Twitter(TWITTER_API_KEY, TWITTER_KEY_SECRET, TWITTER_CLIENT_ID, TWITTER_CLIENT_SECRET, TWITTER_BEARER_TOKEN, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter.MakePost(formatted, the_movie.imgUrl)