import pytest

from chapter_align.utils.Sentence import Sentence  # type: ignore


@pytest.fixture
def a_sentence() -> Sentence:
    r"""Create a Sentence"""
    return Sentence("<p>A short sentence.</p>")


def test_sentence_norm_1(a_sentence: Sentence) -> None:
    r"""MAKEDOC: what is test_sentence_norm_1 doing?"""
    assert a_sentence.norm_tra == "A short sentence."
