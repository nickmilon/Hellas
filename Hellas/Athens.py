'''
Created on Dec 10, 2014

@author: nickmilon
scientific stuff here only as Athens was the mother of science
'''


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
