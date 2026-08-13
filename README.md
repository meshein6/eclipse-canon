# Canon of Solar Eclipses

An interactive canon of every solar eclipse from 2000 BCE to 3000 CE — 11,898 of them —
plus a working model of the saros cycle that produces them.

Every eclipse quantity is computed from first principles. No eclipse catalogue is
downloaded or scraped — dates, types, gamma, saros and inex numbers, ground tracks,
path widths and durations all come out of lunar/solar theory plus a land raster.

Geography is the exception, and only geography: country and province borders come
from Natural Earth and populated places from GeoNames, purely as reference overlays
so a zoomed-in globe has recognisable landmarks. Nothing about the eclipses depends
on them. The whole thing still builds into a single self-contained HTML file that
makes no network requests at run time.

**[Live demo](https://meshein6.github.io/eclipse-canon/)**

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
eclipse for its ground track, path width, maximum duration and time of greatest eclipse.
On a wide screen the selected eclipse opens beside the canon; the canon returns to full
width when nothing is selected.

**Ground view** — tap the globe anywhere and you are standing there, looking up. The sky is
drawn from the topocentric Sun and Moon at whatever the clock says: the two discs at their
real sizes and separation, the sky dimming as the Moon eats into the Sun, the corona and
chromosphere at totality, the ring at annularity, the diamond ring either side of it, and
the stars coming out when it goes dark enough for them. Drag to look around, scroll to zoom
from a 120° sky down to half a degree, and the view tracks the Sun until you drag it away.
**W A S D** walks you a degree at a time — about the width of an umbral path, which is
usually the difference between totality and 98%. The bar underneath gives your local
circumstances: maximum obscuration and when, the length of totality or annularity, and
first to last contact. It says so when the Sun sets partway through, and when the eclipse
reaches you only after the Sun has gone down.

**Live** — when an eclipse is actually in progress, the masthead says so and one tap puts
you under the shadow with the clock following real time, on the globe and on the ground at
once. The rest of the time the chip counts down to the next eclipse.

**Eclipse viewer** — the selected eclipse on an orthographic globe, spinnable by drag and
zoomable to 120×. It shows the central path, the northern and southern limits of the
umbral path as dotted lines, a dotted line around everyone who sees any of the eclipse and
a solid one around everyone seeing it at that instant, the umbra itself at whatever the
time slider says, the day/night terminator with a twilight gradient, and the sub-solar
point. The central line is coloured by the local type, so a **hybrid** shows plainly where
it stops being annular and turns total and back again. Partial eclipses, which have no
track at all because the shadow axis misses Earth, get both zones like everything else.
Run the slider (or hit play) and the shadow crosses while the terminator and the
sun-overhead point move with it.

The slider spans the **whole event**, first to last penumbral contact, not just the umbra's
crossing — which is what gives a partial eclipse a clock to run, and what lets somebody
standing well off to one side of a total track watch their own partial phases begin before
the umbra has landed anywhere. The umbra appears partway along the slider and leaves before
the end. Play runs the lot in about 40 seconds, and the length of the central phase under
the umbra is shown live — it climbs from zero at the sunrise limit to the maximum at
greatest eclipse and back to zero at sunset. **Expand** gives it the whole pane. City pins fade in as you zoom,
in three tiers. The flat equirectangular map is still there under **Flat**, and that one
ghosts the two previous returns of the same series behind the current track to show the
~115° westward march.

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
| Central duration | Cone diameter / shadow ground speed, at each of the 13 sampled points |
| Day/night on the globe | Sun elevation per pixel from the same solar position and apparent sidereal time |
| Sun and Moon in the browser | Meeus ch.25 solar theory and the ch.47 truncated ELP-2000/82, with ch.22 nutation and Laskar's obliquity |
| The sky from the ground | Topocentric Sun and Moon against the WGS-84 observer vector; lunar parallax is over a degree, so this *is* the calculation |
| Magnitude and obscuration | Separation against the two apparent radii; obscuration is the circle–circle lens area |
| Contact times | The scan bisected on separation, and on the horizon, whichever ends the phase first |
| Event window | First and last penumbral contact, bisected on the cone radius against the globe |
| Star positions | 60 stars brighter than magnitude 2.2, precessed to date by Meeus ch.21 |
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

The browser's own Sun and Moon, which the ground view runs on, are checked separately.
Against pyephem at matched terrestrial time the Moon agrees to about 10 arcsec over
1000–2000 CE and 25 arcsec over the rest of the canon, the Sun to about 25 arcsec
throughout — all of it far inside the half-degree discs being drawn. The local
circumstances that come out of it:

| Where and when | Computed | Published |
| --- | --- | --- |
| 2024 Apr 8, whole event on Earth | 15:43–20:53 UT | 15:42–20:52 UT |
| 2024 Apr 8 at greatest eclipse | 4m28s totality | 4m28s |
| 2017 Aug 21, Hopkinsville KY | 2m42s totality | 2m40s |
| 2027 Aug 2 at greatest eclipse | 6m24s totality | 6m23s |
| 2027 Feb 6, annular centre line | 7m48s annularity | 7m51s |
| 2022 Apr 30, whole event on Earth | 18:44–22:38 UT | 18:45–22:37 UT |

Two cross-checks that share no code with the ground view: over a sample spanning the whole
canon, the magnitude it computes at greatest eclipse for a partial matches the catalogue's
own Meeus ch.54 value to within 0.024, and every central eclipse it is given comes out
central — total ones reaching 100% obscuration, annular ones stopping at the ring, and only
eclipses sitting exactly on the total/annular boundary disagreeing about which they are.

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
  smooth interpolation. The path limits are the per-point umbral width laid off
  perpendicular to the track, which ignores the tilt of the shadow ellipse — good to a
  few kilometres near greatest eclipse, rougher towards the ends.
- Near the sunrise and sunset ends of a track the shadow axis grazes the surface and the
  computed width diverges, so the incidence cosine is floored at 0.15. Widths within a few
  hundred kilometres of either end are indicative only.
- Coastlines are 0.1° (about 11 km), country lines are simplified to 0.02° and province
  lines to 0.05°, so at high zoom the geography is coarser than the eclipse path drawn
  over it. Use it for orientation, not to judge whether a path clips a particular town.
- The partial-eclipse zones are the penumbral cylinder cut against a **spherical** Earth:
  the solid one at the instant the clock is showing, the dotted one the union of those
  across the whole event. The union is traced by sweeping azimuths out from the
  most-eclipsed point, which assumes the region is star-shaped about it — true of the lens
  shape these actually take.
- The ground view and the ground tracks come from two different ephemerides: the tracks
  were computed once with pyephem and packed into the page, the sky is computed live from
  the Meeus series. They agree to a few tens of kilometres, so within a couple of hundred
  metres of a path limit the globe and the sky can disagree about whether you just catch
  totality. Everywhere else the difference is invisible.
- The sky is arcseconds-honest from about 1600 to 2400 CE and good to tens of arcsec across
  1000–3000. Before that it is notional in the same way the tracks are: at 2000 BCE ΔT
  itself is uncertain by half an hour, which is thousands of kilometres of shadow.
- Stars are precessed but not given proper motion, which is a degree or so of error at the
  far ends of the canon for the fastest of them. There are no planets, so the Venus that
  people remember from totality is missing.
- The sky's brightness is a plausible curve, not photometry. It tracks the uncovered area
  of the disc until the last three per cent and then falls off a cliff, which is the right
  shape and roughly the right depth.
- "Duration" means the central phase: totality for total eclipses, annularity for annular
  ones.

## Building

```bash
pip install -r requirements.txt
python src/mapdata.py --fetch  # borders and places, ~11 MB, cached in data/
python src/build.py            # full canon, about 20 seconds
python src/build.py --quick    # 1800-2200 only, faster still
```

`build.py` fetches the map data itself on first run if `data/` is empty, so the
explicit fetch is only there if you would rather do it deliberately.

Writes `index.html` at the repo root. Open it directly — no server needed.

Editing the page itself does not change any of that packed data, so there is a shortcut
for it:

```bash
python src/relink.py           # pull the data back out of index.html, re-emit through the template
```

Seconds instead of minutes, and it needs neither pyephem nor the downloads.

```
src/
  eclipses.py    Meeus ch.49/54; dates, type, gamma, saros, inex
  geometry.py    shadow axis, ground track, per-point width/duration/type, penumbra, delta-T
  coastlines.py  land raster to simplified polylines
  mapdata.py     downloads and simplifies borders and populated places
  encode.py      base64-style packing
  template.py    the single-page app, including its own Sun and Moon
  build.py       orchestrates the above
  relink.py      rebuilds the page from an existing build's data
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

Country and province borders from [Natural Earth](https://www.naturalearthdata.com/)
(public domain). Populated places from [GeoNames](https://www.geonames.org/), licensed
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Jean Meeus, *Astronomical Algorithms* (2nd ed.) for the lunation and eclipse machinery,
and for the Sun and Moon the page carries with it. Fred Espenak's catalogues and the
EclipseWise saros panoramas for the published values checked against. Build-time positions
from [pyephem](https://rhodesmill.org/pyephem/); land raster from
[global-land-mask](https://pypi.org/project/global-land-mask/). Bright-star coordinates are
the standard J2000 catalogue positions, precessed in the page.

## Licence

MIT — see [LICENSE](LICENSE).
