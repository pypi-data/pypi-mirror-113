from __future__ import unicode_literals
import random
from unames.constants import Constants
from unames.utils import fx_switch, fx_short_uname, fx_leet

__title__ = "unames"
__version__ = "1.0.3"
__author__ = "chankruze"
__author_email__ = "chankruze@gmail.com"
__license__ = "GNU General Public License v3 or later (GPLv3+)"


def gen_username(full_name):
    first_name = full_name.split()[0]
    last_name = full_name.split()[-1]
    fmt = fx_switch(random.choice(range(Constants.TYPE_MISC + 1)))
    fmt_type = fmt["type"]
    fmt_pattern = random.choice(fmt["patterns"])

    if fmt_type == Constants.TYPE_FL:
        return fmt_pattern.format(first_name, last_name)
    elif fmt_type == Constants.TYPE_F:
        return fmt_pattern.format(first_name)
    elif fmt_type == Constants.TYPE_L:
        return fmt_pattern.format(last_name, first_name)
    elif fmt_type == Constants.TYPE_MISC:
        return fmt_pattern.format(random.choice([fx_short_uname(full_name), fx_leet(full_name)]))
