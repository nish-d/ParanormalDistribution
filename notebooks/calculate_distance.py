# This file consists of methods to calculate the distance between each property and the closest mrt station,
# as well as number of mrt stations within a 200m radius. This distance can be changed in order to have a better
# fit with our data,

import geopy.distance


def calculate_distance(p1, p2):
    return geopy.distance.geodesic(p1, p2)


