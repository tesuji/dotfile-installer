#!/usr/bin/env python
##########################################################
## This script for installing Firefox Quantumn on Debian 9
## EXPERIMENTAL! Use at your own risk!
##########################################################

from __future__ import print_function
from builtins import input

import errno
import os
import sys
import re
import tarfile
from subprocess import call

import requests

HERE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(HERE_DIR)

from helpers.colour import ForeText
from helpers.prompt import ask_yesno
from helpers.backup import backup_file, rm_if_exists

HOME_DIR = os.path.expanduser("~")

def exitting(errno):
    print("Exiting ...", file=sys.stderr)
    sys.exit(errno)


class FirefoxInstaller():
    """docstring for FirefoxInstaller"""
    ENTRY_URL = 'https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US'

    HEADERS = {
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        # "Referer": "https://dkhp.uit.edu.vn/",
        # "Cookie": "has_js=0",
        "Connection": "keep-alive",
    }

    def __init__(self):
        self.ff_session = requests.Session()
        self.ff_session.headers.update(FirefoxInstaller.HEADERS)

        # self.url = None
        # self.filename = None
        self.target = None

        self.url = 'https://download-installer.cdn.mozilla.net/pub/firefox/releases/59.0.2/linux-x86_64/en-US/firefox-59.0.2.tar.bz2'
        self.filename = 'firefox-59.0.2.tar.bz2'

    def test_exists(self):
        print("Testing firefox download link ...", file=sys.stderr)
        try:
            r = self.ff_session.head(FirefoxInstaller.ENTRY_URL)
            if r.status_code == requests.codes.found:
                self.url = r.headers.get('location')
                self.filename = os.path.basename(self.url)
                return True
        except Exception as e:
            print(str(e), file=sys.stderr)

        print('Remote file does not exist -- broken link!!!', file=sys.stderr)

        return False

    def valid_firefox_name(self):
        regex = r'firefox-\d{2}\.(\d\.){1,2}tar\.bz2'
        if re.search(regex, self.filename):
            return True
        if '0b' in self.filename:
            print("This is BETA release: %s"%self.filename, file=sys.stderr)
        else:
            print("It's NOT likely a tar.bz2 file ...", file=sys.stderr)
        return False

    def download(self):
        """
        download large file: https://stackoverflow.com/a/16696317/5456794
        progress bar: https://stackoverflow.com/a/15645088/5456794
        """
        # exist = self.test_exists()
        exist = True

        if not exist or not self.valid_firefox_name():
            exitting(127)

        if not ask_yesno("Download %s ?" % ForeText.colored(self.filename, ForeText.RED)):
            exitting(1)

        self.target = os.path.join(os.getcwd(), self.filename)
        response = input('Enter file (%s): '% self.target)

        if response:
            self.target = response

        if os.path.exists(self.target):
            os.rename(self.target, self.target+'_backup')

        print("Downloading %s ..." % self.url)

        # with open(self.target, 'wb') as fd:
        #     r = self.ff_session.get(self.url, stream=True)
        #     total_length = r.headers.get('content-length')

        #     if total_length is None: # no content length header
        #         print("Download is broken", file=sys.stderr)
        #         exitting(2)

        #     dl = 0
        #     total_length = int(total_length)
        #     for chunk in r.iter_content(chunk_size=4096):
        #         if chunk: # filter out keep-alive new chunks
        #             dl += len(chunk)
        #             fd.write(chunk)
        #             status = r"Bytes: %10d [%3.2f%%]" % (dl, dl * 100. / total_length)
        #             sys.stdout.write("\r%s"%status)
        #             sys.stdout.flush()

    @staticmethod
    def extract_bz2(filename, path="."):
        with tarfile.open(filename, "r:bz2") as tar:
            tar.extractall(path)

    def install(self):
        """
        Ref: https://wiki.debian.org/Firefox
        """
        if not ask_yesno("Do you want to install ?"):
            exitting(1)

        bin_dir = os.path.join(HOME_DIR, 'bin')
        firefox_dir = os.path.join(bin_dir, 'firefox')
        firefox_bin = os.path.join(firefox_dir, 'firefox')

        if not os.path.exists(bin_dir):
            os.mkdir(bin_dir)

        if not os.path.isdir():
            print("%s is not directory"%bin_dir, file=sys.stderr)
            exitting(3)

        print("Backup old firefox ...")
        rm_if_exists(firefox_dir, backup=True)

        print("Unpacking firefox to %s"%bin_dir)
        extract_bz2(self.target, bin_dir)

        cur_user = os.path.basename(HOME_DIR)
        print("Setting owner and permissions (only %s user) ..."%cur_user)
        call(['find', firefox_dir, '-exec', 'chown', cur_user+'.', '{}', '+'])
        call(['find', firefox_dir, '-type', 'd', '-exec', 'chmod', '755', '{}', '+'])

        print("Configuring alternative links to set Firefox be default browser ...")
        browsers = ('x-www-browser', 'gnome-www-browser', 'www-browser')
        for prog in browsers:
            call(['sudo', 'update-alternatives', '--install', '/usr/bin/%s'%prog, prog, firefox_bin, '100'])
            call(['sudo', 'update-alternatives', '--set', prog, firefox_bin])

        print("Creating symlink to /usr/bin/firefox")
        call(['sudo', 'ln', '-sf', firefox_bin, '/usr/bin/firefox'])

    def remove_addons(self, firefox_dir):
        wanted_lists = (
            'followonsearch@mozilla.com.xpi', 'firefox@getpocket.com.xpi', 'screenshots@mozilla.org.xpi')
        print("Disabling addons %s"%wanted_lists)

        if ask_yesno("Do you want to diable ?"):
            for ext in wanted_lists:
                filename = os.path.join(firefox_dir, 'browser', 'features', ext)
                call(['sudo', 'chmod', 'a-r', filename])


def main():
    installer = FirefoxInstaller()
    installer.download()
    installer.install()

if __name__ == '__main__':
    main()



