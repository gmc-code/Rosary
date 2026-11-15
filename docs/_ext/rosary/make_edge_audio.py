"""Record the Rosary prayers with Microsoft Edge's neural voices (edge-tts).

Makes one .mp3 per prayer in rosary_data.PRAYERS, named after the prayer
(Our Father.mp3, Hail Mary.mp3, ...), and one per mystery announcement
(First Joyful Mystery.mp3 ... Fifth Glorious Mystery.mp3, saying "First
Joyful Mystery. The Annunciation. The fruit of the mystery: Humility."),
so the rosary directive finds them, in
a folder per voice under docs/_static/prayers:

    docs/_static/prayers/natasha/   en-AU-NatashaNeural   (Australian, female)
    docs/_static/prayers/william/   en-AU-WilliamMultilingualNeural (Australian, male)
    VOICES = [
        'en-CA-LiamNeural',
        'en-US-AndrewNeural',
        'en-US-SteffanNeural',
        'en-US-EricNeural',
        'en-US-EmmaMultilingualNeural',
        'en-US-AvaNeural',
    ]


Each folder is listed in rosary_recordings in conf.py, so it shows up in the
Voice menu.  The recordings are made once on your own PC (edge-tts needs the
internet) and committed with the site; Read the Docs does not need edge-tts.

Setup (once):
    pip install edge-tts

Run from the docs folder:
    python _ext/rosary/make_edge_audio.py              # both voices, new files only
    python _ext/rosary/make_edge_audio.py --force      # record everything again
    python _ext/rosary/make_edge_audio.py --list       # English voices to choose from
    python _ext/rosary/make_edge_audio.py --voice en-GB-SoniaNeural:sonia
    python _ext/rosary/make_edge_audio.py --rate -15%  # slower (default -10%)
    python _ext/rosary/make_edge_audio.py --only hail-mary glory-be
    python _ext/rosary/make_edge_audio.py --only joyful-1      # one mystery
    (or list them in ONLY = [...] below; these are always recorded again)
    python _ext/rosary/make_edge_audio.py --record mysteries   # the 20 announcements
    python _ext/rosary/make_edge_audio.py --record prayers     # the prayers only
    (or set RECORD = 'prayers' / 'mysteries' / 'both' below and just run it)
"""

import argparse
import asyncio
import importlib.util
import re
import sys
from pathlib import Path

try:
    import edge_tts
except ImportError:
    sys.exit('edge-tts is not installed.  Run:  pip install edge-tts')

HERE = Path(__file__).resolve().parent            # docs/_ext/rosary
STATIC = HERE.parent.parent / '_static' / 'prayers'   # docs/_static/prayers

# voice name -> folder under docs/_static/prayers.  Microsoft renames voices now and
# then; see https://github.com/microsoft/edge-tts/issues/5
# What to record when the script is run with no options:
#   'prayers'    the 11 prayers (Our Father, Hail Mary, ...)
#   'mysteries'  the 20 mystery announcements (First Joyful Mystery. ...)
#   'both'       all of them
RECORD = 'mysteries'
ONLY = ['hail-mary', 'hail-holy-queen', 'rosary-prayer']
# Record just these, again (replacing the files that are there), e.g.
#   ONLY = ['creed', 'hail-mary']
#   ONLY = ["The Apostles' Creed", 'Hail Mary', 'joyful-1']
# Use a prayer's key or its title (any capitals), or a mystery such as
# joyful-1 ... glorious-5.  Leave it empty, ONLY = [], to use RECORD instead.
# ONLY = []

# voice name -> folder under docs/_static/prayers
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
FALLBACK = {}


# Words read differently from how they are written, so the voice says them
# well.  The text on the page is not changed, only what is spoken.
# Whole words or phrases, any capitals ("Blessed" -> "Blessid").
SAY_AS = {
    'Pontius Pilate': 'Ponshus Pilate',
    'blessed': 'blessid',       # two syllables, BLESS-id, not "blest"
}


def load_data():
    """rosary_data.py, without importing the whole extension."""
    spec = importlib.util.spec_from_file_location('rosary_data', HERE / 'rosary_data.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_prayers():
    return load_data().PRAYERS


def load_items(prayers_too=True, mysteries_too=True):
    """Everything to record: {key: (title, words)}.  The mysteries are
    announced the way the site says them, e.g. "First Joyful Mystery. The
    Annunciation. The fruit of the mystery: Humility." (key joyful-1, file
    First Joyful Mystery.mp3)."""
    data = load_data()
    items = {}
    if prayers_too:
        items.update(data.PRAYERS)
    if mysteries_too:
        for skey in data.SET_ORDER:
            for i, m in enumerate(data.SETS[skey]['mysteries']):
                ordinal = '%s %s Mystery' % (data.ORDINALS[i], data.SETS[skey]['name'])
                items['%s-%d' % (skey, i + 1)] = (
                    ordinal, '%s. %s. The fruit of the mystery: %s.' % (ordinal, m['title'], m['fruit']))
    return items


# file names that differ from the prayer's title (matching your own recordings)
FILE_NAMES = {
    'fatima': 'Fatima Prayer',
}


def file_name(title, key=None):
    """A prayer's file name, safe for Windows ('Hail, Holy Queen' stays)."""
    name = FILE_NAMES.get(key, title)
    return re.sub(r'[\\/:*?"<>|]', '', name).strip() + '.mp3'


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


async def english_voices():
    voices = await edge_tts.list_voices()
    return sorted((v for v in voices if v['Locale'].startswith('en-')),
                  key=lambda v: (v['Locale'], v['ShortName']))


async def record(text, voice, rate, out_path):
    tmp = out_path.with_suffix('.part')
    await edge_tts.Communicate(text, voice, rate=rate).save(str(tmp))
    tmp.replace(out_path)


async def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--voice', action='append', metavar='NAME:FOLDER',
                    help='a voice and its folder under _static/prayers (may repeat); '
                         'default: the voices in VOICES')
    ap.add_argument('--rate', default='-10%',
                    help='speaking speed, e.g. -10%% (a little slower, the default), +0%%, -20%%')
    ap.add_argument('--only', nargs='+', metavar='KEY',
                    help='record only these prayers (keys such as hail-mary glory-be)')
    ap.add_argument('--force', action='store_true', help='record again even if the file exists')
    ap.add_argument('--record', choices=('prayers', 'mysteries', 'both'), default=RECORD,
                    help=f'what to record (default {RECORD!r}, set by RECORD at the top)')
    ap.add_argument('--no-mysteries', action='store_true', help='same as --record prayers')
    ap.add_argument('--mysteries-only', action='store_true', help='same as --record mysteries')
    ap.add_argument('--list', action='store_true', help='list the English voices and stop')
    args = ap.parse_args()

    voices = await english_voices()
    names = {v['ShortName'] for v in voices}
    if args.list:
        for v in voices:
            print(f"{v['ShortName']:38} {v['Gender']:7} {v['Locale']}")
        return

    chosen = dict(VOICES)
    for name in list(chosen):
        if name not in names and name in FALLBACK:
            locale, gender = FALLBACK[name]
            alts = [v['ShortName'] for v in voices
                    if v['Locale'] == locale and v['Gender'] == gender]
            if alts:
                print(f'{name} is not available; using {alts[0]} instead.')
                chosen[alts[0]] = chosen.pop(name)
    if args.voice:
        chosen = {}
        for item in args.voice:
            name, _, folder = item.partition(':')
            chosen[name] = folder or name.split('-')[-1].replace('Neural', '').lower()
    for name in chosen:
        if name not in names:
            sys.exit(f'No voice called {name}.  Run with --list to see the English voices.')

    what = args.record
    if args.no_mysteries:
        what = 'prayers'
    if args.mysteries_only:
        what = 'mysteries'
    if RECORD not in ('prayers', 'mysteries', 'both'):
        sys.exit(f"RECORD = {RECORD!r} at the top of the script: use 'prayers', 'mysteries' or 'both'.")
    print(f'Recording: {what}')
    prayers = load_items(prayers_too=what != 'mysteries', mysteries_too=what != 'prayers')
    only = args.only or ONLY
    if only:
        # every prayer and mystery, found by key or by title
        everything = load_items()
        lookup = {}
        for k, (title, _w) in everything.items():
            lookup[k.lower()] = k
            lookup[_squash(title)] = k
            lookup[_squash(file_name(title, k)[:-4])] = k
        keys, unknown = [], []
        for item in only:
            k = lookup.get(item.lower()) or lookup.get(_squash(item))
            (keys if k else unknown).append(k or item)
        if unknown:
            sys.exit('Not found: ' + ', '.join(unknown) + '\nKeys: ' + ', '.join(everything))
        prayers = everything
        args.force = True            # ONLY means record these again
        print('Recording only: ' + ', '.join(keys))
    else:
        keys = list(prayers)

    made = skipped = 0
    for name, folder in chosen.items():
        out_dir = STATIC / folder
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f'\n{name}  ->  {out_dir}')
        for key in keys:
            title, text = prayers[key]
            out = out_dir / file_name(title, key)
            old_out = out_dir / file_name(title)       # named after the title before
            if old_out != out and old_out.exists():
                if out.exists():
                    old_out.unlink()
                else:
                    old_out.rename(out)
                print(f'  renamed {old_out.name} -> {out.name}')
            if out.exists() and not args.force:
                print(f'  (have)  {out.name}')
                skipped += 1
                continue
            for attempt in (1, 2, 3):
                try:
                    await record(spoken(text), name, args.rate, out)
                    break
                except Exception as e:          # the service sometimes drops a request
                    if attempt == 3:
                        sys.exit(f'  Could not record {title}: {e}')
                    await asyncio.sleep(2 * attempt)
            print(f'  made    {out.name}')
            made += 1
    print(f'\nDone: {made} recorded, {skipped} already there.  '
          'Rebuild the docs (make clean html) to hear them.')


if __name__ == '__main__':
    asyncio.run(main())
