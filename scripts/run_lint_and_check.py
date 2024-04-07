"""This module runs code quality tools (docformatter, black, mypy, pylint) in sequence on the
project's Python codebase, specifically targeting the 'src/' and 'scripts/' directories, to ensure
compliance with coding standards and to identify potential errors.

The tools are run in the following order:
1. docformatter
2. black
3. mypy
4. pylint
"""

import subprocess
import sys


def run_command(command, description):
    """Executes a shell command and exits if the command fails."""
    print(f"-> Running: {description}")
    try:
        subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        print(f"\t- {description} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"\t- Error: {description} failed with exit code {e.returncode}", file=sys.stderr)
        print(f"\t- Command: {command}", file=sys.stderr)


def main():
    """Runs docformatter, black, mypy, and pylint in sequence."""

    directories = ["src/", "scripts/"]
    for directory in directories:
        print(f"\n=== Processing files in '{directory}' ===\n")
        run_command(f"poetry run docformatter --in-place --recursive {directory}", "Docformatter")
        run_command(f"poetry run black {directory}", "Black")
        run_command(f"poetry run mypy {directory}", "Mypy")
        run_command(f"poetry run pylint {directory}", "Pylint")


if __name__ == "__main__":
    main()
