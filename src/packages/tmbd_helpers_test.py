from tmbd_helpers import *

films = getFilms(1991, 3, 3)
cast = getCastMembers(map(lambda film: film.id, films), 2, 5)