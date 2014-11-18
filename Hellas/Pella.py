'''
Created on Nov 15, 2007

@author: nickmilon
'''


from base64 import b64encode
from Hellas.Sparta import Error


class FileTooBig(Error):
    pass


def file_to_base64(path_or_obj, max_mb=None):
    """ converts contents of a file to base64 encoding
        Args:path_or_obj fool pathname or a file like object that supports read
            :max_mb maximum number in MegaBytes to accept
        Raises:FileTooBig if file contents > max_bt
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
            raise FileTooBig("File is too big ({.2f} MBytes)" (len_mb))
    return b64encode(rt)
