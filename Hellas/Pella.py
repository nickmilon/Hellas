'''
Created on Nov 15, 2007

@author: nickmilon
'''

from copy import copy
import signal
from base64 import b64encode
from random import random
from Hellas.Sparta import Error


class ErrorFileTooBig(Error):
    pass


# file operations -------------------------------------------------------------
def file_to_base64(path_or_obj, max_mb=None):
    """ converts contents of a file to base64 encoding
        Args:path_or_obj fool pathname or a file like object that supports read
            :max_mb maximum number in MegaBytes to accept
        Raises:ErrorFileTooBig if file contents > max_bt
               IOError: if file path can't be found
               Also possible other exceptions depending on file_object
    """
    def read_file():
        with open(path_or_obj, 'rb') as fin:
            return fin.read()
    if not hasattr(path_or_obj, 'read'):
        rt = read_file()
    else:
        rt = path_or_obj.read()
    if max_mb:
        len_mb = len(rt) / (10024.0 * 1000)
        if len_mb > max_mb:
            raise ErrorFileTooBig("File is too big ({.2f} MBytes)" (len_mb))
    return b64encode(rt)


# dictionary operations -------------------------------------------------------
def dict_copy(a_dict, exclude_keys_lst=None, exclude_values_lst=None):
    """ a SALLOW copy of a dict excluding items in exclude_keys_lst
        and exclude_values_lst
        useful for copying locals etc... remember it is NOT a deep copy
    """
    if exclude_keys_lst is None:
        exclude_keys_lst = list()
    if exclude_values_lst is None:
        exclude_values_lst = list()
    return dict([copy(i) for i in a_dict.items()
                 if i[0] not in exclude_keys_lst and i[1] not in exclude_values_lst])


def dict_clip(a_dict, inlude_keys_lst):
    return dict([[i[0], i[1]] for i in a_dict.items() if i[0] in inlude_keys_lst])


# list operations -------------------------------------------------------------
def list_randomize(lst):
    "returns list in random order"
    return sorted(lst, key=lambda x: random())


def list_pp(ll, separator='|', header_line=True, autonumber=True):
    if autonumber:
        for cnt, i in enumerate(ll):
            i.insert(0, cnt if cnt > 0 or not header_line else '#')

    def lenlst(l):
        return [len(str(i)) for i in l]

    lst_len = [lenlst(i) for i in ll]
    lst_rot = zip(*lst_len[::-1])
    lst_len = [max(i) for i in lst_rot]
    frmt = separator + separator.join(["{!s:"+str(i)+"}" for i in lst_len]) + separator
    if header_line:
        header_line = '-' * len(frmt.format(*ll[0]))
    for cnt, l in enumerate(ll):
        if cnt < 2 and header_line:
            print header_line
        print frmt.format(*l)
    if header_line:
        print header_line
    return lst_len

# signal -----------------------------------------------------------------------
def signal_terminate(on_terminate):
        for i in [signal.SIGINT, signal.SIGHUP, signal.SIGUSR1, signal.SIGUSR2, signal.SIGTERM]:
            signal.signal(i, on_terminate)


# classes -----------------------------------------------------------------------
class Base62(object):
    """unsigned integer coder codes to and from base 62
    """
    symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    numeric_symbols = symbols[:10]

    def __repr__(self):
        return "<base62: (%s)>" % (self.symbols)

    @staticmethod
    def _code(number, from_digits, to_digits):
        x = 0
        len_from_digits = len(from_digits)
        len_to_digits = len(to_digits)
        for ch in str(number):
            x = x * len_from_digits + from_digits.index(ch)
        if x == 0:
            res = to_digits[0]
        else:
            res = ''
            while x > 0:
                digit = x % len_to_digits
                res = to_digits[digit] + res
                x = int(x // len_to_digits)
        return res

    @classmethod
    def encode(cls, number):
        return cls._code(number, cls.numeric_symbols, cls.symbols)

    @classmethod
    def decode(cls, number):
        return cls._code(number, cls.symbols, cls.numeric_symbols)
