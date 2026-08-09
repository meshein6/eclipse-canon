"""Compact base64-style packing so the whole canon fits in one HTML file."""
AB = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def e2(n):
    n = max(0, min(4095, int(round(n))))
    return AB[n >> 6] + AB[n & 63]


def e4(n):
    n = max(0, min(16777215, int(round(n))))
    return AB[(n >> 18) & 63] + AB[(n >> 12) & 63] + AB[(n >> 6) & 63] + AB[n & 63]


def e3(n):
    n = max(0, min(262143, int(round(n))))
    return AB[(n >> 12) & 63] + AB[(n >> 6) & 63] + AB[n & 63]


def eL(v, lo, hi):
    """Quantise a bounded float to two characters (4096 levels)."""
    return e2((v - lo) / (hi - lo) * 4095)


def eL3(v, lo, hi):
    """Three characters, 262144 levels: about 150 m of longitude.

    Two characters is only ~10 km, which the globe's 30x zoom shows as a visible
    wobble once the track is splined through the points.
    """
    return e3((v - lo) / (hi - lo) * 262143)


def pack_meta(rows, durs):
    """31 chars per eclipse.

    First 15: date(4) saros(2) type(1) gamma(2) inex(2) width(2) duration(2).
    Then 16 of penumbral geometry, present for every eclipse including partials:
    axis direction lon/lat (3+3), closest-approach direction lon/lat (3+3),
    gamma(2), penumbral radius L1(2). L1 packs to zero when it could not be
    computed, which is how the viewer knows to skip it.
    """
    out = []
    for r in rows:
        code = ((r['y'] + 2000) * 12 + (r['m'] - 1)) * 32 + r['d']
        w, du = durs.get((r['y'], r['m'], r['d']), (0, 0))
        pen = r.get('pen')
        if pen:
            ul, ub, pl, pb, g, l1 = pen
            ptxt = (eL3(ul, -180, 180) + eL3(ub, -90, 90)
                    + eL3(pl, -180, 180) + eL3(pb, -90, 90)
                    + eL(g, 0, 2) + eL(l1, 0.4, 0.7))
        else:
            ptxt = AB[0] * 16
        out.append(e4(code) + e2(r['S'] + 20) + AB[r['t']] + eL(r['g'], -1.6, 1.6)
                   + e2(r['I'] + 10) + e2(min(w, 4095)) + e2(min(du, 4095)) + ptxt)
    return "".join(out)


def pack_paths(rows):
    """Index of eclipses with a track, then 151 chars per record: 13 lon/lat pairs
    at 3 chars each, UT, width, duration, crossing span, then 13 per-point widths,
    13 per-point central durations, and 13 per-point flags (1 = annular there),
    which is what makes a hybrid's total and annular stretches distinguishable."""
    idx, dat = [], []
    for i, r in enumerate(rows):
        if 'pts' not in r:
            continue
        idx.append(e4(i))
        dat.append("".join(eL3(p[0], -180, 180) + eL3(p[1], -90, 90) for p in r['pts'])
                   + e2(r['ut']) + e2(min(r['w'], 4095)) + e2(min(r['dur'], 4095))
                   + e2(min(r['span'], 4095))
                   + "".join(e2(w) for w in r['wp'])
                   + "".join(e2(d) for d in r['dp'])
                   + "".join(AB[t] for t in r['tp']))
    return "".join(idx), "".join(dat)


def pack_coast(polys):
    return "~".join("".join(eL(p[0], -180, 180) + eL(p[1], -90, 90) for p in poly)
                    for poly in polys)


def pack_places(rows):
    """Seven chars each: lon(3) lat(3) tier(1), plus the names as one ~-joined run.

    Rows arrive sorted by descending population, so tiers only ever increase and
    the viewer can stop iterating as soon as a tier is too small to draw.
    """
    dat = "".join(eL3(lo, -180, 180) + eL3(la, -90, 90) + AB[t] for _, lo, la, t in rows)
    return dat, "~".join(n for n, _, _, _ in rows)
