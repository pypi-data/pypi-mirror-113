"Suppress unwanted warnings"
from pylint.checkers.base import DocStringChecker
from pylint.checkers.design_analysis import MisdesignChecker
from pylint.lint import PyLinter
from pylint_plugin_utils import suppress_message

from .ast import (
    is_translatable_model,
    is_translatablemeta_subclass,
)


def suppress_warnings(linter: PyLinter) -> None:
    "Register functions to suppress spurious warnings"
    # TranslatableMeta class on models
    suppress_message(
        linter,
        DocStringChecker.visit_classdef,
        "missing-class-docstring",
        is_translatablemeta_subclass,
    )
    suppress_message(
        linter,
        MisdesignChecker.leave_classdef,
        "too-few-public-methods",
        is_translatablemeta_subclass,
    )
    suppress_message(
        linter,
        MisdesignChecker.leave_classdef,
        "too-few-public-methods",
        is_translatable_model,
    )
