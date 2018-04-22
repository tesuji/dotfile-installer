# dotfile-installer
:earth_asia: A failed dotfiles installer in Python (Now replaced by GNU Stow)

Separated from my [dotfiles repo][dotfliles].

### A Firefox installer in Python for Debian 9

May not really helpful when come to Firefox 60esr.

### Dependencies

List of dependencies:
- python-builtins
- python-future
- python-requests

### Usage

This script will not backup your own dotfiles! Please do it yourself or turn on back up in [install.py](install.py).

```bash
cd ~
git clone https://github.com/lzutao/dotfile-installer.git
cd dotfiles-installer
python install.py
```


[dotfliles]: https://github.com/lzutao/dotfliles

