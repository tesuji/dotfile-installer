#!/usr/bin/env python
######################################################
## This script for installing all the @lzutao dotfiles
## Use at your own risk!
######################################################

from __future__ import print_function

import os
import sys

HERE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(HERE_DIR)

from helpers.colour import ForeText
from helpers.prompt import ask_yesno
from helpers.backup import handle_samefile

HOME_DIR = os.path.expanduser("~")


def realjoin(dirname, *args):
    return os.path.realpath(os.path.join(dirname, *args))


def install_links(from_dir, to_dir=HOME_DIR, backup=False):
    target_dir = realjoin(HERE_DIR, '..', from_dir)
    len_source = len(target_dir) + 1

    for dirname, dirnames, filenames in os.walk(target_dir):
        for filename in filenames:
            target = os.path.join(dirname, filename)
            common_path = os.path.join(dirname, target)[len_source:]
            link_name = os.path.join(to_dir, common_path)

            handle_samefile(target, link_name, backup)


def install_home(backup=False):
    print(ForeText.colored('Copying home config files ...', ForeText.RED))
    install_links('home.d', backup=backup)
    print(ForeText.colored(' => Finishing ...', ForeText.CYAN))


def install_config(backup=False):
    print(ForeText.colored('Installing config file in HOME/.config ...', ForeText.RED))
    print(ForeText.colored(' -> Copying sublime text settings...', ForeText.RED))
    install_links('config.d', backup=backup)
    print(ForeText.colored('=>  Finishing ...', ForeText.CYAN))


def main():
    if ask_yesno(ForeText.colored("Install bash, zsh config in HOME folder ?", ForeText.ORANGE)):
        install_home()
    if ask_yesno(ForeText.colored("Install config file ?", ForeText.ORANGE)):
        install_config()


if __name__ == '__main__':
    main()
