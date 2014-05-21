# Fitbit API as done for CottonSocket.com
# 2014-05-17 sgp structure: enter, get some Fitbit data, then exit
print 'begin fitbit_api imports and setup'
import requests
import json
import datetime

try:
    from urllib.parse import urlencode
except ImportError:
    # Python 2.x
    from urllib import urlencode

import fitbit

from _credentials import client_key, client_secret, consumer_key, consumer_secret, have_access_token, resource_owner_key_saved, resource_owner_secret_saved

import exceptions

# https://github.com/requests/requests-oauthlib/blob/master/docs/oauth1_workflow.rst
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1
from urlparse import parse_qs


def main():
    print 'begin fitbit api driver'

    # following the approach in https://github.com/requests/requests-oauthlib/blob/master/docs/oauth1_workflow.rst
    base_url = "https://api.fitbit.com"
    request_token_url = base_url + "/oauth/request_token"
    access_token_url = base_url + "/oauth/access_token"
    authorize_url = "http://www.fitbit.com/oauth/authorize"

    # print consumer_key + '    ' + consumer_secret
    # print request_token_url + '  ' + access_token_url + '  ' + authorize_url

    if have_access_token == 'y':
        resource_owner_key = resource_owner_key_saved
        resource_owner_secret = resource_owner_secret_saved
        print 'Using saved access_token 3: ' + resource_owner_key + '    ' + resource_owner_secret
    else: 
        print 'Obtaining access_token'
        # bail_out_here

        # Obtain a request token which will identify you (the client) in the next step
        oauth = OAuth1Session(client_key, client_secret=client_secret)
        fetch_response = oauth.fetch_request_token(request_token_url)
        # print 'oauth_token' + oauth_token + '    ' + oauth_token_secret

        resource_owner_key = fetch_response.get('oauth_token')
        resource_owner_secret = fetch_response.get('oauth_token_secret')
        print 'resource_owner 1: ' + resource_owner_key + '    ' + resource_owner_secret

        # Using OAuth1 auth helper
        oauth = OAuth1(client_key, client_secret=client_secret)
        r = requests.post(url=request_token_url, auth=oauth)
        r.content
        print 'r.content 2: ' + r.content
        credentials = parse_qs(r.content)
        resource_owner_key = credentials.get('oauth_token')[0]
        resource_owner_secret = credentials.get('oauth_token_secret')[0]
        print 'resource_owner 2: ' + resource_owner_key + '    ' + resource_owner_secret

        # Obtain authorization from the user (resource owner) to access their protected resources
        base_authorization_url = 'http://www.fitbit.com/oauth/authorize'
        # Using OAuth1Session (approach crashed)
        #     error: authorization_url = oauth.authorization_url(base_authorization_url)
        #         AttributeError: 'OAuth1' object has no attribute 'authorization_url'
        # Using OAuth1 auth helper
        authorize_url = base_authorization_url + '?oauth_token='
        authorize_url = authorize_url + resource_owner_key
        print 'Please go here and authorize,', authorize_url
        verifier = raw_input('Please input the verifier: ')
        print 'verifier: ', verifier

        # Obtain an access token from the OAuth provider. Save this token as it can be re-used later.
        # access_token_url = 'https://api.twitter.com/oauth/access_token'
        # Using OAuth1Session
        oauth = OAuth1Session(client_key,
            client_secret=client_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier)
        oauth_tokens = oauth.fetch_access_token(access_token_url)
        resource_owner_key = oauth_tokens.get('oauth_token')
        resource_owner_secret = oauth_tokens.get('oauth_token_secret')
        print 'resource_owner 3: ' + resource_owner_key + '    ' + resource_owner_secret

        """ the following section has errors, and is not needed
        # Using OAuth1 auth helper
        oauth = OAuth1(client_key, ...
        """

    # Access protected resources. OAuth1 access tokens typically do not expire and may be re-used until revoked
    # protected_url = 'https://api.twitter.com/1/account/settings.json'
    protected_url = 'http://api.fitbit.com/1/user/-/activities.json'
    # Using OAuth1Session
    oauth = OAuth1Session(client_key,
        client_secret=client_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret)
    r = oauth.get(protected_url)
    # Using OAuth1 auth helper
    oauth = OAuth1(client_key,
        client_secret=client_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret)
    r = requests.get(url=protected_url, auth=oauth)
    print 'r: '
    print r
    print r.json()


    print 'end fitbit api driver'

if __name__ == '__main__':
    main()
