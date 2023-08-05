"""
This test verifies that the "TranslatableMeta" class defined inside a Django
model does not trigger the "missing-class-docstring" warning.
"""
# pylint: disable=too-few-public-methods
from typing import List

from translations.models import Translatable


class CrazyModel(Translatable):
    "CrazyModel"

    class TranslatableMeta:
        fields: List[str] = []
