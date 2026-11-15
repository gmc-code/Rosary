"""Record the Rosary prayers with Microsoft Edge's neural voices (edge-tts).

Makes one .mp3 per prayer in rosary_data.PRAYERS, named after the prayer
(Our Father.mp3, Hail Mary.mp3, ...) so the rosary directive finds them, in
a folder per voice under docs/_static:

    docs/_static/edge_natasha/   en-AU-NatashaNeural   (Australian, female)
    docs/_static/edge_william/   en-AU-WilliamMultilingualNeural (Australian, male)
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
    python _ext/rosary/make_edge_audio.py --voice en-GB-SoniaNeural:edge_sonia
    python _ext/rosary/make_edge_audio.py --rate -15%  # slower (default -10%)
    python _ext/rosary/make_edge_audio.py --only hail-mary glory-be
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
STATIC = HERE.parent.parent / '_static'           # docs/_static

# voice name -> folder under docs/_static.  Microsoft renames voices now and
# then; if one of these has gone, the first Australian voice of the same
# gender is used instead (see FALLBACK).
# VOICES = {
#     'en-AU-NatashaNeural': 'edge_natasha',
#     'en-AU-WilliamMultilingualNeural': 'edge_william',
# }
# FALLBACK = {
#     'en-AU-NatashaNeural': ('en-AU', 'Female'),
#     'en-AU-WilliamMultilingualNeural': ('en-AU', 'Male'),
# }
# voice name -> folder under docs/_static
VOICES = {
    'en-CA-LiamNeural': 'edge_liam',
    'en-US-AndrewNeural': 'edge_andrew',
    'en-US-SteffanNeural': 'edge_steffan',
    'en-US-EricNeural': 'edge_eric',
    'en-US-EmmaMultilingualNeural': 'edge_emma',
    'en-US-AvaNeural': 'edge_ava',
}
FALLBACK = {}


# Words read differently from how they are written, so the voice says them
# well.  The text on the page is not changed, only what is spoken.
SAY_AS = {
    # 'Pontius Pilate': 'Pontius Pilate',
}


def load_prayers():
    """PRAYERS from rosary_data.py, without importing the whole extension."""
    spec = importlib.util.spec_from_file_location('rosary_data', HERE / 'rosary_data.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.PRAYERS


# file names that differ from the prayer's title (matching your own recordings)
FILE_NAMES = {
    'fatima': 'Fatima Prayer',
}


def file_name(title, key=None):
    """A prayer's file name, safe for Windows ('Hail, Holy Queen' stays)."""
    name = FILE_NAMES.get(key, title)
    return re.sub(r'[\\/:*?"<>|]', '', name).strip() + '.mp3'


def spoken(text):
    for written, said in SAY_AS.items():
        text = text.replace(written, said)
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
                    help='a voice and its folder under _static (may repeat); '
                         'default: the voices in VOICES')
    ap.add_argument('--rate', default='-10%',
                    help='speaking speed, e.g. -10%% (a little slower, the default), +0%%, -20%%')
    ap.add_argument('--only', nargs='+', metavar='KEY',
                    help='record only these prayers (keys such as hail-mary glory-be)')
    ap.add_argument('--force', action='store_true', help='record again even if the file exists')
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
            chosen[name] = folder or 'edge_' + name.split('-')[-1].replace('Neural', '').lower()
    for name in chosen:
        if name not in names:
            sys.exit(f'No voice called {name}.  Run with --list to see the English voices.')

    prayers = load_prayers()
    keys = args.only or list(prayers)
    unknown = [k for k in keys if k not in prayers]
    if unknown:
        sys.exit('Unknown prayer key(s): ' + ', '.join(unknown) + '\nKeys: ' + ', '.join(prayers))

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
