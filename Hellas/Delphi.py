'''
Created on Nov 19, 2009

Delphi ( http://en.wikipedia.org/wiki/Delphi )
is a famous city in Greece where Oracle of Delphi was located

@author: nickmilon
'''
from __future__ import print_function
from __future__ import unicode_literals
from Hellas.Sparta import DotDot


class Color(object):
    """ This will NOT work on windows unless import colorama colorama.init()
        some basic color handling for printing in color
        br=bright _dk=dark
        usage:>>> cl = Color()
              >>> cl.printc("this is green", cl.colors.green)
              >>> cl.print ("this is red, "red")
    """
    colors = DotDot({
        'black':    (0, 30),    'gray_br':   (0, 37),
        'blue':     (0, 34),    'white':     (1, 37),
        'green':    (0, 32),    'blue_br':   (1, 34),
        'cyan':     (0, 36),    'green_br':  (1, 32),
        'red':      (0, 31),    'cyan_br':   (1, 36),
        'purple':   (0, 35),    'red_br':    (1, 31),
        'yellow':   (0, 33),    'purple_br': (1, 35),
        'gray_dk':  (1, 30),    'yellow_br': (1, 33),
        'normal':   (0,)
        })

    @classmethod
    def help(cls):
        print ("for named colors use :")
        for c in sorted(list(cls.colors.items())):
            print ("{:10} {}".format(*c))

    @classmethod
    def color_code(cls, color):
        """ color is either a tuple as in colors.values or a string key to colors dictionary
        """
        if not isinstance(color, tuple):
            color = cls.colors[color]
        return "{:d};{}".format(color[0], str(color[1]) if len(color) == 2 else "")

    @classmethod
    def color_switch_txt(cls, color=colors.red):
        return "\033[{}m".format(cls.color_code(color))

    @classmethod
    def color_txt(cls, txt="", color=None):
        return "{}{}\033[0m".format(cls.color_switch_txt(color), txt)

    @classmethod
    def printc(cls, txt, color=colors.red):
        """Print in color."""
        print (cls.color_txt(txt, color))

    @classmethod
    def color_switch_print(cls, color):
        print (cls.color_switch_txt(color))


import logging
from logging.handlers import TimedRotatingFileHandler
import time


class ColoredFormatter(logging.Formatter):
    color = Color()
    clr_name = color.colors

    def format(self, record):
        levelno = record.levelno
        if(levelno >= 50):
            clr = self.clr_name.red_br       # CRITICAL / FATAL
        elif(levelno >= 40):
            clr = self.clr_name.red          # ERROR
        elif(levelno >= 30):
            clr = self.clr_name.yellow       # WARNING
        elif(levelno >= 20):
            clr = self.clr_name.green        # INFO
        elif(levelno >= 10):
            clr = self.cls_name.purple_br    # DEBUG
        else:
            clr = self.cls_name.normal       # NOTSET etc
        return self.color.color_txt(logging.Formatter.format(self, record), clr)


def double_logger(
        # obsolete TODO remove it when drop support for python 2.x
        # then we can use new style formating ({}) style='{'
        # also see http://pythonhosted.org//logutils/
        # and http://plumberjack.blogspot.gr/2010/10/supporting-alternative-formatting.html
        loggerName="log",
        levelConsol=logging.DEBUG,
        levelFile=logging.DEBUG,
        filename="~/log_"+__name__,
        verbose=1,
        when='midnight',
        interval=1,
        backupCount=7):
    """ a logger that logs to file as well as as screen
        usage : logger=double_logger("log8",verbose=-1,filename="del3.log")
    """
    logger = logging.getLogger(loggerName)
    logger.setLevel(min(levelConsol if levelConsol else 100, levelFile if levelFile else 100))
    frmt = "{'dt':'%(asctime)s','ln':'%(name)s' ,'lv':'%(levelname)-8s','msg':'%(message)s'"
    if verbose > 1:
        frmt += "\n\t\t\t,'Func': '%(funcName)-10s','line':%(lineno)4d, \
                'module':'%(module)s', 'file':'%(filename)s'"
    if verbose > 2:
        frmt += "\n\t\t\t,'Process':['%(processName)s', %(process)d], \
                'thread':['%(threadName)s', %(thread)d], 'ms':%(relativeCreated)d"
    frmt += "}"
    if levelFile:
        formatter = logging.Formatter(frmt.replace(" ", ""), style='{')
        formatter.converter = time.gmtime
        hf = TimedRotatingFileHandler(
            filename, when=when, interval=interval,
            backupCount=backupCount, encoding='utf-8', delay=False, utc=True)
        hf.setFormatter(formatter)
        hf.setLevel(levelFile)
        logger.addHandler(hf)
    if levelConsol:
        frmtC = frmt.translate(dict((ord(c), u'') for c in u"'{},"))
        formatterC = ColoredFormatter(frmtC)
        formatterC.converter = time.gmtime
        hs = logging.StreamHandler()
        hs.setLevel(levelConsol)
        hs.setFormatter(formatterC)
        logger.addHandler(hs)
    return logger
