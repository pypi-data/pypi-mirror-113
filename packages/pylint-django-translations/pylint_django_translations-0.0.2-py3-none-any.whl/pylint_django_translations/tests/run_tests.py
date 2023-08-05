#!/usr/bin/env python
"Tests for pylint_django_translations"
import csv
import os
import sys

from pylint.testutils import (
    FunctionalTestFile,
    LintModuleTest,
)
import pytest


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "pylint_django_translations.tests.django_settings",
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if "test" not in csv.list_dialects():

    class TestDialect(csv.excel):
        "Abuse the CSV module for expected test values"
        # pylint: disable=too-few-public-methods
        delimiter = ":"
        lineterminator = "\n"

    csv.register_dialect("test", TestDialect)


class PylintDjangoTranslationsLintModuleTest(LintModuleTest):
    "Load the necessary plugins into the linter"

    def __init__(self, test_file: str):
        super().__init__(test_file)
        self._linter.load_plugin_modules(
            ["pylint_django", "pylint_django_translations"]
        )
        self._linter.load_plugin_configuration()


def get_tests(input_dir: str = "input"):
    "Find test files in input_dir"
    input_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), input_dir
    )

    tests = []
    for filename in os.listdir(input_dir):
        if filename != "__init__.py" and filename.endswith(".py"):
            tests.append(FunctionalTestFile(input_dir, filename))
    return tests


TESTS = get_tests()
TESTS_NAMES = [test.base for test in TESTS]


@pytest.mark.parametrize("test_file", TESTS, ids=TESTS_NAMES)
def test_it_all(test_file):
    "Run the tests!"
    lint_test = PylintDjangoTranslationsLintModuleTest(test_file)
    lint_test.setUp()
    lint_test._runTest()  # pylint: disable=protected-access


if __name__ == "__main__":
    sys.exit(pytest.main(sys.argv))
