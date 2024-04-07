"""This script defines a temporary pipeline to automate the process of running protobuf compilation
followed by linting and checks on the project codebase."""

from . import run_lint_and_check
from . import run_protoc


def run_pipeline():
    """Executes the project pipeline by first running protobuf compilation and then performing lint
    and other checks."""
    run_protoc.main()
    run_lint_and_check.main()


def main():
    """The main entry point for the pipeline script."""
    run_pipeline()


if __name__ == "__main__":
    main()
