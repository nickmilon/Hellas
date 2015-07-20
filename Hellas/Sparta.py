"""Defines very basic constants, classes and methods named after `Sparta <https://en.wikipedia.org/wiki/Sparta>`_ .
We keep this module simple and  `Laconic <https://en.wikipedia.org/wiki/Laconic_phrase>`_   so No imports in this module
"""

# Date - Time formats
FMT_HTTP_DATE = "%a, %d %b %Y %H:%M:%S GMT"
FMT_RFC_2822_DATE_FMT = "%a, %d %b %Y %H:%M:%S +0000"
FMT_DT_GENERIC = "%y%m%d %H:%M:%S"        # generic date time format
FMT_T_GENERIC = "%H:%M:%S"                # generic date format
FMT_DT_COMPR = "%y%m%d%H%M%S%f%V%u"       # compressed date+time+milliseconds + weekday + weeknumber
FMT_DT_COMPR_SI = "%y%m%d%H%M%S%V%u"      # compressed date+time+weekday + weeknumber
FMT_DT_COMPR_S = "%y%m%d%H%M%S"           # compressed up to seconds
FMT_DT_COMPR_M = "%y%m%d%H%M"             # compressed up to minute
FMT_DT_COMPR_H = "%y%m%d%H"               # compressed up to Hour
FMT_DHMS_DICT = "{days:03d}-{hours:02d}:{minutes:02d}:{seconds:02d}"
from Hellas import _IS_PY2
# other formats
FMT_INT_SEP = "{:,d}"                      # integer with comma separator every 3 digits


def seconds_to_DHMS(seconds, as_str=True):
    """converts seconds to Days, Hours, Minutes, Seconds

    :param int seconds: number of seconds
    :param bool as_string: to return a formated string defaults to True
    :returns: a formated string if as_str else a dictionary
    :Example:
        >>> seconds_to_DHMS(60*60*24)
        001-00:00:00
        >>> seconds_to_DHMS(60*60*24, False)
        {'hours': 0, 'seconds': 0, 'minutes': 0, 'days': 1}
    """
    d = DotDot()
    d.days = int(seconds // (3600 * 24))
    d.hours = int((seconds // 3600) % 24)
    d.minutes = int((seconds // 60) % 60)
    d.seconds = int(seconds % 60)
    return FMT_DHMS_DICT.format(**d) if as_str else d


class Error(Exception):
    pass


class DotDot(dict):
    """
    A dictionary that can handle dot notation to access its members (useful when parsing JSON content),
    although it can perform write operations using dot notation on single level dictionary its mainly use is for reads
    also to keep casting to it cheap it doesn't handle creating multilevel keys using dot notation.
    For this functionality look for `easydict <https://github.com/makinacorpus/easydict>`_
    or `addict <https://github.com/mewwts/addict>`_

    :Example:
        >>> dd = DotDot()
        >>> dd.a = 1
        >>> dd
        {'a': 1}
        >>> dd.b.c = 100
        'AttributeError ...  '
        >>> dd.b = {'b1': 21, 'b2': 22}
        >>> dd.b.b3 = 23
        >>> dd
        {'a': 1, 'b': {'b1': 21, 'b2': 22}, 'b3': 23}

    .. Warning:: don't use for write operations on a nested key using dot notation
       i.e: `del dd.a.b` or  dd.a.b = 1  or dd.a.b +=1 **(it will fail silently !)**
    """
    def __getattr__(self, attr):
        try:
            item = self[attr]
        except KeyError as e:
            raise AttributeError(e)    # expected Error by pickle on __getstate__ etc
        if isinstance(item, dict) and not isinstance(item, DotDot):
            item = DotDot(item)
        return item
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class DictDK(dict):
    '''a dictionary with a single predefined key
    subclasses can redefine the key as:
    >>> class FOO (DictDK):
    >>>     key = 'bar'
    or create an instance with new default key:
    >>> f = type('FOO', (DictDK,), dict(key='foo'))
    '''
    key = ''

    def __init__(self, val):
        super(DictDK, self).__init__([(self.key, val)])


def dict_encode(in_dict):
    """returns a new dictionary with encoded values useful for encoding http queries (python < 3)"""
    if _IS_PY2:
        out_dict = {}
        for k, v in list(in_dict.items()):
            if isinstance(v, unicode):
                v = v.encode('utf8')
            elif isinstance(v, str):
                # Must be encoded in UTF-8
                v.decode('utf8')
            out_dict[k] = v
        return out_dict
    else:
        raise NotImplementedError


class AdHocTree(object):
    """builds an arbitrary tree structure using object attributes

    :Usage:
        >>> aht = AdHocTree().foo.bar
        >>> aht
        <AdHocTree: root/foo/bar>
            - can be extended:
        >>> newtree = newtree = aht.new_foo.new_bar
        >>> newtree
        <AdHocTree: root/foo/bar/new_foo/new_bar>
    """

    __slots__ = ['parent', 'name']  # don't create __dict__ just those 2 slots

    def __init__(self, parent=None, name="root"):
        """
        :param obj parent: parent object, defaults to None
        :param str name: name of the Tree, defaults to root
        """
        self.parent = parent
        self.name = name

    def __call__(self, *args, **kwargs):
        """calls _adHocCmd_ method on root's parent if exists"""
        elements = list(self)
        try:
            cmd = elements[-1].parent.__getattribute__('_adHocCmd_')
            # we don't use get or getattr here to avoid circular references
        except AttributeError:
            raise NotImplementedError("_adHocCmd_ {:!s}".format((type(elements[-1].parent))))
        return cmd(elements[0], *args, **kwargs)

    def __getattr__(self, attr):
        return AdHocTree(self, attr)

    def __reduce__(self):
        """its pickle-able"""
        return (self.__class__, (self.parent, self.name))

    def __iter__(self):
        """iterates breadth-first up to root"""
        curAttr = self
        while isinstance(curAttr, AdHocTree):
            yield curAttr
            curAttr = curAttr.parent

    def __reversed__(self):
        return reversed(list(self))

    def __str__(self, separator="/"):
        return self.path()

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.path())

    def path(self, separator="/"):
        """:returns: a string representing the path to root element separated by separator"""
        rt = ""
        for i in reversed(self):
            rt = "{}{}{}".format(rt, i.name, separator)
        return rt[:-1]

    def root_and_path(self):
        """:returns: a tuple (parent, [members,... ]"""
        rt = []
        curAttr = self
        while isinstance(curAttr.parent, AdHocTree):
            rt.append(curAttr.name)
            curAttr = curAttr.parent
        rt.reverse()
        return (curAttr.parent, rt)


def relations_dict(rel_lst):
    """constructs a relation's dictionary from a list that describes amphidromus relations between objects

    :param list rel_lst: a relationships list of the form [[a,b],[c, a, b]]  # can include duplicates
    :returns: a dictionary

    :Example:
        >>> rl = [('a', 'b', 'c'), ('a', 'x', 'y'), ('x', 'y', 'z')]
        >>> relations_dict(rl)
        {'a': ['x', 'c', 'b', 'y'], 'c': ['a', 'b'], 'b': ['a', 'c'], 'y': ['a', 'x', 'z'], 'x': ['a', 'z', 'y'],
         'z': ['y', 'x']}
    """
    dc = {}
    for c in rel_lst:
        for i in c:
            for k in c:
                dc.setdefault(i, [])
                dc[i].append(k)
    do = {}
    for k in list(dc.keys()):
        if dc[k]:
            vl = list(set(dc[k]))   # remove duplicates
            vl.remove(k)
            do[k] = vl
    return do