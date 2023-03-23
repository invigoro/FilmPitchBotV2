import sys
import tweepy
import requests
import os

class Twitter:
    def __init__(self, api_key, api_secret, client_id, client_secret, bearer_token, access_token, access_secret):
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_secret)

        self.api = tweepy.API(auth)

    def MakePost(self, content, url):
        try:
            if(url):
                filename = 'temp-poster.jpg'
                request = requests.get(url, stream=True)
                if request.status_code == 200:
                    with open(filename, 'wb') as image:
                        for chunk in request:
                            image.write(chunk)
                    self.api.update_status_with_media(status = content, filename = filename)
                    os.remove(filename)
                else:
                    print("Unable to download image")
                    self.api.update_status(content)
            else:
                self.api.update_status(content)
            print(f'Tweet posted: \n{content}')
        except Exception as e:
            print(e)
            sys.exit(f'Failed to post tweet. It was a good one though: \n{content}')