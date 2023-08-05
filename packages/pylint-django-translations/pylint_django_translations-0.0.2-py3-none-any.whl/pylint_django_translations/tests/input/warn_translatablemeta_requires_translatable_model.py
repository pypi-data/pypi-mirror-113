"""
This test verifies that a a "translatablemeta-modelclass" warning is triggered
when a "TranslatableMeta" class is found inside a class which is not a
descendant of "translations.models.Translatable".
"""
from typing import List
from django.db import models


class CrazyModel(models.Model):
    "CrazyModel"

    class TranslatableMeta:  # -3: [translatablemeta-modelclass]
        fields: List[str] = []
