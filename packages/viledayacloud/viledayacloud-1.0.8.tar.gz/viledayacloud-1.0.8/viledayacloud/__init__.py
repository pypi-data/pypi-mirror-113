# coding=utf-8
"""
viledayacloud
"""

__version__ = "1.0.8"

from typing import Tuple

from .common import getsecret as getsecret, tgmjsoncall as tgmjsoncall

__all__: Tuple[str, ...] = (
        "getsecret",
        "tgmjsoncall",
        )
