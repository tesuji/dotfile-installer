#!/usr/bin/env python
from __future__ import print_function
from builtins import input

import tempfile

def ask_yesno(question, default="yes"):
    """Ask a yes/no question via input() and return their answer.

    `question` is a string that is presented to the user.
    `default` is the presumed answer if the user just hits <Enter>.
        It must be `yes` (the default), `no` or None (meaning
        an answer is required of the user).

    The `answer` return value is True for `yes` or False for `no`.

    Ref https://stackoverflow.com/a/3041990/5456794
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        choice = input(question + prompt).lower()
        if default is not None and not choice:
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').")


def can_write(to_dir):
    try:
        with tempfile.TemporaryFile(dir=to_dir) as tmp:
            tmp.write(b'example writing\n')
            return True
    except OSError as e:
        if e.errno == errno.EACCES:
            return False
        # Not a permission error.
        raise e
