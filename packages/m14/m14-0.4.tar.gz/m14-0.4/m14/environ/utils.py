#!/usr/bin/env python3
# coding: utf-8

import datetime
import logging
from typing import Union


def easylog(level):
    root = logging.root
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root.setLevel(level)
    root.addHandler(handler)


def check_prefixes(string: str, include=None, exclude=None) -> bool:
    """
    Args:
        string (str): string to be checked
        include: None = include anything
        exclude: None = no exlusion rule
    """
    if exclude is not None:
        for prefix in exclude:
            if string.startswith(prefix):
                return False
    if include is not None:
        for prefix in include:
            if string.startswith(prefix):
                return True
        return False
    else:
        return True


def relative_date(delta: int = 0, fmt='-') -> Union[str, datetime.date]:
    date = datetime.date.today()
    if delta:
        date += datetime.timedelta(days=delta)
    if fmt is None:
        return date
    elif fmt == '':
        return date.strftime('%Y%m%d')
    elif fmt == '-':
        return date.strftime('%Y-%m-%d')
    return date.strftime(fmt)


def fmt_today(fmt='-') -> Union[str, datetime.date]:
    return relative_date(0, fmt)
