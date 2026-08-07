# Canon of Solar Eclipses

An interactive canon of every solar eclipse from 2000 BCE to 3000 CE — 11,898 of them —
plus a working model of the saros cycle that produces them.

Everything is computed from first principles. No eclipse catalogue is downloaded or
scraped; the only inputs are lunar/solar theory and a land raster. The whole thing
builds into a single self-contained HTML file with no runtime dependencies.

**[Live demo](https://USERNAME.github.io/REPO/)** ← update after enabling Pages

## What's in it

**Canon** — every eclipse as a point, plotted against time. Three vertical axes:

- **Saros series** — each series is a horizontal thread of dots 18.03 years apart.
  The vertical NOW line crosses about 39 of them, which is the "40 concurrent series"
  fact made literal.
- **Inex series** — the other axis of the van den Bergh lattice. Inex series run for
  tens of millennia, so they stretch nearly the full 5,000 years.
- **Gamma** — the shadow-axis miss distance. Each saros series becomes a diagonal
  sweeping from −1.5 to +1.5: the umbra migrating pole to pole over ~1,250 years.

Pan, zoom, filter by eclipse type, and size the dots by central duration. Tap any
eclipse for its ground track, path width, maximum duration and time of greatest eclipse,
with the two previous returns of the same series ghosted behind it to show the ~115°
westward march.

**Saros machine** — a 223-cell spiral dial, the same layout the Antikythera mechanism
used. Its cells are 223 consecutive new moons: one saros. Because eclipses recur every
223 lunations, every eclipse of a given series lands on the same cell forever — saros 139
is always cell 77. Three panels beside it show the actual geometry: the Moon's position
relative to the nodes (*F*), its distance around the orbital ellipse (*M′*), and where
the shadow axis crosses Earth (*gamma*). Step forwards and backwards through a series
and watch gamma march across the globe while the dial pointer never moves.

## How it works

| Quantity | Method |
| --- | --- |
| Eclipse dates, type, gamma | Meeus, *Astronomical Algorithms*, ch. 49 and 54 |
| Saros series | `S ≡ 38(k − 44) mod 223`, branch chosen by epoch |
| Inex series | `I = (k − 44 − 358S)/223`, anchored on 2000 Feb 5 = inex 30 |
| Ground track | Sun→Moon axis intersected with the WGS-84 ellipsoid, via pyephem apparent positions and apparent sidereal time |
| TD → UT | Espenak–Meeus ΔT polynomials |
| Path width | Umbral cone radius at the surface / cosine of local incidence |
| Central duration | Cone diameter / shadow ground speed at greatest eclipse |
| Coastlines | Marching squares on a 30-arcsecond land raster, Douglas–Peucker simplified to 3,310 points |

The saros and inex numbers satisfy `k = 223·I + 358·S + 44`, so once one is fixed the
other follows exactly. It comes out an exact integer for all 11,898 eclipses, which is a
useful check on the whole scheme.

## Validation

Checked against published values:

| Eclipse | Computed | Published |
| --- | --- | --- |
| 2024 Apr 8 | saros 139, γ 0.343, 25.3°N 104.1°W, 200 km, 4m29s | γ 0.3431, 25.30/−104.13, 198 km, 4m28s |
| 2045 Aug 12 | saros 136, γ 0.211, 25.9°N 78.5°W, 257 km, 6m07s | γ 0.2116, 25.90/−78.50, 256 km, 6m06s |
| 2017 Aug 21 | saros 145, 36.95°N 87.60°W, 117 km, 2m42s | 36.97/−87.65, 115 km, 2m40s |
| 2186 Jul 16 | 7m32s (longest total of the era) | 7m29s |
| 2009 Jul 22 | 6m41s | 6m39s |

Distribution over the full canon: 35.3% partial, 33.3% annular, 26.9% total, 4.5% hybrid,
against Espenak's 35.3 / 33.2 / 26.7 / 4.8. Rate 2.38 eclipses per year. Saros series run
a median 72 eclipses over 1,280 years. Saros 136 starts 1360 and 145 runs 1639–3009, both
matching the published series limits.

Structural checks: inex series 30 steps 2000 Feb 5 → 2029 Jan 14 → 2057 Dec 26 in saros
150, 151, 152; saros 136 steps 1991 → 2009 → 2027 → 2045 in inex 52, 53, 54, 55. Over
1850–2300, 57 dial cells are occupied and none is shared between two series.

## Known limits

- **Ground tracks are drawn only for 1000–3000 CE.** Earlier than that the ΔT
  extrapolation is uncertain by many minutes, which smears a track's longitude across
  degrees. Durations do not depend on ΔT and run back to about 250 BCE, which is as far
  as the ephemeris reaches.
- Past ~2100 the ΔT projection shifts tracks east or west by tens of kilometres, growing
  with distance from now.
- Tracks are sampled at 13 points across a ~3¼-hour crossing, so the drawn line is a
  smooth interpolation. Path edges are not drawn — only the central line.
- Coastlines are deliberately coarse. Use them for orientation, not to judge whether a
  path clips a particular town.
- "Duration" means the central phase: totality for total eclipses, annularity for annular
  ones.

## Building

```bash
pip install -r requirements.txt
python src/build.py            # full canon, about 2 minutes
python src/build.py --quick    # 1800-2200 only, about 25 seconds
```

Writes `index.html` at the repo root. Open it directly — no server needed.

```
src/
  eclipses.py    Meeus ch.49/54; dates, type, gamma, saros, inex
  geometry.py    shadow axis, ground track, width, duration, delta-T
  coastlines.py  land raster to simplified polylines
  encode.py      base64-style packing
  template.py    the single-page app
  build.py       orchestrates the above
```

Each module runs standalone and prints its own validation:

```bash
python src/eclipses.py    # catalogue statistics and spot checks
python src/geometry.py    # tracks against published coordinates
```

## Publishing

Settings → Pages → deploy from `main`, folder `/ (root)`. `index.html` is at the root,
so no workflow is needed.

## Sources

Jean Meeus, *Astronomical Algorithms* (2nd ed.) for the lunation and eclipse machinery.
Fred Espenak's catalogues and the EclipseWise saros panoramas for the published values
checked against. Positions from [pyephem](https://rhodesmill.org/pyephem/); land raster
from [global-land-mask](https://pypi.org/project/global-land-mask/).

## Licence

Not yet chosen — add one before sharing widely. MIT is the usual choice for something
like this.
