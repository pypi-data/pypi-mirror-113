# -*- coding: utf-8 -*-
# *************************************
# aitk.robots: Python robot simulator
#
# Copyright (c) 2020 Calysto Developers
#
# https://github.com/ArtificialIntelligenceToolkit/aitk.robots
#
# *************************************

import os

_aitk_base_dir = os.path.expanduser("~")
if not os.access(_aitk_base_dir, os.W_OK):
    _aitk_base_dir = "/tmp"

_aitk_dir = os.path.join(_aitk_base_dir, ".aitk")

if not os.path.exists(_aitk_dir):
    try:
        os.makedirs(_aitk_dir)
    except OSError:
        pass


def get_dataset(dataset):
    get = None
    if dataset == "digits6x6":
        from .digits6x6 import get
    elif dataset == "dogs-vs-cats":
        from .dogs_vs_cats import get
    elif dataset == "dogs":
        from .dogs_vs_cats import get_dogs as get
    elif dataset == "cats":
        from .dogs_vs_cats import get_cats as get
    return get()
