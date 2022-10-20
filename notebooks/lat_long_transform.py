import numpy as np
import pandas as pd
from math import cos, radians


def get_lat_offset(distance_in_m):
    offset = distance_in_m / 111111
    return offset


def get_lng_offset(distance_in_m, lat):
    offset = distance_in_m / (111111 * cos(radians(lat)))
    return offset


def get_bounding_square(lat, lng, side):
    lat_offset = get_lat_offset(side / 2)
    lng_offset = get_lng_offset(side / 2, lat)

    top_lat = lat + lat_offset
    bottom_lat = lat - lat_offset

    right_lng = lng + lng_offset
    left_lng = lng - lng_offset

    return top_lat, bottom_lat, right_lng, left_lng


def get_average_price_psf_within_bbox(lat, lng, bbox_side, df):
    bbox = get_bounding_square(lat, lng, bbox_side)
    filtered_df = df[(df.lat < bbox[0]) & (df.lat > bbox[1]) & (df.lng < bbox[2]) & (df.lng > bbox[3])]
    
    return filtered_df['price_per_sq_ft'].mean().astype(np.int32)


'''
Doesn't return anything - adds a column with `new_column_name` to the input_df. size is side of square drawn on the property in metres.
'''

def add_price_psf_from_lat_long(input_df, new_column_name='price_psf_lat_lng', size = 1000):
    df = input_df.copy(deep=True)
    df = df[df.price > 0]
    df = df[df.lat<=1.47]
    df = df[df.size_sqft>0]
    df['price_per_sq_ft'] = df['price']/df['size_sqft']
    df['price_per_sq_ft'] = df['price_per_sq_ft'].astype(np.int32)
    input_df[new_column_name] = df.apply(lambda x: get_average_price_psf_within_bbox(x['lat'], x['lng'], size, df), axis=1)