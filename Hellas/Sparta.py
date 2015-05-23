'''**Defines very basic constants, classes and methods named after `Sparta  **
we keep this module simple and laconic
No imports in this module
'''

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

# other formats
FMT_INT_SEP = "{:,d}"                      # integer with comma separator every 3 digits


def seconds_to_DHMS(seconds, asStr=True):
    '''| seconds to Days, Hours, Minutes, Seconds
       | useful to display program run time etc...

    :Args: 
      - seconds (int)
        - AsStr (bool) if True returns a formated string else dictionary
    '''
    d = DotDot()
    d.days = int(seconds // (3600 * 24))
    d.hours = int((seconds // 3600) % 24)
    d.minutes = int((seconds // 60) % 60)
    d.seconds = int(seconds % 60)
    return FMT_DHMS_DICT.format(**d) if asStr else d


class Error(Exception):
    pass


class DotDot(dict):
    '''A dictionary with dot notation
        example dd=DotDot()
        dd.a=1
        dd.a ==>> 1
    '''
    def prnt(self):
        for k, v in list(self.items()):
            print ((k, v))

    def __getattr__(self, attr):
        try:
            item = self[attr]
        except KeyError as e:
            raise AttributeError(e)    # expected Error by pickle on __getstate__ etc
        if isinstance(item, dict) and not isinstance(item, DotDot):
            item = DotDot(item)
        return item
    # def __getstate__(self): return self.__dict__
    # def __setstate__(self, d): self.__dict__.update(d)
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


class AdHocTree(object):
    """ builds an arbitrary tree structure using object attributes
        example:
            aht= tps.AdHocTree().foo.bar
            aht ==> <AdHocTree: bar/foo/root>
        can be extended
        newtree=aht.foo.new_foo
        newtree ==>> <AdHocTree: new_foo/foo/bar/foo/root>
    """
    _slots__ = ['parent', 'name']

    def __init__(self, parent=None, name="root"):
        """ Args:parent any object instance
                :name (str) name of toplevel Node
        """
        self.parent = parent
        self.name = name

    def __call__(self, *args, **kwargs):
        """ calls _adHocCmd_ method on root's parent if exists
        """
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
        """it is pickl-able"""
        return (self.__class__, (self.parent, self.name))

    def __iter__(self):
        """ iterates breadth-first up to root """
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
        rt = ""
        for i in reversed(self):
            rt = "%s%s%s" % (rt, i.name, separator)
        return rt[:-1]

    def root_and_path(self):
        rt = []
        curAttr = self
        while isinstance(curAttr.parent, AdHocTree) or curAttr.parent is None:
            rt.append(curAttr.name)
            curAttr = curAttr.parent
        rt.reverse()
        return (curAttr.parent, rt)
