import argparse

from docstring_renderer.ast_runner import AstRunner


def _create_argument_parser() -> argparse.ArgumentParser:
    """Create the argument a parser for this scripts.

    :return: the argument parser instance
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Render docstrings from any class, function or method."
    )
    parser.add_argument(
        "--file-path",
        dest="file_path",
        help="Specify the path to the file to be analized.",
        required=True,
    )
    parser.add_argument(
        "--keyword",
        dest="keyword",
        help=(
            "Specify the name of the function, method or class to visualize its "
            "docstring."
        ),
        required=True,
    )
    return parser


def main() -> None:
    parser = _create_argument_parser()
    args = parser.parse_args()
    runner = AstRunner(args.file_path, args.keyword)

    keyword = runner.find_keyword()
    print(keyword)


if __name__ == "__main__":
    main()
