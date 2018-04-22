#!/usr/bin/env python

class ForeText():
    """This class prepare color string to print in Terminal"""
    BLACK  = '7;30;40'
    RED    = '7;30;41'
    GREEN  = '7;30;42'
    ORANGE = '7;30;43'
    BLUE   = '7;30;44'
    PURPLE = '7;30;45'
    CYAN   = '7;30;46'
    GRAY   = '7;30;47'

    default = GREEN

    @staticmethod
    def colored(text, color=default):
        """Return ANSI escape sequences. Default is `green`"""
        return '\x1b[%(color)sm%(text)s\x1b[0m' % locals()
