# -*- coding: utf-8 -*-

import string
import random

from context import *

# TODO: Mock mysql
def random_letter(len):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(len))


def random_letter_num(len):
    letters = string.ascii_letters + string.digits + '\''
    return ''.join(random.choice(letters) for _ in range(len))


def test():
    dumper = autodump.Autodumper(random_letter(10))
    n_test, n_col = 10, 10
    col_name_len, record_len = 10, 5
    col_name = [random_letter(col_name_len) for _ in range(col_name_len)]
    dumper.persist(random_letter_num(10), random_letter_num(10))
    for t in range(n_test):
        record = []
        for c in range(n_col):
            record.append(random_letter_num(record_len))
            dumper.cache(col_name[c], record[-1])
        print("Test %d: %s" % (t, record))
        dumper.flush()


if __name__ == "__main__":
    test()
