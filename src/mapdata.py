"""Country and province borders, and populated places.

This module is the one place in the project that uses downloaded data. Everything
about the eclipses themselves is still computed from lunar/solar theory; these are
purely reference overlays so that a zoomed-in globe has recognisable geography on it.

    Borders  Natural Earth 1:50m admin-0 boundary lines (land) and 1:10m admin-1
             state/province lines. Public domain, no attribution required.
    Places   GeoNames cities5000, filtered to population >= 10,000.
             Licensed CC-BY 4.0, so the page credits GeoNames.

Both are cached under data/ (gitignored). Run `python src/mapdata.py --fetch` once,
or let build.py fetch on first use. Nothing is fetched at run time, ever.
"""
import io
import os
import sys
import urllib.request
import zipfile

import numpy as np

from coastlines import _rdp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')

ADMIN0 = 'ne_50m_admin_0_boundary_lines_land.zip'
ADMIN1 = 'ne_10m_admin_1_states_provinces_lines.zip'
PLACES = 'cities5000.zip'


URLS = {
    ADMIN0: 'https://naciscdn.org/naturalearth/50m/cultural/' + ADMIN0,
    ADMIN1: 'https://naciscdn.org/naturalearth/10m/cultural/' + ADMIN1,
    PLACES: 'https://download.geonames.org/export/dump/' + PLACES,
}


def fetch(force=False):
    """Populate data/ from the upstream sources. Idempotent."""
    os.makedirs(DATA, exist_ok=True)
    for name, url in URLS.items():
        path = os.path.join(DATA, name)
        if os.path.exists(path) and os.path.getsize(path) > 0 and not force:
            continue
        print(f'  fetching {name} ...')
        with urllib.request.urlopen(url, timeout=240) as r, open(path, 'wb') as f:
            f.write(r.read())
    return DATA


def _read_shapes(zip_name):
    import shapefile
    path = os.path.join(DATA, zip_name)
    zf = zipfile.ZipFile(path)
    base = [n[:-4] for n in zf.namelist() if n.endswith('.shp')][0]
    r = shapefile.Reader(shp=io.BytesIO(zf.read(base + '.shp')),
                         dbf=io.BytesIO(zf.read(base + '.dbf')),
                         shx=io.BytesIO(zf.read(base + '.shx')))
    return r.shapes()


def _lines(zip_name, tolerance, min_span):
    """Simplified (lon, lat) polylines from a Natural Earth line shapefile."""
    out = []
    for s in _read_shapes(zip_name):
        pts = np.asarray(s.points, dtype=float)
        if len(pts) < 2:
            continue
        # shapefiles pack multi-part geometry into one point list
        parts = list(s.parts) + [len(pts)]
        for a, b in zip(parts, parts[1:]):
            seg = pts[a:b]
            if len(seg) < 2:
                continue
            span = max(np.ptp(seg[:, 0]), np.ptp(seg[:, 1]))
            if span < min_span:
                continue
            # a border that crosses the antimeridian would draw as a streak
            if np.abs(np.diff(seg[:, 0])).max() > 180:
                continue
            s2 = _rdp(seg, tolerance) if len(seg) > 2 else seg
            if len(s2) >= 2:
                out.append(s2)
    return out


def borders():
    """Country lines and province lines, as two separate lists."""
    a0 = _lines(ADMIN0, tolerance=0.02, min_span=0.05)
    a1 = _lines(ADMIN1, tolerance=0.05, min_span=0.25)
    return a0, a1


def places(min_pop=10000):
    """(name, lon, lat, tier) for everywhere above min_pop, biggest first.

    Tier buckets the population so the viewer can fade places in as it zooms
    instead of dumping forty thousand dots on screen at once.
    """
    zf = zipfile.ZipFile(os.path.join(DATA, PLACES))
    txt = zf.read('cities5000.txt').decode('utf-8')
    rows = []
    for line in txt.splitlines():
        f = line.split('\t')
        if len(f) < 15:
            continue
        try:
            pop = int(f[14] or 0)
            lat, lon = float(f[4]), float(f[5])
        except ValueError:
            continue
        if pop < min_pop:
            continue
        name = (f[2] or f[1]).strip()
        if not name or '~' in name:
            continue
        rows.append((name, lon, lat, pop))
    rows.sort(key=lambda r: -r[3])

    def tier(pop):
        if pop >= 2000000:
            return 0
        if pop >= 300000:
            return 1
        if pop >= 75000:
            return 2
        if pop >= 25000:
            return 3
        return 4

    return [(n, lo, la, tier(p)) for n, lo, la, p in rows]


if __name__ == '__main__':
    import collections
    if '--fetch' in sys.argv:
        fetch(force='--force' in sys.argv)
    a0, a1 = borders()
    print(f'admin0: {len(a0)} lines, {sum(len(x) for x in a0)} points')
    print(f'admin1: {len(a1)} lines, {sum(len(x) for x in a1)} points')
    p = places()
    print(f'places: {len(p)}, tiers ' +
          str(dict(sorted(collections.Counter(x[3] for x in p).items()))))
    print('name chars:', sum(len(x[0]) for x in p))
