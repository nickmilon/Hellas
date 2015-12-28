"""This module contains only scientific functions and it is named after the ancient city of
`Athens <https://en.wikipedia.org/wiki/History_of_Athens#Origins_and_early_history>`_
`and Athena the godness of science <https://en.wikipedia.org/wiki/Athena>`_
"""

import math


def ngrams(slice_able, n):
    """produces ngram of an object
    :param obj slice_able: any slicable object i.e string list etc
    :param int n: n-th grams

    :Returns: an iterator of ngram tuples 
              (actually returns a list in Python 2.7) but always treat it as iterator for python 3+ compatibility)

    :Example:
        >>> ngrams("The quick brown fox jumps over the lazy dog", 2)
        [('T', 'h'), ('h', 'e'), ('e', ' '), (' ', 'q'), ('q', 'u'), ('u', 'i'), ('i', 'c') .... ]

    .. seealso:: :func:`bigrams`
    """
    return zip(*[slice_able[i:] for i in range(n)])


def bigrams(slice_able):
    """produces bigrams same as ngrams (x, 2) but more efficient

    :Returns: an iterator of bigram tuples
              (actually returns a list in Python 2.7) but always treat it as iterator for python 3+ compatibility)

     .. seealso:: :func:`ngrams`
    """
    return zip(slice_able, slice_able[1:])


def haversine(lon1, lat1, lon2, lat2):
    """Calculate the great circle distance between two points on earth in Kilometers
    on the earth (specified in decimal degrees)

    .. seealso:: :func:`distance_points`

    :param float lon1: longitude of first place (decimal degrees)
    :param float lat1: latitude of first place (decimal degrees)
    :param float lon2: longitude of second place (decimal degrees)
    :param float lat2: latitude of second place (decimal degrees)

    :Example:
        >>> London_long=-0.126 ; London_lat=51.50; Paris_long = 2.350; Paris_lat = 48.856
        >>> haversine(London_long, London_lat, Paris_long, Paris_lat)
        342.55375272454864

    :returns: float distance in Kilometers

    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = list(map(math.radians, [lon1, lat1, lon2, lat2]))
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km


def distance_points(point1, point2):
    """just a wrapper for :func:`haversine`

    :param tuple_or_list point1: (longitude, latitude)  in decimal degrees
    :param tuple_or_list point2: (longitude, latitude)  in decimal degrees

    :Example:
        >>> London = (-0.1262, 51.50,); Paris = (2.350, 48.856)
        >>> distance_points(London, Paris)
        342.55
    """
    return haversine(point1[0], point1[1], point2[0], point2[1])


def bit_set(offset, int_tp=0):
    """sets bit of int_tp at offset to 1

    :param int offset: position offset
    :param int int_tp: original integer or long (defaults to 0)
    :returns: a new int or long

    :Example:
        >>> bit_set(2)
        4
        >>> bit_set(2,4)
        4                            # because bit already set
        >>> bin(bit_set(16))
        '0b10000000000000000'
    """
    return(int_tp | 1 << offset)


def bits_count(int_tp):
    """counts all bits set to 1 in int_tp

    :Example: 
        >>> bits_count(1234567)
        11
    """
    return bin(int_tp).count("1")
 
    