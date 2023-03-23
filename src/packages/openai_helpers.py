import openai

# Load your API key from an environment variable or secret management service

TEXT_CREATE_MODEL = "text-davinci-003"
TEXT_EDIT_MODEL = "text-davinci-edit-001"

def openAIInitialize(key): 
    openai.api_key = key

def getAIOverview(original, minSentences = 1, maxSentences = 3, maxLength = 180, temperature = 0.2):
    prompt = (f'Write a {minSentences}-{maxSentences} sentence overview of a movie based on a description.'
    f'\nDescription: {original}'
    f'\nOverview:')
    for i in range(0, 5):
        try:
            return openai.Completion.create(model=TEXT_CREATE_MODEL, prompt = prompt, temperature = temperature, max_tokens = maxLength)['choices'][0]['text']
        except Exception as e:
            print(e) 
            return original

def getAITagLine(description, minWords = 2, maxWords = 8, maxLength = 30, temperature = 0.2):
    prompt = (f'Write a {minWords}-{maxWords} word overview of a movie based on a description.'
    f'\nDescription: {description}'
    f'\nOverview:')
    for i in range(0, 5):
        try:
            return openai.Completion.create(model=TEXT_CREATE_MODEL, prompt = prompt, temperature = temperature, max_tokens = maxLength)['choices'][0]['text']
        except Exception as e:
            print(e) 
            return ""

def getAIPoster(title, year, tagLine):
    prompt = (f'Movie poster for {year} movie titled "{title}: {tagLine}"')
    ### API currently only allows '256x256', '512x512', '1024x1024'
    STD_WIDTH = 512 #int(400)
    STD_HEIGHT = 512 #int( STD_WIDTH * 1.5)
    for i in range(0, 3):
        try: 
            response = openai.Image.create(prompt=prompt, n=1, size=f'{STD_WIDTH}x{STD_HEIGHT}')
            image_url = response['data'][0]['url']
            return image_url
        except Exception as e:
            print(e)
            return None

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