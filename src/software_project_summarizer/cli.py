"""Command-line interface for the application."""

from __future__ import annotations

import sys
from pathlib import Path

from software_project_summarizer.agent import summarize_project


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface."""
    project_directory = _get_prompt(argv)
    if not project_directory:
        example = "c:\\Temp\\ProjectName"
        raise SystemExit(f'Usage: python -m software_project_summarizer "{example}"')

    project_location = Path(project_directory)
    if not project_location.exists():
        print("Project location does not exist:", project_directory)
        return 1

    if not project_location.is_dir():
        print("Project location is not a directory:", project_directory)
        return 1

    summary = summarize_project(project_location)

    print(summary)
    return 0


def _get_prompt(argv: list[str] | None = None) -> str:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        return ""

    return args[0]
