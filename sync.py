import json
import re
import getpass

from poe import Client

# frameType
RARE = 2
BASE = 3

def sync_account(client, outfile=None):
    """
    Sample method that retrieves all items from all stash tabs and all leagues for which a character exists.
    This is linear and single threaded to showcase the client usage.
    """
    dump = {'stashes': {}}

    print('[+] Retrieving characters')
    chars = client.get_characters()

    leagues = {}
    # Retrieve  all characters.
    for ch in chars:
        print(f"[+]   - {ch['name']},  Level {ch['level']} {ch['class']} ({ch['league']})")
        if ch['league'] in leagues: leagues[ch['league']] += 1
        else: leagues[ch['league']] = 1
    dump["characters"] = chars
    # TODO: Character inventory.

    print(f'[+] Retrieving stash data')
    stash = {}
    for l in leagues:
        print(f'[+]   {l}... ', end='', flush=True)
        s = client.get_stash(l, tab=0, tabs=True)
        ntabs = s['numTabs']
        tabs = s['tabs']
        stash = []

        # Populate tab info
        for i in range(0, ntabs):
            tab = tabs[i]
            if i == 0:
                items = s['items']
            else:
                items = client.get_stash(l, tab=i)['items']

            tab["items"] =  items
            stash.append(tab)
        print(f'found {ntabs} tab(s)')
        dump['stashes'][l] = stash

    if outfile:
        with open(outfile, 'w') as out:
            out.write(json.dumps(dump, ensure_ascii=False, indent=4))
    return dump

def traverse_db(fn, db):
    """
    Iterates through all items in the database, calling the specified function.

    This can be very slow on really large accoounts.
    TODO: Support for character inventories.
    """
    # TODO: Character inventory traversal
    for stash in db['stashes']:
        tabs = db['stashes'][stash]
        for tab in tabs:
            items = tab['items']
            for item in items:
                fn(item, stash, tab)


def normalize(string):
    """Normalizes an API string to remove render-specific markup."""
    return re.sub(r'<<[^>]+>>', '', string)

RARES = {}
TOTAL = 0
def chance_orb_recipe_visitor(item, stash, tab):
    global RARES
    global TOTAL
    if item['frameType'] != RARE: return
    if not item['identified']: return
    TOTAL += 1
    name = normalize(item['name'])
    if stash not in RARES: RARES[stash] = {}

    if name in RARES[stash]:
        RARES[stash][name].append((item, tab))
    else:
        RARES[stash][name] = [(item, tab)]



def get_credentials():
    """
    Prompts for credentials at the command line.
    """
    u = input('Account: ')
    p = getpass.getpass()
    creds = (u, p)
    return creds

if __name__ == '__main__':
    print("Logging in...")
    c = Client(get_credentials())
    db = sync_account(c)
    traverse_db(chance_orb_recipe_visitor, db)
    found = 0
    for league in RARES:
        print(f"LEAGUE: {league}")
        stash = RARES[league]
        for rare in stash:
            count = len(stash[rare])
            if count >= 2:
                print(f'CHANCE ORB: {rare} ({count})')
                for i in stash[rare]:
                    print(f"  - {i[0]['typeLine']} @ ({i[0]['x']},{i[0]['y']} @ {i[1]['n']})")
    print(f"Scanned {TOTAL} rares")
