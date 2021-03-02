# from pathlib import Path

import pytest

from chapter_align.utils.misc import get_package_folders  # type: ignore


def test_get_package_folders_default() -> None:
    """It gets the package root folder using the default arg"""
    package_root_folder = get_package_folders()
    assert package_root_folder.name == "chapter-align"


def test_get_package_folders() -> None:
    """It gets the package root folder explicitly"""
    package_root_folder = get_package_folders("root")
    assert package_root_folder.name == "chapter-align"


def test_get_package_folders_tests() -> None:
    """It gets the package tests folder"""
    tests_folder = get_package_folders("tests")
    assert tests_folder.name == "tests"


def test_get_package_folders_epub() -> None:
    """It gets the package template epub folder"""
    template_epub_folder = get_package_folders("template_epub")
    assert template_epub_folder.name == "template_epub"


def test_get_package_folders_not_valid_key() -> None:
    """Raise KeyError when the folder requested is not known"""
    with pytest.raises(KeyError, match="Not recognized"):
        get_package_folders("notavalidkey")
