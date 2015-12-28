# -*- coding: utf-8 -*-
"""yet some more code snippets named after the ancient city of `Thebes <https://en.wikipedia.org/wiki/Thebes,_Greece>`_
"""

import re
from Hellas.Sparta import chunks_str


def format_header(frmt):
    """creates a header string from a new style format string useful when printing dictionaries

    :param str frmt: a new style format string
    :returns: a table header string

    assumptions for frmt specs:
        - all have a separator = '|' and include a key size format directive i.e.: '{key:size}'
        - no other character allowed in frmt except separator

    :Example:
        >>> frmt = '|{count:12,d}|{percent:7.2f}|{depth:5d}|'
        >>> data_dict = {'count': 100, 'percent': 10.5, 'depth': 10}
        >>> print(format_header(frmt)); print(frmt.format(**data_dict))
        ............................
        |   count    |percent|depth|
        ............................
        |         100|  10.50|   10|

    """
    names = re.sub("{(.*?):.*?}", r"\1", frmt)
    names = [i for i in names.split("|") if i]
    frmt_clean = re.sub("\.\df", r"", frmt)  # get read of floats i.e {:8.2f}
    sizes = re.findall(r'\d+', frmt_clean)
    frmt_header = "|{{:^{}}}" * len(sizes) + "|"
    header_frmt = frmt_header.format(*sizes)
    header = header_frmt.format(*names)
    header_len = len(header)
    header = "{}\n{}\n{}\n".format("." * header_len, header, "." * header_len)
    return header.strip()


def chunks_str_frame(a_str, n=None, center=True):
    """places a frame around a string
    :Parameters:
        - a_str: string to frame
        - n: number of chars in each line
        - center: center string in frame if True and n > len(str)

    :Example:
        >>> print(chunks_str_frame('the quick brown fox', 44))
        ╔════════════════════════════════════════════╗
        ║            the quick brown fox             ║
        ╚════════════════════════════════════════════╝
        >>> print(chunks_str_frame('the quick brown fox',12, False))
        ╔════════════╗
        ║the quick br║
        ║own fox     ║
        ╚════════════╝
    """
    if n is None:
        n = len(a_str)
    elif n > len(a_str) and center is True:
        a_str = a_str.center(n)
    spcs = "" if n == 1 or n == len(a_str) else " " * (n - (len(a_str) % n))
    n = len(a_str) if n is None else n
    r = chunks_str(a_str, n, "║\n║")
    return "╔{}╗\n║{}{}║\n╚{}╝".format('═' * n, r, spcs, '═' * n)