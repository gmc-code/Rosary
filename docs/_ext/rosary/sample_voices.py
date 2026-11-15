"""Record one prayer in several edge-tts voices, to compare them.

The samples go to Downloads\\Claude outputs\\voice samples (not the site),
named like  "The Sign of the Cross - en-GB-RyanNeural.mp3".

Run from the docs folder:
    python _ext/rosary/sample_voices.py
    python _ext/rosary/sample_voices.py --prayer hail-mary
    python _ext/rosary/sample_voices.py --rate -15%
    python _ext/rosary/sample_voices.py --force      # record them all again
"""

import argparse
import asyncio
import importlib.util
import os
import sys
from pathlib import Path

try:
    import edge_tts
except ImportError:
    sys.exit('edge-tts is not installed.  Run:  pip install edge-tts')

HERE = Path(__file__).resolve().parent            # docs/_ext/rosary
OUT = Path(os.path.expanduser('~')) / 'Downloads' / 'Claude outputs' / 'voice samples'

VOICES = [
    'en-CA-LiamNeural',
    'en-US-AndrewNeural',
    'en-US-SteffanNeural',
    'en-US-EricNeural',
    'en-US-EmmaMultilingualNeural',
    'en-US-AvaNeural',
]


def load_prayers():
    spec = importlib.util.spec_from_file_location('rosary_data', HERE / 'rosary_data.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.PRAYERS


async def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--prayer', default='sign-of-cross',
                    help='prayer key, e.g. sign-of-cross (default), hail-mary, glory-be')
    ap.add_argument('--rate', default='-10%', help='speaking speed (default -10%%)')
    ap.add_argument('--force', action='store_true', help='record samples again even if made before')
    args = ap.parse_args()

    prayers = load_prayers()
    if args.prayer not in prayers:
        sys.exit('Unknown prayer.  Keys: ' + ', '.join(prayers))
    title, text = prayers[args.prayer]

    OUT.mkdir(parents=True, exist_ok=True)
    print(f'{title}  ->  {OUT}')
    for voice in VOICES:
        out = OUT / f'{title} - {voice}.mp3'
        if out.exists() and not args.force:
            print(f'  (have) {out.name}')
            continue
        try:
            await edge_tts.Communicate(text, voice, rate=args.rate).save(str(out))
            print(f'  made  {out.name}')
        except Exception as e:
            print(f'  FAILED {voice}: {e}')
    os.startfile(OUT) if hasattr(os, 'startfile') else None   # open the folder (Windows)


if __name__ == '__main__':
    asyncio.run(main())
