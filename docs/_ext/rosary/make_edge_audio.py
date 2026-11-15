"""Record the Rosary with Microsoft Edge's neural voices (edge-tts).

For each voice in VOICES it makes, under docs/_static/audio/<voice>/:

    prayers/     the 11 prayers         Our Father.mp3, Hail Mary.mp3, ...
    mysteries/   the 20 announcements   First Joyful Mystery.mp3 ...
                 ("First Joyful Mystery. The Annunciation. The fruit of the
                 mystery: Humility.")
    steps/       the 200 steps, one     joyful-1-01.mp3 ... glorious-5-10.mp3
                 for each Hail Mary     (joyful-1-03 = Joyful set, first
                                        mystery, third Hail Mary)

and a recorded.json listing the words each file says.  If you change the
wording in rosary_data.py, the next run records just the files whose words
changed.  Files already recorded are left alone.

Each voice folder is listed in rosary_recordings in conf.py, so it shows up
in the Voice menu.  The recordings are made once on your own PC (edge-tts
needs the internet) and committed with the site; Read the Docs does not need
edge-tts.

Setup (once):
    pip install edge-tts

Set RECORD and ONLY below and run it, or from the docs folder:
    python _ext/rosary/make_edge_audio.py                    # what RECORD says
    python _ext/rosary/make_edge_audio.py --record steps     # the 200 steps
    python _ext/rosary/make_edge_audio.py --record all
    python _ext/rosary/make_edge_audio.py --only hail-mary joyful-1-03
    python _ext/rosary/make_edge_audio.py --force            # record again anyway
    python _ext/rosary/make_edge_audio.py --list             # English voices
    python _ext/rosary/make_edge_audio.py --voice en-GB-SoniaNeural:sonia
    python _ext/rosary/make_edge_audio.py --rate -15%        # slower (default -10%)
"""

import argparse
import asyncio
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

try:
    import edge_tts
except ImportError:
    sys.exit('edge-tts is not installed.  Run:  pip install edge-tts')

HERE = Path(__file__).resolve().parent              # docs/_ext/rosary
STATIC = HERE.parent.parent / '_static'             # docs/_static
AUDIO = STATIC / 'audio'                            # docs/_static/audio
# where recordings used to be kept: moved into audio/ when the script runs
OLD_FOLDERS = [STATIC / 'prayers']

# ---------------------------------------------------------------- settings

# What to record (files already made are skipped):
#   'prayers'    the 11 prayers (Our Father, Hail Mary, ...)
#   'mysteries'  the 20 mystery announcements (First Joyful Mystery. ...)
#   'steps'      the 200 steps, one for each Hail Mary
#   'all'        all of them
# or a list, e.g. ['prayers', 'mysteries']
RECORD = 'steps'

# Record just these, again (replacing the files that are there), e.g.
#   ONLY = ['hail-mary', 'hail-holy-queen', 'rosary-prayer']
#   ONLY = ["The Apostles' Creed", 'joyful-1', 'joyful-1-03']
# A prayer's key or title (any capitals), a mystery (joyful-1 or First
# Joyful Mystery) or a step (joyful-1-03).  Empty, ONLY = [], uses RECORD.
ONLY = []

# voice name -> folder under docs/_static/audio.  Microsoft renames voices
# now and then: run with --list to see the current names.
VOICES = {
    'en-AU-NatashaNeural': 'natasha',
    'en-AU-WilliamMultilingualNeural': 'william',
    'en-CA-LiamNeural': 'liam',
    'en-US-AndrewNeural': 'andrew',
    'en-US-SteffanNeural': 'steffan',
    'en-US-EricNeural': 'eric',
    'en-US-EmmaMultilingualNeural': 'emma',
    'en-US-AvaNeural': 'ava',
}

# Words read differently from how they are written, so the voice says them
# well.  The text on the page is not changed, only what is spoken.
# Whole words or phrases, any capitals ("Blessed" -> "Blessid").
SAY_AS = {
    'Pontius Pilate': 'Ponshus Pilate',
    'blessed': 'blessid',       # two syllables, BLESS-id, not "blest"
}

# prayer file names that differ from the prayer's title
FILE_NAMES = {
    'fatima': 'Fatima Prayer',
}

KINDS = ('prayers', 'mysteries', 'steps')

# ----------------------------------------------------------------- the words


def load_data():
    """rosary_data.py, without importing the whole extension."""
    spec = importlib.util.spec_from_file_location('rosary_data', HERE / 'rosary_data.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def safe_name(name):
    """A title as a safe Windows file name ('Hail, Holy Queen' stays)."""
    return re.sub(r'[\\/:*?"<>|]', '', name).strip() + '.mp3'


def load_items():
    """Everything that can be recorded: {key: (kind, file name, title, words)}."""
    data = load_data()
    items = {}
    for key, (title, words) in data.PRAYERS.items():
        items[key] = ('prayers', safe_name(FILE_NAMES.get(key, title)), title, words)
    for skey in data.SET_ORDER:
        for i, m in enumerate(data.SETS[skey]['mysteries']):
            ordinal = '%s %s Mystery' % (data.ORDINALS[i], data.SETS[skey]['name'])
            mkey = '%s-%d' % (skey, i + 1)
            items[mkey] = ('mysteries', safe_name(ordinal), ordinal,
                           '%s. %s. The fruit of the mystery: %s.' % (ordinal, m['title'], m['fruit']))
            for j, (ref, caption) in enumerate(m['refs']):
                step = '%s-%02d' % (mkey, j + 1)
                items[step] = ('steps', step + '.mp3', '%s, step %d' % (ordinal, j + 1), caption)
    return items


def _squash(name):
    """'The Apostles' Creed' -> 'theapostlescreed', for matching titles."""
    return ''.join(ch for ch in name.lower() if ch.isalnum())


def spoken(text):
    for written, said in SAY_AS.items():
        def swap(m, said=said):
            w = m.group(0)
            return said[:1].upper() + said[1:] if w[:1].isupper() else said
        text = re.sub(r'\b' + re.escape(written) + r'\b', swap, text, flags=re.IGNORECASE)
    return text


def find_only(only, items):
    lookup = {}
    for k, (kind, fname, title, _w) in items.items():
        lookup[k.lower()] = k
        lookup[_squash(title)] = k
        lookup[_squash(fname[:-4])] = k
    keys, unknown = [], []
    for item in only:
        k = lookup.get(str(item).lower()) or lookup.get(_squash(str(item)))
        (keys if k else unknown).append(k or item)
    if unknown:
        sys.exit('Not found: ' + ', '.join(map(str, unknown)) +
                 '\nUse a prayer key (' + ', '.join(k for k, v in items.items() if v[0] == 'prayers') +
                 '), a mystery (joyful-1) or a step (joyful-1-03).')
    return keys


# ------------------------------------------------------------ files on disk


def move_old_files(folder, items):
    """Recordings from the old layout (_static/prayers/<voice>/Hail Mary.mp3)
    move into audio/<voice>/prayers or mysteries."""
    by_name = {fname.lower(): kind for kind, fname, _t, _w in items.values()}
    by_name['o my jesus.mp3'] = 'prayers'
    for old_root in OLD_FOLDERS:
        old = old_root / folder
        if not old.is_dir():
            continue
        for f in sorted(old.iterdir()):
            kind = by_name.get(f.name.lower())
            if not f.is_file() or not kind:
                continue
            dest = AUDIO / folder / kind / f.name
            if f.name.lower() == 'o my jesus.mp3':
                dest = AUDIO / folder / kind / safe_name(FILE_NAMES['fatima'])
            if dest.exists():
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), str(dest))
            print(f'  moved   {old_root.name}/{folder}/{f.name} -> audio/{folder}/{kind}/')
        if not any(old.iterdir()):
            old.rmdir()
        if old_root.is_dir() and not any(old_root.iterdir()):
            old_root.rmdir()


def load_manifest(folder):
    path = AUDIO / folder / 'recorded.json'
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def save_manifest(folder, manifest):
    path = AUDIO / folder / 'recorded.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(sorted(manifest.items())), indent=1, ensure_ascii=False),
                    encoding='utf-8')


async def english_voices():
    voices = await edge_tts.list_voices()
    return sorted((v for v in voices if v['Locale'].startswith('en-')),
                  key=lambda v: (v['Locale'], v['ShortName']))


async def record(text, voice, rate, out_path):
    tmp = out_path.with_suffix('.part')
    await edge_tts.Communicate(text, voice, rate=rate).save(str(tmp))
    tmp.replace(out_path)


# ------------------------------------------------------------------- main


async def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--record', nargs='+', choices=KINDS + ('all',),
                    help='what to record (default: RECORD at the top of the script)')
    ap.add_argument('--only', nargs='+', metavar='KEY',
                    help='record just these again, e.g. hail-mary joyful-1 joyful-1-03')
    ap.add_argument('--force', action='store_true', help='record again even if the file exists')
    ap.add_argument('--voice', action='append', metavar='NAME:FOLDER',
                    help='a voice and its folder under _static/audio (may repeat); '
                         'default: the voices in VOICES')
    ap.add_argument('--rate', default='-10%',
                    help='speaking speed, e.g. -10%% (a little slower, the default), +0%%, -20%%')
    ap.add_argument('--list', action='store_true', help='list the English voices and stop')
    args = ap.parse_args()

    voices = await english_voices()
    names = {v['ShortName'] for v in voices}
    if args.list:
        for v in voices:
            print(f"{v['ShortName']:38} {v['Gender']:7} {v['Locale']}")
        return

    chosen = dict(VOICES)
    if args.voice:
        chosen = {}
        for item in args.voice:
            name, _, folder = item.partition(':')
            chosen[name] = folder or name.split('-')[-1].replace('Neural', '').lower()
    for name in chosen:
        if name not in names:
            sys.exit(f'No voice called {name}.  Run with --list to see the English voices.')

    items = load_items()
    only = args.only or ONLY
    if only:
        keys = find_only(only, items)
        force = True                         # ONLY means record these again
        print('Recording only: ' + ', '.join(keys))
    else:
        what = args.record or RECORD
        what = [what] if isinstance(what, str) else list(what)
        bad = [w for w in what if w not in KINDS + ('all',)]
        if bad:
            sys.exit(f"RECORD can be 'prayers', 'mysteries', 'steps' or 'all' (not {bad[0]!r}).")
        kinds = KINDS if 'all' in what else tuple(what)
        keys = [k for k, v in items.items() if v[0] in kinds]
        force = args.force
        print('Recording: ' + ', '.join(kinds))

    made = skipped = 0
    for name, folder in chosen.items():
        print(f'\n{name}  ->  {AUDIO / folder}')
        move_old_files(folder, items)
        manifest = load_manifest(folder)
        try:
            for key in keys:
                kind, fname, title, words = items[key]
                out = AUDIO / folder / kind / fname
                rel = f'{kind}/{fname}'
                said = spoken(words)
                if out.exists() and not force:
                    if rel not in manifest:
                        manifest[rel] = said         # made before the list was kept
                    if manifest[rel] == said:
                        skipped += 1
                        continue
                    print(f'  (words changed) {rel}')
                out.parent.mkdir(parents=True, exist_ok=True)
                for attempt in (1, 2, 3, 4):
                    try:
                        await record(said, name, args.rate, out)
                        break
                    except Exception as e:      # the service sometimes drops a request
                        if attempt == 4:
                            sys.exit(f'  Could not record {title}: {e}')
                        await asyncio.sleep(2 * attempt)
                manifest[rel] = said
                print(f'  made    {rel}')
                made += 1
        finally:
            save_manifest(folder, manifest)      # even if stopped part way
    print(f'\nDone: {made} recorded, {skipped} already there.  '
          'Rebuild the docs (make clean html) to hear them.')


if __name__ == '__main__':
    asyncio.run(main())
