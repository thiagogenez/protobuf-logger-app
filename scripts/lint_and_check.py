# scripts/lint_and_check.py
import subprocess


def run_command(command):
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        exit(result.returncode)


def main():
    run_command("poetry run black .")
    run_command("poetry run mypy src/")
    run_command("poetry run pylint src/")


if __name__ == "__main__":
    main()
