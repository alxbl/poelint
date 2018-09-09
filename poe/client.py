"""client.py
The module that does the interactions with the Path of Exile API
"""
import requests
import re
import json
from bs4 import BeautifulSoup as bs
import getpass

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
POE_API = 'https://www.pathofexile.com/character-window/'
POE_LOGIN = 'https://www.pathofexile.com/login'
HASH_REGX = r'name="hash" value="([^"]+)"'

class Client(object):
    """The Path of Exile python client.

    TODO:
        - [ ] Proper error handling
        - [ ] Validate login state
    """
    def __init__(self, creds=None, **kw):
        """Initializes a client for the given account credentials."""
        self._logged = False
        self._s = requests.Session()
        self._s.headers.update({'User-Agent': USER_AGENT})
        if not creds: raise Error('Provide login credentials in the form of (user, pass)')
        self._login(creds)
        creds = 'XXXXXXXXXXXX' # Hope python doesn't keep the string in memory too long!

    @property
    def logged_in(self): return self._logged

    @property
    def account(self): return self._account

    def get_characters(self):
        """Retrieves the list of characters for the authenticated account."""
        p = {'accountName': self._account}
        r = self._s.post(POE_API + 'get-characters', p).json()
        return r

    def get_items(self, character):
        """Retrieves the inventory of the specified character."""
        p = {'accountName': self._account, 'character': character}
        r = self._s.post(POE_API + 'get-items', p).json()
        return r["items"]

    def get_stash(self, league, tab, tabs=False):
        """Retrieves the list of stash tabs for the given league."""
        p = {
                'accountName': self._account,
                'tabIndex': tab,
                'league': league,
                'tabs': '1' if tabs else '0'
        }
        r = self._s.get(POE_API + 'get-stash-items', params=p).json()
        return r

    def _login(self, creds):
        """Authenticate a session for an account."""
        # Retrieve CSRF token
        csrf = self._s.get(POE_LOGIN).text
        csrf = re.search(HASH_REGX, csrf).group(1)
        p  = {
               'login_email':    creds[0],
               'login_password': creds[1],
               'remember_me':    '0',
               'hash':           csrf,
               'login':          'Login'
             }
        resp = bs(self._s.post(POE_LOGIN, p).text, features="html.parser")
        account = resp.select_one('span.profile-link a')
        if not account:
            print('Login failed.')
            return False
        else:
            print (f'Account: {account.text}')
            self._logged = True
            self._account = account.text
            return True

