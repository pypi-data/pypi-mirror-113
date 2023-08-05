"""
This test verifies that the "TranslatableMeta" class defined inside a Django
model does not trigger the "too-few-public-methods" warning.
"""
# pylint: disable=missing-class-docstring
from typing import List

from translations.models import Translatable


class CrazyModel(Translatable):
    "CrazyModel"

    class TranslatableMeta:
        fields: List[str] = []
