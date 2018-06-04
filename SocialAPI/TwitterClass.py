import base64
import requests
from urllib.parse import quote_plus
from .APIBase import APIBase

class Twitter(APIBase):
    conf_file = ''
    api_url = 'https://api.twitter.com/1.1/'
    tokenurl_request = 'https://api.twitter.com/oauth/request_token'
    tokenurl_authorize = 'https://api.twitter.com/oauth/authorize'
    tokenurl_access = 'https://api.twitter.com/oauth/access_token'
    tokenurl_oauth2 = 'https://api.twitter.com/oauth2/token'
    oauthv = 2

    def GetTokens(self, save=False, file=conf_file, quiet=True):
        self.GetOAuth1Tokens('pin', save, file, quiet)

    def GetAppAuth(self, save, quiet, file='twitter.conf.json'):
        key = quote_plus(self.oauth_key)
        secret = quote_plus(self.oauth_key_sec)
        bearer_token = base64.b64encode(f'{key}:{secret}'.encode('utf8'))

        post_headers = {
            'Authorization': f"Basic {bearer_token.decode('utf8')}",
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }

        res = requests.post(url='https://api.twitter.com/oauth2/token',
                            data={'grant_type': 'client_credentials'},
                            headers=post_headers)

        self.oauth2_token = res.json()

        if save:
            self.conf_save(file)
        if not quiet:
            self.tokens()

    # def favorites(self, **params):
    #     req_url = '/favorites/list.json'
    #     valid_params = ['user_id', 'screen_name', 'count', 'since_id', 'max_id', 'include_entities']
    #
    #     return self.APIRequest('GET', req_url, params, valid_params)