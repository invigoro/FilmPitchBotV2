from tmdbv3api import Discover, Movie
from classes import *
import random

#get x pages of movies from year within year tolerance
def getFilms(year, tolerance, pages): 
    films = []
    discover = Discover()
    for page in range(1, pages):
        movies = discover.discover_movies({
            'primary_release_date.lte': f'{year+tolerance}-01-01',
            'primary_release_date.gte': f'{year-tolerance}-12-31',
            'page': page
        })
        films.extend(convertFilms(movies))
    return films

#converts tmbd movie object to film class
def convertFilms(movies):
    films = []
    for m in movies:
        film = Film(m.title, m.overview, m.release_date, m.id)
        films.append(film)

    return films

#gets betweew min and max random cast members from movies in id list
def getCastMembers(ids, min, max):
    mov = Movie()
    cast = set()
    num = random.randint(min, max)
    while(len(cast) < num):
        id = ids[random.randint(0, len(ids))]
        credits = mov.credits(id)
        actor = credits.cast[0] or None
        if(not actor or cast[actor]):
            continue
        cast.add(actor)

    return cast

def getDirector(ids):
    id = random.randint(0, len(ids) - 1)
    mov = Movie()
