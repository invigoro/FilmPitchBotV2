from tmdbv3api import Discover, Movie, Search
from classes import *
import random

#get x pages of movies from year within year tolerance
def getFilms(year, tolerance, pages): 
    films = []
    discover = Discover()
    for page in range(1, pages):
        movies = discover.discover_movies({
            'primary_release_date.gte': f'{year-tolerance}-01-01',
            'primary_release_date.lte': f'{year+tolerance}-12-31',
            'page': page
        })
        films.extend(convertFilms(movies))
    return sorted(films, key=lambda f: abs(f.year - year))

#converts tmbd movie object to film class
def convertFilms(movies):
    films = []
    for m in movies:
        print(str(m))
        try:
            film = Film(
                m.title if hasattr(m, 'title') else None,
                m.overview if hasattr(m, 'overview') else None, 
                m.release_date if hasattr(m, 'release_date') else None, 
                m.id)
            films.append(film)
        except:
            #may return an invalid type
            continue

    return films

#gets betweew min and max random cast members from movies in id list
def getCastMembers(ids, min, max):
    mov = Movie()
    cast = set()
    num = random.randint(min, max)
    tries = 0
    while(len(cast) < num and tries < 10):
        try: 
            id = ids[random.randint(0, len(ids))]
            credits = mov.credits(id)
            actor = credits.cast[0] or None
            if(not actor or actor.name in cast):
                continue
            cast.add(actor.name)
        except:
            tries += 1

    return cast

def getDirector(ids):
    mov = Movie()
    director = None
    for id in ids:
        try:
            crew = mov.credits(id)["crew"]
            director = next(c for c in crew if c["job"] == "Director" and c["department"] == "Directing").name
            break
        except:
            continue
    return director

def searchMovies(term, pages):
    search = Search()
    films = []
    for page in range(1, pages):
        movies = search.movies(term, None, None, None, None, page)
        films.extend(convertFilms(movies))
    return films