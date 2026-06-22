"""Utilities for the Software Project Summarizer agent."""

from __future__ import annotations


def permit_directory_inspection(directory_name: str) -> bool:
    if directory_name.startswith("."):
        return False
    if directory_name.startswith("__"):
        return False
    if directory_name in ["obj", "bin", "node_modules", "dist", "venv", "build"]:
        return False
    if directory_name.endswith(".egg-info"):
        return False

    return True


def permit_file_inspection(file_name: str) -> bool:
    if file_name.startswith("."):
        return file_name in [".gitignore", ".editorconfig"]
    if file_name.startswith("__"):
        return False
    if file_name.lower().startswith("readme"):
        return False

    return True
