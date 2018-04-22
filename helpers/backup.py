#!/usr/bin/env python
from __future__ import print_function

import errno
import os
import shutil
import sys


def ln(target, link_name, verbose=False, use_hard_link=False):
    """Create a link points to :attr:`target` with the name :attr:`LINK_NAME`"""
    if verbose:
        print("ln: %(link_name)r -> %(target)r"%locals())
    if use_hard_link:
        try:
            os.link(target, link_name)
        except OSError as e:
            if e.errno == errno.EXDEV:
                # Invalid cross-device link
                print('%s'%(str(e)), file=sys.stderr)
                print('\tTrying to use symlink instead ...', file=sys.stderr)
            else:
                raise e
    os.symlink(target, link_name)


def backup_file(filepath):
    os.rename(filepath, filepath + "_backup")


def rm_if_exists(link_name, backup):
    if os.path.exists(link_name):
        if backup:
            backup_file(link_name)
        elif os.path.isfile(link_name):
            os.unlink(link_name)
        elif os.path.isdir(link_name):
            shutil.rmtree(link_name)
        else:
            print(ForeText.colored('%(link_name)r not recognized', ForeText.BLUE),
                  file=sys.stderr)


def handle_samefile(target, link_name, backup):
    """handle_samefile(target, link_name, backup) -> None

    Note:
        makedirs() will become confused if the path elements to
        create include os.pardir such as '..' for Windows and POSIX.
    """
    try:
        if os.path.samefile(target, link_name):
            print("%(link_name)r is identical to %(target)r"%locals())
            return None
        else:
            rm_if_exists(link_name, backup)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise e

    dir_link_name = os.path.dirname(link_name)
    print(dir_link_name)
    if not os.path.exists(dir_link_name):
        os.makedirs(dir_link_name, 0o770)

    ln(target, link_name, verbose=True)

