"""Unit tests for utility inspection filters."""

from __future__ import annotations

import pytest

from software_project_summarizer.utilities import (
    permit_directory_inspection,
    permit_file_inspection,
)


@pytest.mark.parametrize(
    "directory_name",
    [
        "src",
        "tests",
        "docs",
        "scripts",
        "package",
    ],
)
def test_permit_directory_inspection_allows_expected_directories(
    directory_name: str,
) -> None:
    """Directories that are regular project folders should be inspectable."""
    assert permit_directory_inspection(directory_name) is True


@pytest.mark.parametrize(
    "directory_name",
    [
        ".git",
        "__pycache__",
        "obj",
        "bin",
        "node_modules",
        "dist",
        "venv",
        "build",
        "software_project_summarizer.egg-info",
    ],
)
def test_permit_directory_inspection_blocks_expected_directories(
    directory_name: str,
) -> None:
    """Hidden, special, and generated directories should be skipped."""
    assert permit_directory_inspection(directory_name) is False


@pytest.mark.parametrize(
    "file_name",
    [
        "main.py",
        "pyproject.toml",
        "notes.txt",
        ".gitignore",
        ".editorconfig",
    ],
)
def test_permit_file_inspection_allows_expected_files(file_name: str) -> None:
    """Regular files and explicitly allowed dotfiles should be inspectable."""
    assert permit_file_inspection(file_name) is True


@pytest.mark.parametrize(
    "file_name",
    [
        "__init__.py",
        ".env",
        ".vscode",
        "README.md",
        "readme",
        "ReadMe.txt",
    ],
)
def test_permit_file_inspection_blocks_expected_files(file_name: str) -> None:
    """Private, hidden, and readme files should be skipped."""
    assert permit_file_inspection(file_name) is False
