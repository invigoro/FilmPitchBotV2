class Film:
    def __init__(self, title = None, overview = None, release_date = None, id = None):
        self.title = title
        self.overview = overview
        self.id = id
        try:
            self.year = int(release_date[0:4])
        except:
            self.year = None

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
    imgUrl = None
    tagline = ""

    def setYear(self, year, endYear = None):
        if(endYear):
            self.year = f'{year}-{endYear}'
        else: 
            self.year = f'{year}'

    def getInfo(self):
        info = f"{self.title} {f'({self.year})' if self.year else ''}" 
        info += f"\n{self.overview}"
        if self.director:
            info += f"\nDirector: {self.director}"
        info += f"\nStarring: {', '.join(self.cast)}"
        return info

    def getInfo280(self):
        topline = f"{self.title} {f'({self.year})' if self.year else ''}" 
        overview = f"\n{self.overview}"
        bottomline = ""
        if self.director:
            bottomline += f"\nDirector: {self.director}"
        bottomline += f"\nStarring: {', '.join(self.cast)}"
        totallength = len(topline) + len(overview) + len(bottomline)
        if totallength > 280:
            overview = "\n" + overview[0:-((totallength - 280) + 4)].strip() + "..." # 4 = 1 newline + 3 periods
        return topline + overview + bottomline

# Unit test for getinfo280
""" film = generatedProduction()
film.title = "And he and he ahsdlf;kjasd;lkfjas;lkdjfasl;kdfjasl;fadfsdkflkfkfj"
film.setYear(2019)
film.overview = "Oh that this too, too sullied flesh would melt, thaw, and resolve itself into a dew, or that the everlasting had not fix'd his canon 'gainst self-slaughter! Oh god! O god!"
film.director = "Akira Kirusawa"
film.cast = ["Johnny Depp", "Amber Heard", "Al Pacino"]
assert len(film.getInfo280()) < 280 """