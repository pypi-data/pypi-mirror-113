"""
This test verifies that a "Translatable" descendant class does not trigger the
"too-few-public-methods" warning.
"""
from translations.models import Translatable


class CrazyModel(Translatable):
    "CrazyModel"
