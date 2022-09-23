"""Tests for the class `AstRunner`."""
import os
from dataclasses import dataclass, field
from typing import Final, Mapping

import pytest

from docstring_renderer.ast_runner import AstRunner, AstRunnerError

THIS_DIR: Final = os.path.abspath(os.path.dirname(__file__))
"""Directory where this script lies in."""
TEST_DATA_DIR: Final = os.path.join(THIS_DIR, "test_data")
"""Test data directory used for this file."""


@dataclass
class AstRunnerParams:
    """Hold the input parameters used to instantiate the `AstRunner` object."""

    keyword: str = ""
    """Keyword that will use the `AstRunner` object to find any method/func/class."""
    file_path: str = field(init=False)
    """Path pointing to the file that will be processed by the `AstRunner`."""
    file_name: str = field(init=False, default="file.py")
    """
    Name of the file that will be used for the test.

    It must be inside the `test_data` folder.
    """

    def __post_init__(self) -> None:
        """
        Instantiate attributes which depends on the ones instated in __init__.

        :raises FileNotFoundError: When the file name provided cannot be find in the
            test data dir.
        """
        file_path = os.path.join(TEST_DATA_DIR, self.file_name)
        if not os.path.isfile(file_path):
            raise FileNotFoundError(
                f"File proposed for the test `{file_path}` could not be found."
            )
        # Set attributes of the frozen dataclass.
        object.__setattr__(self, "file_path", file_path)

    @property
    def as_dict(self) -> Mapping[str, str]:
        """Parmas of the `AstRunner` that can be directly forwarded to the `__init__`."""
        return {"file_path": self.file_path, "keyword": self.keyword}


class TestAstRunnerLists:
    """Test to verify that the class can lists method, class and functions."""

    FILE: Final = os.path.join(TEST_DATA_DIR, "file.py")

    # Type of objects that can be found in `FILE`.
    FUNCS: Final = ["func1", "func2", "func3"]
    METHODS: Final = [
        "MyClass1.class1func1",
        "MyClass1.class1func2",
        "MyClass2.class2func1",
        "MyClass2.class2func2",
    ]
    CLASSES: Final = ["MyClass1", "MyClass2"]
    ALL: Final = [*FUNCS, *METHODS, *CLASSES]

    @pytest.fixture
    def ast_runner(self) -> AstRunner:
        """Create an object of type `AstRunner`."""
        return AstRunner(file_path=self.FILE, keyword="")

    def test_list_funcs(self, ast_runner: AstRunner) -> None:
        """
        Verify the output of `list_funcs` method.

        :param ast_runner: `AstRunner` object already initialized.
        """
        assert set(self.FUNCS) == set(ast_runner.list_funcs())

    def test_list_methods(self, ast_runner: AstRunner) -> None:
        """
        Verify the output of `list_methods` method.

        :param ast_runner: `AstRunner` object already initialized.
        """
        assert set(self.METHODS) == set(ast_runner.list_methods())

    def test_list_class(self, ast_runner: AstRunner) -> None:
        """
        Verify the output of `list_class` method.

        :param ast_runner: `AstRunner` object already initialized.
        """
        assert set(self.CLASSES) == set(ast_runner.list_classes())

    def test_list_all(self, ast_runner: AstRunner) -> None:
        """
        Verify that `list_all` reads all methods, funcs and classes.

        :param ast_runner: `AstRunner` object already initialized.
        """
        assert set(self.ALL) == set(ast_runner.list_all())


class TestAstRunnerFindKeyword:
    """Test to verify that the class can find the desired keywords."""

    @dataclass(frozen=True)
    class ParamsTest:
        """Class that holds all the parameters used for each test."""

        ast_runner_params: AstRunnerParams
        """Parameters that will be used to instantiate the object to be tested."""
        expected_output: str = ""
        """Expected output of the method to test given the specific ast runner params."""

    @pytest.fixture
    def ast_runner(self, params_test: ParamsTest) -> AstRunner:
        """Create an object of type `AstRunner`."""
        return AstRunner(**params_test.ast_runner_params.as_dict)

    # fmt: off
    @pytest.mark.parametrize(
        "params_test",
        [
            ParamsTest(
                AstRunnerParams(keyword="func1"),
                expected_output="func1"),
            ParamsTest(
                AstRunnerParams(keyword="class1func1"),
                expected_output="MyClass1.class1func1"),
            ParamsTest(
                AstRunnerParams(keyword="Class2"),
                expected_output="MyClass2"),
        ],
    )
    # fmt: on
    def test_find_keyword(self, params_test: ParamsTest, ast_runner: AstRunner) -> None:
        """
        Test that the class is able to locate the given keywords in the Python file.

        :param params_test: Parameters that will be used for the test.
        :param ast_runner: `AstRunner` object already initialized.
        """
        assert params_test.expected_output == ast_runner.find_keyword()

    @pytest.mark.parametrize(
        "params_test",
        [
            ParamsTest(AstRunnerParams(keyword="func5")),
            ParamsTest(AstRunnerParams(keyword="class5")),
        ],
    )
    def test_no_keyword_found(
        self, params_test: ParamsTest, ast_runner: AstRunner
    ) -> None:
        """
        Corresponding exception is raised when the keyword is not present in the file.

        :param params_test: Parameters that will be used for the test.
        :param ast_runner: `AstRunner` object already initialized.
        """
        with pytest.raises(AstRunnerError):
            ast_runner.find_keyword()
