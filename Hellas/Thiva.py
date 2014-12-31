'''
Created on Dec 17, 2014

@author: nickmilon
'''

import re


def format_header(frmt):
    """ Returns a header string for a new style format string
        Args: frmt (str) a new style format string i.e: '|{cnt:12,d}|{percent:7.2f}|{depth:5d}|'
        assumptions for frmt specs:
             all have a separator = '|' and include a key size |{key:size}|
             no other char allowed in frmt except separator
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
