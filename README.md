# Path of Exile Stash Linter

A no-frills tool to make stash tab management less painful.

There may eventually be a GUI on top of it.

Disclaimer: This is a hacky prototype that I threw together in an hour because
I wanted to scan my dump tabs for chance orb recipes. It is nowhere close to
being ready for use. The code needs to be cleaned up and made nice.

## Goals

- Minimize time spent reading item descriptions and theorycrafting when you should be farming
- Identify possible upgrades or strong bases
- Identify common recipes
- Let you ID and dump everything to stash
- Minimize downtime of catching up with stash

## Feature (Wish)list (as I need to make use of it.)

- [ ] Synchronize inventory in offline database (+ diff updates)
- [ ] Search for items matching specific stats
- [ ] Identify common recipes ingredients
- [ ] Flag loose currency items that strayed from their special tab.
- [ ] Print rundown of currency items
- [ ] Fossil & resonator stats


## Running


```
python3 -m venv py3
source py3/bin/activate
pip install -r requirements.txt
python3 sync.py
# type in your PoE account credentials.
# Password will not be shown at the prompt
```

