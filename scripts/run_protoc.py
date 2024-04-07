"""Compile Protocol Buffers (.proto) files to Python.

This script checks if the Protocol Buffers compiler (protoc) is installed and available in the
system's PATH. If protoc is installed, it compiles a specific .proto file to Python using protoc.
"""

import subprocess
import sys
from pathlib import Path


def is_protoc_installed():
    """Check if protoc is installed and available in the system's PATH."""
    try:
        protoc_version = subprocess.check_output(["protoc", "--version"], encoding="utf-8")
        print(f"Found protoc: {protoc_version.strip()}")
        return True
    except (subprocess.CalledProcessError, OSError):
        return False


def run_protoc(proto_src, python_out):
    """Compile a specific .proto file to Python."""
    proto_file_path = Path(proto_src).resolve()
    python_out_path = Path(python_out).resolve()

    # Ensure the .proto file exists
    if not proto_file_path.is_file():
        print(f"Error: The specified .proto file '{proto_src}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Ensure the output directory exists or create it
    python_out_path.mkdir(parents=True, exist_ok=True)

    command = [
        "protoc",
        f"--proto_path={proto_file_path.parent}",
        f"--mypy_out={python_out}",
        f"--python_out={python_out}",
        str(proto_file_path),
    ]

    try:
        subprocess.check_call(command)
        print(f"'{proto_file_path.name}' compiled successfully to '{python_out}'.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to compile '{proto_file_path.name}': {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Compile the specified .proto file."""
    if not is_protoc_installed():
        print("Error: 'protoc' is not installed or not found in PATH.", file=sys.stderr)
        print("Please install the Protocol Buffers compiler (protoc) to proceed.", file=sys.stderr)
        sys.exit(1)

    # hard-coded just for now
    run_protoc("proto/log_message.proto", "src/logger_app")
    run_protoc("proto/log_message.proto", "src/client_app")


if __name__ == "__main__":
    main()
