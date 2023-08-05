==========================
Pylint Django Translations
==========================

This Pylint plugin supresses some warnings that Pylint gives for
django-translations-related classes.  It also adds a checker to verify that
``TranslatableMeta`` classes exist inside classes that are subclasses of
``translations.models.Translatable``.
