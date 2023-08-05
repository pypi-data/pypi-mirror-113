"pylint_django_translations checkers"
from astroid.nodes import ClassDef
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter
from pylint_django.utils import node_is_subclass


def register_checkers(linter: PyLinter) -> None:
    "Register our TranslatableMeta/model checker"
    linter.register_checker(
        TranslatableMetaHasTranslatableModelChecker(linter)
    )


class TranslatableMetaHasTranslatableModelChecker(BaseChecker):
    "TranslatableMeta classes must be inside Translatable model classes"
    __implements__ = IAstroidChecker

    name = "translatablemeta-modelclass"
    priority = -1
    msgs = {
        "W0001": (
            "TranslatableMeta class container is not "
            "translations.models.Translatable.",
            "translatablemeta-modelclass",
            "Django models which have a internal TranslatableMeta class are "
            "expected to be subclasses of translations.models.Translatable.",
        )
    }

    def visit_classdef(self, node: ClassDef) -> None:
        """
        Warn if an internal TranslatableMeta class's parent class is not a
        subclass of translations.models.Translatable.
        """
        if node.name != "TranslatableMeta" or not isinstance(
            node.parent, ClassDef
        ):
            return
        base_classes = "translations.models.Translatable"
        if not node_is_subclass(node.parent, base_classes):
            self.add_message("W0001", node=node.parent)
