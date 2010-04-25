# -*- coding: utf-8 -*-

from random import choice
import string, random

def random_key(length=24, chars=string.letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])