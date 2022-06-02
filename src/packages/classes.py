class Film:
    def __init__(self, title, overview, release_date, id):
        self.title = title
        self.overview = overview
        self.year = int(release_date[0:4])
        #self.cast = list(map(lambda c: c.name, cast))
        #self.director = director
        self.id = id

    def printInfo(self):
        print(f'{self.title} ({self.year})\n{self.overview}')    

class Show:
    def __init__(self, title, overview, release_date_start, release_date_end, id):
        self.title = title
        self.overview = overview
        self.year_start = int(release_date_start[0:4])
        self.year_end = int(release_date_end[0:4])
        #self.cast = list(map(lambda c: c.name, cast))
        #self.director = director
        self.id = id

    def printInfo(self):
        print(f'{self.title} ({self.year_start}-{self.year_end})\n{self.overview}') 