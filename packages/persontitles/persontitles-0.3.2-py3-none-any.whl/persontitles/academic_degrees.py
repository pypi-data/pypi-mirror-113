#!/usr/bin/env python
# -*- coding: utf-8 -*-
# academic_degrees.py
"""Collection of academic degrees."""
import json
import os
import importlib.resources as pkg_resources
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(),
    os.path.expanduser(__file__))),
)  # isort:skip # noqa # pylint: disable=wrong-import-position
sys.path.append(
    os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)),
)  # isort: skip # noqa # pylint: disable=wrong-import-position

from persontitles.academic_german import degrees_ger  # noqa
from persontitles.academic_german import german_abbrevs  # noqa
from persontitles.academic_uk import degrees_uk  # noqa
from persontitles.academic_us import degrees_us  # noqa


def degrees() -> dict:
    print(os.getcwd())
    try:
        with open('./src/persontitles/data/degrees.json', mode='r', encoding='utf-8') as fin:  # noqa
            DEGREES = json.load(fin)
    except FileNotFoundError:
        DEGREES = collect_degrees()
        try:
            with open('./src/persontitles/data/degrees.json', mode='w', encoding='utf-8') as fout:  # noqa
                json.dump(DEGREES, fout)
        except FileNotFoundError:
            DEGREES = load_file_within_package()

    return DEGREES


def load_file_within_package():
    from . import data
    FILE = pkg_resources.read_text(data, 'degrees.json')
    with open(FILE) as fin:
        DATA_FILE = json.load(fin)
    return DATA_FILE


def collect_degrees():
    DEGREES = dict()
    degrees = []

    for degree in degrees_ger():
        degrees.append(degree)
    DEGREES['D'] = degrees

    degrees = []
    degrees_d = degrees_ger()
    for degree in german_abbrevs(degrees_d):
        degrees.append(degree)
    DEGREES['german_abbrevs'] = degrees

    degrees = []
    for degree in degrees_uk():
        degrees.append(degree)
    DEGREES['UK'] = degrees

    degrees = []
    for degree in degrees_us():
        degrees.append(degree)
    DEGREES['US'] = degrees

    return DEGREES


if __name__ == '__main__':
    DEGREES = collect_degrees()
    for k, v in DEGREES.items():
        print(k)
        print(v)
        print()

    print(os.getcwd())
