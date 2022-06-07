import sys
import tweepy

class Twitter:
    def __init__(self, api_key, api_secret, client_id, client_secret, bearer_token, access_token, access_secret):
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_secret)

        self.api = tweepy.API(auth)

    def MakePost(self, content):
        try:
            self.api.update_status(content)
            print(f'Tweet posted: \n{content}')
        except:
            sys.exit(f'Failed to post tweet. It was a good one though: \n{content}')

