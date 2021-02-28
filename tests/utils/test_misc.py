# from pathlib import Path

# import pytest
from chapter_align.utils.misc import get_package_root_folder  # type: ignore


def test_get_package_root_folder() -> None:
    """It gets the package root folder"""
    package_root_folder = get_package_root_folder()
    assert package_root_folder.name == "chapter-align"
