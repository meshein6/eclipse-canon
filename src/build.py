"""Regenerate index.html from scratch.

    python src/build.py            # full canon, -2000 to 3000  (~2 min)
    python src/build.py --quick    # 1800-2200 only, for iterating on the UI

Everything is computed here; nothing is downloaded. The only inputs are the
lunar/solar theory in pyephem and the land raster in global-land-mask.
"""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ephem
from eclipses import catalogue
from geometry import build as build_track, deltaT
import cities
import coastlines
import encode
from template import HTML

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths are only drawn where delta-T is well enough known for the longitude to
# mean anything. Durations do not depend on delta-T, so they run as far back as
# the ephemeris will go (about 250 BCE).
PATH_FROM, PATH_TO = 1000, 3000


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quick', action='store_true', help='narrow date range, faster')
    ap.add_argument('--out', default=os.path.join(ROOT, 'index.html'))
    args = ap.parse_args()

    y0, y1 = (1800, 2200) if args.quick else (-2000, 3000)
    t0 = time.time()

    print(f'computing eclipses {y0}..{y1} ...')
    rows = catalogue(y0, y1)
    rows.sort(key=lambda r: (r['y'], r['m'], r['d']))
    print(f'  {len(rows)} eclipses')

    print('computing shadow tracks, widths and durations ...')
    durs, n_track = {}, 0
    for r in rows:
        if r['t'] == 3:                       # partial: no central phase
            continue
        try:
            p = build_track(r['jde'], r['y'], npts=13)
        except Exception:
            p = None
        if not p or not p['width'] or not p['dur']:
            continue
        durs[(r['y'], r['m'], r['d'])] = (int(round(p['width'])), int(round(p['dur'])))
        if PATH_FROM <= r['y'] <= PATH_TO:
            t = ephem.Date(p['gj'] - 2415020.0).tuple()
            r['pts'] = p['pts']
            r['wp'] = [int(round(min(w, 4095))) for w in p['wpts']]
            r['dp'] = [int(round(min(d, 4095))) for d in p['dpts']]
            r['w'] = int(round(p['width']))
            r['dur'] = int(round(p['dur']))
            r['ut'] = int(round(t[3] * 60 + t[4] + t[5] / 60)) % 1440
            # how long the umbra takes to cross, so the viewer can run a clock
            r['span'] = int(round((p['end'] - p['start']) * 1440))
            n_track += 1
    print(f'  {len(durs)} durations, {n_track} drawn tracks')

    print('tracing coastlines ...')
    # 0.1-degree cells: fine enough that the globe still reads when zoomed in
    coast = coastlines.polylines(step=12, tolerance=0.7, min_area=10)
    print(f'  {len(coast)} polygons, {sum(len(c) for c in coast)} points')

    meta = encode.pack_meta(rows, durs)
    pidx, pdat = encode.pack_paths(rows)
    html = (HTML.replace('__META__', meta)
                .replace('__PIDX__', pidx)
                .replace('__PDAT__', pdat)
                .replace('__COAST__', encode.pack_coast(coast))
                .replace('__CITIES__', cities.pack()))
    with open(args.out, 'w') as f:
        f.write(html)

    print(f'wrote {args.out}  ({len(html)/1024:.0f} KB)  in {time.time()-t0:.0f}s')


if __name__ == '__main__':
    main()
