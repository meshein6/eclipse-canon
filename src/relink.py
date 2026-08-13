"""Re-emit index.html from template.py, reusing the data an earlier build packed.

    python src/relink.py

`build.py` recomputes the whole canon and needs pyephem, the land raster and a
network fetch of the border and place data. None of that changes when the only
thing being edited is the page itself, so this pulls the eight packed blobs back
out of the existing index.html and pushes them through the current template.
Seconds instead of minutes, and no downloads.

It is a UI shortcut, not a substitute: anything that changes what is *in* the
blobs still has to go through build.py.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from template import HTML

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Each blob is pulled out by the line the template emits it on, so these patterns
# have to keep matching whatever template.py currently writes.
FIELDS = [
    ('__META__',   r'const META="([^"]*)"'),
    ('__PIDX__',   r'PIDX="([^"]*)"'),
    ('__PDAT__',   r'PDAT="([^"]*)"'),
    ('__COAST__',  r'const LAND=poly\("([^"]*)"\)'),
    ('__ADMIN0__', r'BORD0=poly\("([^"]*)"\)'),
    ('__ADMIN1__', r'BORD1=poly\("([^"]*)"\)'),
    ('__PLACES__', r'const PLC=\(\(\)=>\{const d="([^"]*)"'),
    ('__PNAMES__', r'nm="([^"]*)"\.split'),
]


def extract(html):
    out = {}
    for key, pat in FIELDS:
        m = re.search(pat, html)
        if not m:
            raise SystemExit(f'{key}: no match for {pat!r} — was index.html built '
                             f'by a different template? Run build.py instead.')
        out[key] = m.group(1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default=os.path.join(ROOT, 'index.html'),
                    help='a previously built page to take the data from')
    ap.add_argument('--out', default=os.path.join(ROOT, 'index.html'))
    args = ap.parse_args()

    with open(args.src) as f:
        blobs = extract(f.read())

    html = HTML
    for key, val in blobs.items():
        html = html.replace(key, val)
    left = [k for k, _ in FIELDS if k in html]
    if left:
        raise SystemExit('placeholders left unfilled: ' + ', '.join(left))

    with open(args.out, 'w') as f:
        f.write(html)
    print(f'wrote {args.out}  ({len(html)/1024:.0f} KB)')
    for key, _ in FIELDS:
        print(f'  {key:<11} {len(blobs[key]):>9,} chars')


if __name__ == '__main__':
    main()
