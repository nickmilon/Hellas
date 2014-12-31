'''
Created on Dec 4, 2014

@author: nickmilon
'''
import zlib
import cPickle as pickle


def pickle_compress(obj, print_compression_info=False):
    """ pickle and compress
    """
    p = pickle.dumps(obj)
    c = zlib.compress(p)
    if print_compression_info:
        print "len = {:,d} compr={:,d} ratio:{:.6f}".format(len(p), len(c), float(len(c))/len(p))
    return c


def pickle_decompress(obj):
    """ decompress  pickle_compress object
    """
    return pickle.loads(zlib.decompress(obj))


def pickle_compress_test(obj):
    cm = pickle_compress(obj, True)
    dc = pickle_decompress(cm)
    assert (dc == obj)


def pickle_compress_str(obj, print_compression_info=False):
    """ str gets better compression ration """
    return pickle_compress(str(obj), print_compression_info)


def pickle_decompress_str(obj):
    """ decompress pickle_compressed as str
    """
    return eval(pickle_decompress_str(obj))
