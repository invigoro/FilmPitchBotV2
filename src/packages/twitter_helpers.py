#from pytwitter import Api  
import sys
import tweepy

class Twitter:
    def __init__(self, api_key, api_secret, client_id, client_secret, bearer_token, access_token, access_secret):
        #self.api = Api(client_id=client_id, client_secret=client_secret, bearer_token=bearer_token, oauth_flow=True)
        #url, code_verifier, _ = self.api.get_oauth2_authorize_url()
        #self.url = url
        #self.code_verifier = code_verifier
        
        #self.access_token = self.api.generate_oauth2_access_token(response=url, code_verifier=self.code_verifier)

        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_secret)

        self.api = tweepy.API(auth)

    def MakePost(self, content):
        try:
            self.api.update_status(content)
            print(f'Tweet posted: \n{content}')
        except:
            sys.exit(f'Failed to post tweet. It was a good one though: \n{content}')

