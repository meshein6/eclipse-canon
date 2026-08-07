"""Simplified world coastlines, derived from a 30-arcsecond land raster.

Downsamples the global-land-mask grid, runs marching squares, and applies
Douglas-Peucker so the outlines cost a few kilobytes rather than a few megabytes.
They exist for orientation on the eclipse-path map, not for measurement.
"""
import sys
import numpy as np
from skimage import measure

sys.setrecursionlimit(20000)


def _rdp(p, eps):
    if len(p) < 3:
        return p
    a, b = p[0], p[-1]
    ab = b - a
    n = np.hypot(ab[0], ab[1])
    if n < 1e-9:
        d = np.hypot(*(p - a).T)
    else:
        d = np.abs(ab[0] * (p[:, 1] - a[1]) - ab[1] * (p[:, 0] - a[0])) / n
    i = int(np.argmax(d))
    if d[i] > eps:
        return np.vstack([_rdp(p[:i + 1], eps)[:-1], _rdp(p[i:], eps)])
    return np.vstack([a, b])


def polylines(step=30, threshold=0.4, tolerance=1.0, min_area=6, min_pts=10):
    """Return a list of (lon, lat) arrays tracing the world's coastlines."""
    from global_land_mask import globe
    land_raw = ~globe._mask                      # package stores True = ocean
    h, w = land_raw.shape
    rows, cols = h // step, w // step
    block = land_raw[:rows * step, :cols * step]
    block = block.reshape(rows, step, cols, step).mean(axis=(1, 3))
    land = (block > threshold).astype(float)

    pad = np.zeros((rows + 2, cols + 2))
    pad[1:-1, 1:-1] = land
    deg = 180.0 / rows

    out = []
    for c in measure.find_contours(pad, 0.5):
        if len(c) < min_pts:
            continue
        x, y = c[:, 1], c[:, 0]
        area = abs(np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)) / 2
        if area < min_area:
            continue
        s = _rdp(c, tolerance)
        if len(s) < 5:
            continue
        lat = 90 - (s[:, 0] - 1 + 0.5) * deg
        lon = (s[:, 1] - 1 + 0.5) * deg - 180
        out.append(np.stack([lon, lat], 1))
    out.sort(key=len, reverse=True)
    return out


if __name__ == '__main__':
    p = polylines()
    print(len(p), 'polygons,', sum(len(q) for q in p), 'points')
