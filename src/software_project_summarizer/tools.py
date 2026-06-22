"""Tools for use by the Software Project Summarizer agent."""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path

from software_project_summarizer.utilities import (
    permit_directory_inspection,
    permit_file_inspection,
)

VERBOSE_DEBUGGING = False


def create_project_tools(project_directory: Path) -> list[Callable[..., str]]:
    project_directory = project_directory.resolve()

    def get_project_tree() -> str:
        """
        Returns the accessible project directory tree.

        Returns:
            (str) : a list of directories and files
        """

        if VERBOSE_DEBUGGING:
            print("Called tool: get_project_tree")

        return _get_project_tree(project_directory)

    def read_project_file(relative_path: str) -> str:
        """
        Returns the text content of a file.

        Args:
            relative_path (str) : the path to the file, relative to the root directory

        Returns:
            (str) : the content of the file.
        """

        if VERBOSE_DEBUGGING:
            print(f"Called tool: read_project_file({relative_path!r})")

        return _read_project_file(project_directory, relative_path)

    return [get_project_tree, read_project_file]


def _get_project_tree(project_directory: Path) -> str:
    """
    Returns a file system tree of the directories and files comprising the project.

    """
    lines: list[str] = []
    _populate_project_structure(project_directory, lines, 0)
    return "\n".join(lines)


def _read_project_file(project_directory: Path, relative_path: str) -> str:
    file_location = project_directory / relative_path
    file_location = file_location.resolve()

    if not file_location.is_relative_to(project_directory):
        raise ValueError("Path is outside the project directory.")

    if not file_location.is_file():
        raise ValueError("Path is not a file.")

    file_size = os.path.getsize(file_location)
    if file_size > 50_000:
        raise ValueError("File is too large.")

    return file_location.read_text(encoding="utf-8")


def _populate_project_structure(directory: Path, lines: list[str], indent: int) -> None:
    directory_name = directory.name
    if not permit_directory_inspection(directory_name):
        return

    indentation = "  " * indent
    lines.append(indentation + directory_name + "/")
    files: list[str] = []
    for item in directory.iterdir():
        if item.is_dir():
            _populate_project_structure(item, lines, indent + 1)
        elif item.is_file():
            file_name = item.name
            if not permit_file_inspection(file_name):
                continue
            files.append(file_name)
    for file in files:
        lines.append(indentation + "  " + file)
