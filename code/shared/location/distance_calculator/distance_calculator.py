from math import sin, cos, sqrt, atan2, radians

# Approximate radius of earth in km
R = 6373.0


def calc_distance_km(c1: tuple[float, float], c2: tuple[float, float]) -> float:
    """
    Calculate distance between two gps coordinates in meters.
    Coordinates should be in the form of (latitude, longitude).
    """
    if not isinstance(c1, tuple) or not isinstance(c2, tuple):
        raise TypeError("Coordinates should be tuples")

    if len(c1) != 2 or len(c2) != 2:
        raise TypeError("Coordinates should be tuples of length 2")

    lat1 = radians(c1[0])
    lon1 = radians(c1[1])
    lat2 = radians(c2[0])
    lon2 = radians(c2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance_km = R * c

    return distance_km
