import openai
import random
from craiyon import Craiyon
from datetime import datetime
generator = Craiyon() # Instantiates the api wrapper

TEXT_CREATE_MODEL = "text-davinci-003"
TEXT_EDIT_MODEL = "text-davinci-edit-001"

def openAIInitialize(key): 
    openai.api_key = key

def getAIOverview(original, minSentences = 1, maxSentences = 3, maxLength = 180, temperature = 0.2):
    prompt = (f'Write a {minSentences}-{maxSentences} sentence overview of a movie based on a description.'
    f'\nDescription: {original}'
    f'\nOverview:')
    if len(original) > maxLength:
        original = original[:maxLength] #insure we don't have way to big of an input by accident
    for i in range(0, 5):
        try:
            return openai.Completion.create(model=TEXT_CREATE_MODEL, prompt = prompt, temperature = temperature, max_tokens = maxLength)['choices'][0]['text']
        except Exception as e:
            print(e) 
            return original

def getAITagLine(description, minWords = 2, maxWords = 8, maxLength = 30, temperature = 0.2):
    prompt = random.choice(DEFAULT_PROMPTS_TAGLINE)(minWords, maxWords, description)
    for i in range(0, 5):
        try:
            return openai.Completion.create(model=TEXT_CREATE_MODEL, prompt = prompt, temperature = temperature, max_tokens = maxLength)['choices'][0]['text']
        except Exception as e:
            print(e) 
            return description

def getAIPoster(title, year, tagLine, useCraiyon = False):
    prompt = random.choice(DEFAULT_PROMPTS_IMAGE)(title, year, tagLine)
    ### API currently only allows '256x256', '512x512', '1024x1024'
    STD_WIDTH = 512 #int(400)
    STD_HEIGHT = 512 #int( STD_WIDTH * 1.5)
    for i in range(0, 3):
        image_url = None
        print(f"Generating image from prompt: {prompt}")
        start_request = datetime.now()
        try: 
            if(useCraiyon):
                image_url = generator.generate(prompt).images.pop()
            else:
                response = openai.Image.create(prompt=prompt, n=1, size=f'{STD_WIDTH}x{STD_HEIGHT}')
                image_url = response['data'][0]['url']
        except Exception as e:
            print(e)
            if "safety system" in str(e).lower(): #some get rejected for containing charged or offensive words
                print(prompt)
                raise Exception(e)   
        print(f'Image generation took {(datetime.now() - start_request).total_seconds()} seconds.')         
        return image_url
            
def getCastListAI(title, year, description, temperature = 1, minNames = 1, maxNames = 3, maxLength = 30):
    names = random.randint(minNames, maxNames)
    prompt = (f"List the names, separated by commas, of {names} possible actors who might be in a movie " 
              f"based on the movie's title, year, and description."
              f"\nTitle: {title}"
              f"\nYear: {year}"
              f"\nDescription: {description}"
              f"\nActors:")
    output = openai.Completion.create(model=TEXT_CREATE_MODEL, prompt = prompt, temperature = temperature, max_tokens=maxLength)['choices'][0]['text']
    return set(map(lambda s: s.strip(), output.split(", ")))
    
def getDirectorAI(title, year, description, cast, temperature = 1, maxLength = 20):
    prompt = (f"Write the name of a possible director of a movie based on the movie's title, year, description, and cast members."
              f"\nTitle: {title}"
              f"\nYear: {year}"
              f"\nDescription: {description}"
              f"\nCast members: {', '.join(cast)}"
              f"\nDirector:")
    output = openai.Completion.create(model=TEXT_CREATE_MODEL, prompt = prompt, temperature = temperature, max_tokens=maxLength)['choices'][0]['text']
    return output.strip()

def rewriteTitleAI(content, temperature = 0.3):
    instructions = (f"Rewrite this text to sound like the title of a motion picture."
    f"\nText: {content}"
    f"\nTitle:")
    try: 
        return openai.Completion.create(model=TEXT_CREATE_MODEL, prompt = instructions, temperature = temperature, max_tokens = len(content))['choices'][0]['text']
    except Exception as e:
        print(e)
        return content

def fixGrammarAI(content):
    instructions = "Fix punctuation, grammar, and capitalization"
    for i in range(0, 3):
        try:
            return openai.Edit.create(model = TEXT_EDIT_MODEL, input=content, instruction = instructions)['choices'][0]['text']
        except Exception as e:
            print(e)
            return content

DEFAULT_PROMPTS_IMAGE = [
    lambda title, year, tag: (f'Movie poster for {year} movie titled "{title}" whose plot can be summarized as "{tag}"'),
    lambda title, year, tag: (f'Promotional poster for {year} movie titled "{title}" whose plot can be summarized as "{tag}"'),
    lambda title, year, tag: (f'Promotional image for {year} movie titled "{title}" whose plot can be summarized as "{tag}"'),
    lambda title, year, tag: (f'Behind-the-scenes still from {year} movie titled "{title}" whose plot can be summarized as "{tag}"'),
    lambda title, year, tag: (f'Production still from {year} movie titled "{title}" whose plot can be summarized as "{tag}"'),
    lambda title, year, tag: (f'Movie frame from {year} movie titled "{title}" whose plot can be summarized as "{tag}"'),
    lambda title, year, tag: (f'"{title}" ({year})\n{tag}')
]

DEFAULT_PROMPTS_TAGLINE = [
    lambda minWords, maxWords, description: (f'Write a {minWords}-{maxWords} word overview of a movie based on a description.\nDescription: {description}\nOverview:'),
    lambda minWords, maxWords, description: (f'Explain what a movie is about in {minWords}-{maxWords}, given a description.\nDescription: {description}')
]