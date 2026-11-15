"""Move the recordings into the new folder layout (no recording, no internet).

From:  docs/_static/prayers/<voice>/Our Father.mp3, First Joyful Mystery.mp3 ...
To:    docs/_static/audio/<voice>/prayers/     Our Father.mp3 ... (11)
                                  mysteries/   First Joyful Mystery.mp3 ... (20)
                                  steps/       joyful-1-01.mp3 ... (made later by
                                               make_edge_audio.py)

Files already in the right place are left alone, and the old folders are
removed once they are empty.  Anything the script does not recognise stays
where it is and is listed at the end.

Run it from anywhere:
    python _ext/rosary/reorganise_audio.py            # move the files
    python _ext/rosary/reorganise_audio.py --dry-run  # only show what would move

Afterwards, in conf.py, change each rosary_recordings path from
/_static/prayers/<voice> to /_static/audio/<voice>.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent              # docs/_ext/rosary
STATIC = HERE.parent.parent / '_static'             # docs/_static
OLD = STATIC / 'prayers'                            # the old layout
NEW = STATIC / 'audio'                              # the new layout

MYSTERY = re.compile(r'^(first|second|third|fourth|fifth) (joyful|luminous|sorrowful|glorious) mystery$', re.I)
STEP = re.compile(r'^(joyful|luminous|sorrowful|glorious)-[1-5]-(0[1-9]|10)$', re.I)
AUDIO = ('.mp3', '.m4a', '.ogg', '.wav')


def kind_of(path):
    """prayers, mysteries or steps for a recording; None for anything else."""
    if path.suffix.lower() not in AUDIO:
        return None
    if STEP.match(path.stem):
        return 'steps'
    if MYSTERY.match(path.stem):
        return 'mysteries'
    return 'prayers'


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--dry-run', action='store_true', help='show what would move, change nothing')
    args = ap.parse_args()
    dry = args.dry_run

    if not OLD.is_dir():
        print(f'Nothing to move: {OLD} does not exist.')
        if NEW.is_dir():
            print(f'The new layout is already in {NEW}:')
            for voice in sorted(p for p in NEW.iterdir() if p.is_dir()):
                counts = ', '.join(f'{k} {len(list((voice / k).glob("*.*")))}'
                                   for k in ('prayers', 'mysteries', 'steps') if (voice / k).is_dir())
                print(f'  {voice.name:10} {counts}')
        return

    moved = 0
    left = []
    for voice in sorted(p for p in OLD.iterdir() if p.is_dir()):
        counts = {'prayers': 0, 'mysteries': 0, 'steps': 0}
        for kind in counts:
            if not dry:
                (NEW / voice.name / kind).mkdir(parents=True, exist_ok=True)
        for f in sorted(voice.iterdir()):
            kind = kind_of(f) if f.is_file() else None
            if not kind:
                left.append(f)
                continue
            dest = NEW / voice.name / kind / f.name
            if dest.exists():
                left.append(f)                       # don't overwrite: leave both
                continue
            if not dry:
                shutil.move(str(f), str(dest))
            counts[kind] += 1
            moved += 1
        print(f'  {voice.name:10} prayers {counts["prayers"]:3}   mysteries {counts["mysteries"]:3}'
              f'   steps {counts["steps"]:3}   -> audio/{voice.name}/')
        if not dry and not any(voice.iterdir()):
            voice.rmdir()
    if not dry and not any(OLD.iterdir()):
        OLD.rmdir()
        print(f'\nRemoved the empty {OLD.name} folder.')

    print(f'\n{"Would move" if dry else "Moved"} {moved} files into {NEW}.')
    if left:
        print('\nLeft where they are (not a recording, or already in the new folder):')
        for f in left:
            print('  ', f.relative_to(STATIC))
    if not dry:
        print('\nNow, in conf.py, change each rosary_recordings path from '
              '/_static/prayers/<voice> to /_static/audio/<voice>, and rebuild.')


if __name__ == '__main__':
    sys.exit(main())
