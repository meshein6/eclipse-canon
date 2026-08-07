import math

D = math.pi / 180.0
def sin(x): return math.sin(x * D)
def cos(x): return math.cos(x * D)

def newmoon_base(k):
    T = k / 1236.85
    jde = (2451550.09766 + 29.530588861 * k
           + 0.00015437 * T**2 - 0.000000150 * T**3 + 0.00000000073 * T**4)
    return jde, T

def eclipse_for_k(k):
    """Meeus Astronomical Algorithms ch.54. Returns dict or None."""
    jde, T = newmoon_base(k)
    E = 1 - 0.002516 * T - 0.0000074 * T**2
    M  = 2.5534 + 29.10535670 * k - 0.0000014 * T**2 - 0.00000011 * T**3
    Mp = (201.5643 + 385.81693528 * k + 0.0107582 * T**2
          + 0.00001238 * T**3 - 0.000000058 * T**4)
    F  = (160.7108 + 390.67050284 * k - 0.0016118 * T**2
          - 0.00000227 * T**3 + 0.000000011 * T**4)
    Om = 124.7746 - 1.56375588 * k + 0.0020672 * T**2 + 0.00000215 * T**3

    # quick rejection test
    Fm = F % 360.0
    if abs(sin(Fm)) > 0.36:
        return None

    F1 = F - 0.02665 * sin(Om)
    A1 = 299.77 + 0.107408 * k - 0.009173 * T**2

    corr = (-0.4075 * sin(Mp)
            + 0.1721 * E * sin(M)
            + 0.0161 * sin(2 * Mp)
            - 0.0097 * sin(2 * F1)
            + 0.0073 * E * sin(Mp - M)
            - 0.0050 * E * sin(Mp + M)
            - 0.0023 * sin(Mp - 2 * F1)
            + 0.0021 * E * sin(2 * M)
            + 0.0012 * sin(Mp + 2 * F1)
            + 0.0006 * E * sin(2 * Mp + M)
            - 0.0004 * sin(3 * Mp)
            - 0.0003 * E * sin(M + 2 * F1)
            + 0.0003 * sin(A1)
            - 0.0002 * E * sin(M - 2 * F1)
            - 0.0002 * E * sin(2 * Mp - M)
            - 0.0002 * sin(Om))
    jde_max = jde + corr

    P = (0.2070 * E * sin(M) + 0.0024 * E * sin(2 * M) - 0.0392 * sin(Mp)
         + 0.0116 * sin(2 * Mp) - 0.0073 * E * sin(Mp + M)
         + 0.0067 * E * sin(Mp - M) + 0.0118 * sin(2 * F1))
    Q = (5.2207 - 0.0048 * E * cos(M) + 0.0020 * E * cos(2 * M)
         - 0.3299 * cos(Mp) - 0.0060 * E * cos(Mp + M) + 0.0041 * E * cos(Mp - M))
    W = abs(cos(F1))
    gamma = (P * cos(F1) + Q * sin(F1)) * (1 - 0.0048 * W)
    u = (0.0059 + 0.0046 * E * cos(M) - 0.0182 * cos(Mp)
         + 0.0004 * cos(2 * Mp) - 0.0005 * cos(M + Mp))

    ag = abs(gamma)
    if ag > 1.5433 + u:
        return None

    if ag < 0.9972:
        # central eclipse
        if u < 0:
            typ = 'T'
        elif u > 0.0047:
            typ = 'A'
        else:
            omega = 0.00464 * math.sqrt(1 - gamma * gamma)
            typ = 'H' if u < omega else 'A'
        mag = 1.0
    else:
        if ag < 0.9972 + abs(u):
            # non-central total or annular
            typ = 'T' if u < 0 else 'A'
            mag = 1.0
        else:
            typ = 'P'
            mag = (1.5433 + u - ag) / (0.5461 + 2 * u)
    return dict(k=k, jde=jde_max, gamma=gamma, u=u, type=typ, mag=mag)

def jd_to_date(jd):
    jd = jd + 0.5
    Z = int(jd); Fr = jd - Z
    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha / 4)
    B = A + 1524
    C = int((B - 122.1) / 365.25)
    Dd = int(365.25 * C)
    Ee = int((B - Dd) / 30.6001)
    day = B - Dd - int(30.6001 * Ee) + Fr
    month = Ee - 1 if Ee < 14 else Ee - 13
    year = C - 4716 if month > 2 else C - 4715
    return year, month, day

# --- saros series assignment ---
# k(S, I) = 358*S + 223*I + c  ->  S = 38*(k - 44) mod 223  (38 = inverse of 135 mod 223)
# calibrated on 2017-08-21 (S=145), 2024-04-08 (S=139), 2026-08-12 (S=126)
def saros_number(k, year):
    s0 = (38 * (k - 44)) % 223
    # active series drift ~ +1 per inex (28.945 yr), centred near 136 at year 2000
    expect = 136 + (year - 2000) / 28.945
    return s0 + 223 * round((expect - s0) / 223)

def catalogue(y0=-2000, y1=3000):
    """Every solar eclipse between y0 and y1, with saros and inex series."""
    k0 = int((y0 - 2000) * 12.3685) - 40
    k1 = int((y1 - 2000) * 12.3685) + 40
    out = []
    for k in range(k0, k1 + 1):
        e = eclipse_for_k(k)
        if not e:
            continue
        y, m, d = jd_to_date(e['jde'])
        if y < y0 or y > y1:
            continue
        ydec = y + ((m - 1) * 30.6 + d) / 365.25
        S = saros_number(k, ydec)
        I = (k - 44 - 358 * S) // 223 + 271   # anchored on 2000 Feb 5 = inex 30
        out.append(dict(k=k, y=y, m=m, d=int(d), S=S, I=I,
                        t={'T': 0, 'A': 1, 'H': 2, 'P': 3}[e['type']],
                        g=e['gamma'], jde=e['jde'], type=e['type']))
    return out


if __name__ == '__main__':
    from collections import Counter
    c = catalogue()
    print(len(c), 'eclipses;', Counter(r['type'] for r in c))
    idx = {(r['y'], r['m'], r['d']): r for r in c}
    for key, sar, ty in [((2017, 8, 21), 145, 'T'), ((2024, 4, 8), 139, 'T'),
                         ((2026, 8, 12), 126, 'T'), ((2045, 8, 12), 136, 'T'),
                         ((2023, 4, 20), 129, 'H'), ((2012, 5, 20), 128, 'A')]:
        r = idx[key]
        ok = 'ok ' if (r['S'] == sar and r['type'] == ty) else 'BAD'
        print(f"{ok} {key} saros {r['S']} {r['type']} gamma {r['g']:+.3f}")
