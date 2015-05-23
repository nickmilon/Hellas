'''
Created on Dec 10, 2014

@author: nickmilon
scientific stuff here only as Athens was the mother of science
'''
import math


def ngrams(slice_able, n):
    """ Args:
            slice_able any sliceble object i.e string list etc.
            n gram
            returns a list of ngram tuples
    """
    return zip(*[slice_able[i:] for i in range(n)])


def bigrams(slice_able):
    """ (see ngrams) just for efficiency
    """
    return zip(slice_able, slice_able[1:])


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points in kmeters
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km


def distance_points(point1, point2):
    '''
    :Args:
        - point1: list or tuple (Longitude, Latitude)
        - point2: list or tuple (Longitude, Latitude)
    '''
    return haversine(point1[0], point1[1], point2[0], point2[1])
