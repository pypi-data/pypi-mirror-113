import random
from unames.constants import Constants


def fx_switch(i):
    return {
        Constants.TYPE_FL: {
            "type": Constants.TYPE_FL,
            "patterns": [
                "{}.{}",
                "__{}.{}__",
                "{}.{}__",
                "{}._.{}",
                "{}_{}",
                "_.{}x{}._"
            ]},
        Constants.TYPE_F: {
            "type": Constants.TYPE_F,
            "patterns": [
                "itz.{}",
                "itz_{}",
                "iam.{}",
                "iam_{}",
            ]},
        Constants.TYPE_L: {
            "type": Constants.TYPE_L,
            "patterns": [
                "{}.{}",
            ]},
        Constants.TYPE_MISC: {
            "type": Constants.TYPE_MISC,
            "patterns": [
                "{}",
            ]},
    }[i]


def fx_leet(full_name):
    for char in full_name:
        if char == 'a':
            full_name = full_name.replace('a', '4')
        elif char == 'b':
            full_name = full_name.replace('b', '8')
        elif char == 'e':
            full_name = full_name.replace('e', '3')
        elif char == 'l':
            full_name = full_name.replace('l', '1')
        elif char == 'o':
            full_name = full_name.replace('o', '0')
        elif char == 's':
            full_name = full_name.replace('s', '5')
        elif char == 't':
            full_name = full_name.replace('t', '7')
        elif char == ' ':
            full_name = full_name.replace(' ', '_')

    return full_name


def fx_short_uname(full_name):
    if len(full_name) > 1:
        first_three_letter = full_name[0:3]
        three_letters_surname = random.choice([full_name[-1:3].rjust(3, 'x'), full_name[-1:3]])
        number = '{:03d}'.format(random.randrange(1, 999))
        return '{}{}{}'.format(first_three_letter, three_letters_surname, number)
