from packages.year_helpers import *
from datetime import date
from packages.text_helpers import *
from tmdbv3api import TMDb
from config import TMDB_API_KEY, TWITTER_API_KEY, TWITTER_KEY_SECRET, TWITTER_CLIENT_ID, TWITTER_CLIENT_SECRET, TWITTER_BEARER_TOKEN, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
from packages.twitter_helpers import Twitter

tmdb = TMDb()
tmdb.api_key = TMDB_API_KEY
tmdb.language = 'en'
tmdb.debug = True

sq = inverseSquareFunction(110, 25)
assert sq >= 0 and sq <= 110
inverseSquareFunction(125, 90)
assert sq >= 0 and sq <= 125

year = getRandomYear(1955, inverseSquareFunction)
assert year >= 1955 and year <= date.today().year

twitter = Twitter(TWITTER_API_KEY, TWITTER_KEY_SECRET, TWITTER_CLIENT_ID, TWITTER_CLIENT_SECRET, TWITTER_BEARER_TOKEN, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter.MakePost("Testing")