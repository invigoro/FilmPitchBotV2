class Film:
    def __init__(self, title = None, overview = None, release_date = None, id = None):
        self.title = title
        self.overview = overview
        self.year = int(release_date[0:4])
        self.id = id

    cast = ""
    director = ""

    def printInfo(self):
        print(f'{self.title} ({self.year})\n{self.overview}')

class Show:
    def __init__(self, title = None, overview = None, release_date_start = None, release_date_end = None, id = None):
        self.title = title
        self.overview = overview
        self.year_start = int(release_date_start[0:4])
        self.year_end = int(release_date_end[0:4])
        self.id = id

    cast = ""
    director = ""

    def printInfo(self):
        print(f'{self.title} ({self.year_start}-{self.year_end})\n{self.overview}') 

class generatedProduction:
    overview = ""
    title = ""
    cast = []
    director = ""
    year = None

    def setYear(self, year, endYear = None):
        if(endYear):
            self.year = f'{year}-{endYear}'
        else: 
            self.year = f'{year}'

    def getInfo(self):
        info = f"{self.title} {f'({self.year})' if self.year else ''}" 
        info += f"\n{self.overview}"
        if self.director:
            info += f"\nDirected by: {self.director}"
        info += f"\nStarring: {', '.join(self.cast)}"
        return info