import os

local = False
try:
    from local_config import *
    local = True
except:
    local = False

#hide
TMDB_API_KEY = LOCAL_TMDB_API_KEY if local else os.environ.get('TMDB_API_KEY')
TWITTER_API_KEY = LOCAL_TWITTER_API_KEY if local else os.environ.get('TWITTER_API_KEY')
TWITTER_KEY_SECRET = LOCAL_TWITTER_KEY_SECRET if local else os.environ.get('TWITTER_KEY_SECRET')
TWITTER_BEARER_TOKEN = LOCAL_TWITTER_BEARER_TOKEN if local else os.environ.get('TWITTER_BEARER_TOKEN')