"""Reference city pins for orientation on the globe.

Unlike everything else in this project, this table is not computed — it is a
hardcoded list of well-known places so that a zoomed-in globe has something
recognisable on it. Coordinates are city-centre approximations, good to a
few kilometres, which is well inside the resolution of the coastlines they
are drawn over. There is no country-border data anywhere in this project;
the only geographic input is a land/sea raster.
"""
import json

# Tier controls when a pin appears: 1 is drawn as soon as pins switch on,
# 2 and 3 fade in as you keep zooming.
TIER1 = {
    "London", "Paris", "Madrid", "Berlin", "Rome", "Moscow", "Istanbul", "Cairo",
    "Lagos", "Nairobi", "Johannesburg", "Tehran", "Dubai", "Delhi", "Mumbai",
    "Bangkok", "Jakarta", "Singapore", "Hong Kong", "Shanghai", "Beijing", "Seoul",
    "Tokyo", "Sydney", "Los Angeles", "Chicago", "Toronto", "New York",
    "Mexico City", "Lima", "Buenos Aires", "Sao Paulo", "Honolulu",
}
TIER3 = {
    "Zurich", "Oslo", "Helsinki", "Warsaw", "Kyiv", "Athens", "Reykjavik", "Nuuk",
    "Tunis", "Tripoli", "Dakar", "Accra", "Luanda", "Khartoum", "Colombo",
    "Kathmandu", "Ulaanbaatar", "Novosibirsk", "Vladivostok", "Almaty", "Tashkent",
    "Osaka", "Darwin", "Brisbane", "Wellington", "Suva", "Port Moresby", "Papeete",
    "Anchorage", "Denver", "Dallas", "Montreal", "Washington", "Mazatlan",
    "Havana", "Santiago", "Rio de Janeiro", "Perth", "Taipei", "Hanoi",
}

# name, lon, lat
CITIES = [
    ("London", -0.13, 51.51), ("Paris", 2.35, 48.86), ("Madrid", -3.70, 40.42),
    ("Lisbon", -9.14, 38.72), ("Dublin", -6.26, 53.35), ("Berlin", 13.40, 52.52),
    ("Rome", 12.50, 41.90), ("Vienna", 16.37, 48.21), ("Zurich", 8.54, 47.38),
    ("Oslo", 10.75, 59.91), ("Stockholm", 18.07, 59.33), ("Helsinki", 24.94, 60.17),
    ("Warsaw", 21.01, 52.23), ("Kyiv", 30.52, 50.45), ("Athens", 23.73, 37.98),
    ("Istanbul", 28.98, 41.01), ("Moscow", 37.62, 55.76), ("Reykjavik", -21.94, 64.15),
    ("Cairo", 31.24, 30.04), ("Algiers", 3.06, 36.75), ("Tunis", 10.18, 36.81),
    ("Tripoli", 13.19, 32.89), ("Casablanca", -7.59, 33.57), ("Dakar", -17.47, 14.72),
    ("Accra", -0.19, 5.60), ("Lagos", 3.38, 6.52), ("Kinshasa", 15.31, -4.32),
    ("Luanda", 13.23, -8.84), ("Khartoum", 32.56, 15.50), ("Addis Ababa", 38.74, 9.03),
    ("Nairobi", 36.82, -1.29), ("Johannesburg", 28.05, -26.20), ("Cape Town", 18.42, -33.92),
    ("Riyadh", 46.68, 24.71), ("Dubai", 55.27, 25.20), ("Baghdad", 44.37, 33.31),
    ("Tehran", 51.39, 35.69), ("Tashkent", 69.24, 41.30), ("Almaty", 76.89, 43.24),
    ("Karachi", 67.01, 24.86), ("Delhi", 77.21, 28.61), ("Mumbai", 72.88, 19.08),
    ("Chennai", 80.27, 13.08), ("Kolkata", 88.36, 22.57), ("Colombo", 79.86, 6.93),
    ("Kathmandu", 85.32, 27.72), ("Dhaka", 90.41, 23.81), ("Bangkok", 100.50, 13.76),
    ("Hanoi", 105.85, 21.03), ("Kuala Lumpur", 101.69, 3.14), ("Singapore", 103.82, 1.35),
    ("Jakarta", 106.85, -6.21), ("Manila", 120.98, 14.60), ("Hong Kong", 114.17, 22.32),
    ("Taipei", 121.57, 25.03), ("Shanghai", 121.47, 31.23), ("Beijing", 116.41, 39.90),
    ("Ulaanbaatar", 106.91, 47.89), ("Novosibirsk", 82.92, 55.03), ("Vladivostok", 131.89, 43.12),
    ("Seoul", 126.98, 37.57), ("Tokyo", 139.65, 35.68), ("Osaka", 135.50, 34.69),
    ("Perth", 115.86, -31.95), ("Darwin", 130.84, -12.46), ("Brisbane", 153.03, -27.47),
    ("Sydney", 151.21, -33.87), ("Melbourne", 144.96, -37.81), ("Auckland", 174.76, -36.85),
    ("Wellington", 174.78, -41.29), ("Suva", 178.44, -18.14), ("Port Moresby", 147.18, -9.44),
    ("Honolulu", -157.86, 21.31), ("Papeete", -149.57, -17.54), ("Anchorage", -149.90, 61.22),
    ("Nuuk", -51.69, 64.18), ("Vancouver", -123.12, 49.28), ("Seattle", -122.33, 47.61),
    ("San Francisco", -122.42, 37.77), ("Los Angeles", -118.24, 34.05), ("Denver", -104.99, 39.74),
    ("Dallas", -96.80, 32.78), ("Chicago", -87.63, 41.88), ("Toronto", -79.38, 43.65),
    ("Montreal", -73.57, 45.50), ("New York", -74.01, 40.71), ("Washington", -77.04, 38.91),
    ("Miami", -80.19, 25.77), ("Mexico City", -99.13, 19.43), ("Mazatlan", -106.41, 23.25),
    ("Havana", -82.37, 23.11), ("Bogota", -74.07, 4.71), ("Lima", -77.04, -12.05),
    ("Santiago", -70.67, -33.45), ("Buenos Aires", -58.38, -34.60), ("Sao Paulo", -46.63, -23.55),
    ("Rio de Janeiro", -43.17, -22.91),
]


def tier(name):
    return 1 if name in TIER1 else 3 if name in TIER3 else 2


def pack():
    """A compact JS array literal: [["name",lon,lat,tier],...]"""
    return json.dumps([[n, round(lo, 2), round(la, 2), tier(n)] for n, lo, la in CITIES],
                      separators=(",", ":"))


if __name__ == '__main__':
    from collections import Counter
    print(len(CITIES), 'cities,', len(pack()), 'chars,',
          dict(sorted(Counter(tier(n) for n, _, _ in CITIES).items())))
