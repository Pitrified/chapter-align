from chapter_align.utils.SentenceList import SentenceList  # type: ignore


def test_sentence_list_1(a_sentence_list: SentenceList) -> None:
    r"""Create a SentenceList and access a Sentence"""
    a_sentence = a_sentence_list[0]
    assert a_sentence.norm_tra == "A short sentence."


def test_sentence_list_1_outside(a_sentence_list: SentenceList) -> None:
    r"""Access a Sentence beyond the len"""
    a_sentence = a_sentence_list[2]
    assert a_sentence.norm_tra == "_"


def test_sentence_list_1_negative(a_sentence_list: SentenceList) -> None:
    r"""Access a Sentence with negative indexing"""
    a_sentence = a_sentence_list[-1]
    assert a_sentence.norm_tra == "Another short sentence."


def test_sentence_list_1_negative_outside(a_sentence_list: SentenceList) -> None:
    r"""Access a Sentence with negative indexing beyond the len"""
    a_sentence = a_sentence_list[-3]
    assert a_sentence.norm_tra == "_"


def test_sentence_list_1_len(a_sentence_list: SentenceList) -> None:
    r"""Get the length of the inner list"""
    assert len(a_sentence_list) == 2


def test_sentence_list_1_totchar(a_sentence_list: SentenceList) -> None:
    r"""Get the length in chars"""
    tot_chars = a_sentence_list[0].len_norm_tra + a_sentence_list[1].len_norm_tra
    assert a_sentence_list.tot_chars == tot_chars
