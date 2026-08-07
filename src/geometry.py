"""Shadow-axis geometry: where the umbra falls, how wide, how long.

Positions come from pyephem (apparent geocentric Sun and Moon). The shadow
axis is the Sun->Moon vector; the track is its intersection with the WGS-84
ellipsoid, converted through apparent sidereal time to geodetic coordinates.
Meeus gives times in TD, so they are shifted to UT with the Espenak-Meeus
delta-T polynomials.
"""
import ephem, math, json
from math import sin, cos, atan2, sqrt, degrees, radians

AU = 149597870.7
F = 1/298.257223563
OMF = 1 - F
REQ = 6378.137

_sun, _moon = ephem.Sun(), ephem.Moon()
_obs = ephem.Observer(); _obs.lon = 0; _obs.lat = 0; _obs.elevation = 0
_obs.pressure = 0

def vec(ra, dec, dist_au):
    r = dist_au * AU / REQ           # Earth equatorial radii
    return (r*cos(dec)*cos(ra), r*cos(dec)*sin(ra), r*sin(dec))

def axis_hit(jd):
    """Return (lon_deg, lat_deg) where the Sun->Moon shadow axis meets Earth, or None."""
    d = ephem.Date(jd - 2415020.0)   # ephem epoch = 1899-12-31 12:00 UT
    _sun.compute(d); _moon.compute(d)
    S = vec(float(_sun.ra), float(_sun.dec), _sun.earth_distance)
    M = vec(float(_moon.ra), float(_moon.dec), _moon.earth_distance)
    u = [M[i]-S[i] for i in range(3)]
    n = sqrt(sum(c*c for c in u)); u = [c/n for c in u]
    # scale z for oblateness -> unit sphere
    Ms = (M[0], M[1], M[2]/OMF)
    us = (u[0], u[1], u[2]/OMF)
    a = sum(c*c for c in us)
    b = 2*sum(Ms[i]*us[i] for i in range(3))
    c0 = sum(c*c for c in Ms) - 1.0
    disc = b*b - 4*a*c0
    if disc < 0:
        return None
    t = (-b - sqrt(disc)) / (2*a)    # near (sunward) surface
    P = [Ms[i] + t*us[i] for i in range(3)]
    _obs.date = d
    gast = float(_obs.sidereal_time())
    lon = degrees(atan2(P[1], P[0]) - gast)
    while lon > 180: lon -= 360
    while lon < -180: lon += 360
    lat = degrees(atan2(P[2]/OMF, sqrt(P[0]**2 + P[1]**2)))   # geodetic
    return lon, lat

def hits(jd):
    return axis_hit(jd) is not None

def path(jd_max, step_min=6.0):
    """Sample the central line. jd_max = approximate time of greatest eclipse."""
    step = step_min/1440.0
    # walk outward to find the window where the axis strikes Earth
    if not hits(jd_max):
        found = False
        for k in range(1, 60):
            for s in (-1, 1):
                if hits(jd_max + s*k*step):
                    jd_max = jd_max + s*k*step; found = True; break
            if found: break
        if not found:
            return []
    lo = jd_max
    while hits(lo - step): lo -= step
    hi = jd_max
    while hits(hi + step): hi += step
    # bisect the two ends
    a, b = lo - step, lo
    for _ in range(24):
        m = (a+b)/2
        if hits(m): b = m
        else: a = m
    start = b
    a, b = hi, hi + step
    for _ in range(24):
        m = (a+b)/2
        if hits(m): a = m
        else: b = m
    end = a
    N = 26
    pts = []
    for i in range(N+1):
        jd = start + (end-start)*i/N
        p = axis_hit(jd)
        if p: pts.append((p[0], p[1], jd))
    return pts


import ephem, math, json
from math import sin, cos, atan2, sqrt, degrees, radians

RSUN = 696000.0 / REQ      # Earth equatorial radii
RMOON = 1737.4 / REQ

def deltaT(y):
    """Espenak & Meeus polynomial expressions, seconds."""
    if y < 1600:
        u = (y - 1000) / 100.0
        return (1574.2 - 556.01*u + 71.23472*u**2 + 0.319781*u**3
                - 0.8503463*u**4 - 0.005050998*u**5 + 0.0083572073*u**6)
    if y < 1700:
        t = y - 1600
        return 120 - 0.9808*t - 0.01532*t**2 + t**3/7129.0
    if y < 1800:
        t = y - 1700
        return 8.83 + 0.1603*t - 0.0059285*t**2 + 0.00013336*t**3 - t**4/1174000.0
    if y < 1860:
        t = y - 1800
        return (13.72 - 0.332447*t + 0.0068612*t**2 + 0.0041116*t**3 - 0.00037436*t**4
                + 0.0000121272*t**5 - 0.0000001699*t**6 + 0.000000000875*t**7)
    if y < 1900:
        t = y - 1860
        return (7.62 + 0.5737*t - 0.251754*t**2 + 0.01680668*t**3
                - 0.0004473624*t**4 + t**5/233174.0)
    if y < 1920:
        t = y - 1900
        return -2.79 + 1.494119*t - 0.0598939*t**2 + 0.0061966*t**3 - 0.000197*t**4
    if y < 1941:
        t = y - 1920
        return 21.20 + 0.84493*t - 0.076100*t**2 + 0.0020936*t**3
    if y < 1961:
        t = y - 1950
        return 29.07 + 0.407*t - t**2/233.0 + t**3/2547.0
    if y < 1986:
        t = y - 1975
        return 45.45 + 1.067*t - t**2/260.0 - t**3/718.0
    if y < 2005:
        t = y - 2000
        return (63.86 + 0.3345*t - 0.060374*t**2 + 0.0017275*t**3
                + 0.000651814*t**4 + 0.00002373599*t**5)
    if y < 2050:
        t = y - 2000
        return 62.92 + 0.32217*t + 0.005589*t**2
    if y < 2150:
        return -20 + 32*((y-1820)/100.0)**2 - 0.5628*(2150 - y)
    u = (y - 1820) / 100.0
    return -20 + 32*u*u

def geometry(jd_ut):
    """Shadow-cone radius at the Earth-surface hit point, and ground width."""
    d = ephem.Date(jd_ut - 2415020.0)
    _sun.compute(d); _moon.compute(d)
    S = vec(float(_sun.ra), float(_sun.dec), _sun.earth_distance)
    M = vec(float(_moon.ra), float(_moon.dec), _moon.earth_distance)
    u = [M[i]-S[i] for i in range(3)]
    dsm = sqrt(sum(c*c for c in u)); u = [c/dsm for c in u]
    Ms = (M[0], M[1], M[2]/OMF); us = (u[0], u[1], u[2]/OMF)
    a = sum(c*c for c in us); b = 2*sum(Ms[i]*us[i] for i in range(3))
    c0 = sum(c*c for c in Ms) - 1.0
    disc = b*b - 4*a*c0
    if disc < 0: return None
    t = (-b - sqrt(disc)) / (2*a)
    Ps = [Ms[i] + t*us[i] for i in range(3)]
    P = (Ps[0], Ps[1], Ps[2]*OMF)                    # back to real coords
    D = sqrt(sum((P[i]-M[i])**2 for i in range(3)))  # Moon -> surface distance
    rcone = RMOON - D*(RSUN - RMOON)/dsm             # <0 => umbra, >0 => antumbra
    # local outward normal of the ellipsoid
    nrm = [P[0], P[1], P[2]/(OMF*OMF)]
    nn = sqrt(sum(c*c for c in nrm)); nrm = [c/nn for c in nrm]
    cosinc = abs(sum(nrm[i]*u[i] for i in range(3)))
    width = 2*abs(rcone)*REQ / max(cosinc, 0.02)
    diam  = 2*abs(rcone)*REQ
    return width, ('A' if rcone > 0 else 'T'), diam

def ground_speed(jd_ut, dt=30.0/86400):
    p1, p2 = axis_hit(jd_ut - dt), axis_hit(jd_ut + dt)
    if not p1 or not p2: return None
    la = radians((p1[1]+p2[1])/2)
    dlon = (p2[0]-p1[0]+180) % 360 - 180
    km = sqrt((dlon*cos(la)*111.32)**2 + ((p2[1]-p1[1])*110.57)**2)
    return km / (2*dt*86400)

def build(jde_td, year, npts=15):
    jd = jde_td - deltaT(year)/86400.0
    step = 6.0/1440
    if not hits(jd):
        ok = False
        for k in range(1, 80):
            for s in (-1, 1):
                if hits(jd + s*k*step): jd = jd + s*k*step; ok = True; break
            if ok: break
        if not ok: return None
    lo = jd
    while hits(lo - step): lo -= step
    hi = jd
    while hits(hi + step): hi += step
    a, b = lo - step, lo
    for _ in range(22):
        m = (a+b)/2
        if hits(m): b = m
        else: a = m
    start = b
    a, b = hi, hi + step
    for _ in range(22):
        m = (a+b)/2
        if hits(m): a = m
        else: b = m
    end = a
    pts = []
    for i in range(npts):
        p = axis_hit(start + (end-start)*i/(npts-1))
        pts.append(p if p else pts[-1])
    # greatest eclipse: sample for max cone-axis proximity to geocentre (use widest ground track)
    best, bjd = None, None
    for i in range(41):
        j = start + (end-start)*i/40
        g = geometry(j)
        if g and (best is None or g[0] < best[0] or True):
            pass
    # greatest eclipse ~ midpoint of the central track in time
    gj = (start+end)/2
    g = geometry(gj)
    sp = ground_speed(gj)
    dur = (g[2]/sp) if (g and sp and sp > 0) else None
    return dict(pts=pts, start=start, end=end, gj=gj,
                width=(g[0] if g else None), dur=dur)


if __name__ == '__main__':
    # published values for comparison
    for iso, yr, lat, lon, wid, dur in [
            ("2017/8/21 18:25:30", 2017,  36.97,  -87.65, 115, 160),
            ("2024/4/8 18:17:16",  2024,  25.30, -104.13, 198, 268),
            ("2027/8/2 10:07:50",  2027,  25.52,   33.20, 258, 383),
            ("2045/8/12 17:42:39", 2045,  25.90,  -78.50, 256, 366)]:
        jd = ephem.julian_date(ephem.Date(iso)) + deltaT(yr) / 86400.0
        r = build(jd, yr)
        mid = r['pts'][len(r['pts']) // 2]
        print(f"{iso}  {mid[1]:6.2f},{mid[0]:8.2f} (pub {lat},{lon})  "
              f"{r['width']:6.1f} km (pub {wid})  {r['dur']:6.1f} s (pub {dur})")
